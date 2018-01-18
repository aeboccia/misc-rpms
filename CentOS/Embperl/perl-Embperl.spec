Name:           perl-Embperl
Version:        2.5.0
Release:        1%{?dist}
Summary:        Building dynamic Websites with Perl
License:        Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Embperl/
Source0:        http://www.cpan.org/authors/id/G/GR/GRICHTER/Embperl-%{version}.tar.gz
Source1:        embperl.conf
Source2:	99-embperl.conf 
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec) >= 0.8
BuildRequires:  perl(MIME::Base64) perl(HTML::Parser) perl(HTML::HeadParser) perl(Digest::MD5)
BuildRequires:  mod_perl-devel libxml2-devel libxslt-devel libnet-devel perl-libwww-perl perl-CGI
Requires:       perl(File::Spec) >= 0.8
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:	perl-libwww-perl libxml2 libxslt
Patch0: 	apache2.4-compat.patch
Patch1: 	cgi-pm-4.04-compatibility.patch
Patch2: 	delay.patch
Patch3: 	add_unixd_makefile.patch
Patch4: 	perl5.20-compat.patch
Patch5:		perl5.22-compat-PL_sv_objcount-removal.patch
Patch6:		pod-errors.patch
AutoReq:	no
AutoProv:	no

%description
Embperl is a framework for building websites with Perl.

%prep
%setup -q -n Embperl-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
y | %{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

#Rename two binaries to remove the .pl
mv $RPM_BUILD_ROOT%{_bindir}/embpexec.pl $RPM_BUILD_ROOT/%{_bindir}/embpexec
mv $RPM_BUILD_ROOT%{_bindir}/embpmsgid.pl $RPM_BUILD_ROOT/%{_bindir}/embpmsgid

#Fix up file permissions
%{_fixperms} $RPM_BUILD_ROOT/*

#Install Apache Configs
mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d/ && mkdir $RPM_BUILD_ROOT/etc/httpd/conf.modules.d/
install -D -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/conf.d/
install -D -m 0644 %{SOURCE2} $RPM_BUILD_ROOT/etc/httpd/conf.modules.d/

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Doxyfile embpcgi.bat.templ embpcgi.pl.templ embpcgi.test.pl.templ Embperl_BS EmbperlLogo.gif embpexec.bat.templ embpexec.pl.templ embpfastcgi.pl.templ embpfastcgi.test.pl.templ embpmsgid.pl.templ epocgi.bat.templ epocgi.pl.templ epocgi.test.pl.templ META.json README README.v2 TODO
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Embperl*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_bindir}/embpexec
%{_bindir}/embpmsgid
%{_sysconfdir}/httpd/conf.d/embperl.conf
%{_sysconfdir}/httpd/conf.modules.d/99-embperl.conf

%changelog
* Wed Jan 17 2018 aboccia 2.5.0-1
- Initial spec created, all tests working
- Added a new patch #3 for Perl makefile to enable unixd
- Added configs for apache
