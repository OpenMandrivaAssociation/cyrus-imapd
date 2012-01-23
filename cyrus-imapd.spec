# use saslauth group if
%define SASLGROUP 0
%{?_with_saslgroup: %{expand: %%define SASLGROUP 1}}

# preforking cyrus.conf as default
%define PREFORK 1
%{?_without_prefork: %{expand: %%define PREFORK 0}}

# enable idled (default no)
%define IDLED 0
%{?_with_idled: %{expand: %%define IDLED 1}}

# enable automatic mailbox creation on deliver (default no):
%define build_autocreate 1
%{?_without_autocreate: %define build_autocreate 0}

# create on demand folder requested by sieve filter (default no):
%define build_autosieve 1
%{?_without_autosieve: %define build_autosieve 0}

# remove quota files extension:
%define build_rmquota 1
%{?_without_rmquota: %define build_rmquota 0}
 
# snmp support
%global with_snmp 1
%{?_without_snmp: %global with_snmp 0}

# ldap/pts support
%global with_ldap 1
%{?_without_ldap: %global with_ldap 0}

%global with_mysql 1
%{?_without_mysql: %global with_mysql 0}

%global with_pgsql 1
%{?_without_pgsql: %global with_pgsql 0}

%global with_sqlite 1
%{?_without_sqlite: %global with_sqlite 0}

# virtual domains in LDAP support
# needed by Kolab2
%define build_virtualdomains_in_ldap 1
%{?_without_virtualdomains_in_ldap: %define build_virtualdomains_in_ldap 0}

%define db_version 5.2

Summary:	A high-performance mail store with IMAP and POP3 support
Name:		cyrus-imapd
Version:	2.3.18
Release:	%mkrel 2
License:	OSI Approved
Group:		System/Servers
URL:		http://cyrusimap.org/
Source0:	ftp://ftp.cyrusimap.org/cyrus-imapd/%{name}-%{version}.tar.gz
Source1:        ftp://ftp.cyrusimap.org/cyrus-imapd/%{name}-%{version}.tar.gz.sig
Source2:	cyrus-procmailrc
Source4:	cyrus-user-procmailrc.template
Source6:	cyrus-imapd.imap-2.1.x-conf
Source8:	cyrus-imapd.pamd
Source11:	cyrus-imapd.init
Source12:	cyrus-imapd.sysconfig
Source13:       http://clement.hermann.free.fr/scripts/Cyrus/imapcreate.pl
Source14:       cyrus-imapd.README.RPM
Source15:	cyrus-imapd.cvt_cyrusdb_all
Source19:	cyrus-imapd-procmail+cyrus.mc
Source20:	cyrus-imapd.cron-daily
Source21:	http://ftp.andrew.cmu.edu/pub/net/mibs/cmu/cmu.mib
# This patch fixes the perl install path for mdk9.0 and later
Patch1:		cyrus-imapd-mdk9.0perl-patch
# cyrus-master instead of master in syslog
Patch2:		cyrus-imapd-logident.patch
# Autocreate INBOX patch (http://email.uoa.gr/projects/cyrus/autocreate/)
Patch3:	http://email.uoa.gr/download/cyrus/cyrus-imapd-2.3.16/cyrus-imapd-2.3.16-autocreate-0.10-0.diff
# Create on demand folder requested by sieve filter (http://email.uoa.gr/projects/cyrus/autosievefolder/)
Patch4:	http://email.uoa.gr/download/cyrus/cyrus-imapd-2.3.16/cyrus-imapd-2.3.16-autosieve-0.6.0.diff
# Remove QUOTA patch (http://email.uoa.gr/projects/cyrus/quota-patches/rmquota/)
Patch5:	http://email.uoa.gr/download/cyrus/cyrus-imapd-2.3.9/cyrus-imapd-2.3.9-rmquota-0.5-0.diff
# command line switch to disallow plaintext login
Patch6:	cyrus-imapd-plaintext.diff
# 64-bit fixes
Patch7:	cyrus-imapd-2.2.8-64bit-fixes.patch
# (oe) for kolab2: Patch to support virtdomains: ldap (parse domain from "email" field an LDAP user entry)
Patch8:	cyrus-imapd-kolab-ldap.diff
# (oe) for kolab2: Allow for custom annotation
Patch9:	cyrus-imapd-cyradm_annotate.diff
# (bluca) add ptloader to cyrus.conf 
Patch10:	cyrus-imapd-ptloader-conf.diff
# (bluca) fix LDAP_OPT_X_SASL_SECPROPS error in ptloader
Patch11:	cyrus-imapd-ptloader-secprops.diff
# http://wiki.mandriva.com/en/Development/Packaging/Problems#format_not_a_string_literal_and_no_format_arguments
Patch12:	cyrus-imapd-2.3.14-format_not_a_string_literal_and_no_format_arguments.diff
# remove verbosity of some syslog messages (simon matter)
Patch13:	cyrus-imapd-2.1.16-getrlimit.patch
Patch14:	cyrus-imapd-2.3.12-skiplist_verbosity.patch
Patch15:	cyrus-imapd-2.3.12-statuscache_verbosity.patch
Patch16:	cyrus-imapd-2.3.16-user_deny_verbosity.patch
# Other patches from simon matter
Patch17:	cyrus-imapd-2.3.7-mancyrusdb.patch
Patch18:	cyrus-imapd-2.3.13-make_md5_sha1_dirs.patch
Patch19:	cyrus-imapd-2.3.11-mkimap.patch
Patch21:	cyrus-imapd-2.3.16-sieve_port.patch
Patch22:	99-berkelydb-5.1.dpatch
Requires:	perl
# with previous versions of sasl, imap LOGIN would fail
Requires:	%{mklibname sasl 2} >= 2.1.15
#Requires:	krb5-libs
Requires(pre):	/usr/sbin/useradd 
Requires(pre):	rpm-helper
%if %{SASLGROUP}
Requires(pre):	/usr/sbin/groupadd
%endif
Requires(post):	chkconfig /usr/bin/openssl /usr/bin/chattr /bin/grep /bin/cp perl
Requires(preun):/sbin/service chkconfig /usr/sbin/userdel /bin/rm
%if %{SASLGROUP}
Requires(preun):/usr/sbin/groupdel
%endif
Requires(postun):/sbin/service
Provides:	imap
Provides:	imap-server
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	libsasl-devel >= 2.1.15
BuildRequires:	ext2fs-devel
BuildRequires:	perl-devel
BuildRequires:	tcp_wrappers-devel
BuildRequires:	db-devel >= %{db_version}
BuildRequires:	openssl-devel
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	groff >= 1.15-8
BuildRequires:	perl-Digest-SHA1
%if %{with_snmp}
BuildRequires:	net-snmp-devel >= 5.1-6mdk
BuildRequires:  libelfutils-devel
Requires:	net-snmp-mibs
%endif
%if %{with_ldap}
BuildRequires:	openldap-devel
%else
%if %{build_virtualdomains_in_ldap}
BuildRequires:	openldap-devel
%endif
%endif
%if %{with_mysql}
BuildRequires:	mysql-devel
%endif
%if %{with_pgsql}
BuildRequires:	postgresql-devel
%endif
%if %{with_sqlite}
BuildRequires:	sqlite3-devel
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%if %{SASLGROUP}
%define		_saslgroup saslauth
%endif
%define		_cyrususer cyrus
%define		_cyrusgroup mail
%define		_vardata %{_var}/lib/imap
%define		_spooldata %{_var}/spool/imap
# (gb) stick to /usr/lib/cyrus-imapd as this is an existing practise
# from MDK 10.0 and below + /etc/init.d/cyrus-imapd would need to
# runtime-detect the libdir since this ought to be an arch-independent
# script.
%define		_cyrexecdir %{_prefix}/lib/cyrus-imapd
%define		_confdir master/conf
%if %{PREFORK}
%define		_cyrusconf %{_confdir}/prefork.conf
%else
%define		_cyrusconf %{_confdir}/normal.conf
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The Cyrus IMAP Server is a scaleable enterprise mail system
designed for use from small to large enterprise environments using
standards-based technologies.

A full Cyrus IMAP implementation allows a seamless mail and bulletin
board environment to be set up across multiple servers. It differs from
other IMAP server implementations in that it is run on "sealed"
servers, where users are not normally permitted to log in. The mailbox
database is stored in parts of the filesystem that are private to the
Cyrus IMAP system. All user access to mail is through software using
the IMAP, POP3, or KPOP protocols. TLSv1 and SSL are supported for
security.

This is the main package, install also the %{name}-utils package (it
contains server administration tools and depends on the perl-Cyrus
package).

%package	murder
Summary:	Cyrus IMAP server murder aggregator system files
Group:		System/Servers
Requires:	%{name} >= %{version}-%{release}

%description	murder
The %{name}-murder package contains the Cyrus murder aggregator system,
i.e. IMAP, POP3 and LMTP proxies, and the mupdate mailbox master daemon.
It allows for cluster setups where there are many backend Cyrus spools
and frontend proxy servers.

%package	nntp
Summary:	Cyrus IMAP server murder nntp support files
Group:		System/Servers
Requires:	%{name} >= %{version}-%{release}
Conflicts:	leafnode

%description	nntp
Cyrus has the ability to export Usenet via IMAP and/or export shared
IMAP mailboxes via NNTP. This is made possible by a new NNTP daemon
which is included in this package.

%package	devel
Summary:	Cyrus IMAPd development files
Group:		Development/Other

%description	devel
This package contains header files and libraries necessary for 
developing applications which use the imclient library.

The main package is %{name}.

%package -n	perl-Cyrus
Summary:	Cyrus IMAPd utility Perl modules
Group:		Development/Perl
# with previous versions of sasl, imap LOGIN would fail
Requires:	%{mklibname sasl 2} >= 2.1.15

%description -n	perl-Cyrus
This package contains Perl modules necessary to use the Cyrus server
administrative utilities.

The main package is %{name}.

%package	utils
Summary:	Cyrus IMAPd server admin utilities
Group:		System/Servers
Requires:	perl-Cyrus >= %{version}-%{release}

%description	utils
This package contains Cyrus IMAPd server administrative tools. It 
can be installed on systems other than the one running the server.

This package depends on the perl-Cyrus package.
The main package is %{name}.

%prep

%setup -q -n %{name}-%{version}
%patch1 -p0 -b .mdk9.0perl.orig
%patch2
%if %{build_autocreate}
%patch3 -p1 -b .autocreate.orig
%endif
%if %{build_autosieve}
%patch4 -p1 -b .autosieve.orig
%endif
%if %{build_rmquota}
%patch5 -p1 -b .rmquota.orig
%endif

%patch6 -p1 -b .plaintext.orig
%patch7 -p1 -b .64bit-fixes.orig

# (oe) for kolab2: Patch to support virtdomains: ldap (parse domain from "email" field an LDAP user entry)
%if %{build_virtualdomains_in_ldap}
%patch8 -p1 -b .kolab-ldap.orig
%endif
# (oe) for kolab2: Allow for custom annotation
%patch9 -p1 -b .annotate.orig
%if %{with_ldap}
%patch10 -p1 -b .ptloader.orig
%endif
%patch11 -p1 -b .secprops.orig
%patch12 -p1 -b .format_not_a_string_literal_and_no_format_arguments.orig

%patch13 -p1 -b .getrlimit.orig
%patch14 -p1 -b .skiplist_verbosity.orig
%patch15 -p1 -b .statuscache_verbosity.orig
%patch16 -p1 -b .user_deny_verbosity.orig

%patch17 -p1 -b .mancyrusdb.orig
%patch18 -p1 -b .make_md5_sha1_dirs.orig
%patch19 -p1 -b .mkimap.orig
%patch21 -p1 -b .sieve_port.orig
%patch22 -p1 -b .db51

## Extra documentation
mkdir -p extradocs
for i in %{SOURCE2} %{SOURCE4} %{SOURCE19} ; do
  cp $i extradocs
done 

## remove cvs file
rm -f doc/text/.cvsignore

## regenerate html man pages
pushd man
for mp in *[1-8] ; do groff -m man -T html $mp > ../doc/man/$mp.html ; done
popd

# fix build under mdx8.2
perl -ni -e "print unless /^AC_PREREQ/" configure.in

install -m 0644 %{SOURCE8} cyrus-imapd.pamd

# cleanup
for i in `find . -type d -name CVS`  `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%build
%serverbuild

CPPFLAGS="-I%{_includedir}/et $CPPFLAGS"
export CPPFLAGS
CFLAGS="$RPM_OPT_FLAGS -fPIC"
export CFLAGS
LDFLAGS="-L%{_libdir}"
export LDFLAGS

#with the existing autom4te.cache autoheader would fail with the message
#Can't locate object method "path" via package "Request" at /usr/share/autoconf/Autom4te/C4che.pm line 69, <GEN1> line 111.
#

rm -rf autom4te.cache configure
export WANT_AUTOCONF_2_5=1
libtoolize --copy --force; aclocal -I cmulocal; autoheader; autoconf

%configure2_5x \
%if %{IDLED}
    --with-idle=idled \
%endif
%if !%{with_snmp}
    --without-snmp \
%endif
%if %{with_ldap}
    --with-ldap=/usr \
%endif
%if %{with_mysql}
    --with-mysql --with-mysql-incdir=/usr/include/mysql \
%endif
%if %{with_pgsql}
    --with-pgsql \
%endif
%if %{with_sqlite}
    --with-sqlite \
%endif
    --with-extraident="Mandriva-RPM-%{version}-%{release}" \
    --with-syslogfacility=MAIL \
    --with-bdb=db-%{db_version} \
    --enable-murder \
    --enable-netscapehack \
    --enable-listext \
    --enable-nntp \
    --with-perl=%{__perl} \
    --with-cyrus-prefix=%{_cyrexecdir} \
    --with-service-path=%{_cyrexecdir} \
#    --with-krb=%{_prefix}/kerberos \

make clean
# no parallel make - 2.3.10
make

# Modify docs master --> cyrus-master
pushd man
  perl -pi -e "s#master\(8\)#cyrus-master(8)#" `ls *5 *8`
  cd ../doc
  perl -pi -e "s#master#cyrus-master#g;" man.html
  cd man
  perl -pi -e "s#master\(8\)#cyrus-master(8)#;" `ls *html`
popd

# Modify path in perl scripts
pushd perl/imap/examples
  perl -pi -e "s#/usr/local/bin/perl#%{__perl}#" `find . -type f -name "*.pl"`
popd

# Cleanup of doc dir
find doc perl -name CVS -type d | xargs -r rm -fr
find doc -name "*~" -type f | xargs -r rm -f
find doc -name "*.*.orig" -type f | xargs -r rm -f

rm -f doc/Makefile.dist
rm -f doc/text/htmlstrip.c

# modify lmtp socket path in .conf files
perl -pi -e "s#/var/imap#%{_vardata}#" %{_confdir}/*.conf

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std
%makeinstall_std -C man

%{__install} -m 755 imtest/imtest	%{buildroot}%{_cyrexecdir}/
%{__install} -m 755 perl/imap/cyradm	%{buildroot}%{_cyrexecdir}/

# Install tools
for tool in dohash masssievec mkimap mknewsgroups rehash translatesieve undohash  upgradesieve ; do
	 test -f tools/${tool} && %{__install} -m 755 tools/${tool} %{buildroot}%{_cyrexecdir}/
done
%{__install} -m 755 %{SOURCE13} %{buildroot}%{_cyrexecdir}/imapcreate

# Create directories
%{__install} -d \
%if %{with_snmp}
        %{buildroot}%{_datadir}/snmp/mibs \
%endif
%if %{with_ldap}
        %{buildroot}%{_vardata}/ptclient/ \
%endif
	%{buildroot}%{_initrddir} \
	%{buildroot}%{_sysconfdir}/{pam.d,sysconfig,cron.daily} \
	%{buildroot}%{_libdir}/sasl \
	%{buildroot}%{_bindir} \
	%{buildroot}%{_spooldata}/stage. \
	%{buildroot}%{_vardata}/{user,quota,proc,log,msg,socket,db,sieve,rpm,backup}

# Install additional files
%{__install} -m 755 %{SOURCE15}   %{buildroot}%{_cyrexecdir}/cvt_cyrusdb_all

# Install config files
%{__install} -m 644 %{_cyrusconf} %{buildroot}%{_sysconfdir}/cyrus.conf
%{__install} -m 644 %{SOURCE6}    %{buildroot}%{_sysconfdir}/imapd.conf

%{__install} -m 644 cyrus-imapd.pamd %{buildroot}%{_sysconfdir}/pam.d/pop
%{__install} -m 644 cyrus-imapd.pamd %{buildroot}%{_sysconfdir}/pam.d/imap
%{__install} -m 644 cyrus-imapd.pamd %{buildroot}%{_sysconfdir}/pam.d/sieve
%{__install} -m 644 cyrus-imapd.pamd %{buildroot}%{_sysconfdir}/pam.d/mupdate
%{__install} -m 644 cyrus-imapd.pamd %{buildroot}%{_sysconfdir}/pam.d/lmtp
%{__install} -m 644 cyrus-imapd.pamd %{buildroot}%{_sysconfdir}/pam.d/nntp
%{__install} -m 644 cyrus-imapd.pamd %{buildroot}%{_sysconfdir}/pam.d/csync

%{__install} -m 644 %{SOURCE12}   %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -m 755 %{SOURCE11}   %{buildroot}%{_initrddir}/%{name}
%{__install} -m 755 %{SOURCE20}   %{buildroot}%{_sysconfdir}/cron.daily/%{name}

%if %{with_snmp}
# Install snmp mibs
%{__install} -m 644 master/CYRUS-MASTER.mib %{buildroot}%{_datadir}/snmp/mibs/CYRUS-MASTER-MIB.txt
%{__install} -m 644 %{SOURCE21} %{buildroot}%{_datadir}/snmp/mibs/CMU-MIB.txt
%endif

# Install README.RPM
%{__install} -m 644 %{SOURCE14} README.RPM
cat << EOF >> README.RPM

RPM BUILD TIME CONFIGURATION OPTIONS

This RPM package has been compiled with the following options:

use saslauth group
SASLGROUP: %{SASLGROUP}

use preforking cyrus.conf
PREFORK: %{PREFORK}

enable IDLED support
IDLED: %{IDLED}

enable full directory hash
FULLDIRHASH: %{FULLDIRHASH}

EOF

# Install templates
%{__install} -m 755 -d doc/conf
%{__install} -m 644 %{_confdir}/*.conf doc/conf/

# Rename 'master' binary and manpage to avoid crash with postfix
mv -f %{buildroot}%{_cyrexecdir}/master	%{buildroot}%{_cyrexecdir}/cyrus-master
mv -f %{buildroot}%{_mandir}/man8/master.8 %{buildroot}%{_mandir}/man8/cyrus-master.8
cp -af doc/man/master.8.html doc/man/cyrus-master.8.html

# Create symlinks
ln -sf ../lib/cyrus-imapd/cyradm %{buildroot}%{_bindir}/
ln -sf ../lib/cyrus-imapd/imtest %{buildroot}%{_bindir}/
ln -sf ../lib/cyrus-imapd/imapcreate %{buildroot}%{_bindir}/

# required if upgrading from 2.2.x -> 2.3.6+
%{__install} -m 755 tools/migrate-metadata %{buildroot}%{_cyrexecdir}/migrate-metadata

# provide the cyrusMaster.conf file, discovered by doing:
# /usr/lib/cyrus-imapd/cyrus-master -p /var/run/cyrus-master.pid -D
%if %{with_snmp}
install -d %{buildroot}/var/lib/net-snmp
echo "# placeholder" > %{buildroot}/var/lib/net-snmp/cyrusMaster.conf
%endif

# cleanup
find %{buildroot}%{perl_vendorarch} -name "*.annotate" | xargs rm -f

%pre
# Create 'cyrus' user on target host
%if %{SASLGROUP}
/usr/sbin/groupadd -r %{_saslgroup} 2> /dev/null || :
/usr/sbin/useradd -c "Cyrus IMAP Server" -d %{_vardata} -g %{_cyrusgroup} \
				-G %{_saslgroup} -s /bin/bash -r %{_cyrususer} 2> /dev/null || :
%else
/usr/sbin/useradd -c "Cyrus IMAP Server" -d %{_vardata} -g %{_cyrusgroup} \
	-s /bin/bash -r %{_cyrususer} 2> /dev/null || :
%endif
# move ssl certificate/key from /etc/ssl to /etc/pki/tls
if [ -f /etc/ssl/cyrus-imapd/cyrus-imapd.pem -a ! -f /etc/pki/tls/private/cyrus-imapd.pem -a ! -f /etc/pki/tls/certs/cyrus-imapd.pem  ];then
	touch /etc/pki/tls/private/cyrus-imapd.pem
	chmod 600 /etc/pki/tls/private/cyrus-imapd.pem
	awk '/^-----BEGIN PRIVATE KEY-----/ {p=1} /-----END PRIVATE KEY-----/ {p=0;print} p == 1 {print}'  /etc/ssl/cyrus-imapd/cyrus-imapd.pem > /etc/pki/tls/private/cyrus-imapd.pem
	awk '/^-----BEGIN PRIVATE KEY-----/ {p=0} /-----END PRIVATE KEY-----/ {p=1;next} p == 1 {print}' /etc/ssl/cyrus-imapd/cyrus-imapd.pem > /etc/pki/tls/certs/cyrus-imapd.pem
	sed -i -e 's,^[[:space:]]*tls_cert_file:[[:space:]]\+/etc/ssl/cyrus-imapd/cyrus-imapd.pem\>,tls_cert_file: /etc/pki/tls/certs/cyrus-imapd.pem,' /etc/imapd.conf
	sed -i -e 's,^[[:space:]]*tls_key_file:[[:space:]]\+/etc/ssl/cyrus-imapd/cyrus-imapd.pem\>,tls_key_file: /etc/pki/tls/private/cyrus-imapd.pem,' /etc/imapd.conf
	rm -f /etc/ssl/cyrus-imapd/cyrus-imapd.pem
fi

%post
if [ $1 = 1 ] ; then
# make sure we own the stuff, otherwise /var/log/mail/* will fill
# the whole disk with error messages...
chown -R %{_cyrususer}:%{_cyrusgroup} %{_vardata} %{_spooldata}
fi
%_create_ssl_certificate cyrus-imapd
chown %{_cyrususer}:%{_cyrusgroup} /etc/pki/tls/private/cyrus-imapd.pem


# Force synchronous updates only on ext2 filesystems
# Note: This will slow down user creation for 10.000+ users!
for i in %{_vardata}/{user,quota} %{_spooldata}
do
	if [ `find $i -maxdepth 0 -printf %F` = "ext2" ]; then
		chattr -R +S $i 2>/dev/null
	fi
done

# Add sieve service if necessary
if ! grep -q ^sieve %{_sysconfdir}/services; then
	echo -e 'sieve\t\t2000/tcp\t\t\t# Sieve mail filter daemon' >> %{_sysconfdir}/services
fi

# Add lmtp service if necessary
if ! grep -q ^lmtp %{_sysconfdir}/services; then
	echo -e 'lmtp\t\t2003/tcp\t\t\t# Local mail delivery protocol (rfc2033)' >> %{_sysconfdir}/services
fi

# upgrade from previous versions with compiled in database backends
rm -f %{_vardata}/rpm/db.cfg.cache 2> /dev/null

# "ctl_deliver -E" is deprecated, now is "cyr_expire -E"
if grep -q "ctl_deliver *-E" %{_sysconfdir}/cyrus.conf ; then
  perl -pi -e "s/ctl_deliver *-E/cyr_expire -E/" %{_sysconfdir}/cyrus.conf
fi
# compile to byte code sieve scripts on upgrade
# masssievec needs to run:
# - for versions before 2.2.0 (2.1.x) since they had no bytecode
# - upgrading from 2.2.0 since the bytecode has changed
# - upgrading from 2.2.1 since the bytecode has changed
if [ $1 != 1 ] ; then 
  if [ -f %{_vardata}/rpm/version ] ; then
    oldversion=`cat %{_vardata}/rpm/version`
    if [ "$oldversion" = "2.2.0" -o "$oldversion" = "2.2.1" ] ; then
      compile_needed=1
    else
      compile_needed=0
    fi
  else
    # versions prior to 2.2.x didn't write the file
    compile_needed=1
  fi
  if [ $compile_needed = 1 ] ; then
    echo "compiling sieve scripts"
    su cyrus -c "%{_cyrexecdir}/masssievec %{_cyrexecdir}/sievec"
  fi
fi
# cache the installed version for next upgrade
echo %{version} > %{_vardata}/rpm/version

%_post_service %{name}

%preun
%_preun_service %{name}
if [ $1 = 0 ]; then
	/usr/sbin/userdel %{_cyrususer} 2> /dev/null || :
%if %{SASLGROUP}
	if [ "`grep ^%{_saslgroup}: %{_sysconfdir}/group | cut -d: -f4-`" = "" ]; then
		/usr/sbin/groupdel %{_saslgroup} 2> /dev/null || :
	fi
%endif
	rm -f %{_vardata}/socket/lmtp 2> /dev/null
	rm -f %{_vardata}/rpm/version 2> /dev/null
fi

%triggerin -- %{name} < 2.0.0
#To avoid automatic restart of the daemon when upgrading from versions
#1.x.x of Cyrus IMAPd in rpm form, be sure the old daemon is stopped
/sbin/service %{name} stop >/dev/null 2>&1 || :

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc doc/* extradocs/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/*.conf
%attr(0755,root,root) %config(noreplace) %{_initrddir}/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0644,root,root) %config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/pop
%attr(0644,root,root) %config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/imap
%attr(0644,root,root) %config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/sieve
%attr(0644,root,root) %config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/lmtp
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/cron.daily/%{name}
%attr(0755,root,root) %dir %{_cyrexecdir}
%attr(0755,root,root) %{_cyrexecdir}/arbitron
%attr(0755,root,root) %{_cyrexecdir}/chk_cyrus
%attr(0755,root,root) %{_cyrexecdir}/ctl_cyrusdb
%attr(0755,root,root) %{_cyrexecdir}/ctl_deliver
%attr(0755,root,root) %{_cyrexecdir}/ctl_mboxlist
%attr(0755,root,root) %{_cyrexecdir}/cvt_cyrusdb
%attr(0755,root,root) %{_cyrexecdir}/cvt_cyrusdb_all
%attr(0755,root,root) %{_cyrexecdir}/cyr_dbtool
%attr(0755,root,root) %{_cyrexecdir}/cyr_df
%attr(0755,root,root) %{_cyrexecdir}/cyrdump
%attr(0755,root,root) %{_cyrexecdir}/cyr_expire
%attr(0755,root,root) %{_cyrexecdir}/cyr_synclog
%attr(0755,root,root) %{_cyrexecdir}/cyrus-master
%attr(0755,root,root) %{_cyrexecdir}/dohash
%attr(0755,root,root) %{_cyrexecdir}/fud
%attr(0755,root,root) %{_cyrexecdir}/imapd
%attr(0755,root,root) %{_cyrexecdir}/ipurge
%attr(0755,root,root) %{_cyrexecdir}/lmtpd
%attr(0755,root,root) %{_cyrexecdir}/masssievec
%attr(0755,root,root) %{_cyrexecdir}/mbexamine
%attr(0755,root,root) %{_cyrexecdir}/mbpath
%attr(0755,root,root) %{_cyrexecdir}/migrate-metadata
%attr(0755,root,root) %{_cyrexecdir}/mkimap
%attr(0755,root,root) %{_cyrexecdir}/mknewsgroups
%attr(0755,root,root) %{_cyrexecdir}/notifyd
%attr(0755,root,root) %{_cyrexecdir}/pop3d
%attr(0755,root,root) %{_cyrexecdir}/quota
%attr(0755,root,root) %{_cyrexecdir}/reconstruct
%attr(0755,root,root) %{_cyrexecdir}/rehash
%attr(0755,root,root) %{_cyrexecdir}/sievec
%attr(0755,root,root) %{_cyrexecdir}/sieved
%attr(0755,root,root) %{_cyrexecdir}/squatter
%attr(0755,root,root) %{_cyrexecdir}/timsieved
%attr(0755,root,root) %{_cyrexecdir}/tls_prune
%attr(0755,root,root) %{_cyrexecdir}/translatesieve
%attr(0755,root,root) %{_cyrexecdir}/undohash
%attr(0755,root,root) %{_cyrexecdir}/unexpunge
%attr(0755,root,root) %{_cyrexecdir}/upgradesieve
%if %{with_ldap}
%attr(0755,root,root) %{_cyrexecdir}/ptdump
%attr(0755,root,root) %{_cyrexecdir}/ptexpire
%attr(0755,root,root) %{_cyrexecdir}/ptloader
%endif
%if %build_autocreate
%attr(0755,root,root) %{_cyrexecdir}/compile_sieve
%endif
%attr(0755,root,root) %{_cyrexecdir}/smmapd
%if %{IDLED}
%attr(0755,root,root) %{_cyrexecdir}/idled
%endif
%attr(4754,%{_cyrususer},%{_cyrusgroup}) %{_cyrexecdir}/deliver
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %dir %{_vardata}
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %{_vardata}/user
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %{_vardata}/quota
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %{_vardata}/proc
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %{_vardata}/log
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %{_vardata}/msg
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %{_vardata}/socket
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %{_vardata}/db
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %{_vardata}/sieve
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %{_vardata}/rpm
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %{_vardata}/backup
%if %{with_ldap}
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %{_vardata}/ptclient
%endif
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %dir %{_spooldata}
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %{_spooldata}/*
%if %{with_snmp}
%attr(0644,root,root) %{_datadir}/snmp/mibs/*
%attr(0644,%{_cyrususer},%{_cyrusgroup}) /var/lib/net-snmp/cyrusMaster.conf
%endif
%attr(0644,root,root) %{_mandir}/man5/*
%attr(0644,root,root) %{_mandir}/man8/arbitron.8*
%attr(0644,root,root) %{_mandir}/man8/chk_cyrus.8*
%attr(0644,root,root) %{_mandir}/man8/ctl_cyrusdb.8*
%attr(0644,root,root) %{_mandir}/man8/ctl_deliver.8*
%attr(0644,root,root) %{_mandir}/man8/ctl_mboxlist.8*
%attr(0644,root,root) %{_mandir}/man8/cvt_cyrusdb.8*
%attr(0644,root,root) %{_mandir}/man8/cyr_dbtool.8*
%attr(0644,root,root) %{_mandir}/man8/cyr_df.8*
%attr(0644,root,root) %{_mandir}/man8/cyr_expire.8*
%attr(0644,root,root) %{_mandir}/man8/cyr_synclog.8*
%attr(0644,root,root) %{_mandir}/man8/cyrus-master.8*
%attr(0644,root,root) %{_mandir}/man8/deliver.8*
%attr(0644,root,root) %{_mandir}/man8/fud.8*
%attr(0644,root,root) %{_mandir}/man8/idled.8*
%attr(0644,root,root) %{_mandir}/man8/imapd.8*
%attr(0644,root,root) %{_mandir}/man8/ipurge.8*
%attr(0644,root,root) %{_mandir}/man8/lmtpd.8*
%attr(0644,root,root) %{_mandir}/man8/make_md5.8*
%attr(0644,root,root) %{_mandir}/man8/make_sha1.8*
%attr(0644,root,root) %{_mandir}/man8/mbexamine.8*
%attr(0644,root,root) %{_mandir}/man8/mbpath.8*
%attr(0644,root,root) %{_mandir}/man8/notifyd.8*
%attr(0644,root,root) %{_mandir}/man8/pop3d.8*
%attr(0644,root,root) %{_mandir}/man8/quota.8*
%attr(0644,root,root) %{_mandir}/man8/reconstruct.8*
%attr(0644,root,root) %{_mandir}/man8/rmnews.8*
%attr(0644,root,root) %{_mandir}/man8/smmapd.8*
%attr(0644,root,root) %{_mandir}/man8/squatter.8*
%attr(0644,root,root) %{_mandir}/man8/sync_client.8*
%attr(0644,root,root) %{_mandir}/man8/syncnews.8*
%attr(0644,root,root) %{_mandir}/man8/sync_reset.8*
%attr(0644,root,root) %{_mandir}/man8/sync_server.8*
%attr(0644,root,root) %{_mandir}/man8/timsieved.8*
%attr(0644,root,root) %{_mandir}/man8/tls_prune.8*
%attr(0644,root,root) %{_mandir}/man8/unexpunge.8*
%doc COPYRIGHT README README.RPM
%if %{build_autocreate}
%doc README.autocreate
%endif

%files murder
%defattr(-,root,root)
%doc doc/text/install-murder
%config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/mupdate
%config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/csync
%attr(0755,root,root) %{_cyrexecdir}/lmtpproxyd
%attr(0755,root,root) %{_cyrexecdir}/mupdate
%attr(0755,root,root) %{_cyrexecdir}/pop3proxyd
%attr(0755,root,root) %{_cyrexecdir}/proxyd

%files nntp
%defattr(-,root,root)
%doc doc/text/install-netnews
%config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/nntp
%attr(0755,root,root) %{_cyrexecdir}/fetchnews
%attr(0755,root,root) %{_cyrexecdir}/nntpd
%attr(0644,root,root) %{_mandir}/man8/nntpd.8*
%attr(0644,root,root) %{_mandir}/man8/fetchnews.8*

%files devel
%defattr(-,root,root)
%{_includedir}/cyrus
%{_libdir}/lib*.a
%attr(0644,root,root) %{_mandir}/man3/imclient.3*

%files -n perl-Cyrus
%defattr(-,root,root)
%doc perl/imap/README perl/imap/Changes perl/imap/examples
%{perl_vendorarch}/auto/Cyrus
%{perl_vendorarch}/Cyrus
%attr(0644,root,root) %{_mandir}/man3/Cyrus*

%files utils
%defattr(-,root,root)
%attr(0755,root,root) %{_cyrexecdir}/cyradm
%attr(0755,root,root) %{_cyrexecdir}/imtest
%attr(0755,root,root) %{_cyrexecdir}/imapcreate
%attr(0755,root,root) %{_bindir}/*
%attr(0644,root,root) %{_mandir}/man1/*
