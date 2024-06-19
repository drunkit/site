<?php
	header("Expires: Mon, 26 Jul 1997 05:00:00 GMT");
   	header("Cache-Control: no-store, no-cache, must-revalidate");
   	header("Cache-Control: post-check=0, pre-check=0", false);
   	header("Pragma: no-cache");
	class SettingFile extends SettingsFile {
		
	}

	class SettingsFile {
		var $hash;
		var $filename;
__construct
		function __construct ($file) {
			$this->filename = $file;
			$this->reload();
		}

		function reload() {
			$hash = "";
			$settingsHash = @file($this->filename);
			if ($settingsHash) {
				foreach ($settingsHash as $settingLine) {
					$values = preg_split("/\=/",$settingLine);
					@$hash[trim(strtolower($values[0]))] = trim($values[1]); //All values case-insensitive
				}
			}
			$this->hash = $hash;
		}

		function get ($setting) {
			return @rawurldecode($this->hash[strtolower($setting)]);
		}

		function getHash () {
			return $this->hash;
		}
		

		function setHash ($hash) {
			$this->hash = $hash;
		}
		
		function set ($key,$value) {
			$this->hash[strtolower($key)] = @rawurlencode($value);
		}
		
		function setNoEncode ($key,$value) {
			$this->hash[$key] = $value;
		}

		function commit () {
			$output = "";
			$hash = $this->hash;
			if ($hash) {
				foreach ($hash as $key => $value) {
					$output .= strtolower($key)."=".$value."\n";
				}
			}
			$fp = @fopen($this->filename,"w");
				@fwrite($fp,$output);
			@fclose($fp);
		}

		function write($key,$value) {
			$this->set($key,$value);
			$this->commit();
		}
	}
	
	
	class ArticleFile extends SettingsFile {
		function __construct($articleId) {
			$this->filename = "content/articles/".$articleId.".txt";
			$this->reload();
			
		}
	}
	
	class UserInfo extends SettingsFile {
		function __construct ($userName = "") {
			if (!$userName) {
				$userName = getUserName();
			}
			
			if ($userName) {
				$file = getUserDir().$userName.".txt";
				$this->filename = $file;
				$this->reload();
			}
		}
	}
	
	
	// Some non-oop functions to get simple requests (i.e. dirs etc)
	
	function getUserName() {
		$userInfo = @preg_split("/\:/", $_COOKIE['userId']);
		if ($userInfo[0]) {
			$filename = getUserDir()."cache/".$userInfo[0];
			$userInfo = new SettingsFile($filename);
			return $userInfo->get("username");
		}
	}
	
	function getTheme () {
		$userSettings = new UserInfo();
		$themeName = $userSettings->get("template");
		if (!$themeName) {
			$themeName = "default";
		}
		return $themeName;
	}


	function getThemeDir () {
		return "../etc/themes/".getTheme()."/html/";
	}

	function getHtmlThemeDir () {
		return "/etc/themes/".getTheme()."/html/";
	}
	
	function getComponentThemeDir () {
		return "../etc/themes/".getTheme()."/components/";
	}
	
	function getHtmlComponentThemeDir () {
		return "/etc/themes/".getTheme()."/components/";
	}

	function getBaseDir () {
		return "../";
	}

	function getHtmlBaseDir () {
		return "https://drunkit.co.uk/";
	}

	function getUserDir() {
		return "../usr/";
	}
	
	function getSettingsDir() {
		return "../etc/settings/";
	}
	
	function getVarDir() {
		return "../var/";
	}
	
	function getVarHtmlDir () {
		return "https://drunkit.co.uk/var/";
	}

	function error ($errorTitle, $errorMessage) {
		print "<h1>".$errorTitle."</h1><p style=\"margin: 0px;\">".$errorMessage."</p>";
	}
	

?>