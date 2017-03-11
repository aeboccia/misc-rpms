Summary: Share mouse and keyboard between multiple computers over the network
Name: synergy
Version: 1.8.8
Release: 1%{?dist}
License: GPLv2
Group: System Environment/Daemons
URL: http://synergy-foss.org/
Source: https://github.com/symless/synergy/archive/v%{version}-stable.tar.gz

#Don't override build flags
Patch0: system-gtest.patch

# Last built version of synergy-plus was 1.3.4-12.fc20
Provides: synergy-plus = %{version}-%{release}
Obsoletes: synergy-plus < 1.3.4-13
BuildRequires: cmake
BuildRequires: libX11-devel
BuildRequires: libXtst-devel
BuildRequires: qt-devel
BuildRequires: libcurl-devel
BuildRequires: desktop-file-utils
BuildRequires: avahi-compat-libdns_sd-devel
BuildRequires: openssl-devel
BuildRequires: gtest-devel

%description
Synergy lets you easily share your mouse and keyboard between multiple
computers, where each computer has its own display. No special hardware is
required, all you need is a local area network. Synergy is supported on
Windows, Mac OS X and Linux. Redirecting the mouse and keyboard is as simple
as moving the mouse off the edge of your screen.

%prep
%setup -q -n %{name}-%{version}-stable
%patch0 -p1
rm -f ext/cryptopp562.zip
rm -f ext/gmock-1.6.0.zip
rm -f ext/gtest-1.6.0.zip
rm -f ext/openssl-1.0.2.tar.gz
rm -rf src/test
#Disable tests for now (bundled gmock/gtest)
sed -i /.*\(test.*/d src/CMakeLists.txt

%build
PATH="$PATH:/usr/lib64/qt4/bin:/usr/lib/qt4/bin"
%{cmake} .
make %{?_smp_mflags}
pushd src/gui
%qmake_qt4 gui.pro -r
make %{?_smp_mflags}

%install
# No install target (yet? as of 1.3.7)
install -D -p -m 0755 bin/synergyc %{buildroot}%{_bindir}/synergyc
install -D -p -m 0755 bin/synergys %{buildroot}%{_bindir}/synergys
install -D -p -m 0755 bin/synergy %{buildroot}%{_bindir}/synergy
install -D -p -m 0755 bin/syntool %{buildroot}%{_bindir}/syntool
install -D -p -m 0644 doc/synergyc.man %{buildroot}%{_mandir}/man8/synergyc.8
install -D -p -m 0644 doc/synergys.man %{buildroot}%{_mandir}/man8/synergys.8
install -D -p -m 0644 res/synergy.desktop %{buildroot}%{_datadir}/applications/synergy.desktop
install -D -p -m 0644 res/synergy.ico %{buildroot}%{_datadir}/pixmaps/synergy.ico

desktop-file-install --delete-original  \
  --dir %{buildroot}%{_datadir}/applications            \
  --set-icon=%{_datadir}/pixmaps/synergy.ico            \
  %{buildroot}%{_datadir}/applications/synergy.desktop

desktop-file-validate %{buildroot}/%{_datadir}/applications/synergy.desktop

%files
# None of the documentation files are actually useful here, they all point to
# the online website, so include just one, the README
%doc LICENSE README doc/synergy.conf.example*
%{_bindir}/synergyc
%{_bindir}/synergys
%{_bindir}/synergy
%{_bindir}/syntool
%{_datadir}/pixmaps/synergy.ico
%{_datadir}/applications/synergy.desktop
%{_mandir}/man8/synergyc.8*
%{_mandir}/man8/synergys.8*

%changelog
* Fri Mar 10 2017 Anthony Boccia <anthony@boccia.me> - 1.8.8-1
- Update to latest stable
- Added patch to use system gtest
- Added gtest-devel build dep

* Mon Apr 11 2016 Johan Swensson <kupo@kupo.se> - 1.7.6-1
- Update to 1.7.6
- Clean up BuildRequires
- Package syntool

* Sun Feb 21 2016 Johan Swensson <kupo@kupo.se> - 1.7.5-1
- Update to 1.7.5
- Add BuildRequires openssl-devel

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.6.2-2
- Rebuilt for GCC 5 C++11 ABI change

* Sat Dec 20 2014 Johan Swensson <kupo@kupo.se> - 1.6.2-1
- Update to 1.6.2

* Fri Nov 28 2014 Johan Swensson <kupo@kupo.se> - 1.6.1-1
- Update to 1.6.1
- BuildRequire avahi-compat-libdns_sd-devel

* Sat Aug 23 2014 Johan Swensson <kupo@kupo.se> - 1.5.1-1
- Update to 1.5.1

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 25 2014 Johan Swensson <kupo@kupo.se> - 1.5.0-1
- Update to 1.5.0
- Update source url
- libcurl-devel, qt-devel, cryptopp-devel and desktop-file-utils buildrequired
- unbundle cryptopp
- unbundle gmock and gtest
- include synergy gui
- fix icon path

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May  7 2014 Michael Schwendt <mschwendt@fedoraproject.org> - 1.4.10-4
- increase synergy-plus obs_ver once more to obsolete the F20 rebuild

* Mon Sep 16 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.4.10-3
- correct synergy-plus obs_ver

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 18 2013 Christian Krause <chkr@fedoraproject.org> - 1.4.10-1
- Update to 1.4.10 (#843971).
- Cleanup spec file.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-5
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 18 2011 Matthias Saou <matthias@saou.eu> 1.3.7-3
- Add missing Provides for synergy-plus (#722843 re-review).

* Mon Jul 18 2011 Matthias Saou <matthias@saou.eu> 1.3.7-2
- Update summary.

* Tue Jul 12 2011 Matthias Saou <matthias@saou.eu> 1.3.7-1
- Update to 1.3.7.
- Drop patch disabling XInitThreads, see upstream #610.
- Update %%description and %%doc.
- Replace cmake patch with our own install lines : Less rebasing.

* Mon Jul 11 2011 Matthias Saou <matthias@saou.eu> 1.3.6-2
- Update Obsoletes for the latest version + fix (release + 1 because of dist).
- Add missing cmake BuildRequires.
- Update cmake patch to also install man pages.

* Fri Feb 18 2011 quiffman GMail 1.3.6-1
- Update to reflect the synergy/synergy+ merge to synergy-foss.org (#678427).
- Build 1.3.5 and newer use CMake.
- Patch CMakeLists.txt to install the binaries.

* Thu Jul  8 2010 Matthias Saou <matthias@saou.eu> 1.3.4-6
- Don't apply the RHEL patch on RHEL6, only 4 and 5.

* Mon Dec  7 2009 Matthias Saou <matthias@saou.eu> 1.3.4-5
- Obsolete synergy (last upstream released version is from 2006) since synergy+
  is a drop-in replacement (#538179).

* Tue Nov 24 2009 Matthias Saou <matthias@saou.eu> 1.3.4-4
- Disable XInitThreads() on RHEL to fix hang (upstream #194).

* Tue Aug 18 2009 Matthias Saou <matthias@saou.eu> 1.3.4-3
- Don't use the -executable find option, it doesn't work with older versions.

* Tue Aug 18 2009 Matthias Saou <matthias@saou.eu> 1.3.4-2
- Initial RPM release, based on the spec from the original synergy.
- Remove spurious executable bit from sources files.

