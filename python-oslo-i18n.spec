%global sname oslo.i18n

Name:           python-oslo-i18n
Version:        0.4.0
Release:        1%{?dist}
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
%setup -q -n %{sname}-%{version}

# Remove bundled egg-info
rm -rf %{sname}.egg-info

# make doc build compatible with python-oslo-sphinx RPM
sed -i 's/oslosphinx/oslo.sphinx/' doc/source/conf.py

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees   source build/html
popd

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo

%files
%doc AUTHORS ChangeLog CONTRIBUTING.rst HACKING.rst LICENSE PKG-INFO README.rst
%{python2_sitelib}/oslo
%{python2_sitelib}/*.egg-info
%{python2_sitelib}/*.pth

%files doc
%doc doc/build/html

%changelog
* Thu Sep 18 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.4.0-1
- update to 0.4.0 release

* Wed Sep 10 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.3.0-1
- update to 0.3.0 release

* Thu Aug 21 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.2.0-1
- update to 0.2.0 release

* Thu Jul 10 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.1.0-2
- Use correct upstream URL

* Thu Jul 3 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.1.0-1
- Initial release
