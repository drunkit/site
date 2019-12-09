<?
	require "modules/common.php";
	require "modules/templates.php";

	$topTemplate = new Template("top-template.html");
	$topTemplate->printTemplate();
	
	$userInfo = new UserInfo();
	if ($userInfo->get("userlevel") < 3) {
		error("Not Authorised","You are not authorised to view this page. Please log in to an administrative account");
	}
	else if (@$_POST['a'] == "update") {
		$fp = @fopen($_POST['settingfile'],"w");
			@fwrite($fp,$_POST['contents']);
		@fclose($fp);
		print "File updated. <a href=\"".$_SERVER['php_self']."?settingfile=".$_POST['settingfile']."\">Go back</a>.";
	}
	else {	
		?>
		<h1>Settings File Edit</h1>
		<p style="margin: 0px;">Edit the Drunkit Settings files here...</p>

		<form action="<?=$_SERVER['PHP_SELF']?>" method="post">
			<p style="margin: 0px;">
				Filename: <input type="text" name="settingfile" value="<?=@$_REQUEST['settingfile']?>" class="cooledit" style="width: 240px;"> <input type="submit" value="Open">
			</p>
		</form>
		<form action="<?=$_SERVER['PHP_SELF']?>" method="post">
			<p style="margin: 0px;">
				<input type="hidden" name="a" value="update">
				<input type="hidden" name="settingfile" value="<?=$_REQUEST['settingfile']?>">
		<?php
			if (@$_REQUEST['settingfile']) {
				$file = implode("",file($_REQUEST['settingfile']));
				print "<textarea name=\"contents\" cols=\"50\" rows=\"5\" class=\"cooledit\">".$file."</textarea><br />";
			}
		?>
			
			<input type="submit" value="Update">
			</p>
		</form>
		
	<?
	}
	$botTemplate = new Template("bot-template.html");
			
	$botTemplate->printTemplate();
?>