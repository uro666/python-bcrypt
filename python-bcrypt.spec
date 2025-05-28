%undefine _debugsource_packages
%global module bcrypt
%define oname bcrypt

# building with tests enabled
%bcond_without tests

# NOTE To update also run create_vendored_crate_archive.sh to create a vendor
# NOTE archive of the rust crates and update the Source1: line and _abf.yml file
# NOTE Upload the _bcrypt-version-vendor.tar.gz to the file store.

Summary:	Modern password hashing for your software and your servers
Name:		python-bcrypt
Version:	4.3.0
Release:	1
#crypt_blowfish code is in Public domain and all other code in ASL 2.0
License:	ASL 2.0 and Public Domain and BSD
Group:		Development/Python
URL:		https://github.com/pyca/bcrypt
Source0:	https://pypi.python.org/packages/source/b/%{oname}/%{oname}-%{version}.tar.gz
Source1:	_bcrypt-4.3.0-vendor.tar.xz

BuildRequires:  pkgconfig(python)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(cffi)
BuildRequires:  python%{pyver}dist(six)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(setuptools-rust)
BuildRequires:	python%{pyver}dist(wheel)
BuildRequires:	cargo
BuildRequires:	rust-packaging
%if %{with tests}
BuildRequires:	python%{pyver}dist(pytest)
%endif

%description
A good password hashing for your software and your servers written in Python.

%prep
%autosetup -n %{module}-%{version} -p1 -a1
%cargo_prep -v vendor

cat >>.cargo/config << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"

EOF

%build
export CFLAGS="%{optflags} -fno-strict-aliasing"
%py_build

%install
%py_install

%if %{with tests}
%check
export PYTHONPATH="%{buildroot}%{python_sitelib}:${PWD}"
pip install -e .[test]
%{__python} -m pytest --import-mode append -v tests
%endif

%files
%license LICENSE
%doc README.rst
%{python_sitearch}/%{module}/
%{python_sitearch}/%{module}-%{version}*-info
