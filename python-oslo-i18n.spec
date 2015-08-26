%global pypi_name oslo.i18n

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-oslo-i18n
Version:        2.5.0
Release:        1%{?dist}
Summary:        OpenStack i18n Python 2 library
License:        ASL 2.0
URL:            https://github.com/openstack/%{pypi_name}
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

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
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  python3-babel
BuildRequires:  python3-six
BuildRequires:  python3-fixtures

BuildArch:      noarch

Requires:       python3-setuptools
Requires:       python3-babel
Requires:       python3-six
Requires:       python3-fixtures

%description -n python3-oslo-i18n
The oslo.i18n library contain utilities for working with internationalization
(i18n) features, especially translation for text strings in an application
or library.
%endif

%package doc
Summary:    Documentation for OpenStack i18n library
BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx >= 2.3.0

%description doc
Documentation for the oslo.i18n library.

%if 0%{?with_python3}
%package -n python3-oslo-i18n-doc
Summary:    Documentation for OpenStack i18n library
BuildRequires:  python3-sphinx
BuildRequires:  python3-oslo-sphinx

%description -n python3-oslo-i18n-doc
Documentation for the oslo.i18n library.
%endif

%prep
%setup -qc
mv %{pypi_name}-%{version} python2

pushd python2
rm -rf *.egg-info

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

cp -p LICENSE ChangeLog CONTRIBUTING.rst PKG-INFO README.rst ../
popd

%if 0%{?with_python3}
cp -a python2 python3
find python3 -name '*.py' | xargs sed -i 's|^#!python|#!%{__python3}|'
%endif

find python2 -name '*.py' | xargs sed -i 's|^#!python|#!%{__python2}|'

%build
pushd python2
%{__python2} setup.py build
popd
%if 0%{?with_python3}
pushd python3
%{__python3} setup.py build
popd
%endif

%install
%if 0%{?with_python3}
pushd python3
%{__python3} setup.py install --skip-build --root %{buildroot}
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build-3 -b html -d build/doctrees   source build/html

# Fix hidden-file-or-dir warnings
rm -fr build/html/.buildinfo

# Fix this rpmlint warning
sed -i "s|\r||g" build/html/_static/jquery.js
popd
popd
%endif

pushd python2
%{__python2} setup.py install --skip-build --root %{buildroot}
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees   source build/html
# Fix hidden-file-or-dir warnings
rm -fr build/html/.buildinfo

# Fix this rpmlint warning
sed -i "s|\r||g" build/html/_static/jquery.js
popd
popd

%files
%doc ChangeLog CONTRIBUTING.rst PKG-INFO README.rst
%license LICENSE
%{python2_sitelib}/oslo_i18n
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-oslo-i18n
%doc ChangeLog CONTRIBUTING.rst PKG-INFO README.rst
%license LICENSE
%{python3_sitelib}/oslo_i18n
%{python3_sitelib}/*.egg-info
%endif

%files doc
%license LICENSE
%doc python2/doc/build/html

%if 0%{?with_python3}
%files -n python3-oslo-i18n-doc
%license LICENSE
%doc python3/doc/build/html
%endif

%changelog
* Wed Aug 26 2015 Parag Nemade <pnemade AT redhat DOT com> - 2.5.0-1
- Update to upstream 2.5.0
- fix %%docs file list
- Add missing BuildRequires: python3-babel, python3-fixtures
- fix python shebang using sed
- Add python3-oslo-i18n-doc

* Wed Aug 05 2015 Parag Nemade <pnemade AT redhat DOT com> - 2.4.0-1
- Update to upstream 2.4.0

* Wed Aug 05 2015 Parag Nemade <pnemade AT redhat DOT com> - 2.3.0-1
- Update to upstream 2.3.0

* Tue Jul 28 2015 Parag Nemade <pnemade AT redhat DOT com> - 2.2.0-1
- Update to upstream 2.2.0

* Wed Jul 22 2015 Parag Nemade <pnemade AT redhat DOT com> - 2.1.0-1
- Update to upstream 2.1.0

* Mon Jun 29 2015 Alan Pevec <alan.pevec@redhat.com> 2.0.0-1
- Update to upstream 2.0.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

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
