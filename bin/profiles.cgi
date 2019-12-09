#!/usr/bin/perl

use CGI;
use strict;
require "/srv/http/drunkit/bin/common/modules.pl";

my $query = new CGI;

my $userName = $query->param("user");
$userName = $query->param("usr") unless $userName;
my $startingPath = &getToDocumentRoot($ENV{SCRIPT_NAME});
my $skinDir = $startingPath."etc/themes/default/components/Profiles/";

print $query->header(-charset=>"ISO-8859-15");

&printTemplate("top-template.html");

&error("No username") unless $userName;

my $userFile = $startingPath."/usr/".$userName.".txt";

my $bufferOut = &parseTemplate($skinDir."profile.html",$userFile,-1);

$bufferOut =~ s/\[var profileInfo=UserName\]/$userName/gi;

print $bufferOut;



&printTemplate("bot-template.html");