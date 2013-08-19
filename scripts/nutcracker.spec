Summary: Twitter's nutcracker redis and memcached proxy
Name: nutcracker
Version: 0.2.4
Release: tagged2
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

#Install example confog file
%{__install} -p -D -m 0644 conf/%{name}.yml %{buildroot}%{_sysconfdir}/%{name}/%{name}.yml

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
%defattr(-,root,root,-)
/usr/sbin/nutcracker
/usr/share/man/man8/nutcracker.8.gz
%{_initrddir}/%{name}
%config(noreplace)%{_sysconfdir}/%{name}/%{name}.yml
