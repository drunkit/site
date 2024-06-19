<?php
	header("Expires: Mon, 26 Jul 1997 05:00:00 GMT");
   	header("Cache-Control: no-store, no-cache, must-revalidate");
   	header("Cache-Control: post-check=0, pre-check=0", false);
    header("Pragma: no-cache");

    class ForumTemplate extends Template  {}

	class Template {
		
		var $templateFile;
		var $templateContents;
		var $infoVar;
		var $infoVarConstructed;
		var $themeDir;
		
		function __construct ($inTemplateFile) {
			$this->templateFile = getThemeDir().$inTemplateFile;		
		}
		
		function printTemplate () {
			$this->templateContents = implode("", file($this->templateFile));
			print $this->parseVariables();
		}
		
		function getTemplate () {
			$this->templateContents = implode("", file($this->templateFile));
			return $this->parseVariables();
		}
		
		function parseVariables () {
			$template = $this->templateContents;
			constructInfoVar();
			$template = preg_replace_callback("/\[var info=(.*?)\]/", "getReplacement2019", $template);
			$template = preg_replace_callback("/\[include condition=(.*?) parse=(.*?) elseParse=(.*?)\]/", "checkConditional2019", $template);
			$template = str_replace("[DocumentRootBin]","https://drunkit.co.uk/bin",$template);
			
			$poll = new ParsePoll();
			$template = str_replace("[include poll]",$poll->getHtml(),$template);
		
			return $template;
		}
		
	}

    function checkConditional2019($matches) {
        return checkConditional($matches[1], $matches[2], $matches[3]);
    }
	
	function checkConditional($cond, $res1, $res2) {
		$conditions['userName'] = getUserName();
		
		if ($conditions[$cond]) {
			$template = new Template($res1);
			return $template->getTemplate();
		}
		else {
			$template = new Template($res2);
			return $template->getTemplate();
		}
    }

    function getReplacement2019($matches) {
        return getReplacement($matches[1]);
    }
	
	function getReplacement($inputString) {
        $infoVar = constructInfoVar();
		if (!$infoVar[strtolower($inputString)]) {
			print "No for ".strtolower($inputString);
		}
		return $infoVar[strtolower($inputString)];

	}
	function constructInfoVar() {
		
		$userInfo = new UserInfo();
		
		$friendlyName = "";
		
		if ($userInfo->get("friendlyname")) {
			$friendlyName = $userInfo->get("friendlyname");
		}
		$qstr = $_SERVER['QUERY_STRING'];
		if ($qstr) {
			$qstr = str_replace("&","&amp;",$qstr);
			$qstr = "?".$qstr;
		}
		$redirect = $_SERVER['PHP_SELF']."$qstr";
		if (!$redirect) {
			$redirect = "home.cgi";
		}
		
		$title = implode("",file("../etc/settings/title.txt"));
		
		$infoVar['redirectinfo'] = $redirect;
		$infoVar['themedir'] = getHtmlThemeDir();
		$infoVar['title'] = $title;
		$infoVar['imagesdir'] = $infoVar['themedir']."images/";
		$infoVar['timeanddate'] = parseTime(time(),"date");
		$infoVar['friendlyname'] = $friendlyName;
		return $infoVar;
	}
	
	
	function parseTime ($time, $format = "short") {
		$timeArray = localtime($time);
		$month = ($timeArray[4] + 1);
		$day = ($timeArray[6] + 1);
		$months = array("Januray","February","March","April","May","June","July","August","September","October","November","December");
		$days = array("Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday");

		$modDate = $timeArray[3] % 10;
		$ext = "th";
		if ($modDate == 1) { $ext = "st"; }
		else if ($modDate == 2) { $ext = "nd"; }
		else if ($modDate == 3) { $ext = "rd"; }

		if ($timeArray[5] < 1970) { $timeArray[5] += 1900; }

		if ($timeArray[1] < 10) {
			$timeArray[1] = "0".$timeArray[1];
		}
		if ($timeArray[2] < 10) {
			$timeArray[2] = "0".$timeArray[2];
		}

		if ($format == "short") {
			return $timeArray[2].":".$timeArray[1]." ".$timeArray[3]."/".$month."/".$timeArray[5];
		}
		else if ($format == "shortDate") {
			return $timeArray[3]."/".$month."/".$timeArray[5];
		}
		else if ($format == "time") {
			return $timeArray[2].":".$timeArray[1];
		}
		else if ($format == "lngtime") {
			return $timeArray[2].":".$timeArray[1].":".$timeArray[0];
		}
		else if ($format == "date") {
			return $days[$timeArray[6]]." ".$timeArray[3].$ext." ".$months[$timeArray[4]]." ".$timeArray[5];
		}
		else if ($format == "std") {
			return $timeArray[5]."-".$month."-".$day;
		}
		else {
			$date = convertTime($time,"date");
			$time = convertTime($time,"time");
			return $date." at ".$time;
		}
	}



	class ParsePoll {
		
		var $pollHtml;
		var $pollNumber;
	
		function __construct () {
			$pollSettings = new SettingsFile(getSettingsDir()."/Poll/pollSettings.txt");
			$this->pollNumber = $pollSettings->get("pollnumber");
			
			$userSetting = new UserInfo();
			
			$userPoll = $userSetting->get("PollVote");
			
			if ($userPoll != $this->pollNumber) {
				$this->parseHtml("pollMain.html");
			}
			else {
				$this->parseHtml("pollVotedMain.html");
			}			
		}
		
		
		function parseHtml ($pollHtmlFile) {
			
						
			$file = getComponentThemeDir()."Poll/".$pollHtmlFile;
			$this->pollHtml = implode("",file($file));
			
			$pollSettings = new SettingsFile(getVarDir()."Poll/".$this->pollNumber.".txt");
			
			$results = $this->parseResultLine();
			
			$questions = $this->parseOptionLine();
			
			$this->pollHtml = str_replace("[DocumentRootBin]","https://drunkit.co.uk/bin", $this->pollHtml);

			$this->pollHtml = str_replace("[poll parse=results]",$results, $this->pollHtml);
			
			$this->pollHtml = str_replace("[poll parse=Options]",$questions, $this->pollHtml);
			
			$this->pollHtml = str_replace("[poll var=Question]",$pollSettings->get("Question"), $this->pollHtml);
		}
		
		function parseOptionLine () {
			$file = getComponentThemeDir()."Poll/pollQuestionLine.html";
			$fileContents = implode("",file($file));
			$pollSettings = new SettingsFile(getVarDir()."Poll/".$this->pollNumber.".txt");
			
			$output = "";
			
			for ($i = 1; $i; $i++) {
				if ($pollSettings->get($i)) {
					#$output .= str_replace("","",$fileContents);
					$outputLine = str_replace("[poll parse=CurrentLine]", $pollSettings->get($i), $fileContents);
					$outputLine = str_replace("[poll parse=CurrentLineNumber]", $i, $outputLine);
					if ($i == 1) {
						$outputLine = str_replace("[checkOrNot]"," checked=\"checked\"",$outputLine);
					}
					else {
						$outputLine = str_replace("[checkOrNot]","",$outputLine);
					}
					
					
					$output .= $outputLine;
				}
				else {
					break;
				}				
			}
			
			return $output;

		}
		
		
		function parseResultLine () {
			$file = getComponentThemeDir()."Poll/pollResultLine.html";
			$fileContents = implode("",file($file));
			$pollSettings = new SettingsFile(getVarDir()."Poll/".$this->pollNumber.".txt");
			
			$results = "";
			
			#poll parse=percent
			
			$totalReplies = 0;
			
			for ($i = 1; $i; $i++) {
				if ($pollSettings->get($i)) {
					$thisanswerString = "answer".$i;
					$totalReplies += $pollSettings->get($thisanswerString);
				}
				else {
					break;
				}				
			}
			
			for ($i = 1; $i; $i++) {
				if ($pollSettings->get($i)) {
					$resultLine = str_replace("[poll parse=lineNumber]",$i,$fileContents);
					$thisanswerString = "answer".$i;
					
					$currentLine = $pollSettings->get($i);
					
					$votes = $pollSettings->get($thisanswerString);
					if (!$votes) {
						$votes = 0;
					}
					
					if ($totalReplies > 0) {
						$percent = intval((($votes / $totalReplies) * 100));
					}
					else {
						$percent = 0;
					}
					
					$resultLine = str_replace("[poll parse=CurrentLine]", $currentLine, $resultLine);
					
					$resultLine = str_replace("[poll parse=halfpercent]", intval($percent / 2), $resultLine);
					
					$resultLine = str_replace("[poll parse=percent]",$percent,$resultLine);
					
					$resultLine = str_replace("[poll parse=votes]", $votes, $resultLine);
					
					$resultLine = str_replace("[var info=themeDir]","../etc/themes/".getTheme()."/", $resultLine);
					
					$results .= $resultLine;
					#print $pollSettings->get($i)."<br>";
				}
				else {
					break;
				}				
			}
			
			return $results;
			
		}
		
		function getHtml () {
			return $this->pollHtml;
		}
		
	}

?>
