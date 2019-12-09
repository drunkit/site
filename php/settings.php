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
		$keysIndex = "";
		$valuesIndex = "";
		$hash = "";
		foreach ($_POST as $key => $value) {
			if (($key != "a") && ($value) && ($key != "settingfile")) {
				$keyArray = preg_split("/\-/", $key);
				
				if ($keyArray[0] == "KEY") {
					@$keysIndex[$keyArray[1]] = $value;
				}
				else {
					@$valuesIndex[$keyArray[1]] = $value;
				}
			}
		}
		if ($keysIndex) {
			foreach ($keysIndex as $key => $value) {
				$hash[$value] = $valuesIndex[$key];
			}
		}
		$settingFile = new SettingsFile($_POST['settingfile']);
		$settingFile->setHash($hash);
		$settingFile->commit();
		print "<h1>Updated</h1><p style=\"margin: 0px;\">Your settings file has been updated</p><p><a href=\"settings.php?settingfile=".$_POST['settingfile']."\">Go back</a></p>";
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
				$settingFile = $_REQUEST['settingfile'];
				$settingFile = new SettingsFile($settingFile);
				$x = 0;
				if ($settingFile->getHash()) {
					foreach ($settingFile->getHash() as $key => $value) {
						$x++;
						?>
							<input type="text" name="KEY-<?=$x?>" value="<?=$key?>">
							<input type="text" name="VALUE-<?=$x?>" value="<?=$value?>"><br />
						
						<?php
					}
				}
				$x++;
				?>
				<input type="text" name="KEY-<?=$x?>" value="">
				<input type="text" name="VALUE-<?=$x?>" value=""><br />
				<?php
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