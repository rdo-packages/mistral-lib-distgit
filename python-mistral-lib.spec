%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1

%global library mistral-lib
%global module mistral_lib

%global common_desc Python library for writing custom Mistral actions

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    Python library for writing custom Mistral actions
License:    ASL 2.0
URL:        http://launchpad.net/mistral/

Source0:    http://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-macros

%package -n python3-%{library}
Summary:    Python library for writing custom Mistral actions
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

# test dependencies

BuildRequires:  python3-eventlet >= 0.20.0
BuildRequires:  python3-oslotest
BuildRequires:  python3-subunit
BuildRequires:  python3-oslo-log >= 3.36.0
BuildRequires:  python3-oslo-serialization >= 2.21.1
BuildRequires:  python3-testrepository
BuildRequires:  python3-testtools >= 2.2.0
BuildRequires:  python3-yaql >= 1.1.3

Requires: python3-eventlet >= 0.20.0
Requires: python3-oslo-log >= 3.36.0
Requires: python3-oslo-serialization >= 2.21.1
Requires: python3-pbr >= 2.0.0
Requires: python3-yaql >= 1.1.3

%description -n python3-%{library}
%{common_desc}


%package -n python3-%{library}-tests
Summary:    Mistral custom actions library tests
%{?python_provide:%python_provide python3-%{library}-tests}
Requires:   python3-%{library} = %{version}-%{release}

Requires:       python3-oslotest
Requires:       python3-subunit
Requires:       python3-testrepository

%description -n python3-%{library}-tests
Mistral custom actions library tests.

This package contains the Mistral custom actions library test files.

%if 0%{?with_doc}
%package -n python-%{library}-doc
Summary:    Mistral custom actions library documentation

BuildRequires: python3-sphinx
BuildRequires: python3-openstackdocstheme

%description -n python-%{library}-doc
Mistral custom actions library documentation

This package contains the documentation.
%endif

%description
%{common_desc}


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
sphinx-build-3 -b html doc/source doc/build/html
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

%check
%{__python3} setup.py test

%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.egg-info
%exclude %{python3_sitelib}/%{module}/tests

%files -n python3-%{library}-tests
%{python3_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
