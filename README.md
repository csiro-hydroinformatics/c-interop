# Reusable functions for marshalling data between C, C++ and other programming languages

[![license](http://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/csiro-hydroinformatics/rcpp-interop-commons/blob/master/LICENSE.txt)
![status](https://img.shields.io/badge/status-beta-blue.svg)

[![Python package doc](https://readthedocs.org/projects/cinterop/badge/?version=latest)](https://cinterop.readthedocs.io/en/latest/?badge=latest)

The idea is to have more consistency of vocabulary in interoperability glue code, using template-only C++, also avoiding code duplications across several projects I have (and others have, hopefully).

The code design also captures material that evolved over the years to prevent some "gotchas" one can get into when diving deep in native interop accross compilation modules.

This repository started as a repository for material limited to C to R interop via Rcpp, hence the name.

## Content

The C++ header files cover interop for:

* common base types (characters, numeric, and vectors thereof)
* boost date-time
* time series (inherited from its usage in time step modelling systems)

The repo also includes an R package `cinterop` that helps handling consistently (including memory management...) some of the data stemming from the C/C++ glue code. It is expected to host a python package sometime, possibly Matlab material too.

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
