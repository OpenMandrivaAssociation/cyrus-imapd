%define _disable_lto 1

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
%define build_autosieve 0
%{?_without_autosieve: %define build_autosieve 0}

# remove quota files extension:
%define build_rmquota 0
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

Summary:	A high-performance mail store with IMAP and POP3 support
Name:		cyrus-imapd
Version:	2.4.18
Release:	4
License:	OSI Approved
Group:		System/Servers
Url:		http://cyrusimap.org/
Source0:	ftp://ftp.cyrusimap.org/cyrus-imapd/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.cyrusimap.org/cyrus-imapd/%{name}-%{version}.tar.gz.sig
Source2:	cyrus-procmailrc
Source4:	cyrus-user-procmailrc.template
Source6:	cyrus-imapd.imap-2.1.x-conf
Source8:	cyrus-imapd.pamd
Source12:	cyrus-imapd.sysconfig
Source13:	http://clement.hermann.free.fr/scripts/Cyrus/imapcreate.pl
Source14:	cyrus-imapd.README.RPM
Source15:	cyrus-imapd.cvt_cyrusdb_all
Source19:	cyrus-imapd-procmail+cyrus.mc
Source20:	cyrus-imapd.cron-daily
Source21:	http://ftp.andrew.cmu.edu/pub/net/mibs/cmu/cmu.mib
#systemd support
Source22:	cyrus-imapd.service
Source23:	cyr_systemd_helper
# This patch fixes the perl install path for mdk9.0 and later
Patch1:		cyrus-imapd-mdk9.0perl-patch
# cyrus-master instead of master in syslog
Patch2:		cyrus-imapd-logident.patch
# rediffed P3 and P4 comes from http://blog.vx.sk/archives/13-Autocreate-and-autosieve-patches-for-Cyrus-IMAP-Server-24.html
# Autocreate INBOX patch (http://email.uoa.gr/projects/cyrus/autocreate/)
#Patch3:	http://email.uoa.gr/download/cyrus/cyrus-imapd-2.3.16/cyrus-imapd-2.3.16-autocreate-0.10-0.diff
Patch3:		cyrus-imapd-2.4.13-autocreate-0.10-0.diff
# Create on demand folder requested by sieve filter (http://email.uoa.gr/projects/cyrus/autosievefolder/)
#Patch4:	http://email.uoa.gr/download/cyrus/cyrus-imapd-2.3.16/cyrus-imapd-2.3.16-autosieve-0.6.0.diff
Patch4:		cyrus-imapd-2.4.13-autosieve-0.6.0.diff
# Remove QUOTA patch (http://email.uoa.gr/projects/cyrus/quota-patches/rmquota/)
Patch5:		http://email.uoa.gr/download/cyrus/cyrus-imapd-2.3.9/cyrus-imapd-2.3.9-rmquota-0.5-0.diff
# command line switch to disallow plaintext login
Patch6:		cyrus-imapd-2.4.13-plaintext.diff
# (oe) for kolab2: Patch to support virtdomains: ldap (parse domain from "email" field an LDAP user entry)
Patch8:		cyrus-imapd-kolab-ldap.diff
# (bluca) add ptloader to cyrus.conf 
Patch10:	cyrus-imapd-ptloader-conf.diff
# (bluca) fix LDAP_OPT_X_SASL_SECPROPS error in ptloader
Patch11:	cyrus-imapd-ptloader-secprops.diff
# Other patches from simon matter
Patch19:	cyrus-imapd-2.3.11-mkimap.patch
Patch21:	cyrus-imapd-2.3.16-sieve_port.patch
# fedora patches
Patch100:	http://www.oakton.edu/~jwade/cyrus/cyrus-imapd-2.1.3/cyrus-imapd-2.1.3-flock.patch
Patch101:	cyrus-imapd-2.3.1-authid_normalize.patch
# for c-i <= 2.4.12
Patch102:	cyrus-imapd-2.4.12-debugopt.patch
Requires:	perl
# with previous versions of sasl, imap LOGIN would fail
Requires:	%{mklibname sasl 2} >= 2.1.15
#Requires:	krb5-libs
Requires(pre):	rpm-helper
Requires(post):	chkconfig openssl perl systemd-units
Requires(preun):rpm-helper systemd-units chkconfig
%if %{SASLGROUP}
Requires(preun):/usr/sbin/groupdel
%endif
Requires(postun): systemd-units
Provides:	imap
Provides:	imap-server
BuildRequires:	autoconf automake libtool
BuildRequires:	bison
BuildRequires:	db-devel
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	flex
BuildRequires:	groff >= 1.15-8
BuildRequires:	pkgconfig(libsasl2)
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	perl-devel
BuildRequires:	perl-Digest-SHA1
BuildRequires:	wrap-devel
%if %{with_snmp}
BuildRequires:	net-snmp-devel
BuildRequires:  pkgconfig(libelf)
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
BuildRequires:	pkgconfig(sqlite3)
%endif

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
%patch5 -p1 -b .rmquota.orig <- this patch is broken and won't apply
%endif

%patch6 -p1 -b .plaintext.orig

# (oe) for kolab2: Patch to support virtdomains: ldap (parse domain from "email" field an LDAP user entry)
%if %{build_virtualdomains_in_ldap}
%patch8 -p1 -b .kolab-ldap.orig
%endif
%if %{with_ldap}
%patch10 -p1 -b .ptloader.orig
%endif
%patch11 -p1 -b .secprops.orig

%patch19 -p1 -b .mkimap.orig
%patch21 -p1 -b .sieve_port.orig

# fedora patches
%patch100 -p1 -b .flock
%patch101 -p1 -b .authid_normalize
%patch102 -p1 -b .debugopt

find . -name Makefile* |xargs sed -i -e 's,configure.in,configure.ac,g'

## Extra documentation
mkdir -p extradocs
for i in %{SOURCE2} %{SOURCE4} %{SOURCE19} ; do
  cp $i extradocs
done 

## regenerate html man pages
pushd man
    for mp in *[1-8] ; do groff -m man -T html $mp > ../doc/man/$mp.html ; done
popd

# fix build under mdx8.2
#perl -ni -e "print unless /^AC_PREREQ/" configure.in

install -m 0644 %{SOURCE8} cyrus-imapd.pamd

# cleanup
for i in $(find . -type d -name CVS)  $(find . -type d -name .svn) $(find . -type f -name .cvs\*) $(find . -type f -name .#\*); do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%build
%serverbuild

# it does not work with -fPIE and someone added that to the serverbuild macro...
CFLAGS=$(echo $CFLAGS|sed -e 's|-fPIE||g')
CXXFLAGS=$(echo $CXXFLAGS|sed -e 's|-fPIE||g')
RPM_OPT_FLAGS=$(echo $RPM_OPT_FLAGS |sed -e 's|-fPIE||g')

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

# this removes rpath
export andrew_cv_runpath_switch=none

%configure \
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
    --with-bdb=db --with-bdb-libdir=%{_libdir} \
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

%make_install
%makei_nstall -C man

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
    %{buildroot}%{_sysconfdir}/{pam.d,sysconfig,cron.daily} \
    %{buildroot}/lib/systemd/system \
    %{buildroot}%{_libdir}/sasl \
    %{buildroot}%{_bindir} \
    %{buildroot}%{_spooldata}/stage. \
    %{buildroot}%{_vardata}/{user,quota,proc,log,msg,socket,db,sieve,rpm,backup}

# Install additional files
%{__install} -m 755 %{SOURCE15} %{buildroot}%{_cyrexecdir}/cvt_cyrusdb_all

# Install config files
%{__install} -m 644 %{_cyrusconf} %{buildroot}%{_sysconfdir}/cyrus.conf
%{__install} -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/imapd.conf

%{__install} -m 644 cyrus-imapd.pamd %{buildroot}%{_sysconfdir}/pam.d/pop
%{__install} -m 644 cyrus-imapd.pamd %{buildroot}%{_sysconfdir}/pam.d/imap
%{__install} -m 644 cyrus-imapd.pamd %{buildroot}%{_sysconfdir}/pam.d/sieve
%{__install} -m 644 cyrus-imapd.pamd %{buildroot}%{_sysconfdir}/pam.d/mupdate
%{__install} -m 644 cyrus-imapd.pamd %{buildroot}%{_sysconfdir}/pam.d/lmtp
%{__install} -m 644 cyrus-imapd.pamd %{buildroot}%{_sysconfdir}/pam.d/nntp
%{__install} -m 644 cyrus-imapd.pamd %{buildroot}%{_sysconfdir}/pam.d/csync

%{__install} -m 644 %{SOURCE12} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -m 755 %{SOURCE20} %{buildroot}%{_sysconfdir}/cron.daily/%{name}
%{__install} -m 644 %{SOURCE22} %{buildroot}/lib/systemd/system/cyrus-imapd.service
%{__install} -m 755 %{SOURCE23} %{buildroot}%{_cyrexecdir}/cyr_systemd_helper

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
find %{buildroot}%{perl_vendorarch} -name "*.orig" | xargs rm -f

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
for i in %{_vardata}/{user,quota} %{_spooldata}; do
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
	    ompile_needed=1
    fi
    if [ $compile_needed = 1 ] ; then
	echo "compiling sieve scripts"
	su cyrus -c "%{_cyrexecdir}/masssievec %{_cyrexecdir}/sievec"
    fi
fi
# cache the installed version for next upgrade
echo %{version} > %{_vardata}/rpm/version

/bin/systemctl daemon-reload > /dev/null 2>&1 :

%preun
if [ $1 = 0 ]; then
    # Package removal, not upgrade
    /bin/systemctl disable cyrus-imapd.service >/dev/null 2>&1 || :
    /bin/systemctl stop cyrus-imapd.service > /dev/null 2>&1 || :
    /usr/sbin/userdel %{_cyrususer} 2> /dev/null || :
%if %{SASLGROUP}
if [ "`grep ^%{_saslgroup}: %{_sysconfdir}/group | cut -d: -f4-`" = "" ]; then
    /usr/sbin/groupdel %{_saslgroup} 2> /dev/null || :
fi
%endif
    rm -f %{_vardata}/socket/lmtp 2> /dev/null
    rm -f %{_vardata}/rpm/version 2> /dev/null
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart cyrus-imapd.service >/dev/null 2>&1 || :
fi

%triggerun -- cyrus-imapd < 2.4.13-1
/sbin/chkconfig --level 3 cyrus-imapd && /bin/systemctl enable cyrus-imapd.service >/dev/null 2>&1 || :

%files
%doc doc/* extradocs/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/*.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0644,root,root) %config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/pop
%attr(0644,root,root) %config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/imap
%attr(0644,root,root) %config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/sieve
%attr(0644,root,root) %config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/lmtp
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/cron.daily/%{name}
/lib/systemd/system/cyrus-imapd.service
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
%attr(0755,root,root) %{_cyrexecdir}/cyr_sequence
%attr(0755,root,root) %{_cyrexecdir}/cyr_synclog
%attr(0755,root,root) %{_cyrexecdir}/cyr_systemd_helper
%attr(0755,root,root) %{_cyrexecdir}/cyr_userseen
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
%doc doc/text/install-murder
%config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/mupdate
%config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/csync
%attr(0755,root,root) %{_cyrexecdir}/lmtpproxyd
%attr(0755,root,root) %{_cyrexecdir}/mupdate
%attr(0755,root,root) %{_cyrexecdir}/pop3proxyd
%attr(0755,root,root) %{_cyrexecdir}/proxyd

%files nntp
%doc doc/text/install-netnews
%config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/nntp
%attr(0755,root,root) %{_cyrexecdir}/fetchnews
%attr(0755,root,root) %{_cyrexecdir}/nntpd
%attr(0644,root,root) %{_mandir}/man8/nntpd.8*
%attr(0644,root,root) %{_mandir}/man8/fetchnews.8*

%files devel
%{_includedir}/cyrus
%{_libdir}/lib*.a
%attr(0644,root,root) %{_mandir}/man3/imclient.3*

%files -n perl-Cyrus
%doc perl/imap/README perl/imap/Changes perl/imap/examples
%{perl_vendorarch}/auto/Cyrus
%{perl_vendorarch}/Cyrus
%attr(0644,root,root) %{_mandir}/man3/Cyrus*

%files utils
%attr(0755,root,root) %{_cyrexecdir}/cyradm
%attr(0755,root,root) %{_cyrexecdir}/imtest
%attr(0755,root,root) %{_cyrexecdir}/imapcreate
%attr(0755,root,root) %{_bindir}/*
%attr(0644,root,root) %{_mandir}/man1/*


%changelog
* Fri Mar 09 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.4.13-2
+ Revision: 783589
- rebuild

* Thu Jan 26 2012 Oden Eriksson <oeriksson@mandriva.com> 2.4.13-1
+ Revision: 769080
- still parallel make don't work in the build system, oh well...
- eh, forgot one thing there :-)
- 2.4.13
- rediffed some patches
- dropped obsolete patches (some was finally applied upstream and some isn't needed anymore)
- dropped the anti verbosity patches, use new debug config option instead
- added some of the fedora patches (P100,P101,P102)
- added systemd support (fedora)
- added new'ish cyrus-imapd.cvt_cyrusdb_all from fedora (S15)
- disable the rmquota patch as it won't apply cleanly (P5)
- various fixes

* Mon Jan 23 2012 Oden Eriksson <oeriksson@mandriva.com> 2.3.18-2
+ Revision: 767068
- it won't build with -fPIE
- remove rpath (not fixed for the perl modules)
- remove the versioned bdb magic, it will use the latest one now
- more perl-5.14.2 fixes
- P23: fix build with perl-5.14.x (debian)
- fix deps
- fix deps
- rebuilt for perl-5.14.2

* Fri Oct 14 2011 Oden Eriksson <oeriksson@mandriva.com> 2.3.18-1
+ Revision: 704699
- fix deps
- 2.3.18
- drop upstream added patches
- cleanup a little bit

* Mon Jul 18 2011 Oden Eriksson <oeriksson@mandriva.com> 2.3.16-8
+ Revision: 690288
- rebuilt against new net-snmp libs

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 2.3.16-7
+ Revision: 678108
- bump release (weird!)
- P23: security fix for CVE-2011-1926

* Mon Apr 11 2011 Funda Wang <fwang@mandriva.org> 2.3.16-5
+ Revision: 652476
- add debian patch to build with db5.1

* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 2.3.16-4
+ Revision: 645742
- relink against libmysqlclient.so.18

* Mon Mar 14 2011 Thomas Spuhler <tspuhler@mandriva.org> 2.3.16-3
+ Revision: 644463
- added -p0 to line %%patch1 -b .mdk9.0perl.orig to make patch work
- rebuild

* Tue Oct 12 2010 Funda Wang <fwang@mandriva.org> 2.3.16-2mdv2011.0
+ Revision: 585010
- rebuild

* Sun Oct 03 2010 Luca Berra <bluca@mandriva.org> 2.3.16-1mdv2011.0
+ Revision: 582777
- New version 2.3.16
  updated autosieve and autocreate patches
  removed Kolab imapd-annotate patch (merged upstream)
  reworked Kolab ldap patch
  reworked spec file (renumbered patches, removed compat macros)
  remove skiplist magic (it is already known to file)
  move ssl certificates from /etc/ssl to /etc/pki/tls
  add verbosity patches from simon matter
  add other misc patcges from simon
  fix cron daily script

* Sat Sep 11 2010 Thomas Spuhler <tspuhler@mandriva.org> 2.3.15-10mdv2011.0
+ Revision: 577601
- rebuilt with perl 5.12.2

* Sun Aug 01 2010 Luca Berra <bluca@mandriva.org> 2.3.15-9mdv2011.0
+ Revision: 564212
- rebuild for perl 5.12.1

* Wed Jul 21 2010 Jérôme Quelin <jquelin@mandriva.org> 2.3.15-8mdv2011.0
+ Revision: 556351
- rebuild for perl 5.12

* Mon Apr 05 2010 Funda Wang <fwang@mandriva.org> 2.3.15-7mdv2010.1
+ Revision: 531738
- rebuild for new openssl

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3.15-6mdv2010.1
+ Revision: 511557
- rebuilt against openssl-0.9.8m

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3.15-5mdv2010.1
+ Revision: 484970
- rebuild
- really link against bdb 4.8

* Fri Jan 01 2010 Funda Wang <fwang@mandriva.org> 2.3.15-4mdv2010.1
+ Revision: 484838
- rebuild for db 4.8

* Fri Jan 01 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3.15-3mdv2010.1
+ Revision: 484744
- rebuilt against bdb 4.8

* Thu Oct 15 2009 Oden Eriksson <oeriksson@mandriva.com> 2.3.15-2mdv2010.0
+ Revision: 457611
- rebuilt against new net-snmp libs

* Thu Sep 10 2009 Oden Eriksson <oeriksson@mandriva.com> 2.3.15-1mdv2010.0
+ Revision: 436545
- 2.3.15
- rediffed P11,P23
- fixed linkage (P27)

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 2.3.14-2mdv2010.0
+ Revision: 413308
- rebuild

* Wed Apr 08 2009 Oden Eriksson <oeriksson@mandriva.com> 2.3.14-1mdv2009.1
+ Revision: 365126
- 2.3.14
- new autosieve and autocreate patches (P11,P13)
- rediffed the string format patch and added one more fix (P26)

* Tue Dec 16 2008 Oden Eriksson <oeriksson@mandriva.com> 2.3.13-1mdv2009.1
+ Revision: 314815
- 2.3.13
- really link against bdb-4.7 libs
- new upstream patches; P11,P13
- rediffed P17,P22,P23
- added P26 to make it build with -Werror=format-security (thanks pixel)
- enable the new mysql, postgresql and sqlite backends (enabled per default for now)

* Mon Dec 15 2008 Oden Eriksson <oeriksson@mandriva.com> 2.3.12-0.p2.5mdv2009.1
+ Revision: 314524
- rediffed fuzzy patches
- rebuilt against db4.7

* Tue Sep 16 2008 Luca Berra <bluca@mandriva.org> 2.3.12-0.p2.4mdv2009.0
+ Revision: 285186
- enable building of pts/ldap
- fix a problem with ptloader and sasl binds

* Thu Jul 17 2008 Oden Eriksson <oeriksson@mandriva.com> 2.3.12-0.p2.2mdv2009.0
+ Revision: 237677
- rebuild

* Sun May 18 2008 Oden Eriksson <oeriksson@mandriva.com> 2.3.12-0.p2.1mdv2009.0
+ Revision: 208742
- fix buildroot
- 2.3.12p2
- new P11,P13
- rediffed P17,P22

* Thu Apr 17 2008 Oden Eriksson <oeriksson@mandriva.com> 2.3.11-7mdv2009.0
+ Revision: 195128
- revert the "conform to the 2008 specs (don't start the services per
  default)" changes and let this be handled some other way...

* Wed Mar 26 2008 Oden Eriksson <oeriksson@mandriva.com> 2.3.11-6mdv2008.1
+ Revision: 190297
- don't start it per default

* Sat Feb 23 2008 Oden Eriksson <oeriksson@mandriva.com> 2.3.11-5mdv2008.1
+ Revision: 174079
- make it backportable

* Wed Jan 23 2008 Thierry Vignaud <tv@mandriva.org> 2.3.11-4mdv2008.1
+ Revision: 157244
- rebuild with fixed %%serverbuild macro

* Mon Jan 14 2008 Pixel <pixel@mandriva.com> 2.3.11-3mdv2008.1
+ Revision: 151350
- rebuild for perl-5.10.0

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Wed Jan 02 2008 Andreas Hasenack <andreas@mandriva.com> 2.3.11-2mdv2008.1
+ Revision: 140374
- updated to version 2.3.11

* Fri Dec 21 2007 Oden Eriksson <oeriksson@mandriva.com> 2.3.10-2mdv2008.1
+ Revision: 136258
- rebuilt against bdb 4.6.x libs
- rebuilt against openldap-2.4.7 libs

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - s/mandrake/mandriva/

* Mon Nov 05 2007 Andreas Hasenack <andreas@mandriva.com> 2.3.10-1mdv2008.1
+ Revision: 106031
- updated to version 2.3.10
- dropped db patch, same effect can be obtained with a configure option
- updated rmquota and auto* patches, redid cyradm_annotate one

  + Thierry Vignaud <tv@mandriva.org>
    - kill file require on chkconfig

* Wed Aug 08 2007 Oden Eriksson <oeriksson@mandriva.com> 2.3.8-4mdv2008.0
+ Revision: 60200
- rebuilt against new net-snmp libs

* Wed Jun 27 2007 Andreas Hasenack <andreas@mandriva.com> 2.3.8-3mdv2008.0
+ Revision: 45145
- rebuild with new serverbuild macro (-fstack-protector-all)

* Fri Jun 22 2007 Andreas Hasenack <andreas@mandriva.com> 2.3.8-2mdv2008.0
+ Revision: 43136
- using %%serverbuild macro

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 2.3.8-1mdv2008.0
+ Revision: 33602
- fix deps (net-snmp-mibs)
- add the /var/lib/net-snmp/cyrusMaster.conf file

* Mon May 28 2007 Oden Eriksson <oeriksson@mandriva.com> 2.3.8-0mdv2008.0
+ Revision: 32052
- 2.3.8
- dropped upstream patches; P9,P26,P27
- rediffed P17
- new upstream P11,P13,P14
- new P22,P23 (from gentoo)
- misc spec file fixes


* Wed Aug 16 2006 Andreas Hasenack <andreas@mandriva.com> 2.2.13-4mdv2007.0
+ Revision: 56199
- added parallel init information to the initscript (closes #24222)

* Sun Aug 06 2006 Andreas Hasenack <andreas@mandriva.com> 2.2.13-3mdv2007.0
+ Revision: 53022
- added some commented options to default imapd.conf (#22197)
- bunzip pam conf files
- import cyrus-imapd-2.2.13-2mdv2007.0

* Mon Jun 12 2006 Oden Eriksson <oeriksson@mandriva.com> 2.2.13-2mdv2007.0
- added P27 (#23051)

* Fri Jun 02 2006 Oden Eriksson <oeriksson@mandriva.com> 2.2.13-1mdv2007.0
- 2.2.13
- drop upstream patches; P0,P24,P25
- new P11
- rediffed patches; P21,P23
- cleaned up the spec file some
- make it backportable for older pam (S7,S8)

* Fri May 26 2006 Andreas Hasenack <andreas@mandriva.com> 2.2.12-22mdk
- added patch from CVS to fix a compatibility issue with sasl-2.1.22 final
  (imtest was incorrectly relying on a sasl bug that was fixed)
- removed buildrequires for XFree86-devel, couldn't find anything using it

* Sat May 13 2006 Stefan van der Eijk <stefan@eijk.nu> 2.2.12-21mdk
- rebuild for sparc

* Tue Apr 18 2006 Andreas Hasenack <andreas@mandriva.com> 2.2.12-20mdk
- added patch for timsieved, from amal@krasn.ru, to fix
  "Database handles remain at environment close" errors when using
  berkeley db for tls sessions

* Fri Mar 24 2006 Andreas Hasenack <andreas@mandriva.com> 2.2.12-19mdk
- updated auto-* patches

* Wed Jan 04 2006 Oden Eriksson <oeriksson@mandriva.com> 2.2.12-18mdk
- rebuilt against new net-snmp with new major (10)

* Wed Dec 21 2005 Oden Eriksson <oeriksson@mandriva.com> 2.2.12-17mdk
- rebuilt against net-snmp that has new major (9)

* Sun Nov 13 2005 Oden Eriksson <oeriksson@mandriva.com> 2.2.12-16mdk
- rebuilt against openssl-0.9.8a

* Thu Sep 08 2005 Andreas Hasenack <andreas@mandriva.com> 2.2.12-15mdk
- added patch from wes@umich.edu to avoid an off-by-one error which
  was causing cyrus to reject messages with long lines. Thanks to 
  joeghi for supplying a sample message and being patient.
  (fixes https://bugzilla.andrew.cmu.edu/show_bug.cgi?id=2676)

* Wed Aug 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.2.12-14mdk
- rebuilt against new openldap-2.3.6 libs

* Sat Aug 13 2005 Oden Eriksson <oeriksson@mandriva.com> 2.2.12-13mdk
- added one more annotation patch for kolab2 from the kolab cvs

* Fri Aug 05 2005 Oden Eriksson <oeriksson@mandriva.com> 2.2.12-12mdk
- revert the lib64 fixes

* Fri Aug 05 2005 Oden Eriksson <oeriksson@mandriva.com> 2.2.12-11mdk
- /usr/lib/cyrus-imapd is now /usr/lib64/cyrus-imap

* Sat Jul 30 2005 Andreas Hasenack <andreas@mandriva.com> 2.2.12-10mdk
- enabled virtual domains in ldap by default (needed by Kolab2)
- moved virtual domains' buildrequires (openldap) outside the nested %%if
  it was in (otherwise, it would only be required if snmp support was also
  enabled)

* Sat Jul 23 2005 Oden Eriksson <oeriksson@mandriva.com> 2.2.12-9mdk
- use a more descriptive build option for virtual domains in ldap (Andreas Hasenack)
- reworked the virtual domains in ldap patch (Andreas Hasenack)

* Thu Jul 07 2005 Oden Eriksson <oeriksson@mandriva.com> 2.2.12-8mdk
- added rediffed P21, P22 from the openpkg kolab2 packages
- added one gcc4 patch by Ondrej Sury

* Sun Mar 20 2005 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.2.12-7mdk
- fix #9788, conflicts is in the eyes of the beholder...

* Sat Mar 19 2005 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.2.12-6mdk
- only do the recursive chown if not upgrading (Luca Olivetti)

* Thu Mar 17 2005 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.2.12-5mdk
- make sure cyrus:mail owns /var/lib/imap 
  and /var/spool/imap in %%post

* Fri Mar 11 2005 Luca Berra <bluca@vodka.it> 2.2.12-4mdk
- revert liblm_sensors-devel change, fixed in net-snmp package

* Thu Mar 10 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.12-3mdk
- buildrequires: liblm_sensors-devel (cyrus-imapd/master)

* Fri Feb 25 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.2.12-2mdk
- rebuilt against the system bdb (P20)

* Tue Feb 15 2005 Luca Olivetti <luca@olivetti.cjb.net> 2.2.12-1mdk
- 2.2.12 (bug fix release)
- ugly compatibility macros for uglier release tag. See
  http://qa.mandrakesoft.com/twiki/bin/view/Main/DistroSpecificReleaseTag
- new autocreate and autosievefolder patches

* Thu Jan 13 2005 Luca Olivetti <luca@olivetti.cjb.net> 2.2.10-2mdk
- drop last digit from release tag
- fetchnews man page moved to cyrus-imapd-nntp subpackage (conflict with
  leafnode, thanks to Marek Kruz.el <marek@good.solutions.net.pl>
- new version of autocreate patch
- removed last chunk from 64bit fixes patch (the fault was in the
  previous autocreate patch, not in cyrus proper)

* Wed Nov 24 2004 Luca Olivetti <luca@olivetti.cjb.net> 2.2.10-1mdk
- 2.2.10 (security fixes)
- removed failing hunk in 64-bit fixes patch, it shouldn't be necessary
  anymore

* Wed Oct 27 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.8-3mdk
- some 64-bit fixes
- stick to /usr/lib/cyrus-imapd as _cyrexecdir

* Sun Aug 29 2004 Luca Berra <bluca@vodka.it> 2.2.8-2.mdk
- rebuild with db-4.2

* Sat Jul 31 2004 Luca Olivetti <luca@olivetti.cjb.net> 2.2.8-1mdk
- 2.2.8

* Wed Jul 28 2004 Luca Olivetti <luca@olivetti.cjb.net> 2.2.7-1mdk
- 2.2.7
- new autocreate,autosievefolder,rmquota patches
- removed p100 (quota patches from cvs)
- removed p2 and p3 (man pages fixes, fixed upstream)
- patch9 (munge8bit) and patch17 (plaintext) no longer patch html manpage
  (it's less tiresome to regenerate them with groff)
- removed patch19 (masssievec, fixed upstream)
- cleanup

* Fri Jul 02 2004 Luca Olivetti <luca@olivetti.cjb.net> 2.2.6-2mdk
- new imapcreate.pl script
- added quota patches from cvs

* Thu Jun 24 2004 Luca Olivetti <luca@olivetti.cjb.net> 2.2.6-1mdk
- 2.2.6
- changed version detection defines (and now it builds under 10.0 again)
- new autocreate,autosievefolder,rmquota patches
- removed patch0 (mandir, fixed upstream)
- removed patch1 (cflags, fixed upstream)
- rediffed patch9 (munge8bit)
- removed patch16 (netsnmp, , upstream package already has net-snmp support)
- rediffed patch17 (disallow plaintext login with a command line switch)
- removed patch100 (fix list command for non personal namespaces, fixed
  upstream)
- added BuildRequires libelfutils-devel for net-snmp

* Fri Jun 18 2004 Luca Berra <bluca@vodka.it> 2.2.3-7mdk
- updated p15 and rebuilt against updated net-snmp
- add 10.1 to recognized versions

* Tue Apr 06 2004 Florin <florin@mandrakesoft.com> 2.2.3.6
- update to 2.2.3 (merge with the L. Olivetti's work)

