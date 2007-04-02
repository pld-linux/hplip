# TODO:
#	- add desktop file for toolbox
#	- check if all GUI tools were separated
#	- check for all files required by daemon package (or Reqs)
#	- prepare fax packages for fax utilities
#	- check if symlinks /usr/lib/sane/libsane-hpaio.so.1 -> ../libsane-hpaio.so.1.0.0
#	  are "right way" of making them available to sane.
#	- separate package for hpijs (hplip Req: hpijs, hplip-hpijs Prov: hpijs?)
#	- hp-checks looks for installer module (unpackaged files?)
#
# Conditional build:
%bcond_without	cups	# without CUPS support
#
Summary:	Hewlett-Packard Linux Imaging and Printing Project
Summary(pl.UTF-8):	Serwer dla drukarek HP Inkjet
Name:		hplip
Version:	1.7.3
Release:	3
License:	BSD, GPL v2 and MIT
Group:		Applications/System
Source0:	http://dl.sourceforge.net/hplip/%{name}-%{version}.tar.gz
# Source0-md5:	6921d256c9efc37446f5d2fad71979f8
Source1:	%{name}.init
Source2:	%{name}-DJ670C.xml
URL:		http://hplip.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_cups:BuildRequires:	cups-devel}
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libusb-devel
BuildRequires:	net-snmp-devel
BuildRequires:	openssl-devel
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	sane-backends-devel
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	python-modules
Obsoletes:	hpijs
Obsoletes:	python-hplip
Conflicts:	ghostscript <= 7.00-3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _ulibdir        %{_prefix}/lib

%if %{with cups}
%define 	_cupsdir 	%(cups-config --datadir)
%define		_cupsppddir	%{_cupsdir}/model
%endif

%description
The Hewlett-Packard Linux Imaging and Printing project (HPLIP)
provides a unified single and multi-function connectivity solution for
Linux. The goal of this project is to provide "radically simple"
printing, faxing, scanning, photo-card access, and device management
to the consumer and small business desktop Linux users.

%package daemon
Summary:	HPLIP daemon
Summary(pl.UTF-8):	Server HPLIP
Group:		Applications/System
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description daemon
HPLIP daemon.

%description daemon -l pl.UTF-8
Server HPLIP.

%package gui-tools
Summary:	HPLIP GUI tools
Summary(pl.UTF-8):	Narzędzia graficzne HPLIP
Group:		Applications/System
Requires:	python-PyQt
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description gui-tools
HPLIP GUI tools.

%description gui-tools -l pl.UTF-8
Narzędzia graficzne HPLIP.

%package libs
Summary:	HPLIP Libraries
Summary(pl.UTF-8):	Biblioteki HPLIP
Group:		Libraries

%description libs
HPLIP Libraries.

%description libs -l pl.UTF-8
Biblioteki HPLIP.

%package sane
Summary:	HPLIP SANE Libraries
Summary(pl.UTF-8):	Biblioteki HPLIP SANE
Group:		Libraries
Requires(post):	/bin/grep
Requires(postun):	/bin/sed
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description sane
HPLIP SANE Libraries.

%description sane -l pl.UTF-8
Biblioteki HPLIP SANE.

%package ppd
Summary:	PPD database for Hewlett Packard printers
Summary(pl.UTF-8):	Baza danych PPD dla drukarek Hewlett Packard
Group:		Applications/System
Requires:	cups

%description ppd
PPD database for Hewlett Packard printers.

%description ppd -l pl.UTF-8
Baza danych PPD dla drukarek Hewlett Packard.

%package -n cups-backend-hp
Summary:	HP backend for CUPS
Summary(pl.UTF-8):	Backend HP dla CUPS-a
Group:		Applications/Printing
Requires:	%{name} = %{version}-%{release}
Requires:	cups

%description -n cups-backend-hp
This package allow CUPS printing on HP printers.

%description -n cups-backend-hp -l pl.UTF-8
Ten pakiet umożliwia drukowanie z poziomu CUPS-a na drukarkach HP.

%prep
%setup -q
sed -i -e's,^#!/usr/bin/env python$,#!/usr/bin/python,' *.py

%build
install %{SOURCE2} data/xml
install /usr/share/automake/config.* .
install /usr/share/automake/config.* prnt
CXXFLAGS="%{rpmcflags} -fno-exceptions -fno-rtti"
%configure \
	--enable-foomatic-install \
	%{!?with_cups:--disable-cups-install}
%{__make} \
	hpppddir=/usr/share/cups/model \
	hpppddir=%{_cupsppddir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_sysconfdir}/hp}

%if %{with cups}
install -d $RPM_BUILD_ROOT$(cups-config --datadir)/model \
	$RPM_BUILD_ROOT$(cups-config --serverbin)/filter
%endif

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	rpm_install=yes \
	hpppddir=%{_cupsppddir}

%if %{with cups}
rm -f $RPM_BUILD_ROOT%{_cupsppddir}/foomatic-ppds
mv $RPM_BUILD_ROOT{%{_datadir}/ppd/HP/*,%{_cupsppddir}}
%endif

ln -sf %{_datadir}/%{name}/hpssd.py $RPM_BUILD_ROOT%{_sbindir}/hpssd
ln -sf %{_datadir}/%{name}/setup $RPM_BUILD_ROOT%{_sbindir}/hp-setup

for tool in align clean check colorcal fab firmware info levels makecopies makeuri print \
		probe sendfax setup testpage timedate toolbox unload ; do
	ln -sf %{_datadir}/%{name}/$tool $RPM_BUILD_ROOT%{_bindir}/hp-$tool
done

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/hplip

mv $RPM_BUILD_ROOT{%{_datadir}/%{name}/%{name}.conf,%{_sysconfdir}/hp}
rm -rf $RPM_BUILD_ROOT{%{_bindir}/foomatic-rip,%{_libdir}/*.la,%{_docdir}/hpijs*} \
	$RPM_BUILD_ROOT{%{_datadir}/%{name}/hplip{,.sh},%{_sysconfdir}/sane.d/*} \
	$RPM_BUILD_ROOT/etc/init.d

%clean
rm -rf $RPM_BUILD_ROOT

%post daemon
/sbin/chkconfig --add hplip
%service hplip restart "HPLIP daemons"

%preun daemon
if [ "$1" = "0" ]; then
	%service hplip stop
	/sbin/chkconfig --del hplip
fi

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post sane
/bin/grep -q '^hpaio' /etc/sane.d/dll.conf || echo hpaio >> /etc/sane.d/dll.conf

%postun sane
if [ "$1" = "0" ]; then
	/bin/sed -e'/^hpaio/d' -i /etc/sane.d/dll.conf || :
fi

%files
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_bindir}/hpijs
%attr(755,root,root) %{_bindir}/hp-align
%attr(755,root,root) %{_bindir}/hp-clean
%attr(755,root,root) %{_bindir}/hp-check
%attr(755,root,root) %{_bindir}/hp-colorcal
%attr(755,root,root) %{_bindir}/hp-firmware
%attr(755,root,root) %{_bindir}/hp-info
%attr(755,root,root) %{_bindir}/hp-levels
%attr(755,root,root) %{_bindir}/hp-makecopies
%attr(755,root,root) %{_bindir}/hp-makeuri
%attr(755,root,root) %{_bindir}/hp-print
%attr(755,root,root) %{_bindir}/hp-probe
%attr(755,root,root) %{_bindir}/hp-sendfax
%attr(755,root,root) %{_bindir}/hp-setup
%attr(755,root,root) %{_bindir}/hp-testpage
%attr(755,root,root) %{_bindir}/hp-timedate
%attr(755,root,root) %{_bindir}/hp-unload
%dir %{_datadir}/hplip
# info about GPL v2 for some files
%{_datadir}/hplip/COPYING
# initscript for hplip helpers
#%{_datadir}/hplip/hplip
#%{_datadir}/hplip/hplip.sh
%{_datadir}/hplip/__init__.py
%dir %{_datadir}/hplip/copier
%{_datadir}/hplip/copier/*.py
#%{_datadir}/hplip/*.png
#%{_datadir}/hplip/*.html
%attr(755,root,root) %{_datadir}/hplip/align
%attr(755,root,root) %{_datadir}/hplip/check
%attr(755,root,root) %{_datadir}/hplip/clean
%attr(755,root,root) %{_datadir}/hplip/colorcal
%attr(755,root,root) %{_datadir}/hplip/firmware
%attr(755,root,root) %{_datadir}/hplip/info
%attr(755,root,root) %{_datadir}/hplip/levels
%attr(755,root,root) %{_datadir}/hplip/makeuri
%attr(755,root,root) %{_datadir}/hplip/makecopies
%attr(755,root,root) %{_datadir}/hplip/print
%attr(755,root,root) %{_datadir}/hplip/probe
%attr(755,root,root) %{_datadir}/hplip/sendfax
%attr(755,root,root) %{_datadir}/hplip/setup
%attr(755,root,root) %{_datadir}/hplip/testpage
%attr(755,root,root) %{_datadir}/hplip/timedate
%attr(755,root,root) %{_datadir}/hplip/unload
%{_datadir}/hplip/base
# need look
%{_datadir}/hplip/data
# fax subpackage ?
%{_datadir}/hplip/fax
%{_datadir}/hplip/pcard
%{_datadir}/hplip/plugins
%{_datadir}/hplip/prnt
%{_datadir}/hplip/scan
%{_datadir}/hplip/ui
%attr(755,root,root) %{py_sitedir}/*.so
%dir %{_sysconfdir}/hp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hp/*

%files daemon
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/hp*
%attr(754,root,root) /etc/rc.d/init.d/hplip
%attr(755,root,root) %{_datadir}/hplip/hpssd.py

%files gui-tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hp-fab
%attr(755,root,root) %{_bindir}/hp-toolbox
%attr(755,root,root) %{_datadir}/hplip/fab
%attr(755,root,root) %{_datadir}/hplip/toolbox

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhpip*.so.*

%files sane
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsane*.so.*
%attr(755,root,root) %{_libdir}/sane/libsane*.so.*
%{_datadir}/hplip/hpaio.desc

%if %{with cups}
%files ppd
%defattr(644,root,root,755)
%{_cupsppddir}/*

%files -n cups-backend-hp
%defattr(644,root,root,755)
%attr(755,root,root) %{_ulibdir}/cups/backend/hp
%endif
