<?php
include_once "classes/base.php";
include_once "classes/settings.php";
include_once "classes/controlpanel.php";

class ControlPanelParse {

	var $filename;
	var $fileContents;
	var $controlPanel;


	function __construct ($filename = "data/controlpanel/controlpanel") {
		$this->fileContents = file($filename);
		$this->controlPanel = new ControlPanel();
	}
	
	function doParse () {
		$fileContents = implode("",$this->fileContents);


		$fileContents = preg_replace("/\[head title=(.*?)\]/", "<h1>\\1</h1>", $fileContents);
		
		$fileContents = preg_replace("/\r/","",$fileContents);
		$fileContents = preg_replace("/\n/","<br />",$fileContents);
		$fileContents = preg_replace_callback("/\[list type=(.*?) id=(.*?) title=(.*?) level=(.*?)\]/i", array($this, parseControlPanelInput), $fileContents);
		
		$fileContents = preg_replace("/<br \/><br \/>/","<p />",$fileContents);
		
		#$fileContents = preg_replace("/<p>(.*?)<p>/im","<p>\\1</p><p>", $fileContents);
		#$fileContents = preg_replace("/<p>(.*?)[^(<\/p>)]$/mi", "<p>\\1</p>", $fileContents);
		#$fileContents = preg_replace("/<p>(.*?)[^(<p>)(^<\/p>)]$/im", "<p>\\1</p>", $fileContents);
	
		
		
	
		
		
		print $fileContents;
	}
	
	
	function parseControlPanelInput ($infoArray) {
		if (base::getUserLevel() >= $infoArray[4]) {
			if ($infoArray[1] == "users") {
				return $this->controlPanel->getUserLevelDropDown($infoArray[3],$infoArray[2]);
			}
		}
		return "";
	}



}




?>