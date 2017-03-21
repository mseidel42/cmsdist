### RPM external py2-numpy 1.11.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: https://pypi.python.org/packages/e0/4c/515d7c4ac424ff38cc919f7099bf293dd064ba9a600e1e3835b3edefdb18/numpy-1.11.1.tar.gz
Requires: python py2-setuptools zlib lapack
%prep
%setup -n numpy-%realversion

%build
%install
case %cmsos in
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac

cat > site.cfg <<EOF
[blas]
include_dirs = $LAPACK_ROOT/include
library_dirs = $LAPACK_ROOT/lib64
blas_libs = blas
[lapack]
include_dirs = $LAPACK_ROOT/include
library_dirs = $LAPACK_ROOT/lib64
lapack_libs = lapack
EOF

export ATLAS=None
export OPENBLAS=None
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES

python setup.py build  %{makeprocesses} --fcompiler=gnu95
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH python setup.py install --prefix=%i
sed -ideleteme 's|#!.*/bin/python|#!/usr/bin/env python|' \
  %{i}/bin/f2py \
  %{i}/lib/python*/site-packages/numpy-*/EGG-INFO/scripts/f2py \
  %{i}/lib/python*/site-packages/numpy-*/numpy/core/tests/test_arrayprint.py \
  %{i}/lib/python*/site-packages/numpy-*/numpy/distutils/from_template.py \
  %{i}/lib/python*/site-packages/numpy-*/numpy/distutils/conv_template.py
  
find %{i} -name '*deleteme' -delete
