#
# Conditional build:
%bcond_with	gnutls		# GnuTLS library instead of OpenSSL
%bcond_without	gpgme		# signing/encrypting with gnupg using gpgme library
%bcond_without	pam		# PAM authentication
%bcond_without	pcre		# PCRE library support
%bcond_without	tcp_wrappers	# tcp_wrappers for access control
%bcond_with	mysql		# MySQL support
%bcond_with	pgsql		# PostgreSQL support
#
Summary:	An outgoing mail processor, and the SMTP tunnel
Summary(pl.UTF-8):	Procesor wychodzącej poczty i tunel SMTP
Name:		anubis
Version:	4.3
Release:	1
License:	GPL v3+
Group:		Applications/Mail
Source0:	https://ftp.gnu.org/gnu/anubis/%{name}-%{version}.tar.bz2
# Source0-md5:	32dc9adf1d0daa54bff70f10b4e289b5
Source1:	%{name}.init
Source2:	%{name}.pamd
Patch0:		%{name}-info.patch
Patch1:		%{name}-nolibnsl.patch
Patch2:		%{name}-pl.po-update.patch
URL:		http://www.gnu.org/software/anubis/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.16
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gdbm-devel
BuildRequires:	gettext-tools >= 0.21
%{?with_gnutls:BuildRequires:	gnutls-devel >= 1.2.5}
%{?with_gpgme:BuildRequires:	gpgme-devel >= 1:1.0.0}
BuildRequires:	gsasl-devel >= 0.2.3
BuildRequires:	guile-devel >= 5:2.2.0
BuildRequires:	libgcrypt-devel >= 1.7.0
%{?with_tcp_wrappers:BuildRequires:	libwrap-devel}
%{?with_mysql:BuildRequires:	mysql-devel}
%{!?with_gnutls:BuildRequires:	openssl-devel >= 0.9.7d}
%{?with_pam:BuildRequires:	pam-devel}
BuildRequires:	pcre-devel
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	texinfo
Requires(post,preun):	/sbin/chkconfig
Requires:	identserver
Requires:	libgcrypt >= 1.7.0
Requires:	pam >= 0.77.3
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNU Anubis is an outgoing mail processor. It goes between the MUA
(Mail User Agent) and the MTA (Mail Transport Agent), and can perform
on the fly various sorts of processing and conversion on the outgoing
mail in accord with the sender's specified rules, based on a highly
configurable regular expressions system. It operates as a proxy
server, independently from mail user agents. GNU Anubis can edit
outgoing mail headers, encrypt and/or sign mail with the GNU Privacy
Guard, build secure SMTP tunnels (Simple Mail Transport Protocol)
using the TLS/SSL encryption even if your mail user agent doesn't
support it, or tunnel a connection through a SOCKS proxy. Moreover,
GNU Anubis supports the remailers (it allows sending mail in an
anonymous way).

Remember, that to use per-user configuration files ident server has to
be running. Without it only system-wide configuration file is used.

If you want to use GNU Anubis with mutt mail client, install msg2smtp
package.

%description -l pl.UTF-8
GNU Anubis zajmuje się przetwarzaniem poczty wychodzącej. Znajduje się
on pomiędzy MUA (Mail User Agent) i MTA (Mail Transport Agent) i może
wykonywać w locie różne rodzaje przetwarzania i konwersji poczty
wychodzącej zależnie od podanych reguł, bazujących na wysoce
konfigurowalnym systemie wyrażeń regularnych. GNU Anubis działa jako
serwer proxy, niezależnie od programów pocztowych. Potrafi on zmieniać
nagłówki listów, szyfrować lub podpisywać jest przy pomocy GNU Privacy
Guard, tworzyć bezpieczne tunele SMTP używając szyfrowania TLS/SSL
nawet, gdy Twój program pocztowy nie ma takich możliwości. Możliwe
jest też tunelowanie połączeń przez SOCKS proxy. Co więcej, GNU Anubis
wspiera także remailery (czyli pozawala na anonimowe wysyłanie
poczty).

Pamiętaj, że aby używać plików konfiguracyjnych użytkowników, serwer
ident musi być aktywny. Inaczej, użyty będzie tylko główny plik
konfiguracyjny.

Jeśli chcesz używać GNU Anubis z klientem poczty mutt, zainstaluj
pakiet msg2smtp.

%package -n msg2smtp
Summary:	msg2smtp takes mail at input and relays it to an SMTP server
Summary(pl.UTF-8):	msg2smtp wysyła pocztę przyjmowaną na wejściu do serwera SMTP
Group:		Applications/Mail

%description -n msg2smtp
The msg2smtp script is a bridge between MUA programs which use
"sendmail" command to send mail (such as Mutt) and smtp servers. It is
particularly useful when used in connection with GNU Anubis mail
processor.

%description -n msg2smtp -l pl.UTF-8
Skrypt msg2smtp jest pomostem między programami pocztowymi używającymi
polecenia "sendmail" do wysyłania listów (np. Mutt), a serwerem smtp.
Jest on szczególnie przydatny w połączeniu z procesorem poczty GNU
Anubis.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{__rm} po/stamp-po

%build
%{__gettextize}
%{__aclocal} -I m4 -I am -I gint -I doc/imprimatur
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-dependency-tracking \
	--disable-silent-rules \
	%{!?with_gnutls:--without-gnutls} \
	%{!?with_gpgme:--without-gpgme} \
	%{?with_mysql:--with-mysql} \
	%{!?with_gnutls:--with-openssl} \
	%{?with_pam:--with-pam} \
	%{?with_pcre:--with-pcre} \
	%{?with_pgsql:--with-postgres} \
	%{?with_tcp_wrappers:--with-tcp-wrappers}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/pam.d,%{_sysconfdir},%{_bindir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install ./contrib/msg2smtp.pl $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/anubis
cp -p ./examples/2anubisrc $RPM_BUILD_ROOT%{_sysconfdir}/anubisrc
%{?with_pam:cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/anubis}
cp -pf ./examples/1anubisrc examples/anubisrc

rm -f $RPM_BUILD_ROOT%{_datadir}/info/dir

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add anubis
%service anubis restart
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1


%preun
if [ "$1" = "0" ]; then
	%service anubis stop
	/sbin/chkconfig --del anubis
fi

%postun	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README INSTALL NEWS ChangeLog TODO examples/anubisrc %{?with_pam:examples/pam}
%attr(754,root,root) /etc/rc.d/init.d/anubis
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/anubisrc
%{?with_pam:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/anubis}
%attr(755,root,root) %{_sbindir}/anubis
%attr(755,root,root) %{_sbindir}/anubisadm
%{_datadir}/anubis
%{_mandir}/man1/anubis.1*
%{_infodir}/anubis.info*

%files -n msg2smtp
%defattr(644,root,root,755)
%doc contrib/msg2smtp.txt
%attr(755,root,root) %{_bindir}/msg2smtp.pl
