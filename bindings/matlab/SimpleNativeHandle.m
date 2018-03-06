
classdef SimpleNativeHandle < NativeHandle
    % SimpleNativeHandle - A simplest implementation for a native handle class. 
    % This can cater for simple C APIs for object disposal function with 
    % a signature such as void dispose_of(void* native_object)

    properties (Access = private)
        nativeLibName
        disposeFuncName
    end

    methods (Access = protected)
        function obj = SimpleNativeHandle(pointer, libname, dispfuncname)
            % SimpleNativeHandle - constructor for a simplest implementation for a native handle class. 
            % 
            % parameters
            % libname - name of the native library, e.g. mylib if a call to mylib.dll
            % dispfuncname - name of the C function for disposal of the native object this wraps.
            obj = obj@NativeHandle(pointer)
            obj@nativeLibName = libname;
            obj@disposeFuncName = dispfuncname;
        end

        function s = ReleaseHandle(obj)
            % ReleaseHandle - call the native library to 
            % dispose of the native object of this handle 
            s = true;
            if (~obj.IsInvalid)
                calllib(libname, disposeFuncName, obj.GetHandle());
            end
        end
    end
end
