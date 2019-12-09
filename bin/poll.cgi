#!/usr/bin/perl
use CGI;
use strict;

require "/srv/http/drunkit/bin/common/modules.pl";

my $startingPath = &getToDocumentRoot($ENV{SCRIPT_NAME});
my $pollSettingsFile = $startingPath."etc/settings/Poll/pollSettings.txt";
my $thisPollNumber = &getSetting($pollSettingsFile,"PollNumber");
my $thisPollFileName = $startingPath."var/Poll/".$thisPollNumber.".txt";
my %thisPoll = &getSettingHash($thisPollFileName);
my %userHash = &getUserSettingHash();
my $userName = &getUserName();

my $themeDir;

if ($userName) {
	my $userTheme = getUserSetting("Template");
	$themeDir = $startingPath."etc/themes/".$userTheme."/";
}
else {
	$themeDir = $startingPath."etc/themes/default/";
}

my $query = new CGI;

if (($query->param('viewResults') || ($query->param('a') eq 'view'))) {
	&viewResults;
}
elsif ($query->param('a') eq 'vote') {
	print $query->header(-charset=>"ISO-8859-15");
	&printTemplate("top-template.html");
	&vote($query->param('option'));
	&printTemplate("bot-template.html");
}
else {
	&viewResults;
}


sub vote {
	&promptLogin unless &getUserName;
	if (&getUserSetting("PollVote") == $thisPollNumber) {
		&error("You have already voted on this poll!");
	}
	my $voteString = "answer".$query->param('option');
	$thisPoll{$voteString}++;
	&writeSetting($thisPollFileName,$voteString,$thisPoll{$voteString});
	&writeUserSetting("PollVote",$thisPollNumber);
	&writeUserSetting("PollVoted".$thisPollNumber,$query->param('option'));
	print &parsePollTemplate("voteThanks.html",$thisPollNumber);
}

sub viewResults {
	
	if ($query->param("id")) {
		print "Location: https://drunkit.co.uk/php/pollspy?id=".$query->param("id")."\n\n";
	}
	else {
		print "Location: https://drunkit.co.uk/php/pollspy?id=latest\n\n";
	}
	my @pollResultsArray;
	my @pollLabelArray;
	my $totalResults = 0;
	my $resultsOutput;
	if ($query->param("id")) {
		$thisPollNumber	= $query->param("id");
		$thisPollFileName = $startingPath."var/Poll/".$thisPollNumber.".txt";
		%thisPoll = &getSettingHash($thisPollFileName);
	}
	for (my $thisPollResult = 1; $thisPollResult; $thisPollResult++) {
		if ($thisPoll{$thisPollResult}) {
			my $answersLabel = "answer".$thisPollResult;
			$thisPoll{$answersLabel} = 0 unless ($thisPoll{$answersLabel});
			$totalResults += $thisPoll{$answersLabel};
			push(@pollResultsArray,$thisPoll{$answersLabel});
			push(@pollLabelArray,$thisPoll{$thisPollResult});
		}
		else {
			last;
		}
	}

	for (my $sofar = 0; $sofar <= $#pollLabelArray; $sofar++) {
		my $percent;
		if ($totalResults > 0) {
			$percent = int((($pollResultsArray[$sofar] / $totalResults) * 100));
		}
		else {
			$percent = 0;
		}
		my %resultsLineHash;
		$resultsLineHash{label} = $pollLabelArray[$sofar];
		$resultsLineHash{votes} = "$pollResultsArray[$sofar]";
		$resultsLineHash{percent} = $percent;
		$resultsLineHash{doublePercent} = $percent * 2;
		my $tempParse = &parsePollTemplate("PollLargeResultResultLine.html",$thisPollNumber);
		$tempParse =~ s/\[var result=(.*?)\]/$resultsLineHash{$1}/gi;
		$resultsOutput .= $tempParse;

	}
	my $printOut = &parsePollTemplate("pollLargeResult.html",$thisPollNumber);
	$printOut =~ s/\[poll results=results\]/$resultsOutput/gi;
	$printOut =~ s/\[poll results=total\]/$totalResults/gi;
	$printOut =~ s/\[var info=themeDir\]/$themeDir/gi;
	print $printOut;
}
