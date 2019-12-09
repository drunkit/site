<?PHP
include_once "io.php";

class settings extends io {

    public $test = "moo";

	function settings ($settingsFile) {
        $this->filename = "data/settings/".strtolower($settingsFile);
        $this->constructHash();
	}
}

?>
