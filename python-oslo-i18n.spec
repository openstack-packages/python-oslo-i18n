%global sname oslo.i18n

Name:           python-oslo-i18n
Version:        XXX
Release:        XXX
Summary:        OpenStack i18n library
License:        ASL 2.0
URL:            https://github.com/openstack/%{sname}
Source0:        https://pypi.python.org/packages/source/o/%{sname}/%{sname}-%{version}.tar.gz

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
BuildArch:      noarch
Requires:       python-setuptools

%description
The oslo.i18n library contain utilities for working with internationalization
(i18n) features, especially translation for text strings in an application
or library.

%package doc
Summary:    Documentation for OpenStack i18n library
BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description doc
Documentation for the oslo.i18n library.


%prep
%setup -q -n %{sname}-%{upstream_version}

# Remove bundled egg-info
rm -rf %{sname}.egg-info

%build
%{__python2} setup.py build

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

%files
%doc AUTHORS ChangeLog CONTRIBUTING.rst HACKING.rst LICENSE PKG-INFO README.rst
%{python2_sitelib}/oslo_i18n
%{python2_sitelib}/*.egg-info


%files doc
%doc doc/build/html

%changelog
