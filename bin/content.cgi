#!/usr/bin/perl

use strict;
use CGI;

my $query = new CGI;

require "/srv/http/drunkit/bin/common/modules.pl";

my $startingPath = &getToDocumentRoot($ENV{SCRIPT_NAME});

print $query->header(-charset=>"utf-8");

&printTemplate("top-template.html");

my @scriptSlashCount = split(/\//,$ENV{SCRIPT_NAME});
my @uriSlashCount = split(/\//,$ENV{REQUEST_URI});
my %var;

for (my $i = ($#scriptSlashCount + 1); ($i <= $#uriSlashCount); $i++) {
	my ($key,$val) = split(/\,/,$uriSlashCount[$i]);
	$var{$key} = $val;
}

if ($var{'page'}) {
	my $path = $startingPath."/var/StaticPages/".$var{'page'}.".html";
	my @file = openFile($path);
	my $pathRoot = "/var/StaticPages";
	foreach my $line (@file) {
		$line =~ s/\[var pageOutParse=StaticPage\]/$pathRoot/gi;
		print $line;
	}
}
else {
	print "<h1>Offline</h1>Sorry, Drunkit is still in progress. This page has not yet been made.";
}

&printTemplate("bot-template.html");
