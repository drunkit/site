#!/usr/bin/perl

use CGI;
use strict;

my $query = new CGI;

my $parseMode;

if ($query->param("source") =~ m/(.*?).js/gi) {
	$parseMode = "javascript";
}
elsif ($query->param("source") =~ m/((.*?).cgi|(.*?).pl)/gi) {
	$parseMode = "perl";
}
elsif ($query->param("source") =~ m/(.*?).html?/gi) {
	$parseMode = "html";
}
else {
	$parseMode = "perl";
}

open(FILE,$query->param("source"));
	my @filecontents = <FILE>;
close(FILE);

print "Content-Type: text/html\n\n";

print "<title>Source code for ".$query->param("source")."</title><body><font family=\"courier new\"><span style=\"font-family: monospace; font-size: 10pt\">";

foreach my $line (@filecontents) {
	print &parseCode($parseMode,$line);
}


sub parseCode {
	my $parseMode = shift;
	my $line = shift;


	$line =~ s/&/&amp;/gi;
	$line =~ s/</&lt;/gi;
	$line =~ s/>/&gt;/gi;
	$line =~ s/\t/&nbsp;&nbsp;&nbsp;&nbsp;/gi;
	$line =~ s/  /&nbsp;&nbsp;/gi;


	if ($parseMode eq 'javascript') {
		$line = &highlightJavaScript($line);
	}
	if ($parseMode eq 'perl') {
		$line = &highlightPerl($line);
	}
	if ($parseMode eq 'html') {
		$line = &highlightHtml($line);
	}

	print "$line<br>";

	return;
}




sub highlightJavaScript {
	my $line = shift;

	if ($line =~ m/\/\*/g) {
		$line = "<span style=\"color: green\">$line";		
	}
	elsif ($line =~ m/\/\//gi) {
		$line = "<span style=\"color: green\">$line</span>";
	}
	elsif ($line =~ m/\*\//g) {
		$line = "$line</span>";
	}
	else {
		$line =~ s/function/<span style=\"color\: blue\">function<\/span>/g;
		$line =~ s/return/<span style=\"color\: blue\">return<\/span>/g;
		$line =~ s/if/<span style=\"color\: blue\">if<\/span>/g;
		$line =~ s/alert/<span style=\"color\: blue\">alert<\/span>/g;
		$line =~ s/else/<span style=\"color\: blue\">else<\/span>/g;
	}

	return $line;
}

sub highlightHtml {
	my $line = shift;

	my $commentline = "";

	$line =~ s/=/&PROP_EQUALS/gi;
	
	$line =~ s/&lt;!--/<span style="color: green">&lt!--/gi;
	$line =~ s/--&gt;/--&uiut;<\/span>/gi;

	
	$line =~ s/&lt;(.*?)(\s|&gt;)/&lt;<span style="color: brown">$1<\/span>$2/gi;

	$line =~ s/(.*?)\&PROP_EQUALS(.*?)(\s|&gt;)/<span style="color: red">$1<\/span><span style="color: blue">=$2<\/span>$3/gi;
	
	$line =~ s/&lt;/<span style="color: blue">&lt;<\/span>/gi;
	$line =~ s/&gt;/<span style="color: blue">&gt;<\/span>/gi;

	$line =~ s/--&uiut;/--&gt;/gi;

	$line = $line . $commentline;

	return $line;
}

sub highlightPerl {
	my $line = shift;
	my $commentline = "";
	if ($line =~ m/(^|\s|\t|;)#/gi) {
		($line,$commentline) = split(/#/,$line);
		$commentline = "<span style=\"color: green\">#$commentline</span>";
	}
	else {
		$commentline = "";
	}


#	$line =~ s/"/<span style="color\: orange">"<\/span>/g;
#	$line =~ s/'/<span style="color\: orange">'<\/span>/g;
	$line =~ s/(\$|@|%)(.*?)(;|\/)?(\/|&|\\|\s|{|}|\)|\(|=|\?|"|\\)/\<span style="color: olive">$1$2<\/span>$3$4/gi;
	$line =~ s/open(\s|\()/<span style=\"color\: blue\">open<\/span>$1/g;
	$line =~ s/\\<span style="color: orange">"<\/span>/\\"/g;
	$line =~ s/eval(\s|\()/<span style=\"color\: blue\">eval<\/span>$1/g;
	$line =~ s/readdir(\s|\()/<span style=\"color\: blue\">readdir<\/span>$1/g;
	$line =~ s/return(\s|;)/<span style=\"color\: blue\">return<\/span>$1/g;
	$line =~ s/shift(\s|;)/<span style=\"color\: blue\">shift<\/span>$1/g;
	$line =~ s/die(\s|;)/<span style=\"color\: blue\">die<\/span>$1/g;
#		$line =~ s/pack(\s|;|\()/<span style=\"color\: blue\">pack<\/span>$1/g;
	$line =~ s/use(\s|;)/<span style=\"color\: blue\">use<\/span>$1/g;
	$line =~ s/(^|\s|;)our(\s)/<span style=\"color\: blue\">our<\/span>$2/g;
	$line =~ s/opendir(\s|\()/<span style="color: blue">opendir<\/span>$1/g;
	$line =~ s/closedir(\s|\()/<span style="color: blue">closedir<\/span>$1/g;
	$line =~ s/require(\s|\()/<span style=\"color\: blue\">require<\/span>$1/g;
	$line =~ s/print(\s|\()/<span style=\"color\: blue\">print<\/span>$1/g;
	$line =~ s/sub(\s|\()/<span style=\"color\: blue\">sub<\/span>$1/g;
	$line =~ s/read(\s|\()/<span style=\"color\: blue\">read<\/span>$1/g;
	$line =~ s/my(\s)/<span style=\"color\: blue\">my<\/span>$1/g;
	$line =~ s/foreach(\s|\()/<span style=\"color\: blue\">foreach<\/span>$1/g;
	$line =~ s/split(\(|\s)/<span style=\"color\: blue\">split<\/span>$1/g;
	$line =~ s/elsif(\s|\()/<span style=\"color\: blue\">elsif<\/span>$1/g;
	$line =~ s/eq(\s)/<span style=\"color\: orange\">eq<\/span>$1/g;
	$line =~ s/if(\(|\s)/<span style=\"color\: blue\">if<\/span>$1/g;
	$line =~ s/unless(\(|\s)/<span style=\"color\: blue\">unless<\/span>$1/g;
	$line =~ s/else(\{|\s)/<span style=\"color\: blue\">else<\/span>$1/g;
	$line =~ s/push(\s|\()/<span style=\"color\: blue\">push<\/span>$1/g;
	$line =~ s/close(\s|\()/<span style=\"color\: blue\">close<\/span>$1/g;
#	$line =~ s/\{/<span style=\"color\: blue\">\{<\/span>/g;
#	$line =~ s/\}/<span style=\"color\: blue\">\}<\/span>/g;
#	$line =~ s/\(/<span style=\"color\: blue\">\(<\/span>/g;
#	$line =~ s/\)/<span style=\"color\: blue\">\)<\/span>/g;


	$line =~ s/<span<\/span>/<\/span><span/gi;

	$line = $line . $commentline;

	return $line;
}
