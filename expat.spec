### RPM external expat 2.0.0-CMS3
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
Source: http://dl.sourceforge.net/sourceforge/%n/%n-%realversion.tar.gz

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%{i} 
make 
make install

%if "%(ldd /usr/bin/gcc | xargs | grep lib64)" != ""
make clean
echo "64 bit compiler found let's build expat in 64 bit to be used by scram perl modules." 
export PATH=/usr/bin:/bin
export GCC_EXEC_PREFIX=/usr/lib/gcc/

CXX=/usr/bin/c++ CC=/usr/bin/gcc setarch x86_64 ./configure --prefix=%{i} --bindir=%{i}/bin/64 --libdir=%{i}/lib64
setarch x86_64 make
setarch x86_64 make install
%endif
%install
echo "Nothing to be done in install"
