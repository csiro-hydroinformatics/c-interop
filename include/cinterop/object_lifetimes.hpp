#pragma once

// Intended for specialized disposal of C interop structs.

namespace cinterop
{
	namespace disposal {
		template<typename T>
		void dispose_of(T& d);
	}
}