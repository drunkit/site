#!/usr/bin/perl
require "/srv/http/drunkit/bin/common/modules.pl";
use CGI;

print `ls`;

$query = new CGI;
print $query->header();

foreach my $env (keys %ENV) {
	print "\t".$env." = ".$ENV{$env}."<br />\n";
}
