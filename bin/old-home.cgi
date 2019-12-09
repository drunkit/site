#!/usr/bin/perl

use CGI;
use strict;
require "/srv/http/drunkit/bin/common/modules.pl";

my $query = new CGI;

my $time = time;

print $query->header();


&printTemplate("top-template.html");



my @quotes = &openFile("../home/quotes.txt");
my $random = int(rand($#quotes + 1));

my $output;
if (&getUserName) {
	$output = &parseTemplate("../home/homeLoggedIn.html","",-1);
}
else {
	$output = &parseTemplate("../home/homeLoggedOut.html","",-1);
}

my $totalMessages = &getSetting("../etc/settings/MessageBoard/settings.txt","messageCount");

my $unreadMessages = &getUserSetting("messageBoardView");

if (($unreadMessages > $totalMessages) || (!$unreadMessages)) {
	&writeUserSetting("messageBoardView",$totalMessages);
}

my $plural = "s";

my $actualUnread = ($totalMessages - $unreadMessages);

if ($actualUnread == 1) { $plural = ""; }

if ($actualUnread == 0) {
	$output =~ s/\[ONLYUNREADMESSAGES(.*?)ENDONLYUNREADMESSAGES\]//gi; 
}
else {
	$output =~ s/\[ONLYUNREADMESSAGES(.*?)ENDONLYUNREADMESSAGES\]/$1/gi; 
}

$actualUnread = "no" if ($actualUnread == 0);

$output =~ s/\[MESSAGES\]/$actualUnread/gi;

$output =~ s/\[PLURALMESSAGES\]/$plural/gi;

my $unreadArticles = &getUserSetting("articleView");

my $articleSettingsFile = "../etc/settings/Articles/Articles.txt";
my $numberOfArticles = &getSetting($articleSettingsFile,"NumberOfArticles");

if (($unreadArticles > $numberOfArticles) || (!$unreadArticles)) {
	&writeUserSetting("articleView",$numberOfArticles);
}

$actualUnread = ($numberOfArticles - $unreadArticles);

if ($actualUnread == 0) {
	$output =~ s/\[ONLYUNREADARTICLES(.*?)ENDONLYUNREADARTICLES\]//gi; 
}
else {
	$output =~ s/\[ONLYUNREADARTICLES(.*?)ENDONLYUNREADARTICLES\]/$1/gi; 
}

$plural = "s";


$output =~ s/\[QUOTE\]/$quotes[$random]/gi;

if ($actualUnread == 1) { $plural = ""; }

$actualUnread = "no" if ($actualUnread == 0);

$output =~ s/\[ARTICLES\]/$actualUnread/gi;

$output =~ s/\[PLURALARTICLES\]/$plural/gi;

my @announcements = &openFile("../var/Announcements/Announcements.txt");

$output =~ s/\[ANNOUNCEMENTS\]/$announcements[0]/gi;

if (&getUserSetting("UserLevel") == 3) {
	$output =~ s/\[ADMINISTRATORONLY\](.*?)\[ENDADMINISTRATORONLY\]/$1/gi;
}
else {
	$output =~ s/\[ADMINISTRATORONLY\](.*?)\[ENDADMINISTRATORONLY\]//gi;
}


print $output;

&printTemplate("bot-template.html");

my $time2 = time;
$time = $time2 - $time;