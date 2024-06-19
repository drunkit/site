<?PHP
	include_once "base.php";

	class Template extends base {
		
		var $filename;
		var $templateContents;
		
		function __construct ($templateFile, $render = true, $stylesheet = false) { # stylesheet parsing option possible in future
			$this->filename = $this->getTemplateRoot().$templateFile;
			if ($render) {
				$this->reloadTemplate();
			}
		}
		
		function reloadTemplate () {
			$this->templateContents = file($this->filename);
			$this->parseTemplate();			
		}
		
	
	
		function parseTemplate () {
			foreach ($this->templateContents as $lineNumber => $line) {
				
				$line = preg_replace_callback("/\[input (.*?)\=(.*?)\]/si",array($this, dataCallBack), $line);
				
				if (preg_match_all("/\[addtemplate\=(.*?)\]/si",$line,$matches)) {
					foreach ($matches[1] as $match) {
						$additionalTemplate = new Template($match);
						$line = preg_replace("/\[addtemplate\=(.*?)\]/si",@implode("", $additionalTemplate->returnTemplate()),$line);
					}
				}
				
				$line = preg_replace_callback("/\[special parse=(.*?) template=(.*?)\]/i", array($this, specialParse), $line);
				
				
				$line = preg_replace_callback("/\[usercheck level=(.*?)\](.*?)\[endusercheck\]/i", array($this, userCheck), $line);
		
				$this->templateContents[$lineNumber] = $line;
			}
			
		}
		
		
		function userCheck ($inputArray) {
			include_once "settings.php";
			$settings = new Settings("articles");
			if (base::getUserLevel() >= $settings->get($inputArray[1])) {
				return $inputArray[2];
			}
			else {
				return "";
			}
		}

		function printTemplate () {
			print @implode("",$this->returnTemplate());
		}
		
		function returnTemplate () {
			return $this->templateContents;
		}
		
		
		function specialParse ($parseArray) {
			$output = "";
			$template = @implode("", file(base::getTemplateRoot().$parseArray[2]));

			if ($parseArray[1] == "categorylist") {
				include_once "settings.php";
				$settings = new Settings("articlecategories");
				if ($categories = $settings->getHash()) {
					foreach ($categories as $categoryId => $categoryName) {
							$output .= $template;
							$output = preg_replace("/\[categoryid\]/",$categoryId,$output);
							$output = preg_replace("/\[categoryname\]/",$categoryName,$output);
					}
				}
			}

			return $output;
		}
		
			
		function dataCallBack ($input) {
			if (strtolower($input[1]) == "get") {
				return $_GET[$input[2]];
			}
			else if (strtolower($input[1]) == "post") {
				return $_POST[$input[2]];
			}
			else if (strtolower($input[1]) == "cookie") {
				return $_COOKIE[$input[2]];
			}
			else {
				return $_REQUEST[$input[2]];
			}
		}
		
		#function getInfoCallback ($input) {
		#	if ($input[1]
		#}

	}

?>