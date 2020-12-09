# Building Debian packages

Adapted from [this](https://github.com/csiro-hydroinformatics/cinterop/blob/master/doc/debian-packaging.md)

## Notes

```sh
sudo apt install dh-make
#https://gitlab.kitware.com/debian/dh-cmake
sudo apt install dh-cmake
sudo apt install equivs
sudo apt install dh-r
```

### Creating the libcinterop-dev pkg

```sh
pkgname=libcinterop-dev
pkgname_ver=${pkgname}-1.1
fn_ver=${pkgname}_1.1
SRC=~/src/github_jm/rcpp-interop-commons
DEST=~/tmp/cinterop/${pkgname_ver}
FILES="cinterop.pc.in CMakeLists.txt cmake_uninstall.cmake.in debian/ doc/ include/ LICENSE.txt  README.md"

mkdir -p ${DEST}
cd ${DEST}
rm -rf ${DEST}/*
cd ${SRC}
cp -Rf ${FILES} ${DEST}/
cd ${DEST}
# rm -rf ./obj-x86_64-linux-gnu
# rm -rf ./debian/libcinterop-dev  # whu not a tmp folder like other pkg?
ls -a
cd ${DEST}/..
tar -zcvf ${fn_ver}.orig.tar.gz ${pkgname_ver}
cd ${DEST}
debuild -us -uc 
```

Check:

```sh
cd ${DEST}/..
dpkg -c libcinterop-dev_1.1-1_amd64.deb 
sudo dpkg -i libcinterop-dev_1.1-1_amd64.deb 
```

### Creating the r-cinterop pkg

Possibly `sudo apt install r-cran-generics r-cran-rcpp`. 

```sh
pkgname=r-cinterop
pkgname_ver=${pkgname}-1.1
fn_ver=${pkgname}_1.1
SRC=~/src/github_jm/rcpp-interop-commons/bindings/R/pkgs/cinterop
DEST=~/tmp/cinterop/${pkgname_ver}
FILES="./*"

mkdir -p ${DEST}
cd ${DEST}
rm -rf ${DEST}/*
cd ${SRC}
cp -Rf ${FILES} ${DEST}/
cd ${DEST}
ls -a
cd ${DEST}/..
tar -zcvf ${fn_ver}.orig.tar.gz ${pkgname_ver}
cd ${DEST}
debuild -us -uc 
```

Check:

```sh
cd ${DEST}/..
dpkg -c r-cinterop_1.1-1_amd64.deb 
sudo dpkg -i libcinterop-dev_1.1-1_amd64.deb 
```
