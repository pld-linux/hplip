# TODO:
#	- Review unpackaged files
#	- Remove conflict with hpijs (binary name conflict) or add obsoletes
#	- package /usr/share/hplip (split into few separate subpackages?)
#
# Conditional build:
%bcond_without	cups	# without CUPS support
#
Summary:	Hewlett-Packard Linux Imaging and Printing Project
Summary(pl):	Serwer dla drukarek HP Inkjet
Name:		hplip
Version:	0.9.6
Release:	0.1
License:	BSD
Group:		Applications/System
Source0:	http://dl.sourceforge.net/hpinkjet/%{name}-%{version}.tar.gz
# Source0-md5:	a95d8087198e16dde758332b612fb112
URL:		http://hpinkjet.sourceforge.net/
BuildRequires:	automake
BuildRequires:	autoconf
%{?with_cups:BuildRequires:	cups-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	net-snmp-devel
BuildRequires:	openssl-devel
BuildRequires:	python-devel
Conflicts:	ghostscript <= 7.00-3
Conflicts:	hpijs
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
