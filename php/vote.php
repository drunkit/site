<?php
	include "modules/common.php";
	include "modules/templates.php";
	
	if ($_GET['viewResults']) {
		header('Location: https://drunkit.co.uk/php/pollspy?id=latest');
	}
	else if ($_GET['a'] == 'vote') {
		$topTemplate = new Template("top-template.html");
		$topTemplate->printTemplate();
		$voteOption = $_GET['option'];
		
		$pollSettings = new SettingsFile('../etc/settings/Poll/pollSettings.txt');
		$pollNumber = $pollSettings->get('pollnumber');
		$pollInfo = new SettingsFile('../var/Poll/'.$pollNumber.'.txt');
		
		$userInfo = new UserInfo();
		
		if (getUserName() == '') {
			?>
			<h1>Not Logged In</h1>
			<p class="first">You need to be logged in to vote in Drunkit polls. You will need a <a href='/bin/messages?a=signup'>Drunkit account</a> (note: this is different from a forum account).</p>
			<p>Use the login box available on the screen to log in and then vote in the poll again.</a>
			
			<?php
			$topTemplate = new Template("bot-template.html");
			$topTemplate->printTemplate();
			exit;
		}
		else if ($userInfo->get('pollvote') == $pollNumber) {
			?>
			<h1>Already Voted</h1>
			<p class="first">You cannot vote more than once in a single poll.</p>
			<p><a href='/php/pollspy?id=latest'>View</a> the current poll results or visit Drunkit's <a href='/bin/welcome'>home page</a>
			
			<?php
			$topTemplate = new Template("bot-template.html");
			$topTemplate->printTemplate();
			exit;
		}
		
		$voteString = 'answer'.$voteOption;
		$pollInfo->hash[$voteString]++;
		$pollInfo->commit();
		
		$recordString = 'pollvoted'.$pollNumber;
		$userInfo->set($recordString, $voteOption);
		$userInfo->set('pollvote', $pollNumber);
		$userInfo->commit();

		?>
		<h1>Voted</h1>
		<p class="first">Thanks for voting! Your vote has been counted and will show up in the poll immediately.</p>
		<p><a href='/php/pollspy?id=latest'>View</a> poll results or return to the <a href='/bin/welcome'>home page</a>.</p>
		<?php
		$topTemplate = new Template("bot-template.html");
		$topTemplate->printTemplate();
	}


?>
