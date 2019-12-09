#!/usr/bin/perl

use strict;
#Gasp! Matt's using CGI.pm now!
use CGI;
 
my $query = new CGI;

require "/srv/http/drunkit/bin/common/modules.pl";


# First of all, let's get some settings
my $userName = &getUserName();

my $startingPath = &getToDocumentRoot($ENV{SCRIPT_NAME});
my $settingsDir = $startingPath."etc/settings/MessageBoard/";
my $messagesDir = $startingPath."var/MessageBoard/Messages/";
my $skinDir = $startingPath."etc/themes/default/components/MessageBoard/";
my $thisFileName = &removePath($ENV{SCRIPT_NAME});


print $query->header() unless ($query->param('a') eq 'unread');

&printTemplate("top-template.html") unless ($query->param('a') eq 'unread');

if ($query->param('a') eq "view") {
	&viewMessage($query->param('msg'));
}
elsif ($query->param('a') eq "newmessage") {
	&newMessage();
}
elsif ($query->param('a') eq "signup") {
	&signup;
}
elsif ($query->param('a') eq "edit") {
	&editMessage($query->param('msg'));
}
elsif ($query->param('a') eq "info") {
	&messageInfo($query->param('msg'));
}
elsif ($query->param('a') eq "stats") {
	&messageStats();
}
elsif ($query->param('a') eq 'createNewMessage') {
	&writeNewMessage($query->param('FriendlyName'),$query->param('Topic'),$query->param('message'));
}
elsif ($query->param('a') eq 'reply') {
	&reply($query->param('msg'));
}
elsif ($query->param('a') eq 'recent') {
	&showRecent($query->param('show'));
}
elsif ($query->param('a') eq 'unread') {
	&unread();
}
elsif ($query->param('a') eq 'search') {
	&search($query->param('q'));
}
elsif ($query->param('a') eq 'createNewReply') {
	&writeNewMessage($query->param('FriendlyName'),$query->param('Topic'),$query->param('message'),$query->param('linksFrom'));
}
elsif ($query->param('a') eq 'editmessage') {
	&writeNewMessage($query->param('FriendlyName'),$query->param('Topic'),$query->param('message'),$query->param('linksFrom'),$query->param('msg'));
}
elsif ($query->param('a') eq 'newAccount') {
	&createNewAccount($query->param('userName'),$query->param('Password1'),$query->param('Password2'),$query->param('FriendlyName'),$query->param('email'),$query->param('profile'));
}
else {
	&printAllMessages;
}

&printTemplate("bot-template.html");


sub unread {
	my $numberOfMessages = &getNumberOfMessages();
	my $numberToShow = ($numberOfMessages - &getUserSetting("messageBoardView"));
	if ($numberToShow == 1) { print "Location: messages?a=view&msg=".$numberOfMessages."\n\n\n\n"; exit }
	else {
		print $query->header();
		&printTemplate("top-template.html");
		my $recentBuffer = &parseTemplate($skinDir."UnreadMessages.html","",-1);
		my $recentLineBuffer;
		for (my $sofar = ($numberOfMessages - $numberToShow + 1); ($sofar <= $numberOfMessages); $sofar++) {
			if ($sofar > 0) {
				$recentLineBuffer = &parseTemplate($skinDir."RecentMessagesLine.html",$messagesDir.$sofar.".txt",$sofar).$recentLineBuffer;
			}
		}
		$recentBuffer =~ s/\[recentMessages\]/$recentLineBuffer/gi;
		print $recentBuffer;
	}
}


sub search {
	my $query = shift;
	my $results;
	my $outBuffer = &parseTemplate($skinDir."messageSearch.html","",-1);

	$results = &doSearch($query) if ($query);

	$outBuffer =~ s/\[var search=query\]/$query/gi;
	$outBuffer =~ s/\[var search=results\]/$results/gi;

	print $outBuffer;

}

sub showRecent {
	my $numberToShow = shift;
	$numberToShow = 10 unless $numberToShow;
	my $numberOfMessages = &getNumberOfMessages();
	my $recentBuffer = &parseTemplate($skinDir."RecentMessages.html","",-1);
	my $recentLineBuffer;
	for (my $sofar = ($numberOfMessages - $numberToShow + 1); ($sofar <= $numberOfMessages); $sofar++) {
		if ($sofar > 0) {
			$recentLineBuffer = &parseTemplate($skinDir."RecentMessagesLine.html",$messagesDir.$sofar.".txt",$sofar).$recentLineBuffer;
		}
	}
	$recentBuffer =~ s/\[recentMessages\]/$recentLineBuffer/gi;
	print $recentBuffer;

}

sub doSearch {
	my $query = shift;
	my $bufferOutput;
	opendir(MESSAGEDIR,$messagesDir);
		my @messages = readdir(MESSAGEDIR);
	closedir(MESSAGEDIR);

	@messages = sort {$a <=> $b} @messages;

	foreach my $element (@messages) {
		unless (($element eq ".") || ($element eq "..")) {
			my $message = getSetting($messagesDir.$element,"Message");
			my ($no,$ext) = split(/\./,$element);
			if (&escapeFromHex($message) =~ m/$query/gi) {
				$bufferOutput .= &parseTemplate($skinDir."messageSearchResult.html",$messagesDir.$element,$no);
			}
		}
	}
	$bufferOutput = "No matches" unless $bufferOutput;
	return $bufferOutput;
}


sub createNewAccount {
	my $user = shift;
	my $pass1 = shift;
	my $pass2 = shift;
	my $friendlyname = shift;
	my $email = shift;
	my $profile = shift;

	$user = strtolower($user);

	if ($profile) {
		$profile = &escapeToHex($profile);
	}
	my $encpass1 = encrypt($pass1);

	&error("Not all detail entered. Please try again") unless (($user) && ($pass1) && ($pass2) && ($friendlyname));
	&error("Your passwords do not match. Please go back and ensure you have typed it correctly") if ($pass1 ne $pass2);

	my $userFile = $startingPath."usr/".$user.".txt";
	&error("Username already in use. Please select another") if (&getSetting($userFile,"FriendlyName"));

	writeSetting($userFile,"UserLevel",1);
	writeSetting($userFile,"FriendlyName",$friendlyname);
	writeSetting($userFile,"Password",$encpass1);
	writeSetting($userFile,"UserLevel",1);
	writeSetting($userFile,"Template","default");
	if ($profile) {
		writeSetting($userFile,"Profile",$profile);
	}
	if ($email) {
		writeSetting($userFile,"Email",$email);
	}
	&printTemplate("SignedUp-template.html");
	
}



sub signup {
	&printTemplate("signUp-template.html");
}


sub reply {
	&promptLogin unless &getUserName;
	my $messageToReplyTo = shift;
	my $messageFile = $messagesDir.$messageToReplyTo.".txt";
	print &parseTemplate($skinDir."ReplyToMessage.html",$messageFile,$messageToReplyTo);
	
}

sub writeNewMessage {
	my $alias = $query->param('FriendlyName');
	my $userName = $query->param('UserName');
	my $topic = $query->param('Topic');
	my $message = $query->param('message');
	my $linksFrom = $query->param('linksFrom');
	my $msg = $query->param('msg');
	my $totalMessages;

	$message = &escapeToHex($message);
	&error("Not all detail entered. Please try again.") unless (($alias) && ($topic) && ($message));
	unless ($msg) {
		$totalMessages = getNumberOfMessages();
		$totalMessages++;
	}
	else {
		$totalMessages = $msg;
	}
	my $messageFile = $messagesDir.$totalMessages.".txt";

	if ($userName) {
		writeSetting($messageFile,"Username",strtolower($userName));
	}
	$userName = &getUserName;
	writeSetting($messageFile,"Username",$userName) unless ($msg);
	writeSetting($messageFile,"FriendlyName",$alias);
	writeSetting($messageFile,"Message",$message);
	writeSetting($messageFile,"Time",time) unless ($msg);
	writeSetting($messageFile,"Topic",$topic);
	my $linksTo = "";
	my $writeLinksFrom = -1;
	if ($linksFrom) {
		addLinksTo($linksFrom,$totalMessages) unless ($msg);
		$writeLinksFrom = $linksFrom;
	}
	else {
		&addMainThreads($totalMessages) unless ($msg);
	}
	writeSetting($messageFile,"IP",$ENV{REMOTE_ADDR}) unless ($msg);
	writeSetting($messageFile,"UserAgent",$ENV{HTTP_USER_AGENT}) unless ($msg);
	writeSetting($messageFile,"LinksFrom",$writeLinksFrom) unless ($msg);
	writeSetting($messageFile,"LinksTo","$linksTo") unless ($msg);
	writeNumberOfMessages($totalMessages) unless ($msg);
	print &parseTemplate($skinDir."MessageCreated.html",$messageFile,$totalMessages);	
}

sub addLinksTo {
	my $linksToFile = shift;
	my $fileToLinkTo = shift;
	my $messageFile = $messagesDir.$linksToFile.".txt";
	my $currentLinks = getSetting($messageFile,"LinksTo");
	$currentLinks = $fileToLinkTo.",".$currentLinks;
	&writeSetting($messageFile,"LinksTo",$currentLinks);
}

sub getNumberOfMessages {
	return getSetting($settingsDir."settings.txt","messageCount");
}

sub writeNumberOfMessages {
	writeSetting($settingsDir."settings.txt","messageCount",$_[0]);
}

sub getMainThreads {
	return getSetting($settingsDir."settings.txt","messageThreads");
}

sub addMainThreads {
	my $newThreadNumber = shift;
	my $currentThread = &getMainThreads;
	$currentThread = $newThreadNumber.",".$currentThread;
	writeSetting($settingsDir."settings.txt","messageThreads",$currentThread);
}


sub newMessage {
	&promptLogin unless &getUserName;
	my $templateFile = $skinDir."NewMessage.html";
	print &parseTemplate($templateFile,"",-1);
}

sub messageInfo {
	my $messageThread = shift;
	my $messageFileName = $messagesDir.$messageThread.".txt";

	my $templateFile = $skinDir."messageInfo.html";
	print &parseTemplate($templateFile,$messageFileName,$messageThread);	

}

sub editMessage {
	&promptLogin unless &getUserName;
	my $messageThread = shift;
	my $messageFileName = $messagesDir.$messageThread.".txt";

	&checkPermission(&getSetting($messageFileName,"Username"));

	my $templateFile = $skinDir."editWindow.html";
	my $bufferOut = &parseTemplate($templateFile,$messageFileName,$messageThread);

	if (&getUserSetting("UserLevel") >= 3) {
		$templateFile = $skinDir."editWindowAdmin.html";
		my $advEdit = &parseTemplate($templateFile,$messageFileName,$messageThread);
		$bufferOut =~ s/\[advedit\]/$advEdit/gi;
	}
	else {
		$bufferOut =~ s/\[advedit\]//gi;
	}

	print "$bufferOut";
}

sub viewMessage {
	my $messageThread = shift;
	if (&getUserSetting("messageBoardView") < $messageThread) {
		&writeUserSetting("messageBoardView",$messageThread);
	}
	my $messageFileName = $messagesDir.$messageThread.".txt";
	my $templateFile = $skinDir."ViewMessage.html";
	print &parseTemplate($templateFile,$messageFileName,$messageThread);
	my $linksTo = getSetting($messageFileName,"linksto");
	$linksTo =~ s/\s//gi;
	my @messages = split(/\,/,$linksTo);
	if ($linksTo) {
		print &openFile($skinDir."IfRepliesLine.htm");
		print "\n<ul style=\"margin-top: 5px\">\n";
		foreach my $messageThread (@messages) {
			$messageThread =~ s/\s//gi;
			if ($messageThread) {
				&printMessageThread($messageThread);
			}
		}
		print "\n</ul>\n";
	}
	print &parseTemplate($skinDir."BottomViewMessage.html",$messageFileName,$messageThread);

}

sub printAllMessages {
	my $perpage = $query->param('perpage');
	my $pageNumber = $query->param('page');
	unless ($perpage) { $perpage = 10; }
	$pageNumber = 0 unless $pageNumber;
	my @startingMessages = split(/\,/,&getMainThreads);
	my $topParse = &parseTemplate($skinDir."TopOfMessageBoard.html","",-1);
	my $botParse = &parseTemplate($skinDir."BottomOfMessageBoard.html","",-1);
	
	my $totalPages = int($#startingMessages / $perpage + 1);
	my $currentPage = ($pageNumber + 1);

	if ($currentPage > $totalPages) {
		$pageNumber = ($totalPages - 1);
		$currentPage = ($totalPages);
	}

	my $previousPage = ($pageNumber - 1);

	$topParse =~ s/\[totalpages\]/$totalPages/gi;
	$topParse =~ s/\[pagenumber\]/$currentPage/gi;
	$botParse =~ s/\[totalpages\]/$totalPages/gi;
	$botParse =~ s/\[pagenumber\]/$currentPage/gi;

	my $nextFile;
	if ($currentPage >= $totalPages) {
		$nextFile = "nextPageNotOk.html";
	}
	else {
		$nextFile = "nextPageOk.html";
	}
	my $nextPageLink = &parseTemplate($skinDir.$nextFile,"",-1);
	$nextPageLink =~ s/\[nextpage\]/$thisFileName?a=viewall&amp;page=$currentPage&amp;perpage=$perpage/gi;
	$topParse =~ s/\[nextpage\]/$nextPageLink/gi;
	$botParse =~ s/\[nextpage\]/$nextPageLink/gi;

	my $previousFile;
	if ($pageNumber <= 0) {
		$previousFile = "previousPageNotOk.html";
	}
	else {
		$previousFile = "previousPageOk.html";
	}
	my $previousPageLink = &parseTemplate($skinDir.$previousFile,"",-1);
	$previousPageLink =~ s/\[previouspage\]/$thisFileName?a=viewall&amp;page=$previousPage&amp;perpage=$perpage/gi;
	$topParse =~ s/\[previouspage\]/$previousPageLink/gi;
	$botParse =~ s/\[previouspage\]/$previousPageLink/gi;

	print $topParse;

	print "\n<ul>\n";

	my $startFrom = $pageNumber * $perpage;
	my $goUpTo = $startFrom + $perpage;

	for (my $i = $startFrom; ($i < $goUpTo); $i++) {
		&printMessageThread($startingMessages[$i]) unless (($i < 0) || (!$startingMessages[$i]));
	}
	print "</ul>";
	print $botParse;
}

sub printMessageThread {
	my $messageThread = shift;
	my $messageFileName = $messagesDir."".$messageThread.".txt";
	my %threadHash = getSettingHash($messageFileName);

	my $templateFile = $skinDir."MessageThread.html";
	
	print &parseTemplate($templateFile,$messageFileName,$messageThread);

	my $threadsFollowing = $threadHash{linksto};
	if ($threadsFollowing) {
		my @threadsFollowing = split(/\,/,$threadsFollowing);
		foreach my $threadFollowing (@threadsFollowing) {
			if ($threadFollowing > 0) {
				$threadFollowing =~ s/\s//gi;
				print "<ul>";
				&printMessageThread($threadFollowing);
				print "</ul>";
			}
		}
	}
}

sub printAllMessagesByDate {
	opendir(MESSAGEDIR,$messagesDir);
		my @messages = readdir(MESSAGEDIR);
	closedir(MESSAGEDIR);

	@messages = sort {$a <=> $b} @messages;

	foreach my $element (@messages) {
		unless (($element eq ".") || ($element eq "..")) {
			print "$element<br />";
		}
	}
}

sub messageStats {
	print <<"	eof";
		<h1>Drunkit Stats</h1>
		<p style="margin: 0px:">I know how much you all loved the stats! Here goes!</p>

		<p>Note: It will be better in future... That's a promise.</p>

	eof

	opendir(MESSAGEDIR,$messagesDir);
		my @messages = readdir(MESSAGEDIR);
	closedir(MESSAGEDIR);

	my %messages;

	foreach my $element (@messages) {
		unless (($element eq ".") || ($element eq "..")) {
			my $file = $messagesDir.$element;
			my $uname = strtolower(&getSetting($file,"Username"));
			$messages{$uname}++;
		}
	}

	foreach my $messageName (sort {$b <=> $a} (keys(%messages))) {
		print $messageName." --> ".$messages{$messageName}."<br>";
	}

}





