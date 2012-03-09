### RPM cms PHEDEX-lifecycle 1.0.0
## INITENV +PATH PERL5LIB %i/perl_lib
%define downloadn %(echo %n | cut -f1 -d-)
%define cvsversion LIFECYCLE_%(echo %realversion | tr . _)
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source0: %cvsserver&strategy=export&module=%{downloadn}&export=%{downloadn}&&tag=-r%{cvsversion}&output=/%{n}.tar.gz
Source1: %cvsserver&strategy=export&module=T0&export=T0&&tag=-rPHEDEX_%{cvsversion}&output=/T0.tar.gz

Requires: p5-poe p5-poe-component-child
Requires: p5-clone p5-time-hires p5-text-glob p5-compress-zlib p5-log-log4perl
Requires: mod_perl2
Provides: perl(XML::LibXML)
Provides: perl(T0::FileWatcher)
Provides: perl(T0::Logger::Sender)
Provides: perl(T0::Util)

# Actually, it is p5-xml-parser that requires this, but it doesn't configure itself correctly
# This is so it gets into our dependencies-setup.sh
#Requires:  expat

%prep
%setup -n PHEDEX
tar zxf %_sourcedir/T0.tar.gz

%build
%install
mkdir -p %i/etc/{env,profile}.d
tar -cf - * | (cd %i && tar -xf -)

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
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