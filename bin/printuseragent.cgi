use CGI;
$query = new CGI;

print $query->header();

print "$ENV{HTTP_USER_AGENT}";