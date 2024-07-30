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

Summary:	A high-performance mail store with IMAP and POP3 support
Name:		cyrus-imapd
Version:	3.8.4
Release:	1
License:	OSI Approved
Group:		System/Servers
Url:		http://cyrusimap.org/
Source0:	https://github.com/cyrusimap/cyrus-imapd/releases/download/cyrus-imapd-%{version}/cyrus-imapd-%{version}.tar.gz
Source1:	https://github.com/cyrusimap/cyrus-imapd/releases/download/cyrus-imapd-%{version}/cyrus-imapd-%{version}.tar.gz.sig
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
# cyrus-master instead of master in syslog
Patch2:		cyrus-imapd-logident.patch
# Create on demand folder requested by sieve filter (http://email.uoa.gr/projects/cyrus/autosievefolder/)
#Patch4:	http://email.uoa.gr/download/cyrus/cyrus-imapd-2.3.16/cyrus-imapd-2.3.16-autosieve-0.6.0.diff
Patch4:		cyrus-imapd-2.4.13-autosieve-0.6.0.diff
# Remove QUOTA patch (http://email.uoa.gr/projects/cyrus/quota-patches/rmquota/)
Patch5:		http://email.uoa.gr/download/cyrus/cyrus-imapd-2.3.9/cyrus-imapd-2.3.9-rmquota-0.5-0.diff
Patch6:		cyrus-imapd-3.8.4-sqlite-OMIT_DEPRECATED.patch
Patch7:		cyrus-imapd-3.8.4-no-Lusrlib.patch
# Other patches from simon matter
Patch19:	cyrus-imapd-2.3.11-mkimap.patch
Requires:	perl
# with previous versions of sasl, imap LOGIN would fail
Requires:	%{mklibname sasl 2} >= 2.1.15
#Requires:	krb5-libs
Requires(pre):	rpm-helper
Requires(post):	openssl perl
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
BuildRequires:	pkgconfig(jansson)
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	pkgconfig(icu-uc)
BuildRequires:	pkgconfig(libical)
BuildRequires:	pkgconfig(libcap)
BuildRequires:	perl-devel
BuildRequires:	perl-Digest-SHA1
BuildRequires:	wrap-devel
BuildRequires:	slibtool
%if %{with_snmp}
BuildRequires:	net-snmp-devel
BuildRequires:  pkgconfig(libelf)
Requires:	net-snmp-mibs
%endif
%if %{with_ldap}
BuildRequires:	pkgconfig(ldap)
%else
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
%define		_confdir doc/examples/cyrus_conf
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
%patch 2 -p1 -b .p1~
%if %{build_autosieve}
%patch 4 -p1 -b .autosieve.orig
%endif
%if %{build_rmquota}
%patch 5 -p1 -b .rmquota.orig <- this patch is broken and won't apply
%endif
%patch 6 -p1 -b .p6~
%patch 7 -p1 -b .p7~

%patch 19 -p1 -b .mkimap.orig

## Extra documentation
mkdir -p extradocs
for i in %{SOURCE2} %{SOURCE4} %{SOURCE19} ; do
  cp $i extradocs
done 

## regenerate html man pages
pushd man
    for mp in *[1-8] ; do groff -m man -T html $mp > ../doc/html/$mp.html ; done
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
export LIBTOOL=slibtool
slibtoolize --copy --force; aclocal -I cmulocal; autoheader; autoconf

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
#    --with-krb=%{_prefix}/kerberos \

for i in annotator imap; do
	cd perl/$i
	perl Makefile.PL INSTALLDIRS=vendor
	cd ../..
done

# no parallel make - 2.3.10
make

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

%{__install} -m 755 imtest/imtest	%{buildroot}%{_libexecdir}/
%{__install} -m 755 perl/imap/cyradm	%{buildroot}%{_libexecdir}/

# Install tools
for tool in dohash masssievec mkimap mknewsgroups rehash translatesieve undohash  upgradesieve ; do
    test -f tools/${tool} && %{__install} -m 755 tools/${tool} %{buildroot}%{_libexecdir}/
done
%{__install} -m 755 %{SOURCE13} %{buildroot}%{_libexecdir}/imapcreate

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
%{__install} -m 755 %{SOURCE15} %{buildroot}%{_libexecdir}/cvt_cyrusdb_all

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
%{__install} -m 755 %{SOURCE23} %{buildroot}%{_libexecdir}/cyr_systemd_helper

%if %{with_snmp}
# Install snmp mibs
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
mv -f %{buildroot}%{_libexecdir}/master	%{buildroot}%{_libexecdir}/cyrus-master
mv -f %{buildroot}%{_mandir}/man8/master.8 %{buildroot}%{_mandir}/man8/cyrus-master.8
cp -af doc/html/master.8.html doc/html/cyrus-master.8.html

# Create symlinks
ln -sf ../lib/cyrus-imapd/cyradm %{buildroot}%{_bindir}/
ln -sf ../lib/cyrus-imapd/imtest %{buildroot}%{_bindir}/
ln -sf ../lib/cyrus-imapd/imapcreate %{buildroot}%{_bindir}/

# provide the cyrusMaster.conf file, discovered by doing:
# /usr/lib/cyrus-imapd/cyrus-master -p /var/run/cyrus-master.pid -D
%if %{with_snmp}
install -d %{buildroot}/var/lib/net-snmp
echo "# placeholder" > %{buildroot}/var/lib/net-snmp/cyrusMaster.conf
%endif

# cleanup
find %{buildroot}%{perl_vendorarch} -name "*.orig" | xargs rm -f

mkdir -p %{buildroot}%{_sysusersdir}
cat >%{buildroot}%{_sysusersdir}/%{name}.conf <<EOF
%if %{SASLGROUP}
g %{_saslgroup} - -
%endif
g %{_cyrusgroup} - -
u %{_cyrususer} "Cyrus IMAP Server" %{_vardata} %{_bindir}/bash
%if %{SASLGROUP}
m %{_saslgroup} %{_cyrususer}
%endif
EOF

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

%preun
if [ $1 = 0 ]; then
    # Package removal, not upgrade
    /bin/systemctl disable cyrus-imapd.service >/dev/null 2>&1 || :
    /bin/systemctl stop cyrus-imapd.service > /dev/null 2>&1 || :
    rm -f %{_vardata}/socket/lmtp 2> /dev/null
    rm -f %{_vardata}/rpm/version 2> /dev/null
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart cyrus-imapd.service >/dev/null 2>&1 || :
fi

%files
%{_sysusersdir}/%{name}.conf
%doc doc/* extradocs/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/*.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0644,root,root) %config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/pop
%attr(0644,root,root) %config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/imap
%attr(0644,root,root) %config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/sieve
%attr(0644,root,root) %config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/lmtp
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/cron.daily/%{name}
/lib/systemd/system/cyrus-imapd.service
%attr(0755,root,root) %dir %{_libexecdir}
%attr(0755,root,root) %{_libexecdir}/cyr_systemd_helper
%attr(0755,root,root) %{_libexecdir}/cyrus-master
%attr(0755,root,root) %{_libexecdir}/fud
%attr(0755,root,root) %{_libexecdir}/imapd
%attr(0755,root,root) %{_libexecdir}/lmtpd
%attr(0755,root,root) %{_libexecdir}/masssievec
%attr(0755,root,root) %{_libexecdir}/mkimap
%attr(0755,root,root) %{_libexecdir}/mknewsgroups
%attr(0755,root,root) %{_libexecdir}/notifyd
%attr(0755,root,root) %{_libexecdir}/pop3d
%attr(0755,root,root) %{_libexecdir}/rehash
%attr(0755,root,root) %{_libexecdir}/timsieved
%attr(0755,root,root) %{_libexecdir}/translatesieve
%{_libexecdir}/cvt_cyrusdb_all
%{_libexecdir}/promstatsd
%if %{with_ldap}
%attr(0755,root,root) %{_libexecdir}/ptloader
%endif
%attr(0755,root,root) %{_libexecdir}/smmapd
%if %{IDLED}
%attr(0755,root,root) %{_libexecdir}/idled
%endif
%{_libdir}/libcyrus.so.*
%{_libdir}/libcyrus_imap.so.*
%{_libdir}/libcyrus_min.so.*
%{_libdir}/libcyrus_sieve.so.*
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
%attr(0644,root,root) %{_mandir}/man8/smmapd.8*
%attr(0644,root,root) %{_mandir}/man8/squatter.8*
%attr(0644,root,root) %{_mandir}/man8/timsieved.8*
%attr(0644,root,root) %{_mandir}/man8/tls_prune.8*
%attr(0644,root,root) %{_mandir}/man8/unexpunge.8*
%{_mandir}/man8/backupd.8*
%{_mandir}/man8/ctl_backups.8*
%{_mandir}/man8/ctl_conversationsdb.8*
%{_mandir}/man8/cvt_xlist_specialuse.8*
%{_mandir}/man8/cyr_backup.8*
%{_mandir}/man8/cyr_buildinfo.8*
%{_mandir}/man8/cyr_deny.8*
%{_mandir}/man8/cyr_info.8*
%{_mandir}/man8/cyr_ls.8*
%{_mandir}/man8/cyr_userseen.8*
%{_mandir}/man8/cyr_virusscan.8*
%{_mandir}/man8/cyradm.8*
%{_mandir}/man8/cyrdump.8*
%{_mandir}/man8/lmtpproxyd.8*
%{_mandir}/man8/mbtool.8*
%{_mandir}/man8/mupdate.8*
%{_mandir}/man8/pop3proxyd.8*
%{_mandir}/man8/promstatsd.8*
%{_mandir}/man8/proxyd.8*
%{_mandir}/man8/ptdump.8*
%{_mandir}/man8/ptexpire.8*
%{_mandir}/man8/ptloader.8*
%{_mandir}/man8/relocate_by_id.8*
%{_mandir}/man8/restore.8*
%{_mandir}/man8/sievec.8*
%{_mandir}/man8/sieved.8*
%doc README.RPM

%files murder
%config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/mupdate
%config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/csync
%attr(0755,root,root) %{_libexecdir}/lmtpproxyd
%attr(0755,root,root) %{_libexecdir}/mupdate
%attr(0755,root,root) %{_libexecdir}/pop3proxyd
%attr(0755,root,root) %{_libexecdir}/proxyd

%files nntp
%config(noreplace) %verify(not size,not md5) %{_sysconfdir}/pam.d/nntp
%attr(0755,root,root) %{_libexecdir}/nntpd
%attr(0644,root,root) %{_mandir}/man8/nntpd.8*
%attr(0644,root,root) %{_mandir}/man8/fetchnews.8*

%files devel
%{_includedir}/cyrus
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%attr(0644,root,root) %{_mandir}/man3/imclient.3*

%files -n perl-Cyrus
%doc perl/imap/README perl/imap/Changes perl/imap/examples
%{perl_vendorarch}/auto/Cyrus
%{perl_vendorarch}/Cyrus
%{_datadir}/perl5/vendor_perl/Cyrus
%{_libdir}/perl5/Cyrus
%{_libdir}/perl5/auto/Cyrus
%attr(0644,root,root) %{_mandir}/man3/Cyrus*

%files utils
%attr(0755,root,root) %{_libexecdir}/cyradm
%attr(0755,root,root) %{_libexecdir}/imtest
%attr(0755,root,root) %{_libexecdir}/imapcreate
%attr(0755,root,root) %{_bindir}/*
%attr(0644,root,root) %{_mandir}/man1/*
