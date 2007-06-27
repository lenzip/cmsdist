### RPM external hepmc 2.00.02-CMS3
Requires: clhep
Source: http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-%realversion.tar.gz

%prep
%setup -q -n HepMC-%{realversion}

echo "CLHEP_ROOT is: " $CLHEP_ROOT
./configure  --with-CLHEP=$CLHEP_ROOT --prefix=%{i} 

%build
make 

%install
make install
