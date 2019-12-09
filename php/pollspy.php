<?php
	require "modules/common.php";
	require "modules/templates.php";
	
	$topTemplate = new Template("top-template.html");
		
	$topTemplate->printTemplate();

	$userInfo = new UserInfo();
	
	/*if ($userInfo->get("userlevel") < 3) {
		error("Not Authorised","You are not authorised to view this page. Please log in to an administrative account");
	}
	else */if ($_GET['id']) {
		
		if ($_GET['id'] == "latest") {
			$pollSettings = new SettingsFile("../etc/settings/Poll/pollSettings.txt");
			$id = $pollSettings->get("pollnumber");
		}
		else {
			$id = $_GET['id'];
		}
		$pollSettings = new SettingsFile("../var/Poll/".$id.".txt");
		print "<h1>".$pollSettings->get("question")."</h1>";
		?>
			<table width="700" cellspacing="0" border="0" cellpadding="0">
		<?php

		$pollStringCatcher = "pollvoted".$id;

		$userVoteArray = array();
		
		if ($handle = @opendir("../usr/")) {
			while (false !== ($file = readdir($handle))) { 
				if ($file != "." && $file != ".." && $file != "cache") { 
                    $settings = new SettingsFile("../usr/".$file);
                    $pollVote = $settings->get($pollStringCatcher);
                    if ($pollVote) {
						$userVoteArray[$pollVote][] = $file;
					}
				}
			}
			closedir($handle);
		}

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
		
		print "In this poll ".$totalReplies." votes have been cast<p>";

		for ($i = 1; $i; $i++) {
			if ($pollSettings->get($i)) {
				#$resultLine = str_replace("[poll parse=lineNumber]",$i,$fileContents);
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

				$width = ($percent * 2 + 1);
				
				$pollUsers = $userVoteArray[$i];

				$userList = array();
				$realNames = array();

				if ($pollUsers) {
					foreach ($pollUsers as $user) {
						$settings = new SettingsFile("../usr/".$user);
						$userList[] = $settings->get("friendlyname");
						$username = preg_split("/\./", $user);
						$realNames[] = "Login name: ".$username[0];
					}
				}

					print "<tr>";


/*
		
			Alright:
		</td>
		<td width="20" valign="top" class="label">

			&nbsp;
		</td>
		<td width="270" valign="top" class="label">
			<img src="https://drunkit.co.uk/etc/themes/default/components/Poll/images/poll.gif" alt="Alright - 1 vote(s) - 16%" height="8" width="32"> 1 (16%)
		</td>

*/
		?>
		<tr>
			<td width="150" align="right" valign="top" class="label">
				<?=$currentLine?>:
			</td>
	
			<td width="20" valign="top" class="label">
				&nbsp;
			</td>
			<td width="270" valign="bottom" class="label">
				<?="<img src=\"https://drunkit.co.uk/etc/themes/default//components/Poll/images/poll.gif\" width=\"".$width."\" height=\"8\"> $votes (".$percent."%)"?>
			</td>
			<td valign="bottom" class="label">
			<?php
				if ($userInfo->get("userlevel") == 3) {
					print getList($userList, $realNames);	
				}
				else {
					print "&nbsp;";
				}
			?>
			</td>
		</tr>	
		<?php
					

#				print $i.". ".$currentLine.": ".$votes." vote(s) <img src=\"https://drunkit.co.uk/etc/themes/default//components/Poll/images/poll.gif\" width=\"".$width."\" height=\"8\"> (".$percent."%)<br />";
#				
			}
			else {
				break;
			}				
		}


	print "</table>";
	print "<p>View <a href=\"pollspy\">other poll</a> results. <a href=\"editpoll?id=$id\">Edit</a> this poll.";
		
	}
	else {

		$pollSettings = new SettingsFile("../etc/settings/Poll/pollSettings.txt");
		$pollNumber = $pollSettings->get("pollnumber");
		print "<h1>Select a poll to view</h1>";
		print "<ul>";
		for ($i = $pollNumber; $i >= 1; $i--) {
			$pollSettings = new SettingsFile("../var/Poll/".$i.".txt");
			print "<li /><a href=\"pollspy?id=".$i."\">".$pollSettings->get("question")."</a>";
		}
		print "</ul>";
	}

	$botTemplate = new Template("bot-template.html");
			
	$botTemplate->printTemplate();




	function getList ($inputArray, $realNames = "") {
		if (!$inputArray) {
			return;
		}
		if (count($inputArray) == 1) { return "<acronym title=\"".$realNames[0]."\" style=\"cursor: help\">".$inputArray[0]."</acronym>"; }

		$output = "";
		foreach ($inputArray as $key => $name) {
			
			$descline = "<acronym title=\"".$realNames[$key]."\" style=\"cursor: help\">".$name."</acronym>";
			
			if ($key == (count($inputArray) - 1)) {
				$output .= " and ".$descline;
			}
			else if ($key > 0) {
				$output .= ", ".$descline;
			}
			else {
				$output = $descline;
			}

		}

		return $output;
		
	}


?>
