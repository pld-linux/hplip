Summary:	Hewlett-Packard Linux Imaging and Printing Project
Summary(pl.UTF-8):	Serwer dla drukarek HP Inkjet
Name:		hplip
Version:	3.10.9
Release:	1
License:	BSD, GPL v2 and MIT
Group:		Applications/System
Source0:	http://dl.sourceforge.net/hplip/%{name}-%{version}.tar.gz
# Source0-md5:	609718830a26874fc0ea84a47b8132f3
Patch0:		%{name}-desktop.patch
Patch1:		unresolved.patch
URL:		http://hplipopensource.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cups-devel
BuildRequires:	dbus-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	libusb-compat-devel
BuildRequires:	libusb-devel
BuildRequires:	net-snmp-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	sane-backends-devel
BuildRequires:	sed >= 4.0
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	python-modules
Obsoletes:	hpijs
Obsoletes:	hplip-daemon
Obsoletes:	python-hplip
Conflicts:	ghostscript <= 7.00-3
# used in scan.py
Suggests:	python-ReportLab >= 2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _ulibdir        %{_prefix}/lib

%define 	_cupsdir 	%(cups-config --datadir)
%define		_cupsppddir	%{_cupsdir}/model

%description
The Hewlett-Packard Linux Imaging and Printing project (HPLIP)
provides a unified single and multi-function connectivity solution for
Linux. The goal of this project is to provide "radically simple"
printing, faxing, scanning, photo-card access, and device management
to the consumer and small business desktop Linux users.

%package gui-tools
Summary:	HPLIP GUI tools
Summary(pl.UTF-8):	Narzędzia graficzne HPLIP
Group:		Applications/System
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	python-PyQt4

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
Requires:	cups-filter-foomatic
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

%description -n cups-backend-hp
This package allow CUPS printing on HP printers.

%description -n cups-backend-hp -l pl.UTF-8
Ten pakiet umożliwia drukowanie z poziomu CUPS-a na drukarkach HP.

%package -n cups-backend-hpfax
Summary:	HP fax backend for CUPS
Summary(pl):	Backend HP fax dla CUPS-a
Group:		Applications/Printing
Requires:	%{name} = %{version}-%{release}
Requires:	cups

%description -n cups-backend-hpfax
This package allow CUPS faxing using HP AiO devices.

%description -n cups-backend-hpfax -l pl.UTF-8
Ten pakiet umożliwia wysyłanie faksów z poziomu CUPS-a poprzez
urządzenia HP AiO.

%package -n hal-hplip
Summary:	HAL device information for HPLIP
Group:		Applications/Printing
Requires:	%{name} = %{version}-%{release}

%description -n hal-hplip
HAL device information for HPLIP supported devices

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%{__sed} -i -e's,^#!/usr/bin/env python$,#!/usr/bin/python,' *.py

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
install /usr/share/automake/config.* prnt
%{__sed} -i -e 's#test -d /usr/share/polkit-1#true#' configure
CXXFLAGS="%{rpmcflags} -fno-exceptions -fno-rtti"
%configure \
	--enable-hpcups-install \
	--enable-cups-drv-install \
	--enable-cups-ppd-install \
	--enable-hpijs-install \
	--enable-foomatic-ppd-install \
	--enable-foomatic-drv-install  \
	--enable-foomatic-rip-hplip-install \
	--enable-policykit \
	--enable-pp-build \
	--enable-udev-acl-rules \
	--with-mimedir=%{_datadir}/cups/mime \
	--with-hpppddir=%{_cupsppddir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_cupsppddir} \
	$RPM_BUILD_ROOT$(cups-config --serverbin)/filter

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	rpm_install=yes

for tool in align clean colorcal fab firmware info levels makecopies makeuri print \
		probe scan sendfax setup testpage timedate toolbox unload ; do
	ln -sf %{_datadir}/%{name}/$tool.py $RPM_BUILD_ROOT%{_bindir}/hp-$tool
done

rm -rf $RPM_BUILD_ROOT{%{_bindir}/foomatic-rip,%{_libdir}/*.la,%{_docdir}/hpijs*} \
	$RPM_BUILD_ROOT{%{_datadir}/%{name}/hplip{,.sh},%{_sysconfdir}/sane.d/*} \
	$RPM_BUILD_ROOT/etc/init.d
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/{install.py,hplip-install}
rm -f $RPM_BUILD_ROOT%{_libdir}/sane/*.la
rm -f $RPM_BUILD_ROOT%{py_sitedir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/libhp{ip,mud}.so

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
%{_sysconfdir}/udev/rules.d/*
%attr(755,root,root) %{_bindir}/hpijs
%attr(755,root,root) %{_bindir}/hp-align
%attr(755,root,root) %{_bindir}/hp-check
%attr(755,root,root) %{_bindir}/hp-clean
%attr(755,root,root) %{_bindir}/hp-colorcal
%attr(755,root,root) %{_bindir}/hp-firmware
%attr(755,root,root) %{_bindir}/hp-info
%attr(755,root,root) %{_bindir}/hp-levels
%attr(755,root,root) %{_bindir}/hp-makecopies
%attr(755,root,root) %{_bindir}/hp-makeuri
%attr(755,root,root) %{_bindir}/hp-mkuri
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
%{_datadir}/dbus-1/system-services/com.hp.hplip.service
%dir %{_datadir}/hplip
# info about GPL v2 for some files
#%{_datadir}/hplip/COPYING
# initscript for hplip helpers
#%{_datadir}/hplip/hplip
#%{_datadir}/hplip/hplip.sh
%{_datadir}/hplip/__init__.py
%dir %{_datadir}/hplip/copier
%{_datadir}/hplip/copier/*.py
%attr(755,root,root) %{_datadir}/hplip/align.py
%attr(755,root,root) %{_datadir}/hplip/check.py
%attr(755,root,root) %{_datadir}/hplip/clean.py
%attr(755,root,root) %{_datadir}/hplip/colorcal.py
%attr(755,root,root) %{_datadir}/hplip/firmware.py
%attr(755,root,root) %{_datadir}/hplip/hpdio.py
%attr(755,root,root) %{_datadir}/hplip/hpssd.py
%attr(755,root,root) %{_datadir}/hplip/info.py
%attr(755,root,root) %{_datadir}/hplip/levels.py
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
%{_datadir}/hplip/fax
%{_datadir}/hplip/installer
%{_datadir}/hplip/pcard
%{_datadir}/hplip/prnt
%{_datadir}/hplip/scan
%{_datadir}/polkit-1/actions/com.hp.hplip.policy
%attr(755,root,root) %{py_sitedir}/cupsext.so
%attr(755,root,root) %{py_sitedir}/hpmudext.so
%attr(755,root,root) %{py_sitedir}/pcardext.so
%attr(755,root,root) %{py_sitedir}/scanext.so
/etc/dbus-1/system.d/com.hp.hplip.conf
%{_datadir}/cups/mime/pstotiff.types
%{_datadir}/cups/mime/pstotiff.convs
%dir %{_sysconfdir}/hp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hp/*

%files gui-tools
%defattr(644,root,root,755)
%{_sysconfdir}/xdg/autostart/hplip-systray.desktop
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
#%{_datadir}/hplip/plugins
%{_datadir}/hplip/ui4
%{_datadir}/hplip/data/images
%{_desktopdir}/hplip.desktop
%dir %{_sharedstatedir}/hp
%verify(not md5 mtime size) %{_sharedstatedir}/hp/hplip.state

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhpip*.so.*
%attr(755,root,root) %{_libdir}/libhpmud*.so.*

%files sane
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/sane/libsane*.so.*
%attr(755,root,root) %{_libdir}/sane/libsane*.so

%files ppd
%defattr(644,root,root,755)
%{_cupsppddir}/*
%{_datadir}/cups/drv/hp

%files -n cups-backend-hp
%defattr(644,root,root,755)
%attr(755,root,root) %{_ulibdir}/cups/backend/hp
%attr(755,root,root) %{_ulibdir}/cups/filter/foomatic-rip-hplip
%attr(755,root,root) %{_ulibdir}/cups/filter/hpcups
%attr(755,root,root) %{_ulibdir}/cups/filter/hplipjs
%attr(755,root,root) %{_ulibdir}/cups/filter/hpcac
%attr(755,root,root) %{_ulibdir}/cups/filter/pstotiff
%{_cupsdir}/drv/hp

%files -n cups-backend-hpfax
%defattr(644,root,root,755)
%attr(755,root,root) %{_ulibdir}/cups/backend/hpfax
%attr(755,root,root) %{_ulibdir}/cups/filter/hpcupsfax


%files -n hal-hplip
%defattr(644,root,root,755)
%{_datadir}/hal/fdi/preprobe/10osvendor/20-hplip-devices.fdi
