#!/usr/bin/perl

use CGI;
use strict;

require "/srv/http/drunkit/bin/common/modules.pl";

my $query = new CGI;

my $startingPath = &getToDocumentRoot();
my $articleDir = $startingPath."var/Articles/";
my $skinDir = $startingPath."etc/themes/default/components/Articles/";


my @scriptSlashCount = split(/\//,$ENV{SCRIPT_NAME});
my @uriSlashCount = split(/\//,$ENV{REQUEST_URI});
my %var;

for (my $i = ($#scriptSlashCount + 1); ($i <= $#uriSlashCount); $i++) {
	my ($key,$val) = split(/\,/,$uriSlashCount[$i]);
	$var{$key} = $val;
}

unless (($var{id} eq "all") || ($var{id} eq "")) {
    print $query->header(-charset=>"utf-8");
	&printTemplate("top-template.html");
	&showArticle($var{id});
	&printTemplate("bot-template.html");
}
else {
	print "Location: https://drunkit.co.uk/bin/articles\n\n\n\n\n\n";
}


sub showArticle {
	my $articleId = shift;
	my $templateFile = $skinDir."viewArticle.html";
	my $articleFile = $articleDir.$articleId.".txt";
	my $parseInfo = &parseTemplate($templateFile,$articleFile,$articleId);

	my $comments = &getComments($articleFile);

	if (&getUserSetting("articleView") < $articleId) {
		&writeUserSetting("articleView",$articleId);
	}

	$parseInfo =~ s/\[insertComments\]/$comments/gi;

	print $parseInfo;
}


sub getComments {
	my $articleFile = shift;
	my $returnBuffer;
	my @comments = split(/\;/,&getSetting($articleFile,"comments"));
	foreach my $comment (@comments) {
		my ($userName,$userComment) = split(/:/,$comment);
		$userName = strtolower($userName);
		if ($userComment) {
			my $lineBuffer;
			my @commentLine = openFile($skinDir."CommentLine.html");
			my %userHash = &getUserSettingHash($userName);
			$userComment = &formatTableHtml(&escapeFromHex($userComment));
			foreach my $line (@commentLine) {
				$line =~ s/\[username\]/$userName/gi;
				$line =~ s/\[comment\]/$userComment/gi;
				$line =~ s/\[var user=(.*?)\]/$userHash{strtolower($1)}/gi;
				$lineBuffer .= $line;
			}
			$returnBuffer = $lineBuffer.$returnBuffer;
		}

	}
	return $returnBuffer;
}

sub getCommentTemplate {
	my $userName = shift;
	my $comment = shift;
}
