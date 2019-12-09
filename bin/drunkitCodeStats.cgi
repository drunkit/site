#!/usr/bin/perl

use CGI;
use strict;
require "/srv/http/drunkit/bin/common/modules.pl";

my $query = new CGI;

print $query->header();

printTemplate("top-template.html");

open(FILE,"common/modules.pl");
	my @modulesFile = <FILE>;
close(FILE);

my $totalLines;

print <<"eof";

<h1>Drunkit Code Statistics</h1>
<p style="margin: 0px">Drunkit has lots of lines of code running behind it. Just out of interest really, this programme tells you how many lines there are at the moment...</p>

<h2 style="margin-top: 20px">modules.pl</h2>
<p style="margin: 0px"><b>Type</b>: Library<br>
<b>Lines of code</b>: $#modulesFile</p>
eof


opendir(DIR,"./");
my @dir = readdir(DIR);
closedir(DIR);

foreach my $file (@dir) {
	unless (($file eq "..") || ($file eq ".") || ($file eq "common")) {
		my $lines = &getLines($file);
		$totalLines = $lines + $totalLines;
		print <<"		eof";
			<h2 style="margin-top: 20px">$file</h2>
			<p style="margin: 0px"><b>Type</b>: Page<br>
			<b>Lines of code</b>: $lines</p>
		eof
	}
}

		print <<"		eof";
			<h2 style="margin-top: 20px">Total Lines</h2>
			<b>Lines of code</b>: $totalLines</p><br><br><br>
		eof

printTemplate("bot-template.html");


sub getLines {
	my $file = shift;
	open(FILE,$file);
	my @file = <FILE>;
	close(FILE);
	return $#file;
}