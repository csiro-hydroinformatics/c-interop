#pragma once

// Intended for specialized disposal of C interop structs.

namespace cinterop
{
	namespace disposal {
		template<typename T>
		void dispose_of(T& d);

		template<typename F>
		void free_c_array(F* values, size_t  arrayLength);

		template<typename F = double>
		void free_c_ptr_array(F** values, size_t  arrayLength)
		{
			for (size_t  i = 0; i < arrayLength; i++)
				delete[] values[i];
			delete[] values;
		}

		template<>
		inline void free_c_array<double>(double* values, size_t  arrayLength)
		{
			delete values;
		}
	}
}