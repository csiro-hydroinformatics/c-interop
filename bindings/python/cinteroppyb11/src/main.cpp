#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#define USING_MOIRAI
#include <moirai/opaque_pointers.hpp>

#include <cinterop/c_cpp_interop.hpp>
#include <cinterop/pybind11_timeseries_interop.hpp>

namespace py = pybind11;

bool c_test_expected(const date_time_to_second& d, int year, int month, int day, int hour, int minute, int second) {

	return
		d.year == year &&
		d.month == month &&
		d.day == day &&
		d.hour == hour &&
		d.minute == minute &&
		d.second == second;
}

class cpp_multi_regular_time_series_data : public multi_regular_time_series_data
{
public:
	cpp_multi_regular_time_series_data() {
		this->numeric_data = nullptr;
		this->ensemble_size = 0;
	}
	void set_numeric_data(const std::vector<std::vector<double>>& v)
	{
		this->numeric_data = cinterop::utils::to_double_ptr_array(v);
	}
	void clear_numeric_data()
	{
		cinterop::disposal::dispose_of<multi_regular_time_series_data>(*this);
	}
};

using moirai::opaque_pointer_handle;
// Nope... dont think so since this is a return value, unless we add str type info to the generated cpp code.
//
//class named_opaque_pointer_handle : public opaque_pointer_handle
//{
//public:
//	using opaque_pointer_handle::opaque_pointer_handle;
//};

PYBIND11_MODULE(cinteroppyb11, m) {
    m.doc() = R"pbdoc(
        Experimental python bindings for C/C++ ensemble forecasting data interop
        -----------------------

        .. currentmodule:: cinteroppyb11

        .. autosummary::
           :toctree: _generate

           add
           subtract
    )pbdoc";

    m.def("test_date_time_to_second", &c_test_expected);

	py::class_<date_time_to_second>(m, "DateTimeToSecond")
		.def(py::init<>())
		.def_readwrite("year", &date_time_to_second::year)
		.def_readwrite("month", &date_time_to_second::month)
		.def_readwrite("day", &date_time_to_second::day)
		.def_readwrite("hour", &date_time_to_second::hour)
		.def_readwrite("minute", &date_time_to_second::minute)
		.def_readwrite("second", &date_time_to_second::second)
		;

	py::class_<regular_time_series_geometry>(m, "RegularTimeSeriesGeometry")
		.def(py::init<>())
		.def_readwrite("length", &regular_time_series_geometry::length, R"pbdoc(
        Length of the time series

        Length of the time series
    )pbdoc")
		.def_readwrite("start", &regular_time_series_geometry::start, R"pbdoc(
        Start of the time series

        Start of the time series - time stamp
    )pbdoc")
		.def_readwrite("time_step_seconds", &regular_time_series_geometry::time_step_seconds, R"pbdoc(
        length in seconds of the time step of the time series

        length in seconds of the time step of the time series
    )pbdoc")
		//.def("setName", &regular_time_series_geometry::setName)
		//.def("getName", &regular_time_series_geometry::getName)
		;

	py::class_<multi_regular_time_series_data>(m, "MultiRegularTimeSeriesStruct")
		.def(py::init<>())
		.def_readwrite("ensemble_size", &multi_regular_time_series_data::ensemble_size)
		.def_readwrite("time_series_geometry", &multi_regular_time_series_data::time_series_geometry)
		;

	py::class_<cpp_multi_regular_time_series_data, multi_regular_time_series_data>(m, "MultiRegularTimeSeries")
		.def(py::init<>())
		.def("set_numeric_data", &cpp_multi_regular_time_series_data::set_numeric_data)
		.def("clear_numeric_data", &cpp_multi_regular_time_series_data::clear_numeric_data)
		;

	py::class_<moirai::opaque_pointer_handle>(m, "OpaquePointer", py::dynamic_attr())
		.def("get_reference_count", &moirai::opaque_pointer_handle::get_reference_count)
		;

	


#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
