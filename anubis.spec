Summary:	An outgoing mail processor, and the SMTP tunnel
Summary(pl):	Preprocesor wychodzącej poczty i tunel SMTP
Name:		anubis
Version:	3.4.1
Release:	1
License:	GPL
Group:		Applications/Mail
Source0:	http://cesnet.dl.sourceforge.net/sourceforge/anubis/%{name}-%{version}.tar.gz
URL:		http://anubis.sourceforge.net/
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	openssl-devel
BuildRequires:	gpgme-devel
BuildRequires:	pcre-devel
PreReq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Anubis is an outgoing mail processor, and the SMTP tunnel between the
MUA and the MTA. It supports: extended regular expressions, TLS/SSL
encryption, GnuPG (via the GPGME library), SOCKS Proxy and WinGates,
remailers, and more.

%description -l pl
Anubis jest preprocesorem wychodzącej poczty i tunelem między MUA and
the MTA. Anubis wspiera rozszerzone wyrażenia regularne, szyfrowanie
TLS/SSL, GnuPG, SOCKS Proxy oraz WinGates, remailery i nie tylko.

%prep
%setup -q

%build
%configure \
	--prefix=%{_prefix} \
	--with-pcre \
	--disable-dependency-tracking
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install ./scripts/redhat.init $RPM_BUILD_ROOT/etc/rc.d/init.d/anubis
install ./examples/defaultrc $RPM_BUILD_ROOT%{_sysconfdir}/anubisrc

%clean
rm -fr $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add anubis
if [ -f %{_localstatedir}/lock/subsys/anubis ]; then
	/etc/rc.d/init.d/anubis restart >&2
else
	echo "Run \"/etc/rc.d/init.d/anubis start\" to start anubis." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f %{_localstatedir}/lock/subsys/anubis ]; then
		/etc/rc.d/init.d/anubis stop
	fi
	/sbin/chkconfig --del anubis
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS README INSTALL NEWS ChangeLog TUTORIAL TODO examples
%attr(755,root,root) %{_sbindir}/anubis
%attr(750,root,root) /etc/rc.d/init.d/anubis
%attr(600,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/anubisrc
%{_mandir}/man1/*
