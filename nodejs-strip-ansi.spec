#
# Conditional build:
%bcond_with	tests		# build with tests

%define		pkg	strip-ansi
Summary:	Strip ANSI escape codes (used for colorizing strings in the terminal)
Name:		nodejs-%{pkg}
Version:	0.2.0
Release:	1
License:	MIT
Group:		Development/Libraries
Source0:	http://registry.npmjs.org/strip-ansi/-/strip-ansi-%{version}.tgz
# Source0-md5:	77fe06c131c3aa499f7071effd0bcd13
Source1:	https://raw.githubusercontent.com/sindresorhus/strip-ansi/3c9b37e5381603925ba16b27a05ccbfd338906b8/test.js
# Source1-md5:	16c9da163ab34ea3ff8c373bae2542e5
# https://github.com/sindresorhus/strip-ansi/pull/1
Source2:	LICENSE
URL:		https://github.com/sindresorhus/strip-ansi
BuildRequires:	rpmbuild(macros) >= 1.634
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	nodejs-mocha
%endif
Requires:	nodejs
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Strip ANSI escape codes (used for colorizing strings in the terminal).

%prep
%setup -qc
mv package/* .
cp -p %{SOURCE1} .
cp -p %{SOURCE2} .

%{__sed} -i -e '1s,^#!.*node,#!/usr/bin/node,' cli.js

%build
%if %{with tests}
mocha
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{nodejs_libdir}/%{pkg}}
cp -pr package.json cli.js index.js \
    $RPM_BUILD_ROOT%{nodejs_libdir}/strip-ansi

# `strip-ansi` is used as the command.
ln -sf %{nodejs_libdir}/strip-ansi/cli.js \
    $RPM_BUILD_ROOT%{_bindir}/strip-ansi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc readme.md LICENSE
%attr(755,root,root) %{_bindir}/strip-ansi

%dir %{nodejs_libdir}/%{pkg}
%{nodejs_libdir}/%{pkg}/package.json
%{nodejs_libdir}/%{pkg}/index.js
%attr(755,root,root) %{nodejs_libdir}/%{pkg}/cli.js
