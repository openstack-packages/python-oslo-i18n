%global sname oslo.i18n

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-oslo-i18n
Version:        XXX
Release:        XXX
Summary:        OpenStack i18n Python 2 library
License:        ASL 2.0
URL:            https://github.com/openstack/%{sname}
Source0:        https://pypi.python.org/packages/source/o/%{sname}/%{sname}-%{version}.tar.gz

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
BuildRequires:  python-babel
BuildRequires:  python-six
BuildRequires:  python-fixtures

BuildArch:      noarch

Requires:       python-setuptools
Requires:       python-babel
Requires:       python-six
Requires:       python-fixtures

%description
The oslo.i18n library contain utilities for working with internationalization
(i18n) features, especially translation for text strings in an application
or library.

%if 0%{?with_python3}
%package -n python3-oslo-i18n
Summary:        OpenStack i18n Python 3 library
License:        ASL 2.0
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  python3-six
BuildArch:      noarch

Requires:       python3-setuptools
Requires:       python3-six
Requires:       python3-fixtures

%description -n python3-oslo-i18n
The oslo.i18n library contain utilities for working with internationalization
(i18n) features, especially translation for text strings in an application
or library.
%endif

%package doc
Summary:    Documentation for OpenStack i18n library
#TODO: In future we want to switch using python3
BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx >= 2.3.0

%description doc
Documentation for the oslo.i18n library.


%prep
%setup -q -n %{sname}-%{upstream_version}
%if 0%{?with_python3}
cp -a . %{py3dir}
%endif

%build
%{__python2} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees   source build/html
popd

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo

# Fix this rpmlint warning
sed -i "s|\r||g" doc/build/html/_static/jquery.js

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
popd
%endif

%files
%doc AUTHORS ChangeLog CONTRIBUTING.rst HACKING.rst PKG-INFO README.rst
%license LICENSE
%{python2_sitelib}/oslo_i18n
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-oslo-i18n
%doc AUTHORS ChangeLog CONTRIBUTING.rst HACKING.rst PKG-INFO README.rst
%license LICENSE
%{python3_sitelib}/oslo_i18n
%{python3_sitelib}/oslo
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/*.pth
%endif

%files doc
%doc doc/build/html

%changelog
