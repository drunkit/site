#!/usr/bin/perl
use strict;
use CGI;

my $query = new CGI;

print <<"end";
Set-Cookie: userId=; path=/; expires=Sun, 16-Dec-2001 21:25:51 GMT
Date: Tue, 17 Dec 2000 21:25:51 GMT
Content-Type: text/html; charset=ISO-8859-1
Location: $ENV{HTTP_REFERER}


end
