<?PHP
require_once "base.php";


class io {
	var $filename;
	var $hash;

	# Constructor
	function __construct ($inFilename) {
		$this->filename = strtolower($inFilename);
		$this->constructHash();
	}

	function constructHash () {
		print "Constructing hash for $filename \n";
		$fileContents = file($this->filename);
		if ($fileContents) {
			foreach ($fileContents as $line) {
				$lineArray = preg_split("/\=/",$line);
                $this->hash[strtolower($lineArray[0])] = rawurldecode(chop($lineArray[1]));
                print $lineArray[0];
			}
		}
	}

	function get ($key) {
		return @$this->hash[$key];
	}

	function set ($key, $value) {
		$this->hash[strtolower($key)] = $value;
	}

	function write ($key, $value) {
		$this->set($key, $value);
		$this->commit();
	}
	
	function getHash () {
		return $this->hash;
	}
	
	function setHash ($hash) {
		$this->hash = $hash;
	}

	function commit() {
		$output = "";
		if ($this->hash) {
			foreach ($this->hash as $key => $value) {
				$output .= strtolower($key)."=".rawurlencode($value)."\n";	
			}
			$fp = @fopen($this->filename,"w");
				@fwrite($fp, $output);
			@fclose($fp);
		}
	}

}


?>
