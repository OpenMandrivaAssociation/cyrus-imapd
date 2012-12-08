#!/usr/bin/perl -w
# 
# imapcreate: create IMAP mailboxes with quotas
#			 Reads user names from standard input.
# launch without argument for a short help.
#
# originally found on http://cyrus-utils.sourceforge.net
# (could not find any copyright info, thought)
# 
# enhanced by Clément "nodens" Hermann <clement.hermann@free.fr>
#
# I'd like to consider this as GPL'd (cf www.gnu.org), but won't add any copyright without the original author's consent.
# 

use Getopt::Long;
use Cyrus::IMAP::Admin;
use strict;


my $debug;
my $user;
my $pass;
my $quota;
my @part;
my $useunixhierarchy;
my @mailboxes;
my $delete;
my $cyrus;

sub usage {
  print <<EOU;
imapcreate - create IMAP mailboxes with quotas
  usage:
	imapcreate [-d] [-u user] [-p pass] [-m mailbox1[,mailbox2][,mailbox<n>]] 
	[-q quota] [-t partition:list] [-s] [-v] <server>

Options:
   -t : the partition to use. Default to the \"default\" partition
   -q ; the quota, if a quota is needed. It is normally in KiloBytes, but you can use m,M,g or G suffix to use MB or GB instead, e.g 10k, 2048M or 100g
   -m : a comma-separated mailbox list
   -u : your cyrus admin user (usually cyrus or cyradm)
   -p : your cyrus admin password (if not provided, it will be asked for)
   -s : use the unix hierarchy separator (see imapd.conf(1))
   -d : delete mailboxes instead of creating them
   -v : run in debug mode, and print information on stdout

If no password is submitted with -p, we'll prompt for one.
if no mailbox name is specified with -m, read user names from standard input

  examples: 
	imapcreate -u cyradm -m foo,bar,joe -q 50000 -t p1:p2 mail.testing.umanitoba.ca
	cat list.txt | imapcreate -u cyradm -p 'cyruspass' -q 50M mail.testing.umanitoba.ca
EOU
  exit 1;
}

# Create a mailbox... usage : &CreateMailBox(user,partition[,quota]).
# You have to be authentified already. We use "$cyrus" as the connection name.
# partition can be 'default'
sub CreateMailBox {
	my $mbuser = $_[0];
	my $mbpart = $_[1];
	my $mbquota = $_[2];
	
	print "Creating $mbuser on $mbpart\n" if $debug;
	if ($mbpart eq 'default') {
	$cyrus->createmailbox($mbuser);
	}
	else {
	$cyrus->createmailbox($mbuser, $mbpart);
	}
	warn $cyrus->error if $cyrus->error;
	
	# Set the quota
	if ($mbquota) {
	print "Setting quota for $mbuser to $mbquota\n" if $debug;
	$cyrus->setquota($mbuser, 'STORAGE', $mbquota);
	warn $cyrus->error if $cyrus->error;
	}
}

# Delete a mailbox. Usage: $DeleteMailBox($user)
# Assuming we use $user as the admin.
sub DeleteMailBox {
	my $mbuser = $_[0];
	my $delacl = "c";
	
	print "Deleting $mbuser\n" if $debug;
	$cyrus->setaclmailbox($mbuser, $user, $delacl);
	$cyrus->deletemailbox($mbuser);
	warn $cyrus->error if $cyrus->error;
}

GetOptions("d|delete" => \$delete, "u|user=s" => \$user, "p|pass=s" => \$pass, "m|mailboxes=s" => \@mailboxes, "q|quota=s" => \$quota,
   "t|part=s" => \@part, "s|UnixHierarchy" => \$useunixhierarchy, "v|verbose" => \$debug );
@part = split(/:/, join(':', @part));
push @part, 'default' unless @part;
my $pn = 0;
@mailboxes = split(/,/, join(',', @mailboxes));

my $server = shift(@ARGV) if (@ARGV);
usage unless $server;

# quotas formatting:
if ($quota) {
	if ($quota =~ /^(\d+)([mk]?)$/i) {
		my $numb = $1;
		my $letter = $2;
		if ($letter =~ /^m$/i) {
			$quota = $numb * 1024;
			print "debug: quota=$quota\n" if $debug;
		} elsif ($letter =~ /^k$/i) {
			$quota = $numb;
			print "debug: quota=$quota\n" if $debug;
		} else {
			die "malformed quota: $quota (must be at least one digit eventually followed by m, M, k or K\n";
#			$quota = $numb;
#			print "debug: quota=$quota\n" if $debug;
		}
	} else {
		die "malformed quota: $quota (must be at least one digit eventually followed by m, M, k or K\n";
	}
}

# Authenticate
$cyrus = Cyrus::IMAP::Admin->new($server);
$cyrus->authenticate(-mechanism => 'login', -user => $user,
	 -password => $pass);
die $cyrus->error if $cyrus->error;

# if there isn't any mailbox defined yet, get them from standard input
if (! (defined $mailboxes[0])) { 
	# For all users
	while (<>) {
		chomp;
		my $mbox = $_;
		push @mailboxes, $mbox;
	}
}

# create/delete mailboxes for each user
foreach my $mailbox (@mailboxes) {
	if ($useunixhierarchy) {
	$mailbox = 'user/' . $mailbox;
	} else {
	$mailbox = 'user.' . $mailbox;
	}

	if ($delete) {
		&DeleteMailBox($mailbox)
	} else {
		# Select the partition
		my $pt = $part[$pn];
		$pn += 1;
		$pn = 0 unless $pn < @part;
		&CreateMailBox($mailbox,$pt,$quota)
	}
}

