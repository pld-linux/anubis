
# Conditional build:
# --with gnutls			use GnuTLS library instead of OpenSSL
# --without tcp_wrappers	disable using tcp_wrappers for access control
# --without pam			disable using of PAM authentcation
# --without gpgme		disable using gpgme library for signing/encrypting with gnupg
# --without pcre		disable using pcre library

%include	/usr/lib/rpm/macros.perl
Summary:	An outgoing mail processor, and the SMTP tunnel
Summary(pl):	Procesor wychodz±cej poczty i tunel SMTP
Name:		anubis
Version:	3.6.2
Release:	1
License:	GPL
Group:		Applications/Mail
Source0:	ftp://ftp.gnu.org/gnu/anubis/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.pamd
Patch0:		%{name}-info.patch
Patch1:		%{name}-configure_gpgme.patch
URL:		http://www.gnu.org/software/anubis/
#BuildRequires:	gettext-devel
BuildRequires:  autoconf >= 2.54
BuildRequires:  automake >= 1.7
BuildRequires:	texinfo
BuildRequires:	bison
BuildRequires:	rpm-perlprov
%{?_with_gnutls:BuildRequires:		gnutls-devel}
%{!?_with_gnutls:BuildRequires:		openssl-devel}
%{!?_without_pam:BuildRequires:		pam-devel}
%{!?_without_tcp_wrappers:BuildRequires:libwrap-devel}
%{!?_without_pcre:BuildRequires:	pcre-devel}
%{!?_without_gpgme:BuildRequires:	gpgme-devel >= 0.3.12}
Requires:	identserver
PreReq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNU Anubis is an outgoing mail processor. It goes between the MUA (Mail
User Agent) and the MTA (Mail Transport Agent), and can perform on the
fly various sorts of processing and conversion on the outgoing mail in
accord with the sender's specified rules, based on a highly
configurable regular expressions system. It operates as a proxy
server, independently from mail user agents. GNU Anubis can edit outgoing
mail headers, encrypt and/or sign mail with the GNU Privacy Guard,
build secure SMTP tunnels (Simple Mail Transport Protocol) using the
TLS/SSL encryption even if your mail user agent doesn't support it, or
tunnel a connection through a SOCKS proxy.
Moreover, GNU Anubis supports the remailers (it allows sending mail in an
anonymous way).

Remember, that to use per-user configuration files ident server has to be
running. Without it only system-wide configuration file is used.

If you want to use GNU Anubis with mutt mail client, install msg2smtp
package.

%description -l pl
GNU Anubis zajmuje siê przetwarzaniem poczty wychodz±cej. Znajduje siê on
pomiêdzy MUA (Mail User Agent) i MTA (Mail Transport Agent) i mo¿e
wykonywaæ w locie ró¿ne rodzaje przetwarzania i konwersji poczty
wychodz±cej zale¿nie od podanych regu³, bazuj±cych na wysoce
konfigurowalnym systemie wyra¿eñ regularnych. GNU Anubis dzia³a jako
serwer proxy, niezale¿nie od programów pocztowych. Potrafi on zmieniaæ
nag³ówki listów, szyfrowaæ lub podpisywaæ jest przy pomocy GNU Privacy
Guard, tworzyæ bezpieczne tunele SMTP u¿ywaj±c szyfrowania TLS/SSL
nawet, gdy Twój program pocztowy nie ma takich mo¿liwo¶ci. Mo¿liwe
jest te¿ tunelowanie po³±czeñ przez SOCKS proxy.
Co wiêcej, GNU Anubis wspiera tak¿e remailery (czyli pozawala na anonimowe
wysy³anie poczty).

Pamiêtaj, ¿e aby u¿ywaæ plików konfiguracyjnych u¿ytkowników, serwer ident
musi byæ aktywny. Inaczej, u¿yty bêdzie tylko g³ówny plik konfiguracyjny.

Je¶li chcesz u¿ywaæ GNU Anubis z klientem poczty mutt, zainstaluj pakiet
msg2smtp.

%package -n msg2smtp
Summary:	msg2smtp takes mail at input and relays it to an SMTP server
Summary(pl):	msg2smtp wysy³a pocztê przyjmowan± na wej¶ciu do serwera SMTP
Group:		Applications/Mail

%description -n msg2smtp
The msg2smtp script is a bridge between MUA programs which use "sendmail"
command to send mail (such as Mutt) and smtp servers. It is particularly
useful when used in connection with GNU Anubis mail processor.

%description -n msg2smtp -l pl
Skrypt msg2smtp jest pomostem miêdzy programami pocztowymi u¿ywaj±cymi
polecenia "sendmail" do wysy³ania listów (np. Mutt), a serwerem smtp.
Jest on szczególnie przydatny w po³±czeniu z procesorem poczty GNU Anubis.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm -f missing
#%{__gettextize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
%{?_with_gnutls:	--with-gnutls} \
%{!?_with_gnutls:	--with-openssl} \
%{!?_without_pam:	--with-pam} \
%{?_without_pam:	--without-pam} \
%{!?_without_pcre:	--with-pcre} \
%{?_without_pcre:	--without-pcre} \
%{!?_without_gpgme:	--with-gpgme} \
%{?_without_gpgme:	--without-gpgme} \
%{!?_without_tcp_wrappers:	--with-tcp-wrappers} \
%{?_without_tcp_wrappers:	--without-tcp-wrappers} \
	--disable-dependency-tracking

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/pam.d,%{_sysconfdir},%{_bindir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install ./contrib/msg2smtp.pl $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/anubis
install ./examples/2anubisrc $RPM_BUILD_ROOT%{_sysconfdir}/anubisrc
%{!?_without_pam:install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/anubis}
cp -f ./examples/1anubisrc examples/anubisrc

%find_lang %{name}

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

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README INSTALL NEWS ChangeLog TODO examples/anubisrc
%{!?_without_pam:%doc examples/pam}
%attr(754,root,root) /etc/rc.d/init.d/anubis
%attr(600,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/anubisrc
%{!?_without_pam:%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/pam.d/anubis}
%attr(755,root,root) %{_sbindir}/anubis
%{_mandir}/man1/*
%{_infodir}/*info*

%files -n msg2smtp
%defattr(644,root,root,755)
%doc contrib/msg2smtp.txt
%attr(755,root,root) %{_bindir}/msg2smtp.pl
