#pragma once

// Intended for specialized disposal of C interop structs.

namespace cinterop
{
	namespace disposal {

		/**
		 * \brief	template definition for functions in charge of disposing of the content of objects (usually structs)
		 * 
		 * \tparam	T	The type of the object to dispose of
		 * \param d	object to dispose of by deleting its members, as appropriate
		 */
		template<typename T>
		void dispose_of(T& d);

		/**
		 * \brief	template definition for functions in charge of disposing of heap allocated objects (usually structs)
		 * 
		 * \tparam	T	The type of the object to dispose of
		 * \param d	object to dispose of by deleting its members, as appropriate, and then delting the heap allocated object itself.
		 */
		template<typename T>
		void dispose_of(T* d)
		{
			T& ref = *d;
			dispose_of<T>(ref);
			delete d;
		}

		/**
		 * \brief	Default template definition for functions in charge of disposing of heap allocated C arrays and its items (usually arrays of structs)
		 * 
		 * \tparam	F	The type of elements of the array to dispose of
		 * \param values	array of objects to dispose of by deleting its members, as appropriate, and then delting the heap allocated object itself.
		 * \param arrayLength	array size
		 */
		template<typename F>
		void free_c_array(F* values, size_t  arrayLength)
		{
			delete values;
		}

		/**
		 * \brief	template definition for functions in charge of disposing of arrays of arrays
		 * 
		 * \tparam	F	The type of elements of the array to dispose of; usually double, int, char* etc. More complicated types needs due thinking about not leaving memory leaks  
		 * \param values	2D array of objects to dispose of by deleting its members, as appropriate, and then delting the heap allocated object itself.
		 * \param arrayLength	array size (first dimension)
		 */
		template<typename F = double>
		void free_c_ptr_array(F** values, size_t  arrayLength)
		{
			for (size_t  i = 0; i < arrayLength; i++)
				delete[] values[i];
			delete[] values;
		}
	}
}