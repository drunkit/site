#!/usr/bin/perl

use CGI;
use strict;

require "/srv/http/drunkit/bin/common/modules.pl";

my $query = new CGI;

my $fileName = $query->param("file");

my @typeOfFile = split(/\./,$fileName);

my $typeOfFile = $typeOfFile[$#typeOfFile];



my $content = "text/html";

if ($typeOfFile eq "gif") { $content = "image/gif"; }
elsif ($typeOfFile eq "jpg") { $content = "image/jpeg"; }
elsif ($typeOfFile eq "jpeg") { $content = "image/jpeg"; }
elsif ($typeOfFile eq "css") { $content = "text/css"; }
elsif ($typeOfFile eq "js") { $content = "text/javascript"; }
elsif ($typeOfFile eq "txt") { $content = "text/plain"; }
elsif ($typeOfFile eq "png") { $content = "image/png"; }

my $startingPath = &getToDocumentRoot($ENV{SCRIPT_NAME});
my $themeDir = $startingPath."etc/themes/".&getThemeName."/";

my $fileName = $themeDir."html/".$fileName;

open (THEMEFILE,$fileName);
	binmode THEMEFILE;
	my @file = <THEMEFILE>;
close(THEMEFILE);

if (@file) {
	print $query->header(-type=>$content);
	print @file;
}
else {
	print $query->header(-type=>"text/html",-status=>'404 Not Found');
}