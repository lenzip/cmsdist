### RPM cms t0 1.0.1
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
%define wmcver 0.8.26pre1
%define webdoc_files %i/doc/
%define svnserver svn://svn.cern.ch/reps/CMSDMWM
Source0: %svnserver/WMCore/tags/%{wmcver}?scheme=svn+ssh&strategy=export&module=WMCore&output=/wmcore_das.tar.gz
Source1: %svnserver/T0/tags/%{realversion}?scheme=svn+ssh&strategy=export&module=T0&output=/T0.tar.gz
Requires: python py2-sphinx

%prep
%setup -T -b 0 -n WMCore
%setup -D -T -b 1 -n T0

# setup version
cat src/python/T0/__init__.py | sed "s,development,%{realversion},g" > init.tmp
mv -f init.tmp src/python/T0/__init__.py

%build
cd ../WMCore
python setup.py build
cd ../T0
python setup.py build

# build T0 sphinx documentation
PYTHONPATH=$PWD/src/python:$PYTHONPATH
cd doc
cat sphinx/conf.py | sed "s,development,%{realversion},g" > sphinx/conf.py.tmp
mv sphinx/conf.py.tmp sphinx/conf.py
mkdir -p build
make html

%install
cd ../WMCore
python setup.py install --prefix=%i
cd ../T0
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
#cp -r src/python/T0 %{i}

mkdir -p %i/doc
tar --exclude '.buildinfo' -C doc/build/html -cf - . | tar -C %i/doc -xvf -

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%i/
%exclude %i/doc
## SUBPACKAGE webdoc