# TODO:
#	- Review unpackaged files
#       - write initscript (based on /usr/share/hplip/hplip
#       - add desktop file for toolbox
#       - "env python" -> "/usr/bin/python"
#       - symlinks in /usr/bin for scripts from /usr/share/hplip
#       - all scripts are in python, merge pyhton subpackage to main
#       package ?
#       - /usr/share/hplip/toolbox requires python-qt
#
# Conditional build:
%bcond_without	cups	# without CUPS support
#
Summary:	Hewlett-Packard Linux Imaging and Printing Project
Summary(pl):	Serwer dla drukarek HP Inkjet
Name:		hplip
Version:	0.9.11
Release:	0.1
License:	BSD, GPL v2 and MIT
Group:		Applications/System
Source0:	http://dl.sourceforge.net/hplip/%{name}-%{version}.tar.gz
# Source0-md5:	5cf362c972d5b1733af4fb8e2ade92e4
Source1:	%{name}.init
URL:		http://hplip.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_cups:BuildRequires:	cups-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	libusb-devel
BuildRequires:	net-snmp-devel
BuildRequires:	openssl-devel
BuildRequires:	python-devel
Obsoletes:	hpijs
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

%package libs
Summary:	HPLIP Libraries
Summary(pl):	Biblioteki HPLIP
Group:		Libraries

%description libs
HPLIP Libraries.

%description libs -l pl
Biblioteki HPLIP.

%package sane
Summary:	HPLIP SANE Libraries
Summary(pl):	Biblioteki HPLIP SANE
Group:		Libraries

%description sane
HPLIP SANE Libraries.

%description sane -l pl
Biblioteki HPLIP SANE.

%package ppd
Summary:	PPD database for Hewlett Packard printers
Summary(pl):	Baza danych PPD dla drukarek Hewlett Packard
Group:		Applications/System
Requires:	cups

%description ppd
PPD database for Hewlett Packard printers.

%description ppd -l pl
Baza danych PPD dla drukarek Hewlett Packard.

%package -n cups-backend-hp
Summary:	HP backend for CUPS
Summary(pl):	Backend HP dla CUPS-a
Group:		Applications/Printing
Requires:	cups

%description -n cups-backend-hp
This package allow CUPS printing on HP printers.

%description -n cups-backend-hp -l pl
Ten pakiet umo¿liwia drukowanie z poziomu CUPS-a na drukarkach HP.

%package -n python-%{name}
Summary:	Python HPLIP bindings
Summary(pl):	Interfejs Pythonowy do HPLIP
Group:		Development/Languages/Python

%description -n python-%{name}
Python HPLIP bindings.

%description -n python-%{name} -l pl
Interfejs Pythonowy do HPLIP.

%prep
%setup -q

%build
install /usr/share/automake/config.* .
install /usr/share/automake/config.* prnt
CXXFLAGS="%{rpmcflags} -fno-exceptions -fno-rtti"
%configure \
	--enable-foomatic-install \
	%{!?with_cups:--disable-cups-install}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%if %{with cups}
install -d $RPM_BUILD_ROOT$(cups-config --datadir)/model \
	$RPM_BUILD_ROOT$(cups-config --serverbin)/filter
%endif

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	rpm_install=yes

%if %{with cups}
rm -f $RPM_BUILD_ROOT%{_cupsppddir}/foomatic-ppds
mv $RPM_BUILD_ROOT{%{_datadir}/ppd/HP/*,%{_cupsppddir}}
%endif

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/hplip

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post sane -p /sbin/ldconfig
%postun sane -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc hplip_readme.html
%attr(755,root,root) %{_bindir}/hp*
%attr(755,root,root) %{_sbindir}/hp*
%attr(754,root,root) /etc/rc.d/init.d/hplip
%dir %{_datadir}/hplip
# info about GPL v2 for some files
%{_datadir}/hplip/COPYING
# initscript for hplip helpers
#%{_datadir}/hplip/hplip
#%{_datadir}/hplip/hplip.sh
%{_datadir}/hplip/__init__.py
#%{_datadir}/hplip/*.png
#%{_datadir}/hplip/*.html
%attr(755,root,root) %{_datadir}/hplip/align
%attr(755,root,root) %{_datadir}/hplip/check
%attr(755,root,root) %{_datadir}/hplip/clean
%attr(755,root,root) %{_datadir}/hplip/colorcal
%attr(755,root,root) %{_datadir}/hplip/fab
%attr(755,root,root) %{_datadir}/hplip/hpssd.py
%attr(755,root,root) %{_datadir}/hplip/info
%attr(755,root,root) %{_datadir}/hplip/levels
%attr(755,root,root) %{_datadir}/hplip/makeuri
%attr(755,root,root) %{_datadir}/hplip/photo
%attr(755,root,root) %{_datadir}/hplip/print
%attr(755,root,root) %{_datadir}/hplip/sendfax
%attr(755,root,root) %{_datadir}/hplip/setup
%attr(755,root,root) %{_datadir}/hplip/testpage
%attr(755,root,root) %{_datadir}/hplip/toolbox
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

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhpip*.so.*

%files sane
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsane*.so.*

%files -n python-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/*.so

%if %{with cups}
%files ppd
%defattr(644,root,root,755)
%{_cupsppddir}/*

%files -n cups-backend-hp
%defattr(644,root,root,755)
%attr(755,root,root) %{_ulibdir}/cups/backend/hp
%endif
