%define		_modname	netools
Summary:	Networking tools
Summary(pl):	Narz�dzia sieciowe
Name:		php-pecl-%{_modname}
Version:	0.2
Release:	0.1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/%{_modname}-%{version}.tgz
URL:		http://pear.php.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	php-devel
Requires:	php-common
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
Netools provides tools to deal with devices, TCP and UDP
clients/servers, etc.

%description -l pl
Netools-y dostarczaj� narz�dzi do pracy z urz�dzeniami,
klientami/serwerami TCP oraz UDP, itp.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%{__aclocal}
%{__autoconf}
%configure \
	--with-%{_modname}=%{_prefix}/X11R6/include/X11/

%{__make} CPPFLAGS="-DHAVE_CONFIG_H -I%{_prefix}/X11R6/include/X11/"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install %{_modname} %{_sysconfdir}/php.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove %{_modname} %{_sysconfdir}/php.ini
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/CREDITS
%attr(755,root,root) %{extensionsdir}/%{_modname}.so