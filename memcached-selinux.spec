%global selinuxtype	targeted
%global moduletype	contrib
%global modulename	memcached

Name: memcached-selinux 
Version: 1.0
Release: 2%{?dist}
License: GPLv2
#URL: # URL to git repository with policy source files
Summary: SELinux policies for memcached.
#cd memcached-selinux-% {version}
#make
#cd ..
#tar -czf memcached-selinux-% {version}.tar.gz memcached-selinux-% {version}/
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch
BuildRequires: selinux-policy
%selinux_requires

%description
SELinux security policy for memcached a high-performance, dstributed memory object caching system.

%prep
%setup -q
 
%build
make

%pre 
%selinux_relabel_pre -s %{selinuxtype}
 
%install
# install policy modules
install -d %{buildroot}%{_datadir}/selinux/packages
install -d -p %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}
install -p -m 644 %{modulename}.if %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}
install -m 0644 %{modulename}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages

%check

%post
%selinux_modules_install -s %{selinuxtype} -p 200 %{_datadir}/selinux/packages/%{modulename}.pp.bz2 &> /dev/null

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} -p 200 %{modulename}
fi

%posttrans 
%selinux_relabel_post -s %{selinuxtype} &> /dev/null

%files 
%defattr(-,root,root,0755) 
%attr(0644,root,root) %{_datadir}/selinux/packages/%{modulename}.pp.bz2 
%attr(0644,root,root) %{_datadir}/selinux/devel/include/%{moduletype}/%{modulename}.if
%license COPYING

%changelog
* Thu Dec 14 2017 Vit Mojzis <vmojzis@redhat.com> -  1.0 - 2
- Allow memcached_t to mmap memcached_exec_t

* Thu Jun 15 2017 vmojzis@redhat.com -  1.0 - 1 
- Initial build

