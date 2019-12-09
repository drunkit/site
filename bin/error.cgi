#!/usr/bin/perl
use CGI;

use strict;

my $query = new CGI;

print $query->header();


    my $error = $query->cgi_error;
    if ($error) {
        print $query->header(-status=>$error),
              $query->start_html('Problems'),
              $query->h2('Request not processed'),
              $query->strong($error);
    }

print $cool;