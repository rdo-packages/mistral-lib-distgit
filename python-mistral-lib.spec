# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
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

BuildArch:  noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%package -n python%{pyver}-%{library}
Summary:    Python library for writing custom Mistral actions
%{?python_provide:%python_provide python%{pyver}-%{library}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools

# test dependencies

BuildRequires:  python%{pyver}-eventlet >= 0.20.0
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-oslo-log >= 3.36.0
BuildRequires:  python%{pyver}-oslo-serialization >= 2.21.1
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-testtools >= 2.2.0
BuildRequires:  python%{pyver}-yaql >= 1.1.3

Requires: python%{pyver}-eventlet >= 0.20.0
Requires: python%{pyver}-oslo-log >= 3.36.0
Requires: python%{pyver}-oslo-serialization >= 2.21.1
Requires: python%{pyver}-pbr >= 2.0.0
Requires: python%{pyver}-yaql >= 1.1.3

%description -n python%{pyver}-%{library}
%{common_desc}


%package -n python%{pyver}-%{library}-tests
Summary:    Mistral custom actions library tests
%{?python_provide:%python_provide python%{pyver}-%{library}-tests}
Requires:   python%{pyver}-%{library} = %{version}-%{release}

Requires:       python%{pyver}-oslotest
Requires:       python%{pyver}-subunit
Requires:       python%{pyver}-testrepository

%description -n python%{pyver}-%{library}-tests
Mistral custom actions library tests.

This package contains the Mistral custom actions library test files.

%if 0%{?with_doc}
%package -n python-%{library}-doc
Summary:    Mistral custom actions library documentation

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-openstackdocstheme

%description -n python-%{library}-doc
Mistral custom actions library documentation

This package contains the documentation.
%endif

%description
%{common_desc}


%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

%check
%{pyver_bin} setup.py test

%files -n python%{pyver}-%{library}
%license LICENSE
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/%{module}-*.egg-info
%exclude %{pyver_sitelib}/%{module}/tests

%files -n python%{pyver}-%{library}-tests
%{pyver_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
