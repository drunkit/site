#!/usr/bin/perl
use strict;
use CGI;
require "/srv/http/drunkit/bin/common/modules.pl";

my $query = new CGI;

my $startingPath = &getToDocumentRoot($ENV{SCRIPT_NAME});

if ($query->param('user')) {
	&doLogin($query->param('user'),$query->param('pass'));
}
else {
	&loginError();
}


sub doLogin {
	my $loginName = shift;
	my $loginPass = shift;
	$loginName = strtolower($loginName);
	my $startingPath = &getToDocumentRoot($ENV{SCRIPT_NAME});
	my $userFile = $startingPath."usr/".$loginName.".txt";
	my $password = getSetting($userFile,"Password");
	#print "Content-type: text/html\n\n";
	#print $userFile." = ".$loginPass;
	#exit;
	unless ($password) {
		&loginError("<b>No such Username:</b>","The username you have chosen does not exist. Please ensure you have typed it correctly");
	}
	else {
		my $pass = encrypt($loginPass);
		unless ($pass == $password) {
			&loginError("<b>Invalid Password:</b>","Please ensure you have typed your password correctly");
		}
		else {
			createLoginCache($loginName);
		}
	}
}

sub createLoginCache {
	my $userName = shift;
	my $loginFile = &randomHash;

	my $userString = $loginFile.":".$ENV{REMOTE_ADDR};

	my $startingPath = &getToDocumentRoot($ENV{SCRIPT_NAME});
	my $userFile = $startingPath."usr/cache/".$loginFile;

	my $redirect = $query->param("redirect");
	$redirect = "/" unless $query->param("redirect");

	writeSetting($userFile,"UserName",$userName);
	writeSetting($userFile,"IPCache",$ENV{REMOTE_ADDR});
if ($ENV{HTTP_USER_AGENT} =~ m/^Links/i) {

	my $cookie = $query->cookie(-name=>'userId',
                             -value=>$userString,
                             -expires=>'+1h',
                             -path=>'/');
	print $query->header(-cookie=>$cookie);

	print <<"	endCookie";
<html><head><title>Login Okay!</title></head><body><h1>Login Okay!</h1>Logged in okay! <a href="$redirect">Go back</a> to Drunkit.</body></html>
	endCookie

}
else {
	print <<"	endCookie";
Content-Type: text/html; charset=utf-8
Set-Cookie: userId=$userString; path=/; expires=Sun, 16-Dec-2020 21:08:33 GMT
Date: Tue, 17 Dec 2002 21:08:33 GMT
Location: $redirect



	endCookie
}
}

sub randomHash {
	my $lower = 1000000;
	my $upper = 9999999; 
	my $random = int(rand($upper-$lower+1)) + $lower; 
	$random = encrypt($random);
	return $random;
}

sub loginError {
	print "Content-type: text/html\n\n";
	my $loginError = shift;
	my $loginExplanation = shift;
	if ($loginError) {
		$loginError = "<span style=\"color: red\">".$loginError."</span> ".$loginExplanation."<p>";
	}
	

	my $skinDir = $startingPath."etc/themes/default/components/login/";
	print $query->header;
	&printTemplate("top-template.html");
	my $templateFile = $skinDir."LoginPrompt.html";
	print &parseTemplate($templateFile,"",-1,$loginError);
	&printTemplate("bot-template.html");
}


