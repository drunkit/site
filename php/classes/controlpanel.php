<?php

include_once "base.php";
include_once "settings.php";


class Controlpanel extends base {
	var $articleSettings;
	var $userArray;
	var $userTextArray;
	
	function __construct () {
		 $this->articleSettings = new Settings("articles");
		 $this->userArray = array(1,2,3,4);
		 $this->userTextArray = array("Regular User","Privilaged User","Moderator","Administrator");
	}
	
	function getUserLevelDropDownStatus ($setting, $level) {
		if ($this->articleSettings->get($setting) == $level) {
			return " selected";
		}
		else {
			return;
		}
	}
	
	function getUserArray () {
		return $this->userArray;
	}
	
	function getUserTextArray () {
		return $this->userTextArray;
	}
	
	function getUserText($level) {
		return $this->userTextArray[($level - 1)];
	}
	
	
	function getUserLevelDropDown ($title, $setting) {
		$output = "<label for=\"id_".$setting."\">".$title."</label> <select id=\"id_".$setting."\" name=\"".$setting."\">\n";

		$users = $this->getUserArray();
		foreach ($users as $user) {
			$output .= "<option value=\"".$user."\"".$this->getUserLevelDropDownStatus($setting,$user).">".$this->getUserText($user)."</option>\n";
		}
		$output .= "</select>";
		return $output;
	}
	

}

?>