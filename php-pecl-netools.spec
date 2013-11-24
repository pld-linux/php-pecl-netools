# TODO
# fix build:
# checking for lcrzo files in default path... not found
# configure: error: Please reinstall the lcrzo distribution
%define		php_name	php%{?php_suffix}
%define		modname	netools
%define		status		alpha
Summary:	%{modname} - Networking tools
Summary(pl.UTF-8):	%{modname} - Narzędzia sieciowe
Name:		%{php_name}-pecl-%{modname}
Version:	0.2
Release:	0.2
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	4e8da7ee78ff40c9eaec64568735eaeb
URL:		http://pecl.php.net/package/netools/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
# ??? (lcrzo.h, lcrzo_init() in liblcrzo)
BuildRequires:	lcrzo-devel
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
Provides:	php(%{modname}) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Netools provides tools to deal with devices, TCP and UDP
clients/servers, etc.

In PECL status of this package is: %{status}.

%description -l pl.UTF-8
Netools zawierają narzędzia do pracy z urządzeniami sieciowymi,
klientami/serwerami TCP oraz UDP, itp.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
