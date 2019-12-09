#!/usr/bin/perl

require "/srv/http/drunkit/bin/common/modules.pl";

use CGI;
use strict;

my $query = new CGI;

my $themeDir = "../etc/themes/html32/";

print $query->header(-charset=>"utf8");

&printTemplate("../../html32/html/top-template.html");

print "<h1>This is shitty Netscape!</h1>";

print <<"eof";
	<p>Yes, this is it... shitty netscape to ruin the day. I hope this validates to HTML 4 or 3.</p>

eof

&printTemplate("../../html32/html/bot-template.html");