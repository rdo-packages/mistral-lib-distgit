%{!?upstream_version: %global upstream_version %{version}}
%global upstream_name mistral-lib

%{?!_licensedir:%global license %%doc}

Name:           python-mistral-lib
Summary:        Python library for Mistral custom actions
Version:        XXX
Release:        XXX
License:        ASL 2.0
URL:            https://github.com/openstack/mistral-lib

Source0:        https://tarballs.openstack.org/%{upstream_name}/%{upstream_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  git
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  python-pbr

Requires: python-oslo-serialization >= 1.10.0
Requires: python-pbr >= 1.8

Provides:  mistral-lib = %{version}-%{release}
Obsoletes: mistral-lib < %{version}-%{release}

%prep
%autosetup -n %{upstream_name}-%{upstream_version} -S git
rm -rf *.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}

%description
Python library for creating custom Mistral actions

%files
%license LICENSE
%doc README.rst AUTHORS ChangeLog
%{python2_sitelib}/mistral_lib
%exclude %{python2_sitelib}/mistral_lib/test*
%{_datadir}/%{name}
%{_datadir}/%{upstream_name}

%changelog

