<?php
	require "modules/common.php";
	require "modules/templates.php";


	$userinfo = new UserInfo();

	$userlevel = $userinfo->get("userlevel");

	if ($userlevel >= 500) {
		$topTemplate = new Template("top-template.html");
		$topTemplate->printTemplate();
		?>
		<h1>Permission Deined!</h1>
		<p style="margin: 0px;">You have tried to access an area of Drunkit that is not for web viewing</p>

		<p>Please use the <a href="javascript:history.back(1)"><- back</a> button on your browser to go back to the page you came from. If you came here from another web site, our link may have unfortunately changed. In this case, please visit our <a href="https://drunkit.co.uk">home page</a> and navigate from there.</p>

<?php
	$botTemplate = new Template("bot-template.html");
			
	$botTemplate->printTemplate();

	}
	else {
		?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "https://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="https://www.w3.org/1999/xhtml" xml:lang="en-gb">
<head>
	<title>Index of <?=$_SERVER['REQUEST_URI'];?></title>
	<meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
	<style type="text/css">
		body {
			color: #000000;
			background-color: #FFFFFF;
			font-family: serif;
			font-size: 100%;
		}
		h1 {
			font-family: serif;
			color: #000000;
			background-color: #FFFFFF;
		}
		td {
			font-family: monospace;
			font-size: 100%;
			color: #000000;
			background-color: #FFFFFF;
		}
		th {
			font-family: monospace;
			font-size: 100%;
			text-align: left;
		}
	</style>
</head>
<body>
		<h1>Index of <?=$_SERVER['REQUEST_URI'];?></h1>
		<hr />
		<table>
			<col width="200" />
			<col width="140" />
			<col width="200" />
			<tr>
				<th>Name</th>
				<th>Modified</th>
				<th>Size</th>
			</tr>

		<?php
			if ($handle = @opendir($_SERVER['DOCUMENT_ROOT'])) {
				while (false !== ($file = readdir($handle))) { 
					$filePath = $_SERVER['DOCUMENT_ROOT']."/".$file;
					if ($file != "." && $file != "..") {
						print "<tr>\n"; 
						print "<td><a href=\"".$file."\">".$file."</a></td>\n";
						print "<td>".date("d-M-Y h:i",filemtime($filePath))."</td>\n";
						print "<td>".filesize($filePath)."</td>\n";
#						print "<td>".$file."</td>\n";
						print "</tr>\n\n";
					}
				}
			closedir($handle);
			}

		?>

	</table>

	<p>
		<a href="https://validator.w3.org/check/referer"><img src="https://www.w3.org/Icons/valid-xhtml11" alt="Valid XHTML 1.1!" height="31" width="88" /></a> | 
		<a href="https://jigsaw.w3.org/css-validator/"><img style="border:0;width:88px;height:31px" src="https://jigsaw.w3.org/css-validator/images/vcss" alt="Valid CSS!" /></a>
	</p>

	</body>
</html>

		<?php

	}
?>