#pragma once

#include <vector>
#include <functional>
#include <boost/date_time/gregorian/gregorian.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>

#include "cinterop/c_cpp_interop.hpp"

using std::vector;
using std::string;

using namespace boost::gregorian;
using namespace boost::posix_time;

namespace cinterop
{
	namespace utils
	{
		template<typename date_int_type = uint32_t>
		boost::posix_time::ptime as_ptime(date_int_type year, date_int_type month, date_int_type day, date_int_type hour = 0, date_int_type minute = 0, date_int_type second = 0)
		{
			date d(year, month, day);
			time_duration td = hours(hour) + minutes(minute) + seconds(second);
			return ptime(d, td);
		}

		// date-time interop
		//using namespace boost::gregorian;
		//using namespace boost::posix_time;

		template<typename T = ptime>
		T to_ptime(const date_time_to_second& dt)
		{
			return T(date(dt.year, dt.month, dt.day), hours(dt.hour) + minutes(dt.minute) + seconds(dt.second));
		}

		template<typename T = ptime>
		void to_date_time_to_second(const T& dt, date_time_to_second& tt)
		{
			if (dt.is_not_a_date_time())
				throw std::invalid_argument("to_date_time_to_second cannot handle value not_a_datetime");
			auto d = dt.date();
			tt.year = d.year();
			tt.month = d.month();
			tt.day = d.day();
			auto t = dt.time_of_day();
			tt.hour = t.hours();
			tt.minute = t.minutes();
			tt.second = t.seconds();
		}


		/*
		// C interop Template specialisations for STL classes and common types
		*/

		/**
		 * \brief	interop template specialization for boost ptime
		 */
		template<>
		inline date_time_to_second to_date_time_to_second<ptime>(const ptime& dt)
		{
			date_time_to_second tt;
			to_date_time_to_second(dt, tt);
			return tt;
		}

		template<>
		inline ptime from_date_time_to_second<ptime>(const date_time_to_second& dt)
		{
			return as_ptime<int>(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second);
		}
	}
}