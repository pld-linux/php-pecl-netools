# TODO
# fix build:
# checking for lcrzo files in default path... not found
# configure: error: Please reinstall the lcrzo distribution
%define		_modname	netools
%define		_status		alpha
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

Summary:	Networking tools
Summary(pl):	Narzêdzia sieciowe
Name:		php-pecl-%{_modname}
Version:	0.2
Release:	0.1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	4e8da7ee78ff40c9eaec64568735eaeb
URL:		http://pecl.php.net/package/netools/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.238
%{?requires_php_extension}
Requires:	%{_sysconfdir}/conf.d
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Netools provides tools to deal with devices, TCP and UDP
clients/servers, etc.

In PECL status of this package is: %{_status}.

%description -l pl
Netools zawieraj± narzêdzia do pracy z urz±dzeniami sieciowymi,
klientami/serwerami TCP oraz UDP, itp.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure \
	--with-%{_modname}=%{_prefix}/X11R6/include/X11/

%{__make} CPPFLAGS="-DHAVE_CONFIG_H -I/usr/X11R6/include/X11"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
