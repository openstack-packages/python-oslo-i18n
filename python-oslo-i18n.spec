%global sname oslo.i18n

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-oslo-i18n
Version:        1.5.0
Release:        3%{?dist}
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
%setup -q -n %{sname}-%{version}
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
%{python2_sitelib}/oslo
%{python2_sitelib}/*.egg-info
%{python2_sitelib}/*.pth

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
* Thu Mar 12 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.5.0-3
- Add python3 subpackage

* Thu Mar 12 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.5.0-2
- Add missing buildtime and runtime dependencies
- fix rpmlint warning message

* Thu Mar 12 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.5.0-1
- update to 1.5.0 release
- use %%license macro for license file

* Tue Feb 24 2015 Alan Pevec <alan.pevec@redhat.com> 1.4.0-1
- Update to upstream 1.4.0

* Fri Jan 09 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.3.0-1
- update to 1.3.0 release
- Added BR: python-six

* Fri Dec 05 2014 Parag Nemade <pnemade AT redhat DOT com> - 1.1.0-1
- update to 1.1.0 release

* Fri Sep 19 2014 Parag Nemade <pnemade AT redhat DOT com> - 1.0.0-1
- update to 1.0.0 release

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
