<?PHP
include_once "io.php";

class user extends io {
	function __construct ($username) {
		$this->filename = "data/users/".strtolower($username);
		$this->constructHash();
	}
	function getUserLevel () {
		return $this->get("userlevel");
	}
	function getAlias () {
		return $this->get("alias");
	}
}

?>
