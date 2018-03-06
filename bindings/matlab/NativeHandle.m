classdef NativeHandle < handle
    % NativeHandle  A base abstract class for wrappers around objects in native libraries for easier memory management. 
    % 
    % Say you have a C API as follows:
    % * `void* create_some_object();`
    % * `dispose_of_some_object(void* obj);`
    % and accessing it using Matlab. Users would use the `calllib` function:
    % aLibPointer = callib('mylib', 'create_some_object');
    % but at some point when done need to dispose of it:
    % callib('mylib', 'dispose_of_some_object', aLibPointer);
    % In practice in real systems one quickly ends up with cases 
    % where it is unclear when to dispose of the object. 
    % If you call the `dispose_of_some_object` function more 
    % than once of too soon, you could easily crash the program.
    % NativeHandle is designed to alleviate this headache by 
    % using Matlab native reference counting of `handle` classes to reliably dispose of objects. 
    %
    % This class is originally inspired from a class with a similar purpose in C#. See https://github.com/jmp75/dynamic-interop-dll

    properties (Access = private)
        % Summary:
        % The handle to the native resource.
        % protected IntPtr handle;
        nHandle
        refCount
        finalizing
    end

    properties (Dependent)
        % ReferenceCount - The number of references to the underlying object (Not the wrapper).
        % In practice this would almost always be 0 or 1 and users should not need to take use this. 
        ReferenceCount 
        % Disposed - logical; has the native object and memory already been disposed of.
        Disposed
        % IsInvalid - logical; in practice synonym with Disposed; 
        % has the native object and memory already been disposed of.
        IsInvalid
    end

    % https://au.mathworks.com/help/matlab/matlab_oop/abstract-classes-and-interfaces.html#btgxhug-1

    methods (Abstract, Access = protected)
        % ReleaseHandle Releases the native resource for this handle.
        % This method must be implemented and overriden by inheritors
        % Returns:
        % True if it succeeds, false if it fails.
        ReleaseHandle(obj);
    end

    methods (Access = protected)
        function SetHandle(obj, pointer, currentRefCount)
            % SetHandle - Sets a handle.
            %
            % Parameters:
            %   pointer:
            % The handle (lib.pointer), value of the pointer to the native object
            %
            %   currentRefCount:
            % (Optional) Number of pre-existing references for 
            % the native object. Almost always 0 except in unusual, advanced situations.
            %
            % Exceptions:
            % error message when a pointer is a Zero pointer .
            %
            % Remarks:
            % If a native object was created prior to its use by Matlab, its lifetime may need
            % to extend beyong its use from Matlab, hence the provision for an initial reference 
            % count more than 0. In practice the scenario is very unusual.
            if nargin < 3
                currentRefCount = 0;
            end
            if (~obj.IsValidHandle(pointer))
                error('The lib.pointer argument is not a valid handle')
            end
            obj.nHandle = pointer;
            obj.refCount = currentRefCount + 1;
        end

        function obj = NativeHandle(pointer, currentRefCount)
            % Constructor - Specialised constructor for use only by derived class.
            %
            % Parameters:
            %   pointer:
            % The handle, value of the pointer to the native object
            %
            %   currentRefCount:
            % (Optional) Number of pre-existing references for the native object
            %
            % Remarks:
            % If a native object was created prior to its use by Matlab, its lifetime may need
            % to extend beyong its use from Matlab, hence the provision for an initial reference 
            % count more than 0. In practice the scenario is very unusual.
            obj.finalizing = false;
            obj.nHandle = false;
            obj.refCount = 0;
            if nargin == 0
                return; % defer setting handle to the inheritor.
            end
            if nargin < 2
                currentRefCount = 0;
            end
            obj.SetHandle(pointer, currentRefCount);
        end
    end

    methods (Access = private)
        function f = IsValidHandle(obj, h)
            % IsValidHandle - Test whether an argument is a valid handle (lib.pointer) for this object.
            % Returns a logical.
            % Parameters:
            %   h:
            % The handle, value of the pointer to the native object
            f = isa(h, 'lib.pointer');
        end

        function DisposeImpl(obj, decrement)
            % DisposeImpl - An implementation of the Dispose method, to 
            % avoid cyclic method calls.
            % 
            % Parameters:
            % decrement - logical indicating whether the reference count should be decreased.
            if (obj.Disposed)
                return;
            end
            if (decrement)
                obj.refCount = obj.refCount - 1;
            end
            if (obj.refCount <= 0)
                if (obj.ReleaseHandle())
                    obj.nHandle = false;
                    % if (!finalizing)
                    % GC.SuppressFinalize(this);
                end
            end
        end
    end

    methods
        % Property set and get functions in class 'NativeHandle' must be defined in a methods block that does not have attributes.        % public int ReferenceCount { get; }
        function r = get.ReferenceCount(obj)
            % get.ReferenceCount:
            % Gets the number of references to the native resource for this handle.
            r = obj.refCount;
        end
        function d = get.Disposed(obj)
            % Gets a value indicating whether this handle has been disposed of already
            d = isequal(obj.nHandle, false);
        end
        function d = get.IsInvalid(obj)
            % Gets a value indicating whether this handle is invalid.
            d = isequal(obj.nHandle, false);
        end
    end

    methods (Access = public)
        function delete(h)
        % Finaliser or destructor - Triggers the disposal of this object if not manually done.
            if ~isequal(h.nHandle, false)
                % Protect against accessing properties
                % of partially constructed objects
                h.finalizing = true;
                h.Release();
            end
        end

        function AddRef(obj)
            % AddRef - Manually increments the reference counter.
            % This is very unusual you would need to call this method. 
            obj.refCount = obj.refCount + 1;
        end

        function Dispose(obj)
            % Dispose - If the reference counts allows it, release the resource refered to by this handle.
            obj.DisposeImpl(true);
        end

        function f = GetHandle(obj)
            % GetHandle = Returns the value of the handle.
            %
            % Returns:
            % The handle (lib.pointer)
            f = obj.nHandle;
        end

        function f = Release(obj)
            % Release - Manually decrements the reference counter. Triggers disposal if count 
            % is down to zero.
            obj.DisposeImpl(true);
        end

    end  % of public methods
end % of class
