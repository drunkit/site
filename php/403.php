<?php
	require "modules/common.php";
	require "modules/templates.php";


	$userinfo = new UserInfo();

	$userlevel = $userinfo->get("userlevel");
	
	if (($userlevel < 3) || (!is_dir($_SERVER['DOCUMENT_ROOT'].$_SERVER['REDIRECT_URL']))) {
		printXhtmlHeader();
		?>
		<h1>Permission Deined!</h1>
		<p style="margin: 0px;">You have tried to access an area of Drunkit that is not for web viewing</p>

		<p>Please use the <?php
			if (isset($_SERVER['HTTP_REFERER'])) {
				print "<a href=\"".$_SERVER['HTTP_REFERER']."\">&lt;- back</a>";
			}
			else {
				print "back";
			}
		
		?> button on your browser to go back to the page you came from. If you came here from another web site, our link may have unfortunately changed. In this case, please visit our <a href="https://drunkit.co.uk">home page</a> and navigate from there.</p>
<?php

		printXhtmlFooter();

	}
	else {
		
				
				
		$nameSort = "an";
		$sizeSort = "as";
		$modSort = "am";
		$query = str_replace($_SERVER['REDIRECT_URL'], "", $_SERVER['REQUEST_URI']);
		if ($query) {
			$query = str_replace("?","",$query);
			$query_array = preg_split("/\&/", $query);
			foreach ($query_array as $query) {
				$tempQueryArray = preg_split("/=/", $query);
				$query_string[$tempQueryArray[0]] = $tempQueryArray[1];
			}
		}

		if (($query_string['s'] == "an") || (!$query_string['s'])) {
			$query_string['s'] = "an";
			$nameSort = "dn";
		}
		if ($query_string['s'] == "as") {
			$sizeSort = "ds";
		}
		if ($query_string['s'] == "am") {
			$modSort = "dm";
		}
		
		
		$directoryList = "";
		
		if ($handle = @opendir($_SERVER['DOCUMENT_ROOT'].$_SERVER['REDIRECT_URL'])) {
			while (false !== ($file = readdir($handle))) {
				
				$filePath = $_SERVER['DOCUMENT_ROOT'].$_SERVER['REDIRECT_URL'].$file;
				if ($file != ".") {
					if (is_dir($filePath)) {
						$file = $file."/";
					}
					
					if (($query_string['s'] == "an") || ($query_string['s'] == "dn")) {
						$i = $file;
					}
					if (($query_string['s'] == "as") || ($query_string['s'] == "ds")) {
						$exists = "true";
						if (is_dir($filePath)) {
							$i = "-";
						}
						else {
							$i = filesize($filePath);
						}
						while ($exists == "true") {
							if (!$directoryList[$i]) {
								$exists = "false";
							}
							else {
								$i = $i."a";
							}
							
						}
					}
					if (($query_string['s'] == "am") || ($query_string['s'] == "dm")) {
						$exists = "true";
						$i = filemtime($filePath);
						while ($exists == "true") {
							if (!$directoryList[$i]) {
								$exists = "false";
							}
							else {
								$i = $i."a";
							}
						}
					}
					
					$directoryList[$i]['name'] = $file;
					if (is_dir($filePath)) {
						$directoryList[$i]['size'] = "-";
					}
					else {
						$directoryList[$i]['size'] = filesize($filePath);
					}
					$directoryList[$i]['modified'] = filemtime($filePath);
					
					
					/*
					
					print "<tr>\n"; 
					print "<td><a href=\"".$file."\">".$file."</a></td>\n";
					print "<td>".date("d-M-Y h:i",filemtime($filePath))."</td>\n";
					print "<td>".filesize($filePath)."</td>\n";
					print "</tr>\n\n";
					
					*/
				}
			}
		closedir($handle);
		}
		
		
		
		
		
		
		printXhtmlHeader();
		
		?>
		<h1>Index of <?=$_SERVER['REDIRECT_URL'];?></h1>
		<hr />
		<table>
			<col width="200" />
			<col width="160" />
			<col width="100" />
			<tr>
				<th><a href="<?=$_SERVER['REDIRECT_URL']?>?s=<?=$nameSort?>" class="sort">Name</a></th>
				<th><a href="<?=$_SERVER['REDIRECT_URL']?>?s=<?=$modSort?>" class="sort">Modified</a></th>
				<th><a href="<?=$_SERVER['REDIRECT_URL']?>?s=<?=$sizeSort?>" class="sort">Size</a></th>
			</tr>

		<?php
		
			if (substr($query_string['s'], 0, 1) == "d") {
				krsort($directoryList);
			}
			else {
				ksort($directoryList);
			}
		
			foreach ($directoryList as $fileInfoArray) {
				print "<tr>\n"; 
				print "<td><a href=\"".$fileInfoArray['name']."\">".$fileInfoArray['name']."</a></td>\n";
				print "<td>".date("d-M-Y H:i",$fileInfoArray['modified'])."</td>\n";
				print "<td>".$fileInfoArray['size']."</td>\n";
				print "</tr>\n\n";
				
				
			}
		
			/*if ($handle = @opendir($_SERVER['DOCUMENT_ROOT'].$_SERVER['REQUEST_URI'])) {
				while (false !== ($file = readdir($handle))) { 
					$filePath = $_SERVER['DOCUMENT_ROOT'].$_SERVER['REQUEST_URI'].$file;
					if ($file != "." && $file != "..") {
						if (is_dir($filePath)) {
							$file = $file."/";
						}
						print "<tr>\n"; 
						print "<td><a href=\"".$file."\">".$file."</a></td>\n";
						print "<td>".date("d-M-Y h:i",filemtime($filePath))."</td>\n";
						print "<td>".filesize($filePath)."</td>\n";
						print "</tr>\n\n";
					}
				}
			closedir($handle);
			}*/

		?>

	</table>

		<?php
		printXhtmlFooter();
	}
	
	function printXhtmlHeader () {
		?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "https://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="https://www.w3.org/1999/xhtml" xml:lang="en-gb">
<head>
	<title>Index of <?=$_SERVER['REDIRECT_URL'];?></title>
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
		a.sort:link {
			color: #0000FF;
			background-color: #FFFFFF;
		}
		a.sort:visited {
			color: #0000FF;
			background-color: #FFFFFF;
		}
		a.sort:hover {
			color: #FF0000;
			background-color: #FFFFFF;
		}
		.caption {
			color: #000000;
			font-size: 10pt;
			font-family: serif;
			margin-top: 15px;
			
		}
	</style>
</head>
<body>
<?php
	}
	
	function printXhtmlFooter () {
		?>
	<address class="caption">
			Drunkit Server version 1.1
	</address>

	</body>
</html>
<?php
	}
?>
