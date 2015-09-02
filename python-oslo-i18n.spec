%global sname oslo.i18n
%global pypi_name oslo-i18n


%if 0%{?fedora}
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-oslo-i18n
Version:        XXX
Release:        XXX
Summary:        OpenStack i18n Python 2 library
License:        ASL 2.0
URL:            https://github.com/openstack/%{sname}
Source0:        https://pypi.python.org/packages/source/o/%{sname}/%{sname}-%{version}.tar.gz

BuildArch:      noarch

%description
The oslo.i18n library contain utilities for working with internationalization
(i18n) features, especially translation for text strings in an application
or library.

%package -n python2-%{pypi_name}
Summary:        OpenStack i18n Python 2 library
%{?python_provide:%python_provide python2-%{pypi_name}}
# python_provide does not exist in CBS Cloud buildroot
Provides:   python-%{pypi_name} = %{upstream_version}
Obsoletes:  python-%{pypi_name} < %{upstream_version}

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
BuildRequires:  python-babel
BuildRequires:  python-six

# test deps
BuildRequires:  python-mock
BuildRequires:  python-oslotest
BuildRequires:  python-hacking
BuildRequires:  python-coverage

Requires:       python-setuptools
Requires:       python-babel
Requires:       python-six

%description -n python2-%{pypi_name}
The oslo.i18n library contain utilities for working with internationalization
(i18n) features, especially translation for text strings in an application
or library.

%package -n python2-%{pypi_name}-doc
Summary:    Documentation for OpenStack i18n library
%{?python_provide:%python_provide python2-%{pypi_name}-doc}
# python_provide does not exist in CBS Cloud buildroot
Provides:   python-%{pypi_name}-doc = %{upstream_version}
Obsoletes:  python-%{pypi_name}-doc < %{upstream_version}

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx >= 2.3.0

%description -n python2-%{pypi_name}-doc
Documentation for the oslo.i18n library.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        OpenStack i18n Python 3 library
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  python3-six

# test deps
BuildRequires:  python3-mock
BuildRequires:  python3-oslotest
BuildRequires:  python3-hacking
BuildRequires:  python3-coverage

Requires:       python3-setuptools
Requires:       python3-six
Requires:       python3-babel

%description -n python3-%{pypi_name}
The oslo.i18n library contain utilities for working with internationalization
(i18n) features, especially translation for text strings in an application
or library.
%endif

%prep
%setup -q -n %{sname}-%{upstream_version}.%{release}

# let RPM handle deps
rm -rf {test-,}requirements.txt

%build
%{__python2} setup.py build
%if 0%{?with_python3}
%{__python3} setup.py build
%endif

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees   source build/html
popd

%if 0%{?with_python3}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
%endif

%check
%{__python2} setup.py test
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test
%endif

%files -n python2-%{pypi_name}
%doc AUTHORS ChangeLog CONTRIBUTING.rst HACKING.rst PKG-INFO README.rst
%license LICENSE
%{python2_sitelib}/oslo_i18n
%{python2_sitelib}/*.egg-info

%files -n python2-%{pypi_name}-doc
%doc doc/build/html

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc AUTHORS ChangeLog CONTRIBUTING.rst HACKING.rst PKG-INFO README.rst
%license LICENSE
%{python3_sitelib}/oslo_i18n
%{python3_sitelib}/*.egg-info
%endif

%changelog
