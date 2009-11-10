### RPM lcg roofit 5.25.02
%define svnTag %(echo %realversion | tr '.' '-')
Source: svn://root.cern.ch/svn/root/tags/v%svnTag/roofit?scheme=http&module=roofit&output=/roofit.tgz

Patch:  roofit-5.24-00-build.sh 
Patch1: root-5.22-00a-roofit-silence-static-printout
Patch2: roofit-5.24-00-RooFactoryWSTool-include
Patch3: roofit-5.25-02-NOROOMINIMIZER

Requires: root 

%prep
%setup -n roofit
%patch -p1
%patch1 -p2
%patch2 -p1
%patch3 -p1
 
%build
chmod +x build.sh
# Remove an extra -m64 from Wouter's build script (in CXXFLAGS and LDFLAGS)
perl -p -i -e 's|-m64 ||' build.sh
# Add in a macro needed (via the NOROOMINIMIZER patch above) to avoid 
# compiling some code bits in roofit which do not build with 
# ROOT5.22/00 (5.24/00 or later is needed) in CXXFLAGS
perl -p -i -e 's|-O2 -pipe|-O2 -pipe -D__ROOFIT_NOROOMINIMIZER|' build.sh
./build.sh

%install
mv build/lib %i/
mkdir %i/include
cp -r build/inc/* %i/include

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d

# rootroofitcore toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roofitcore
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=roofitcore version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=RooFitCore>
<use name=rootcore>
<use name=roothistmatrix>
<use name=rootgpad>
<use name=rootminuit>
<Client>
 <Environment name=ROOFIT_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$ROOFIT_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$ROOFIT_BASE/include"></Environment>
</Client>
</Tool> 
EOF_TOOLFILE

# rootroofit toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roofit
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=roofit version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=RooFit>
<use name=roofitcore>
<use name=rootcore>
<use name=roothistmatrix>
</Tool> 
EOF_TOOLFILE

# rootroostats toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roostats
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=roostats version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=RooStats>
<use name=roofitcore>
<use name=roofit>
<use name=rootcore>
<use name=roothistmatrix>
<use name=rootgpad>
</Tool> 
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/roofitcore
%{relocateConfig}etc/scram.d/roofit
%{relocateConfig}etc/scram.d/roostats
