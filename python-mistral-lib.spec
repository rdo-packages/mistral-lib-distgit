%{!?upstream_version: %global upstream_version %{version}}
%global upstream_name mistral-lib

%{?!_licensedir:%global license %%doc}

Name:           python-%{upstream_name}
Release:        XXX
Summary:        Python library for Mistral custom actions
Version:        XXX

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/${upstream_name}
Source0:        https://tarballs.openstack.org/%{upstream_name}/%{upstream_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools

Requires: python-oslo-serialization >= 1.10.0
Requires: python-pbr >= 1.8

Provides:  mistral-lib = %{version}-%{release}
Obsoletes: mistral-lib < %{version}-%{release}

%prep
%autosetup -n %{upstream_name}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt


%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%description
Python library for creating custom Mistral actions

%files
%license LICENSE
%doc README.rst AUTHORS ChangeLog
%{python2_sitelib}/mistral_lib
%exclude %{python2_sitelib}/mistral_lib/tests*

%changelog
