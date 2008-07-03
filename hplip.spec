# TODO:
#	- add desktop file for toolbox
#	- prepare fax packages for fax utilities
#	- separate package for hpijs (hplip Req: hpijs, hplip-hpijs Prov: hpijs?)
#	- separate udev files
#	- it would be good to kill "python /usr/share/hplip/hpssd.py" during upgrade/uninstall
#	- hpaio.desc removed in Fedora
#
Summary:	Hewlett-Packard Linux Imaging and Printing Project
Summary(pl.UTF-8):	Serwer dla drukarek HP Inkjet
Name:		hplip
Version:	2.8.6
Release:	1
License:	BSD, GPL v2 and MIT
Group:		Applications/System
Source0:	http://dl.sourceforge.net/hplip/%{name}-%{version}.tar.gz
# Source0-md5:	2571d7bf54d20a9b915288816e8cd895
Patch0:		%{name}-ui-optional.patch
URL:		http://hplip.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cups-devel
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
Obsoletes:	hplip-daemon
Obsoletes:	hpijs
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

%prep
%setup -q
#%patch0 -p1
sed -i -e's,^#!/usr/bin/env python$,#!/usr/bin/python,' *.py

%build
install /usr/share/automake/config.* .
install /usr/share/automake/config.* prnt
CXXFLAGS="%{rpmcflags} -fno-exceptions -fno-rtti"
%configure \
	--disable-foomatic-xml-install \
	--enable-foomatic-ppd-install
%{__make} \
	hpppddir=/usr/share/cups/model \
	hpppddir=%{_cupsppddir}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT$(cups-config --datadir)/model \
	$RPM_BUILD_ROOT$(cups-config --serverbin)/filter

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	rpm_install=yes \
	hpppddir=%{_cupsppddir}

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

%clean
# rm -rf $RPM_BUILD_ROOT

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
%attr(755,root,root) %{_bindir}/hp-probe
%attr(755,root,root) %{_bindir}/hp-scan
%attr(755,root,root) %{_bindir}/hp-sendfax
%attr(755,root,root) %{_bindir}/hp-setup
%attr(755,root,root) %{_bindir}/hp-testpage
%attr(755,root,root) %{_bindir}/hp-timedate
%attr(755,root,root) %{_bindir}/hp-unload
%dir %{_datadir}/hplip
# info about GPL v2 for some files
#%{_datadir}/hplip/COPYING
# initscript for hplip helpers
#%{_datadir}/hplip/hplip
#%{_datadir}/hplip/hplip.sh
%{_datadir}/hplip/__init__.py
%dir %{_datadir}/hplip/copier
%{_datadir}/hplip/copier/*.py
#%{_datadir}/hplip/*.png
#%{_datadir}/hplip/*.html
%attr(755,root,root) %{_datadir}/hplip/align.py
%attr(755,root,root) %{_datadir}/hplip/check.py
%attr(755,root,root) %{_datadir}/hplip/clean.py
%attr(755,root,root) %{_datadir}/hplip/colorcal.py
%attr(755,root,root) %{_datadir}/hplip/firmware.py
%attr(755,root,root) %{_datadir}/hplip/hpssd.py
%attr(755,root,root) %{_datadir}/hplip/info.py
%attr(755,root,root) %{_datadir}/hplip/levels.py
%attr(755,root,root) %{_datadir}/hplip/makeuri.py
%attr(755,root,root) %{_datadir}/hplip/makecopies.py
%attr(755,root,root) %{_datadir}/hplip/probe.py
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
%attr(755,root,root) %{py_sitedir}/cupsext.so
%attr(755,root,root) %{py_sitedir}/hpmudext.so
%attr(755,root,root) %{py_sitedir}/pcardext.so
%attr(755,root,root) %{py_sitedir}/scanext.so
%dir %{_sysconfdir}/hp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hp/*

%files gui-tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hp-fab
%attr(755,root,root) %{_bindir}/hp-print
%attr(755,root,root) %{_bindir}/hp-toolbox
%attr(755,root,root) %{_bindir}/hp-systray
%attr(755,root,root) %{_datadir}/hplip/fab.py
%attr(755,root,root) %{_datadir}/hplip/print.py
%attr(755,root,root) %{_datadir}/hplip/toolbox.py
%attr(755,root,root) %{_datadir}/hplip/systray.py
%{_datadir}/hplip/plugins
%{_datadir}/hplip/ui
%{_datadir}/hplip/data/images
%{_desktopdir}/hplip.desktop

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhpip*.so.*
%attr(755,root,root) %{_libdir}/libhpmud*.so.*

%files sane
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/sane/libsane*.so.*
%{_datadir}/hplip/hpaio.desc

%files ppd
%defattr(644,root,root,755)
%{_cupsppddir}/*

%files -n cups-backend-hp
%defattr(644,root,root,755)
%attr(755,root,root) %{_ulibdir}/cups/backend/hp
%attr(755,root,root) %{_ulibdir}/cups/filter/foomatic-rip-hplip
%attr(755,root,root) %{_ulibdir}/cups/filter/hplipjs


%files -n cups-backend-hpfax
%defattr(644,root,root,755)
%attr(755,root,root) %{_ulibdir}/cups/backend/hpfax
