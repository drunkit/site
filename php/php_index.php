<?
	require "modules/common.php";
	require "modules/templates.php";


	$topTemplate = new Template("top-template.html");
		
	$topTemplate->printTemplate();
	
?>

<h1>Drunkit PHP</h1>
<p style="margin: 0px;">Welcome to the latest Drunkit project!</p>

<p>That's right, Drunkit is being evangelised! Drunkit is being ported over to PHP, with the following constraints:</p>

<ul>
	<li> All code is to be written in PHP, no Perl should be left!
	<li> As much as possible is to be object-orientated
	<li> Current setting file format is to be preserved as well as possible
	<li> Transition should be unnoticable for the user (hence the recent port to extensionless files)
</ul>

<h2>Why is Drunkit being ported?</h2>
<p style="margin: 0px;">With the need for Drunkit to be as extensible as possible, it has been decided that the present way of rendering pages (through one large 'engine' that parses through a series of functions is inefficient, hard to maintain and even redundant at points. With this in mind, a new way of rendering pages has been required that is faster, more efficient and easier to maintain. Given this, a general tidy-up of Drunkit was initiated.</p>

<p>However, with this tidy-up came a number of realisations. The first of these was that a complete re-write of most pages would be required in order to create a new engine; however the settings-file structure etc would not have to be changed. Secondly, that re-writing Drunkit would mainly involve a complete re-write of the complex Drunkit template-parsing engine.</p>

<p>Given these facts, it was decided that the language choice should not be limited to Perl (the language in which Drunkit is presently written). After a consideration of the main programming languages available (Perl, ASP (visual basic/jscript) and PHP, PHP was chosen for its ease of use, portability and closeness to Perl (including perl regular expression support).</p>

<p>Therefore, the Drunkit PHP project was started. So far, the main page parsing has been virtually finalised, with support for page templates and some general page parsing directives. However, items such as message board parsing and other site features are far from being started, as the project is moving in its object orientated fashion, appropriate classes must be written to handle each area.</p>

<p>Stay tuned for more news...</p>

<?	
	$botTemplate = new Template("bot-template.html");
			
	$botTemplate->printTemplate();
?>
