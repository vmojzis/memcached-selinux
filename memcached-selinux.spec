%global selinuxtype	targeted
%global selinux_policyver 3.13.1-257
%global moduletype	services
%global modulename	memcached
 
Name: memcached-selinux 
Version: 1.0 
Release: 1%{?dist} 
License: GPLv2 
#URL: # URL to git repository with policy source files 
Summary: SELinux policy for memecached
#cd memcached-selinux-%{version}
#make
#cd ..
#tar -czf memcached-selinux-%{version}.tar.gz memcached-selinux-%{version}/
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch 
Requires: selinux-policy >= %{selinux_policyver} 
BuildRequires: git 
BuildRequires: pkgconfig(systemd) 
BuildRequires: selinux-policy 
BuildRequires: selinux-policy-devel 
Requires(post): selinux-policy-base >= %{selinux_policyver} 
Requires(post): libselinux-utils 
Requires(post): policycoreutils

%if 0%{?fedora} 
Requires(post): policycoreutils-python-utils 
%else
Requires(post): policycoreutils-python 
%endif
 
%description
SELinux policy modules for use with memcached

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
%selinux_modules_install -s %{selinuxtype} -p 300 %{_datadir}/selinux/packages/%{modulename}.pp.bz2

 
%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} -p 300 %{modulename} 
fi  

%posttrans 
%selinux_relabel_post -s %{selinuxtype}

%files 
%defattr(-,root,root,0755) 
%attr(0644,root,root) %{_datadir}/selinux/packages/%{modulename}.pp.bz2 
%attr(0644,root,root) %{_datadir}/selinux/devel/include/%{moduletype}/%{modulename}.if  

%changelog
* Thu Jun 15 2017 vmojzis@redhat.com -  1.0 - 1 
- Initial build

