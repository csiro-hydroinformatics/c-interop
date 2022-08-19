# Tests for refcount

If you want to explore the unit tests e.g. in debug mode from your IDE, you can use the following steps:

on Linux: 

```sh
cd tests
cd test_native_library
cmake -Bbuild .
cmake --build build
```

```sh
cd tests
python ./test_native_handle.py 
```

## Related work

Mostly a note to self, I am copying the native test library straight from [dynamic-interop-dll](https://github.com/rdotnet/dynamic-interop-dll). This is not ideal (code duplication) but need expediency, and that code is unlikely to change often if at all. Still, should you need to expand on this, keep in mind and consider if something like subrepositories is warranted.

TODO: Consider UT for R and (very last cab) Matlab as well.