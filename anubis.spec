#
# TODO:
# - write PLD specyfic init script.
#
Summary:	An outgoing mail processor, and the SMTP tunnel
Summary(pl):	Preprocesor wychodz±cej poczty i tunel SMTP
Name:		anubis
Version:	3.4.6
Release:	1
License:	GPL
Group:		Applications/Mail
Source0:	http://cesnet.dl.sourceforge.net/sourceforge/anubis/%{name}-%{version}.tar.gz
Patch0:		%{name}-info.patch
URL:		http://anubis.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gpgme-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	texinfo
PreReq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Anubis is an outgoing mail processor, and the SMTP tunnel between the
MUA and the MTA. It supports: extended regular expressions, TLS/SSL
encryption, GnuPG (via the GPGME library), SOCKS Proxy and WinGates,
remailers, and more.

%description -l pl
Anubis jest preprocesorem wychodz±cej poczty i tunelem miêdzy MUA and
the MTA. Anubis wspiera rozszerzone wyra¿enia regularne, szyfrowanie
TLS/SSL, GnuPG, SOCKS Proxy oraz WinGates, remailery i nie tylko.

%prep
%setup -q

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-pcre \
	--disable-dependency-tracking
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_sysconfdir}}

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
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1


%preun
if [ "$1" = "0" ]; then
	if [ -f %{_localstatedir}/lock/subsys/anubis ]; then
		/etc/rc.d/init.d/anubis stop
	fi
	/sbin/chkconfig --del anubis
fi

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc AUTHORS README INSTALL NEWS ChangeLog TODO examples
%attr(754,root,root) /etc/rc.d/init.d/anubis
%attr(600,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/anubisrc
%attr(755,root,root) %{_sbindir}/anubis
%{_mandir}/man1/*
%{_infodir}/*info*
