%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


%global library mistral-lib
%global module mistral_lib

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    Python library for writing custom Mistral actions
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    http://tarballs.openstack.org/%{library}/%{library}-master.tar.gz

BuildArch:  noarch

%package -n python2-%{library}
Summary:    Python library for writing custom Mistral actions
%{?python_provide:%python_provide python2-%{library}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git
# Required to compile translation files (add only if exist)
BuildRequires:  python-babel

Requires:   python-oslo-config >= 2:3.4.0
# If translation files exist
Requires:       python-%{library}-lang = %{version}-%{release}

%description -n python2-%{library}
Python library for writing custom Mistral actions


%package -n python2-%{library}-tests
Summary:    Mistral custom actions library tests.
Requires:   python2-%{library} = %{version}-%{release}

%description -n python2-%{library}-tests
Mistral custom actions library tests.

This package contains the Mistral custom actions library test files.


%package -n python-%{library}-doc
Summary:    Mistral custom actions library documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description -n python-%{library}-doc
Mistral custom actions library documentation

This package contains the documentation.

%if 0%{?with_python3}
%package -n python3-%{library}
Summary:    OpenStack Example library
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git

Requires:   python3-oslo-config >= 2:3.4.0
# If translation files exist
Requires:       python-%{library}-lang = %{version}-%{release}

%description -n python3-%{library}
Python library for writing custom Mistral actions


%package -n python3-%{library}-tests
Summary:    Python library for writing custom Mistral actions
Requires:   python3-%{library} = %{version}-%{release}

%description -n python3-%{library}-tests
Python library for writing custom Mistral actions

This package contains the Mistral custom actions library test files.

%endif # with_python3


%description
Python library for writing custom Mistral actions


%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

# Generate i18n files if translation files exist
%{__python2} setup.py compile_catalog -d build/lib/%{module}/locale

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

# Install i18n .mo files (.po and .pot are not required) if translation files exist
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/%{module}/locale/*/LC_*/%{module}*po
rm -f %{buildroot}%{python2_sitelib}/%{module}/locale/*pot
mv %{buildroot}%{python2_sitelib}/%{module}/locale %{buildroot}%{_datadir}/locale
%if 0%{?with_python3}
rm -rf %{buildroot}%{python3_sitelib}/%{module}/locale
%endif

# Find language files
%find_lang %{module} --all-name


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
%license LICENSE
%{python2_sitelib}/%{module}/tests

%files -n python-%{library}-doc
%license LICENSE
%doc html README.rst

# Only if translation files exist
%files -n python-%{library}-lang -f %{module}.lang

%if 0%{?with_python3}
%files python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.egg-info
%exclude %{python3_sitelib}/%{module}/tests

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{module}/tests
%endif # with_python3

%changelog
