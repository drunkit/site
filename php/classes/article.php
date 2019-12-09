<?PHP
include_once "io.php";

class article extends io {
	var $id;
	var $settings;
	function article ($id = "") {
		if (!$id) {
			$id = $this->getFreeArticleId();
		}
		$this->id = $id;
		$this->filename = "data/articles/".$id;
		$this->constructHash();
	}
	function getFreeArticleId () {
		if (!$this->settings) {
			$this->populateSettings();
		}
		return ($this->settings->get("articlecount") + 1);
	}
	function populateSettings () {
		include_once "settings.php";
		$this->settings = new settings("articles");
	}

	
}

?>
