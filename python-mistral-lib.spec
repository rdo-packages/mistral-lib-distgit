%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


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

%package -n python2-%{library}
Summary:    Python library for writing custom Mistral actions
%{?python_provide:%python_provide python2-%{library}}

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools

# test dependencies

BuildRequires:  python2-oslotest
BuildRequires:  python2-subunit
BuildRequires:  python2-oslo-serialization >= 2.18.0
%if 0%{?fedora} > 0
BuildRequires:  python2-testrepository
%else
BuildRequires:  python-testrepository
%endif

Requires: python2-oslo-serialization >= 2.18.0
Requires: python2-pbr >= 2.0.0

%description -n python2-%{library}
%{common_desc}


%package -n python2-%{library}-tests
Summary:    Mistral custom actions library tests
Requires:   python2-%{library} = %{version}-%{release}

Requires:       python2-oslotest
Requires:       python2-subunit
%if 0%{?fedora} > 0
Requires:       python2-testrepository
%else
Requires:       python-testrepository
%endif

%description -n python2-%{library}-tests
Mistral custom actions library tests.

This package contains the Mistral custom actions library test files.

%package -n python-%{library}-doc
Summary:    Mistral custom actions library documentation

BuildRequires: python-sphinx
# FIXME: remove following line when a new release including https://review.openstack.org/#/c/485542/ is in u-c
BuildRequires: python2-oslo-sphinx
BuildRequires: python2-openstackdocstheme

%description -n python-%{library}-doc
Mistral custom actions library documentation

This package contains the documentation.

%if 0%{?with_python3}
%package -n python3-%{library}
Summary:    Python library for writing custom Mistral actions
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git

# test dependencies

BuildRequires:  python3-oslotest
BuildRequires:  python3-subunit
BuildRequires:  python3-testrepository
BuildRequires:  python3-oslo-serialization >= 2.18.0

Requires:       python3-babel >= 2.3.4
Requires:       python3-oslo-serialization >= 2.18.0
Requires:       python3-pbr >= 2.0.0

%description -n python3-%{library}
%{common_desc}


%package -n python3-%{library}-tests
Summary:    Python library for writing custom Mistral actions
Requires:   python3-%{library} = %{version}-%{release}

Requires:       python3-oslotest
Requires:       python3-subunit
Requires:       python3-testrepository

%description -n python3-%{library}-tests
%{common_desc}

This package contains the Mistral custom actions library test files.

%endif # with_python3


%description
%{common_desc}


%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files -n python2-%{library}
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/%{module}-*.egg-info
%exclude %{python2_sitelib}/%{module}/tests

%files -n python2-%{library}-tests
%{python2_sitelib}/%{module}/tests

%files -n python-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst

%if 0%{?with_python3}
%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.egg-info
%exclude %{python3_sitelib}/%{module}/tests

%files -n python3-%{library}-tests
%{python3_sitelib}/%{module}/tests
%endif # with_python3

%changelog
