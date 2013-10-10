Summary: Twitter's nutcracker redis and memcached proxy
Name: nutcracker
Version: 0.2.4
Release: tagged6
URL: https://github.com/jdi-tagged/twemproxy
Source0: %{name}-%{version}.tar.gz
License: Apache License 2.0
Group: System Environment/Libraries
Packager:  Tom Parrott <tomp@tomp.co.uk>
BuildRoot: %{_tmppath}/%{name}-root

%define debug_package %{nil}

%description
twemproxy (pronounced "two-em-proxy"), aka nutcracker is a fast and lightweight proxy for memcached and redis protocol.
It was primarily built to reduce the connection count on the backend caching servers.

%prep
%setup -q
autoreconf -fvi

%build

%configure --enable-debug=log
%__make

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}

%makeinstall PREFIX=%{buildroot}

#Install init script
%{__install} -p -D -m 0755 scripts/%{name}.init %{buildroot}%{_initrddir}/%{name}

mkdir -p %{buildroot}/var/log/nutcracker
mkdir -p %{buildroot}/var/run/nutcracker

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
 /sbin/service %{name} stop > /dev/null 2>&1
 /sbin/chkconfig --del %{name}
fi

%clean
[ %{buildroot} != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,nobody,nobody,-)
%attr(-,root,root) /usr/sbin/nutcracker
%attr(-,root,root) /usr/share/man/man8/nutcracker.8.gz
%attr(-,root,root) %{_initrddir}/%{name}
%dir /var/log/nutcracker
%dir /var/run/nutcracker
