Summary:	Advanced Linux Sound Architecture (ALSA) wrapper for OSS
Name:		alsa-oss
Version:	1.0.28
Release:	1%{?dist}
License:	GPLv2+
Group:		Applications/Multimedia
URL:		http://www.alsa-project.org/
Source:		ftp://ftp.alsa-project.org/pub/oss-lib/alsa-oss-%{version}.tar.bz2
Patch0:		%{name}-1.0.12-aoss.patch
Patch1:		%{name}-glibc-open.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	alsa-lib-devel >= %{version}
%ifarch x86_64
BuildRequires:	automake, libtool
%endif
Requires:	%{name}-libs = %{version}-%{release}

%description
This package contains the compatibility library and wrapper script for
running legacy OSS applications through ALSA. Unlike the kernel
driver, this has the advantage of supporting DMIX software mixing.

%package libs
Summary:	ALSA/OSS wrapper libraries
Group:		System Environment/Libraries
Requires:	%{name} = %{version}-%{release}
%description libs
System libraries for alsa-oss.

%package devel
Summary:	Headers for ALSA wrapper for OSS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}, %{name}-libs = %{version}-%{release}
%description devel
Header files for alsa-oss.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%ifarch x86_64
autoreconf -f -i
%endif
%configure \
%ifarch x86_64
	--disable-rpath \
%endif
	--disable-static
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/aoss

%files libs
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_mandir}/man?/*

%files devel
%defattr(-,root,root,-)
%doc oss-redir/README
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so


%changelog
* Mon Mar 20 2017 Anthony Boccia <anthony.boccia.me> - 1.0.28-1
- Updated to latest build

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 1.0.17-2
- Fix Patch:/%%patch0 mismatch.

* Tue Jul 29 2008 Jaroslav Kysela <jkysela@redhat.com> 1.0.17-1
- New upstream version

* Mon Oct 22 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 1.0.15-0.1
- New upstream version

* Thu Aug 16 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 1.0.14-3
- License clarification
- Copied glibc open() workaround from alsa-lib-1.0.14-glibc-open.patch

* Wed Jul 25 2007 Warren Togami <wtogami@redhat.com> 1.0.14-2
- binutils/gcc bug rebuild (#249435)

* Tue Jul 24 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 1.0.14-1
- Updated to match F8 alsa-libs
- Changed reference to patch filename

* Thu Feb 08 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 1.0.12-4
- Split out libraries to -libs subpackage, fixing BZ#221711
- Implemented changes as recommended by Jason Tibbitts
- Adjusted aoss patch to allow for 32-bit library use on x86_64
- Added reference in man page to added functionality
- Resultant alsa-oss package reports no-binary error (necessary evil, I guess)

* Fri Oct 06 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 1.0.12-3
- Added conditionalized rpath fixes for x86_64 (thanks Denis!)
- Re-added *.a to -devel package
- Added %%defattr for -devel, added oss-redir/README as %%doc

* Thu Oct 05 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 1.0.12-2
- Adding --disable-static to configure
- Removing *.a from -devel package
- Adding name and version to patch
- Removing commented-out autoreconf line
- Forcibly deleting *.a files in %%install (why didn't it believe me?)

* Tue Oct 03 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 1.0.12-1
- Hijacked from stalled review (BZ#187706)
- Bumped to 1.0.12 for devel branch
- Removed Req for /sbin/ldconfig (unnecessary when using -p in scriptlets)
- Added dist tag!
- Made macros slightly more consistent
- Deleted .la files in %%install

* Sun Apr  2 2006 Michel Salim <michel.salim@gmail.com> 1.0.11-1.rc3
- Initial build.
