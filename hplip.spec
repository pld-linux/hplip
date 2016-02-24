# TODO:
# - add desktop file for toolbox
# - separate hpijs package?
#
# Conditional build:
%bcond_without	dbus	# build dbus
%bcond_without	fax	# build fax, depends on dbus

%if %{without dbus}
%undefine	with_fax
%endif

Summary:	Hewlett-Packard Linux Imaging and Printing suite - printing and scanning using HP devices
Summary(pl.UTF-8):	Narzędzia Hewlett-Packard Linux Imaging and Printing - drukowanie i skanowanie przy użyciu urządzeń HP
Name:		hplip
Version:	3.16.2
Release:	1
License:	BSD (hpijs), MIT (low-level scanning and printing code), GPL v2 (the rest)
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/hplip/%{name}-%{version}.tar.gz
# Source0-md5:	e024f3b52b3b5be66da843fba7da4cf5
Patch0:		%{name}-desktop.patch
Patch1:		unresolved.patch
Patch2:		pld-distro.patch
# note: this patch adds support to fixing only certain binary plugins. Newer plugin
# version have differend md5 sums, different offsets, so handling new binaries need
# to be added
Patch3:		%{name}-binary-fixup.patch
Patch5:		%{name}-udev-rules.patch
URL:		http://hplipopensource.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cups-devel >= 1.2
%{?with_dbus:BuildRequires:	dbus-devel >= 1.0.0}
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	libusb-devel >= 1.0
BuildRequires:	net-snmp-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 2.2
BuildRequires:	python-modules >= 2.2
BuildRequires:	rpm-pythonprov
BuildRequires:	sane-backends-devel
BuildRequires:	sed >= 4.0
Requires:	%{name}-libs = %{version}-%{release}
Requires:	python-modules
Obsoletes:	hal-hplip
Obsoletes:	hpijs
Obsoletes:	hplip-daemon
Obsoletes:	python-hplip
Conflicts:	ghostscript <= 7.00-3
# used in scan.py
Suggests:	python-ReportLab >= 2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _ulibdir        %{_prefix}/lib

%define		cups_datadir	%(cups-config --datadir 2>/dev/null || echo ERROR)
%define		cups_mimedir	%{cups_datadir}/mime
%define		cups_ppddir	%{cups_datadir}/model
%define		cups_serverdir	%(cups-config --serverbin 2>/dev/null || echo ERROR)
%define		cups_backenddir	%{cups_serverdir}/backend
%define		cups_filterdir	%{cups_serverdir}/filter

%description
The Hewlett-Packard Linux Imaging and Printing project (HPLIP)
provides a unified single and multi-function connectivity solution for
Linux. The goal of this project is to provide "radically simple"
printing, faxing, scanning, photo-card access, and device management
to the consumer and small business desktop Linux users.

%description -l pl.UTF-8
Projekt Hewlett-Packard Linux Imaging and Printing (HPLIP) udostępnia
jednolite, wielofunkcyjne rozwiązanie dla Linuksa. Celem tego projektu
jest zapewnienie "radykalnie prostego" drukowania, faksowania,
skanowania, dostępu do kart fotograficznych oraz zarządzania
urządzeniami końcowym użytkownikom Linuksa.

%package gui-tools
Summary:	HPLIP GUI tools
Summary(pl.UTF-8):	Narzędzia HPLIP z graficznym interfejsem użytkownika
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	python-PyQt4

%description gui-tools
HPLIP GUI tools.

%description gui-tools -l pl.UTF-8
Narzędzia HPLIP z graficznym interfejsem użytkownika.

%package libs
Summary:	HPLIP Libraries
Summary(pl.UTF-8):	Biblioteki HPLIP
Group:		Libraries

%description libs
HPLIP Libraries.

%description libs -l pl.UTF-8
Biblioteki HPLIP.

%package sane
Summary:	HPLIP driver for SANE (scanner access)
Summary(pl.UTF-8):	Sterownik HPLIP dla SANE (dostęp do skanera)
Group:		Libraries
Requires(post):	/bin/grep
Requires(postun):	/bin/sed
Requires:	%{name} = %{version}-%{release}

%description sane
HPLIP driver for SANE (provides scanner access).

%description sane -l pl.UTF-8
Sterownik HPLIP dla SANE (umożliwia dostęp do skanera).

%package ppd
Summary:	PPD database for Hewlett Packard printers
Summary(pl.UTF-8):	Baza danych PPD dla drukarek Hewlett Packard
Group:		Applications/System
Requires:	cups
Requires:	cups-filters >= 1.0.43
Obsoletes:	hpijs-ppd

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
Requires:	cups-filters >= 1.0.43

%description -n cups-backend-hp
This package allows CUPS printing on HP printers.

%description -n cups-backend-hp -l pl.UTF-8
Ten pakiet umożliwia drukowanie z poziomu CUPS-a na drukarkach HP.

%package -n cups-backend-hpfax
Summary:	HP fax backend for CUPS
Summary(pl.UTF-8):	Backend HP fax dla CUPS-a
Group:		Applications/Printing
Requires:	%{name} = %{version}-%{release}
Requires:	cups

%description -n cups-backend-hpfax
This package allow CUPS faxing using HP AiO devices.

%description -n cups-backend-hpfax -l pl.UTF-8
Ten pakiet umożliwia wysyłanie faksów z poziomu CUPS-a poprzez
urządzenia HP AiO.

%prep
%setup -q
%undos Makefile.am
%patch0 -p1
%patch1 -p1
%patch2 -p1
#%patch3 -p1
%patch5 -p1

%{__sed} -i -e '1s,^#!/usr/bin/env python$,#!%{__python},' *.py fax/filters/pstotiff prnt/filters/hpps
find base fax installer prnt scan ui ui4 -name '*.py' | xargs \
	%{__sed} -i -e '1s,^#!/usr/bin/env python$,#!%{__python},'
%{__sed} -i -e 's#test -d /usr/share/polkit-1#true#' configure.in

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
CXXFLAGS="%{rpmcflags} -fno-exceptions -fno-rtti"
%configure \
	%{!?with_dbus:--disable-dbus-build} \
	%{!?with_fax:--disable-fax-build} \
	--enable-cups-drv-install \
	--enable-cups-ppd-install \
	--enable-foomatic-drv-install  \
	--enable-foomatic-ppd-install \
	--disable-foomatic-rip-hplip-install \
	--enable-hpcups-install \
	--enable-hpijs-install \
	--enable-policykit \
	--enable-pp-build \
	--with-cupsbackenddir=%{cups_backenddir} \
	--with-cupsfilterdir=%{cups_filterdir} \
	--with-hpppddir=%{cups_ppddir} \
	--with-mimedir=%{_datadir}/cups/mime
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/lib/hp

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

touch $RPM_BUILD_ROOT/var/lib/hp/hplip.state

for tool in align clean colorcal fab firmware info levels makecopies makeuri print \
		probe scan sendfax setup testpage timedate toolbox unload ; do
	ln -sf %{_datadir}/%{name}/$tool.py $RPM_BUILD_ROOT%{_bindir}/hp-$tool
done

# use filter from cups-filters package, the perl script from hplip does not work
# correctly with cups 1.7.x, and is an unnecessary functional duplicate
ln -s %{cups_filterdir}/foomatic-rip $RPM_BUILD_ROOT%{cups_filterdir}/foomatic-rip-hplip

# useless (nothing is going to link to installed libraries/modules)
%{__rm} $RPM_BUILD_ROOT{%{_libdir}/*.{so,la},%{_libdir}/sane/*.{so,la},%{py_sitedir}/*.la}
# handled by post script
%{__rm} $RPM_BUILD_ROOT/etc/sane.d/dll.conf
# junk
%{__rm} $RPM_BUILD_ROOT{%{_bindir}/hp-{uninstall,upgrade},%{_datadir}/hplip/{uninstall,upgrade}.py}
%{__rm} $RPM_BUILD_ROOT/usr/lib/systemd/system/hplip-printer@.service

%if %{without fax}
%{__rm} $RPM_BUILD_ROOT%{cups_filterdir}/pstotiff
%endif

# use udev, hal's dead
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/hal

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

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
%attr(755,root,root) %{_bindir}/hp-check
%attr(755,root,root) %{_bindir}/hp-clean
%attr(755,root,root) %{_bindir}/hp-colorcal
%attr(755,root,root) %{_bindir}/hp-config_usb_printer
%attr(755,root,root) %{_bindir}/hp-diagnose_plugin
%attr(755,root,root) %{_bindir}/hp-diagnose_queues
%attr(755,root,root) %{_bindir}/hp-firmware
%attr(755,root,root) %{_bindir}/hp-doctor
%attr(755,root,root) %{_bindir}/hp-info
%attr(755,root,root) %{_bindir}/hp-levels
%attr(755,root,root) %{_bindir}/hp-logcapture
%attr(755,root,root) %{_bindir}/hp-makecopies
%attr(755,root,root) %{_bindir}/hp-makeuri
%attr(755,root,root) %{_bindir}/hp-pkservice
%attr(755,root,root) %{_bindir}/hp-plugin
%attr(755,root,root) %{_bindir}/hp-probe
%attr(755,root,root) %{_bindir}/hp-query
%attr(755,root,root) %{_bindir}/hp-scan
%attr(755,root,root) %{_bindir}/hp-sendfax
%attr(755,root,root) %{_bindir}/hp-setup
%attr(755,root,root) %{_bindir}/hp-testpage
%attr(755,root,root) %{_bindir}/hp-timedate
%attr(755,root,root) %{_bindir}/hp-unload
%dir %{_datadir}/hplip
%{_datadir}/hplip/__init__.py
%dir %{_datadir}/hplip/copier
%{_datadir}/hplip/copier/*.py
%attr(755,root,root) %{_datadir}/hplip/align.py
%attr(755,root,root) %{_datadir}/hplip/check.py
%attr(755,root,root) %{_datadir}/hplip/check-plugin.py
%attr(755,root,root) %{_datadir}/hplip/clean.py
%attr(755,root,root) %{_datadir}/hplip/colorcal.py
%attr(755,root,root) %{_datadir}/hplip/config_usb_printer.py
%attr(755,root,root) %{_datadir}/hplip/diagnose_plugin.py
%attr(755,root,root) %{_datadir}/hplip/diagnose_queues.py
%attr(755,root,root) %{_datadir}/hplip/doctor.py
%attr(755,root,root) %{_datadir}/hplip/firmware.py
%attr(755,root,root) %{_datadir}/hplip/hpdio.py
%attr(755,root,root) %{_datadir}/hplip/hplip_clean.sh
%attr(755,root,root) %{_datadir}/hplip/hpssd.py
%attr(755,root,root) %{_datadir}/hplip/info.py
%attr(755,root,root) %{_datadir}/hplip/levels.py
%attr(755,root,root) %{_datadir}/hplip/logcapture.py
%attr(755,root,root) %{_datadir}/hplip/makecopies.py
%attr(755,root,root) %{_datadir}/hplip/makeuri.py
%attr(755,root,root) %{_datadir}/hplip/pkservice.py
%attr(755,root,root) %{_datadir}/hplip/plugin.py
%attr(755,root,root) %{_datadir}/hplip/probe.py
%attr(755,root,root) %{_datadir}/hplip/query.py
%attr(755,root,root) %{_datadir}/hplip/scan.py
%attr(755,root,root) %{_datadir}/hplip/sendfax.py
%attr(755,root,root) %{_datadir}/hplip/setup.py
%attr(755,root,root) %{_datadir}/hplip/testpage.py
%attr(755,root,root) %{_datadir}/hplip/timedate.py
%attr(755,root,root) %{_datadir}/hplip/unload.py
%{_datadir}/hplip/base
%dir %{_datadir}/hplip/data
%{_datadir}/hplip/data/ldl
%{_datadir}/hplip/data/localization
%{_datadir}/hplip/data/models
%{_datadir}/hplip/data/pcl
%{_datadir}/hplip/data/ps
# fax subpackage ?
%if %{with fax}
%{_datadir}/hplip/fax
%endif
%{_datadir}/hplip/installer
%{_datadir}/hplip/pcard
%{_datadir}/hplip/prnt
%{_datadir}/hplip/scan
%attr(755,root,root) %{py_sitedir}/cupsext.so
%attr(755,root,root) %{py_sitedir}/hpmudext.so
%attr(755,root,root) %{py_sitedir}/pcardext.so
%attr(755,root,root) %{py_sitedir}/scanext.so
%dir %{_sysconfdir}/hp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hp/hplip.conf
/lib/udev/rules.d/56-hpmud.rules
/etc/dbus-1/system.d/com.hp.hplip.conf
%{_datadir}/dbus-1/system-services/com.hp.hplip.service
%{_datadir}/polkit-1/actions/com.hp.hplip.policy

%files gui-tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hp-devicesettings
%attr(755,root,root) %{_bindir}/hp-fab
%attr(755,root,root) %{_bindir}/hp-faxsetup
%attr(755,root,root) %{_bindir}/hp-linefeedcal
%attr(755,root,root) %{_bindir}/hp-pqdiag
%attr(755,root,root) %{_bindir}/hp-print
%attr(755,root,root) %{_bindir}/hp-printsettings
%attr(755,root,root) %{_bindir}/hp-systray
%attr(755,root,root) %{_bindir}/hp-toolbox
%attr(755,root,root) %{_bindir}/hp-wificonfig
%attr(755,root,root) %{_datadir}/hplip/devicesettings.py
%attr(755,root,root) %{_datadir}/hplip/wificonfig.py
%attr(755,root,root) %{_datadir}/hplip/fab.py
%attr(755,root,root) %{_datadir}/hplip/faxsetup.py
%attr(755,root,root) %{_datadir}/hplip/linefeedcal.py
%attr(755,root,root) %{_datadir}/hplip/pqdiag.py
%attr(755,root,root) %{_datadir}/hplip/print.py
%attr(755,root,root) %{_datadir}/hplip/printsettings.py
%attr(755,root,root) %{_datadir}/hplip/systray.py
%attr(755,root,root) %{_datadir}/hplip/toolbox.py
%{_datadir}/hplip/ui4
%{_datadir}/hplip/data/images
%{_sysconfdir}/xdg/autostart/hplip-systray.desktop
%{_desktopdir}/hplip.desktop
%dir /var/lib/hp
%verify(not md5 mtime size) /var/lib/hp/hplip.state

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhpdiscovery.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhpdiscovery.so.0
%attr(755,root,root) %{_libdir}/libhpip.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhpip.so.0
%attr(755,root,root) %{_libdir}/libhpipp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhpipp.so.0
%attr(755,root,root) %{_libdir}/libhpmud.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhpmud.so.0

%files sane
%defattr(644,root,root,755)
%doc scan/sane/hpaio.desc
%attr(755,root,root) %{_libdir}/sane/libsane-hpaio.so.*.*.*
%attr(755,root,root) %{_libdir}/sane/libsane-hpaio.so.1

%files ppd
%defattr(644,root,root,755)
%if %{with fax}
%{cups_ppddir}/HP-Fax*.ppd.gz
%endif
%{cups_ppddir}/apollo-*.ppd.gz
%{cups_ppddir}/hp-*.ppd.gz

%files -n cups-backend-hp
%defattr(644,root,root,755)
%attr(755,root,root) %{cups_backenddir}/hp
%attr(755,root,root) %{cups_filterdir}/foomatic-rip-hplip
%attr(755,root,root) %{cups_filterdir}/hpcups
%attr(755,root,root) %{cups_filterdir}/hpps
%{cups_datadir}/drv/hp

%if %{with fax}
%files -n cups-backend-hpfax
%defattr(644,root,root,755)
%attr(755,root,root) %{cups_backenddir}/hpfax
%attr(755,root,root) %{cups_filterdir}/hpcupsfax
%attr(755,root,root) %{cups_filterdir}/pstotiff
%{cups_mimedir}/pstotiff.types
%{cups_mimedir}/pstotiff.convs
%endif
