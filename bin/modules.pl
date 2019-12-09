# Standard Library Code
# By Matt Day.
# Version: 1.0
# Date: xx/xx/xx
#
#######################################
# Info:
# First public release.
#
#######################################

# The following addition is provided as part of the standard PERL package
use strict;
use CGI;
my $query = new CGI;

my $time = time;

sub getUserName {
#	return "matt";
	my $userString = $query->cookie('userId');
	my ($userId,$userIp) = split(/\:/,$userString);
	return unless $userId;
	my $startingPath = &getToDocumentRoot($ENV{SCRIPT_NAME});
	my $userIdFile = $startingPath."usr/cache/".$userId;
	my %settingsHash = getSettingHash($userIdFile);
	if ($userIp eq $settingsHash{ipcache}) {
		my $username = $settingsHash{username};
		return strtolower($username);
	}
	else {
		return;
	}
}

sub printStats {
	my $time2 = time;
	$time = $time2 - $time;

	my $loadtime = &convertTime($time2,"date")." ".&convertTime($time2,"lngtime");
	my $URI_root = &getToFileRoot;
	my $FILE_root = &getToDocumentRoot;
	my $username = &getUserName;
	my $theme = &getThemeName;
	my $userLevel = &getUserSetting("UserLevel");
	$userLevel = 0 unless $userLevel;
	my @userDescriptions = ("(not logged in)","Poster","Moderator","Administrator");
	$username = "(not logged in)" unless $username;
	print <<"	end";
<!--
	Page Stats
	.... .....

	Renderer:	$ENV{SERVER_SOFTWARE} ($ENV{GATEWAY_INTERFACE})
	Render Time:	$time second(s).
	Rendered:	$loadtime

	User agent:	$ENV{HTTP_USER_AGENT}
	Loaded Script:	$ENV{SCRIPT_NAME}
	Requested URI:	$ENV{REQUEST_URI}
	Request method:	$ENV{REQUEST_METHOD}
	

	URI home path:	"$URI_root"
	File home path:	"$FILE_root"
	Document root:	$ENV{DOCUMENT_ROOT}
	HTTP Host:	$ENV{HTTP_HOST}

	Logged in as:	$username
	User level:	$userDescriptions[$userLevel] ($userLevel)
	Drunkit Theme:	$theme
-->
	end

}

sub openFile {
	my $filename = shift;
	open(FILE,$filename) || print "<p><b>Error</b>: Can't open file $filename: $!<p>";
	my @contents = <FILE>;
	close(FILE);
	return @contents;
}

sub qOpenFile {
	my $filename = shift;
	open(FILE,$filename);
	my @contents = <FILE>;
	close(FILE);
	return @contents;
}


sub printHtmlHeader {
	print "Content-Type: text/html\n\n";	
}

sub writeSetting {
	my $settingsFile = shift;
	my $settingsKey = shift;
	my $settingsValue = shift;
	my %fileHash = getSettingHash($settingsFile);
	$fileHash{strtolower($settingsKey)} = $settingsValue;
	open(FILE, "> $settingsFile");
	foreach my $temp (keys %fileHash) {
		print FILE $temp."=".$fileHash{$temp}."\n";
	}
	close(FILE);
}

sub getSetting {
	my $settingsFile = shift;
	my $settingsKey = shift;
	$settingsKey = strtolower($settingsKey);
	
	my @settingsFile = qOpenFile($settingsFile);
	foreach my $fileLine (@settingsFile) {
		my @line = split(/\=/,$fileLine);
		$line[0] = strtolower($line[0]);
		if ($line[0] eq $settingsKey) {
			$line[1] = winChomp($line[1]);
			return $line[1];
		}
	}
}

sub strtolower {
	my $input = shift;
	$input =~ tr/A-Z/a-z/;
	return $input;
}

sub checkLevel {
	my $minUserLevel = shift;
	if (&getUserSetting("UserLevel") < $minUserLevel) {
		&printTemplate("AccessDenied.html");
		&printTemplate("bot-template.html");
		exit
	}
}

sub parsePoll {
	my $startingPath = &getToDocumentRoot($ENV{SCRIPT_NAME});
	my $pollSettingsFile = $startingPath."etc/settings/Poll/pollSettings.txt";
	my $pollDataPath = $startingPath."var/Poll/";
	my $pollNumber = &getSetting($pollSettingsFile,"PollNumber");

	if (&getUserSetting("PollVote") != $pollNumber) {
		return &parsePollTemplate("pollMain.html",$pollNumber);
	}
	else {
		return &parsePollTemplate("pollVotedMain.html",$pollNumber);
	}
	

}

sub parsePollTemplate {
	my $pollTemplate = shift;
	my $pollNumber = shift;
	my $optionNumber = shift;
	my $totalReplies = shift;
	my $startingPath = &getToDocumentRoot($ENV{SCRIPT_NAME});
	my $skinDir = &getSkinDir();
	$pollTemplate = $startingPath."etc/themes/".&getThemeName."/components/Poll/".$pollTemplate;
	my %pollHash = &getSettingHash($startingPath."var/Poll/".$pollNumber.".txt");
	my @pollReturn = openFile("$pollTemplate");
	my $returnBuffer;
	my $answerString = "answer".$optionNumber;
	my $percent;

#	if ($query->param("id")) {
#		$thisPollNumber	= $query->param("id");
#	}

	if ($totalReplies) {
		$percent = int(($pollHash{$answerString} / $totalReplies) * 100);
	}
	my $halfPercent = $percent / 2;
	foreach my $line (@pollReturn) {
		$line =~ s/\[poll var=(.*?)\]/$pollHash{strtolower($1)}/gi;
		if ($line =~ m/\[poll parse=Options\]/i) {
			my $pollQuestion;
			for (my $currentPollNumber = 1; $currentPollNumber; $currentPollNumber++) {
				if ($pollHash{$currentPollNumber}) {
					$pollQuestion .= &parsePollTemplate("pollQuestionLine.html",$pollNumber,$currentPollNumber);
				}
				else {
					last;
				}
			}
			$line =~ s/\[poll parse=Options\]/$pollQuestion/gi;
		}

		my $themeDir;

		$themeDir = &getToFileRoot."etc/themes/".&getThemeName;

		$line =~ s/\[var info=themeDir\]/$themeDir/gi;


		if ($line =~ m/\[poll parse=Results\]/i) {
			my $pollQuestion;
			for (my $currentPollNumber = 1; $currentPollNumber; $currentPollNumber++) {
				if ($pollHash{$currentPollNumber}) {
					my $thisanswerString = "answer".$currentPollNumber;
					$totalReplies += $pollHash{$thisanswerString};
				}
				else {
					last;
				}
			}
			for (my $currentPollNumber = 1; $currentPollNumber; $currentPollNumber++) {
				if ($pollHash{$currentPollNumber}) {
					$pollQuestion .= &parsePollTemplate("pollResultLine.html",$pollNumber,$currentPollNumber,$totalReplies);
				}
				else {
					last;
				}
			}
			$line =~ s/\[poll parse=Results\]/$pollQuestion/gi;
		}



		$line =~ s/\[poll parse=percent\]/$percent/gi;
		$line =~ s/\[poll parse=halfpercent\]/$halfPercent/gi;
		$line =~ s/\[poll parse=lineNumber\]/$optionNumber/gi;
		$line =~ s/\[poll parse=votes\]/$pollHash{$answerString}/gi;
		$line =~ s/\[poll parse=total\]/$totalReplies/gi;

		$line =~ s/\[poll parse=CurrentLine\]/$pollHash{$optionNumber}/gi;
		if ($optionNumber == 1) {
			$line =~ s/\[checkOrNot\]/ checked="checked"/gi;
		}
		else {
			$line =~ s/\[checkOrNot\]//gi;
		}

		$line =~ s/\[poll parse=CurrentLineNumber\]/$optionNumber/gi;
		$returnBuffer .= $line;
	}
	return $returnBuffer;
}

sub getSettingHash {
	my $settingsFile = shift;
	my @settingsFile = qOpenFile($settingsFile);
	my %settingsHash;
	foreach my $fileLine (@settingsFile) {
		my @line = split(/\=/,$fileLine);
		$line[0] = strtolower($line[0]);
		
		if ($line[0] eq "username") {
			$line[1] = strtolower($line[1]);
		}
		$line[1] = winChomp($line[1]);
		$settingsHash{strtolower($line[0])} = $line[1];
	}
	return %settingsHash;
}

sub getSkinDir {
	return &getThemeName;
}

sub promptLogin {
	my $skinDir = getSkinDir();
	my $startingPath = &getToDocumentRoot($ENV{SCRIPT_NAME});
	$skinDir = $startingPath."etc/themes/".$skinDir."/components/login/";
	my $templateFile = $skinDir."LoginPrompt.html";
	print &parseTemplate($templateFile,"",-1);
	&printTemplate("bot-template.html");
	exit;
}

sub returnAllArrayElements {
	my $startingElement = shift;
	my $startedElement = $startingElement;
	my $spacingFormat = shift;
	my $returnAllArrayElements;
	while ($startingElement <= $#_) {
		if ($startingElement == $startedElement) {
			$returnAllArrayElements = $_[$startingElement];
		}
		else {
			$returnAllArrayElements .= $spacingFormat . $_[$startingElement];
		}
		$startingElement++;
	}
	return $returnAllArrayElements;
}

sub parseHtml {
	my $filename = shift;
	my @file = openFile($filename);
	
	foreach my $line (@file) {
		print escapeHtml($line)."<br />\n";
	}
	
}


sub formatHtml {
	my $htmlLine = shift;
	$htmlLine = escapeHtml($htmlLine);
	$htmlLine =~ s/\n/\r/gi;
	$htmlLine =~ s/\r/<br \/>/gi;
	$htmlLine =~ s/<br \/><br \/>/<p>/gi;
	return $htmlLine;
}

sub formatTableHtml {
	my $htmlLine = shift;
	$htmlLine = escapeHtml($htmlLine);
	$htmlLine =~ s/\n/\r/gi;
	$htmlLine =~ s/\r/<br \/>/gi;
	$htmlLine =~ s/<br \/><br \/>/<p class=label>/gi;
	return $htmlLine;
}


sub checkPermission {
	my $author = shift;
	my $userLevel = &getUserSetting("UserLevel");
	if (($userLevel < 2) && ($author ne &getUserName)) {
		&printTemplate("AccessDenied.html");
		&printTemplate("bot-template.html");
		exit
	}
}

sub escapeHtml {
	my $htmlLine = shift;
	$htmlLine =~ s/&/&amp;/g;
#	$htmlLine =~ s/</&lt;/g;
#	$htmlLine =~ s/>/&gt;/g;
#	$htmlLine =~ s/"/&quot;/g;
	$htmlLine =~ s/  / &nbsp;/g;
	$htmlLine =~ s/\t/&nbsp;&nbsp;&nbsp;/g;
	return $htmlLine;
}


sub getUserSetting {
	my $setting = shift;
	my $userName = shift;
	$userName = &getUserName unless $userName;
	return "" unless $userName;
	my $startingPath = &getToDocumentRoot($ENV{SCRIPT_NAME});
	my $userFile = $startingPath."usr/".$userName.".txt";
	$setting = &getSetting($userFile,$setting);
	return &winChomp($setting);
}

sub winChomp {
	my $input = shift;
	chomp($input);
	$input =~ s/\r//gi;
	return $input;
}

sub getUserSettingHash {
	my $userName = shift;
	$userName = &getUserName unless $userName;
	return unless $userName;
	my $startingPath = &getToDocumentRoot($ENV{SCRIPT_NAME});
	my $userFile = $startingPath."usr/".$userName.".txt";
	return getSettingHash($userFile);
}

sub writeUserSetting {
	my $key = shift;
	my $setting = shift;
	my $userName = shift;
	$userName = &getUserName unless ($userName);
	return unless $userName;
	my $startingPath = &getToDocumentRoot($ENV{SCRIPT_NAME});
	my $userFile = $startingPath."usr/".$userName.".txt";
	writeSetting($userFile,$key,$setting);
}

sub convertTime {
	my $time = shift;
	my $format = shift;
	$format = "short" unless $format;
	my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($time);
	my $month = ($mon + 1);
	my $day = ($wday + 1);
	my @months = ("January","February","March","April","May","June","July","August","September","October","November","December");
	my @days = ("Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday");

	my $modDate = $mday % 10;
	my $ext = "th";
	if ($modDate == 1) { $ext = "st"; }
	elsif ($modDate == 2) { $ext = "nd"; }
	elsif ($modDate == 3) { $ext = "rd"; }

	if ($year < 1970) { $year += 1900; }

	if ($min < 10) {
		$min = "0".$min;
	}
	if ($hour < 10) {
		$hour = "0".$hour;
	}
	
	if ($format eq "short") {
		return $hour.":".$min." ".$mday."/".$month."/".$year;
	}
	elsif ($format eq "shortDate") {
		return $mday."/".$month."/".$year;
	}
	elsif ($format eq "time") {
		return $hour.":".$min;
	}
	elsif ($format eq "lngtime") {
		return $hour.":".$min.":".$sec;
	}
	elsif ($format eq "date") {
		return $days[$wday]." ".$mday.$ext." ".$months[$mon]." ".$year;
	}
	elsif ($format eq "std") {
		return $year."-".$month."-".$day;
	}
	else {
		my $date = convertTime($time,"date");
		my $time = convertTime($time,"time");
		return $date." at ".$time;
	}
	
}

sub escapeToHex {
	my $input = shift;
	$input =~ s/\%/%25/gi; $input =~ s/\n//gi; $input =~ s/\r/%0A/gi; $input =~ s/\=/%3D/gi; $input =~ s/\:/%3A/gi;
	$input =~ s/;/%3B/gi;
	return $input;
}

sub escapeFromHex {
	my $input = shift;
	$input =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	return $input;
}
sub encrypt {
	my $information = shift;
	$information = unpack("H*", $information);
	return $information;
}


sub parseTemplate {
	my $templateFile = shift;
	my $messageFileName = shift;
	my $threadNumber = shift;
	my $errorMessage = shift;
	my $thisFileName = &removePath($ENV{SCRIPT_NAME});
	my $startingPath = &getToDocumentRoot($ENV{SCRIPT_NAME});
	my %hashParse;
	my %postedUserParse;
	if ($messageFileName) {
		%hashParse = getSettingHash($messageFileName);
		my $usrhsh;
		if ($hashParse{username}) { $usrhsh = strtolower($hashParse{username}) }
		else { $usrhsh = strtolower($hashParse{username}) }
		%postedUserParse = &getUserSettingHash($usrhsh);
	}
	my $userName = &getUserName;
	my %userHash;
	if ($userName) {
		%userHash = getUserSettingHash(strtolower($userName));
	}

	my $templateReturn = &returnAllArrayElements(0,"",openFile($templateFile));
	$templateReturn =~ s/\[include parse=(.*?)\]/&parseTemplate($1)/egi;

	my $comString = "comments";
	if ($hashParse{NumberOfComments} == 1) {
		$comString = "comment";
	}
	$templateReturn =~ s/\[var comments=(.*?)\]/$comString/gi;



	$templateReturn =~ s/\[var profile=(.*?)\]/$userHash{strtolower($1)}/gi;

	$templateReturn =~ s/\[var postField=(.*?)\]/$postedUserParse{strtolower($1)}/gi;

	#$hashParse{LinksFrom};
	$templateReturn =~ s/\[var name\=(.*?)\]/$hashParse{strtolower($1)}/gi;
	my $qstr = $ENV{QUERY_STRING};
	if ($qstr) {
		$qstr =~ s/&/&amp;/gi;
		$qstr = "?".$qstr;
	}
	my $redirect = $thisFileName."$qstr";
	if ($thisFileName eq "doLogin.cgi") {
		$redirect = "home.cgi";
	}
	$redirect = "home.cgi" unless $redirect;
	$templateReturn =~ s/\[var info=ReDirectInfo\]/$redirect/gi;
	$templateReturn =~ s/\[var info\=threadNumber\]/$threadNumber/gi;
	my $replyLine = $hashParse{topic};
	if ($hashParse{topic} !~ m/^(Re:)(.*?)/gi) {
		$replyLine = "Re: $hashParse{topic}";
	}

	if ($templateReturn =~ m/\[var protected=(.*?)\]/i) {
		if ($userHash{userlevel} >= 3) {
			$templateReturn =~ s/\[var protected=(.*?)\]/$hashParse{strtolower($1)}/gi;
		}
		else {
			$templateReturn =~ s/\[var protected=(.*?)\]/Hidden/gi;
		}
	}

	$templateReturn =~ s/\[var info\=replyLine\]/$replyLine/gi;
	$templateReturn =~ s/\[var info\=thisfilename\]/$thisFileName/gi;
	$templateReturn =~ s/\[var info=error\]/$errorMessage/gi;
	$templateReturn =~ s/\[var info\=(.*?)\]//gi;
	$templateReturn =~ s/\[var parseTime=(.*?)\?(.*?)\]/&convertTime($hashParse{strtolower($1)},$2)/egi;


	$templateReturn =~ s/\[var htmlButton=(.*?)\?(.*?)\]/<input type="$1" onMouseOver="this.className='buttonOver'" onMouseOut="this.className='coolbutton'" onMouseDown="this.className='buttonDown'" onMouseUp="this.className='buttonover'" class="coolbutton" value="$2" \/>/gi;

	$templateReturn =~ s/\[var parseHexAndHtml=(.*?)(\?(.*?))?\]/&formatHtml(&escapeFromHex($hashParse{strtolower($1)}))/egi;

	$templateReturn =~ s/\[var parseHex\=(.*?)(\?(.*?))?\]/&escapeFromHex($hashParse{strtolower($1)})/egi;		

	if ($templateReturn =~ m/\[optional case\=(.*?)\](.*?)\[endOptional\]/gi) {
		if ($hashParse{strtolower($1)} > 0) {
			$templateReturn =~ s/\[optional case\=(.*?)\](.*?)\[endOptional\]/$2/gi;
		}
		else {
			$templateReturn =~ s/\[optional case\=(.*?)\](.*?)\[endOptional\]//gi;
		}
	}


	return $templateReturn;
}

sub getThemeName {
	my $themeDir = &getUserSetting("Template");
	unless ($themeDir) {
		$themeDir = "clean";
	}
	if ($ENV{HTTP_USER_AGENT} =~ m/^Mozilla(.*?)4\.(1|2|3|4|5|6|7|8|9)/i) {
		return "html32";
	}
	elsif (($ENV{HTTP_USER_AGENT} =~ m/^Links/i) || ($ENV{HTTP_USER_AGENT} =~ m/^lynx/i)) {
		return "textonly";
	}
	else {
		return $themeDir;
	}
}

sub printTemplate {
	my $template = shift;
	my $error = shift;
	my $thisFileName = &removePath($ENV{SCRIPT_NAME});
	my $userName = &getUserName();

	my @templateFile = &openFile("../etc/settings/title.txt");
	
	my $startingPath = &getToDocumentRoot($ENV{SCRIPT_NAME});
	my $themeDir = $startingPath."etc/themes/".&getThemeName."/";

	my $relThemeDir = &getToFileRoot."etc/themes/".&getThemeName."/";
	


	my @template = openFile($themeDir."html/".$template);
	my %templateHash;
	$templateHash{Title} = $templateFile[0];
	$templateHash{FriendlyName} = &getUserSetting("FriendlyName");
	$templateHash{imagesDir} = $relThemeDir."html/images";
	$templateHash{themeDir} = $relThemeDir."html";
	$templateHash{userName} = $userName;
	$templateHash{error} = $error;
	my $qstr = $ENV{QUERY_STRING};
	if ($qstr) {
		$qstr =~ s/&/&amp;/gi;
		$qstr = "?".$qstr;
	}
	my $redirect = $thisFileName."$qstr";
	foreach my $line (@template) {
		my $time = convertTime(time,"date");
		$line =~ s/\[var info=timeAndDate\]/$time/gi;
		if ($line =~ m/\[include condition=(.*?) parse=(.*?) elseParse=(.*?)\]/gi) {
			$line =~ s/\[include condition=(.*?) parse=(.*?) elseParse=(.*?)\]//gi;
			if ($templateHash{$1}) {
				&printTemplate($2);
			}
			else {
				&printTemplate($3);
			}
		}

		$line =~ s/\[include poll\]/&parsePoll()/egi;

		$line =~ s/\[include parse=(.*?)\]/&printTemplate($1)/egi;
		
		if ($thisFileName eq "doLogin.cgi") {
			$redirect = "home.cgi";
		}
		$line =~ s/\[DocumentRoot\]/&getToFileRoot/egi;
		$line =~ s/\[DocumentRootBin\]/&getToFileRoot."bin"/egi;
		$redirect = "home.cgi" unless $redirect;
		$line =~ s/\[var info=ReDirectInfo\]/$redirect/gi;
		$line =~ s/\[var info=(.*?)\]/$templateHash{$1}/gi;
		print $line;
	}
	if ($template eq "bot-template.html") {
		&printStats;
	}
}

sub removeFileName {
	my $path = shift;
	my @pathInfo = split(/\//,$path);
	my $numberInTree = $#pathInfo;
	my $newPath = $pathInfo[0];
	$numberInTree -= 1;
	my $currentNode = 1;
	while ($currentNode <= $numberInTree) {
		$newPath .= $pathInfo[$currentNode]."/";
		$currentNode++;
	}
	return $newPath;
}

sub removePath {
	my $file = shift;
	my @fileArray = split(/\//,$file);
	$file = $#fileArray;
	$file = $fileArray[$file];
	return $file;
}

sub getToDocumentRoot {
	my @url = split(/\//,$ENV{SCRIPT_NAME});
	return "..\/" x ($#url - 1);
}

sub getToFileRoot {
	my @url = split(/\//,$ENV{REQUEST_URI});
#	print $ENV{REQUEST_URI};
#	return "..\/" x ($#url);
	#return "https://drunkit.co.uk/";
	return "/";
}

sub error {
	my $message = shift;
	print "<h1>$message</h1>";
	&printTemplate("bot-template.html");
	exit;

}

# Return a true value to indicate that this extension file is complete
return 1;
