#!/usr/bin/perl

use strict;
use CGI;
require "/srv/http/drunkit/bin/common/modules.pl";

my $query = new CGI;
print $query->header(-charset=>"ISO-8859-15");

&printTemplate("top-template.html");

&printTemplate("404.html");

&printTemplate("bot-template.html");