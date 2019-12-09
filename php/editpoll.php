<?php
	require "modules/common.php";
	require "modules/templates.php";
	
	$topTemplate = new Template("top-template.html");
		
	$topTemplate->printTemplate();

	$userInfo = new UserInfo();
	
	if ($userInfo->get("userlevel") < 3) {
		error("Not Authorised","You are not authorised to view this page. Please log with administrative privilages, ask an administrator to allow you to view this page or cry like a litle girl");
	}
	else {
		if (@$_REQUEST['a'] == "update") {
			$hash = "";
			$id = $_POST['id'];
			$pollSettings = new SettingsFile("../var/Poll/".$id.".txt");
			foreach ($_POST as $key => $value) {
				if (($key != "a") && ($key != "id")) {
					$hash[strtolower($key)] = $value;
				}
			}
			$pollSettings->hash = $hash;
			$pollSettings->commit();
			$pollSettings = new SettingsFile("../etc/settings/Poll/pollSettings.txt");
			$pollNumber = $pollSettings->get("pollnumber");
			if ($id > $pollNumber) {
				$pollSettings->set("pollNumber",$id);
				$pollSettings->commit();
			}
			print "<h1>Poll updated</h1><p style=\"margin: 0px;\"><a href=\"/bin/poll?viewResults=View&id=".$id."\">View</a> the updated poll.</p>";
		}
		else {
			?>
			<h1>Edit Poll</h1>
			<p style="margin-top:0px;">Edit this poll. Note, it <b>doesn't</b> matter how many (blank) options there are, so long as there are no gaps between options.</p>

			<?PHP
			
			$pollNumber = @$_GET['id'];
			if (!$pollNumber) {
				$pollSettings = new SettingsFile("../etc/settings/Poll/pollSettings.txt");
				$pollNumber = $pollSettings->get("pollnumber");
			}

			$pollSettings = new SettingsFile("../var/Poll/".$pollNumber.".txt");

			$totalQuestions = 0;

			$totalToShow = 0;

			if (@$_GET['total']) {
				$totalToShow = @$_GET['total'];
			}
			
			$totalToShow = 20;


			print "<form action=\"editpoll.php\" method=\"post\">";
			print "<input type=\"hidden\" name=\"a\" value=\"update\">";
			print "<input type=\"hidden\" name=\"id\" value=\"".$pollNumber."\">";
			print "Question: <input type=\"text\" name=\"question\" value=\"".$pollSettings->get("question")."\" size=\"50\"><br />";
			for ($i = 1; ; $i++) {
				$pollQuestion = $pollSettings->get($i);
				$pollAnswers = $pollSettings->get("answer".$i);
				if (!$pollAnswers) {
					$pollAnswers = 0;
				}
				if ((!$pollQuestion) && ($totalQuestions >= $totalToShow)) {
					break;
				}
				else {
					print $i.". <input type=\"text\" name=\"".$i."\" value=\"$pollQuestion\"> &nbsp; <input type=\"text\" name=\"answer".$i."\" value=\"".$pollAnswers."\" size=\"2\"><br />";	
				}
				$totalQuestions++;
			}
			if ($totalToShow == 0) {
				$totalToShow = $totalQuestions + 5;
			}
			print "<input type=\"submit\" value=\"Update\">";
			print "</form>";
			print "<form action=\"editpoll.php\" method=\"get\">";
			print "<input type=\"hidden\" name=\"id\" value=\"".$pollNumber."\">";
			print "Options to display:";
			print "<input type=\"text\" value=\"".$totalToShow."\" name=\"total\" size=\"2\"><input type=\"submit\" value=\"Change\"></form>";

			$pollSettings = new SettingsFile("../etc/settings/Poll/pollSettings.txt");
			$pollNumber = $pollSettings->get("pollnumber");
			$pollNumber++;
			print "<a href=\"editpoll.php?id=".$pollNumber."&total=30\">Create a new poll</a>";
		}
	}
	$botTemplate = new Template("bot-template.html");
			
	$botTemplate->printTemplate();
?>
