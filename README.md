# Reusable functions for marshalling data between C, C++ and other programming languages

[![license](http://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/csiro-hydroinformatics/c-interop/blob/master/LICENSE.txt)
![status](https://img.shields.io/badge/status-beta-blue.svg)
[![Python package doc](https://readthedocs.org/projects/cinterop/badge/?version=latest)](https://cinterop.readthedocs.io/en/latest/?badge=latest)

**Python package**: [![license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/csiro-hydroinformatics/c-interop/blob/master/bindings/python/cinterop/LICENSE.txt) ![status](https://img.shields.io/badge/status-beta-blue.svg) [![Documentation Status](https://readthedocs.org/projects/cinterop/badge/?version=latest)](https://cinterop.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/csiro-hydroinformatics/c-interop/branch/master/graph/badge.svg?token=Bxg1zkbG9G)](https://codecov.io/gh/csiro-hydroinformatics/c-interop) master: [![Python package](https://github.com/csiro-hydroinformatics/c-interop/actions/workflows/python-cinterop.yml/badge.svg?branch=master)](https://github.com/csiro-hydroinformatics/c-interop/actions/workflows/python-cinterop.yml) testing: [![Python package](https://github.com/csiro-hydroinformatics/c-interop/actions/workflows/python-cinterop.yml/badge.svg?branch=testing)](https://github.com/csiro-hydroinformatics/c-interop/actions/workflows/python-cinterop.yml)

## Purpose and context

This repository contains reusable material for interoperability between C/C++ and other languages such as python, R, etc. It is using template-only C++, avoiding code duplications across several projects. The code design also stems from learning over the years to prevent some "gotchas" one can get into when diving deep in native interop accross compilation modules.

## Content

The `C++` header files cover interop for:

* common base types (characters, numeric, and vectors thereof)
* boost date-time
* time series (inherited from its usage in time step modelling systems)

The repo also includes interop packages for several higher level languages, that helps handling consistently (including memory management...) some of the data stemming from the C/C++ glue code:

* python package [cinterop](./bindings/python/cinterop/) also [available on pypi](https://pypi.org/project/cinterop/)
* R package [cinterop](./bindings/R/pkgs/cinterop/)
* Matlab [reference counting helpers](./bindings/matlab/)

## Related work, use cases

One use case arising from hydrologic forecasting is [uchronia-time-series](https://github.com/csiro-hydroinformatics/uchronia-time-series/).

Some features in the present repository depend on related material:

* [moirai](https://github.com/csiro-hydroinformatics/moirai), a C++ library designed to help handling C++ objects from so-called opaque pointers, via a C API.
* The python package [refcount](https://github.com/csiro-hydroinformatics/pyrefcount) for reference counting external resources.

Another resource is a [blog post](https://jmp75.github.io/work-blog/posts/2022-09-03-c-api-wrapper-generation.html) on generating programming language bindings to a C API.

## Example

For instance this library defines a template function `to_custom_character_vector` to convert C `char**` types to something useful for the higher level language at hand.

```c++
namespace cinterop
{
    namespace utils
	{
        template<typename T>
		T to_custom_character_vector(char** names, int size, bool cleanup);
```

One specialization of this is a conversion to Rcpp's `CharacterVector` type for interop with R, which would be used like this:

```c++
int size;
char** values = GetEnsembleDatasetDataIdentifiers(dataLibrary->get(),  &size);
CharacterVector cv = to_custom_character_vector<CharacterVector>(values, size, true);
```

## Related work

* [native interop glue code generation](https://github.com/csiro-hydroinformatics/c-api-wrapper-generation)
* An R package pupetting the former - I have yet to open source it though.
