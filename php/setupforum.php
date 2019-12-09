<?php
	require "modules/common.php";
	require "modules/templates.php";
	
	$topTemplate = new Template("top-template.html");
			
	$topTemplate->printTemplate();
	
	if ($_GET['forumname']) {
		$settings = new SettingsFile("../etc/forumlookup");
		$settings->write(getUserName(), $_GET['forumname']);
		
		$settings = new SettingsFile("../etc/drunkitlookup");
		$settings->write($_GET['forumname'], getUserName());
	
		print "<h1>Settings Updated</h1>";
		print "<p><a href=\"https://forums.drunkit.co.uk/\">Go back to the forums</a>";
		
	}
	else if (getUserName()) {
		$settings = new SettingsFile("../etc/forumlookup");
		$forumname = $settings->get(getUserName());
		?>
		<h1>Setup Drunkit</h1>
		Okay <?=getUserName()?>, all I've got to know is what your forum name is:

		<form method="get" action="setupforum">
			<p>
				<input type="text" value="<?=$forumname?>" name="forumname" /> <input type="submit" value="Change" />
			</p>
		</form>
	<?php
	}
	else {
		print "<h1>Not logged in to Drunkit. Please login above.</h1>";
	}

	$botTemplate = new Template("bot-template.html");
				
	$botTemplate->printTemplate();


?>