<?php
	session_name("phpbb2mysql_sid");
	session_start();
	
	require "../php/modules/common.php";
	require "../php/modules/templates.php";
	require "../php/modules/getforum.php";
	$topTemplate = new Template("top-template.html");
		
	$topTemplate->printTemplate();

	if (getUserName()) {
		$template = "../home/newHomeLoggedIn.html";
	}
	else {
		$template = "../home/newHomeLoggedOut.html";
	}
	
	$template = file($template);
	
	

	// First get the message board entries
	$mySql = @getMessagesArray();
    $messages = "<ul>";
	if ($mySql) {
		foreach ($mySql as $query) {
			$topic = htmlentities($query['topic_title'], ENT_QUOTES, "UTF-8");
			$postId = $query['topic_last_post_id'];
			$topicId = $query['topic_id'];
			$postTime = $query['post_time'];
            $username = $query['username'];
            $forum = $query['forum_name'];
            $forum_id = $query['forum_id'];

            $messages .= "<li><a href=\"https://forums.drunkit.co.uk/viewtopic.php?t=".$topicId."#".$postId."\" class=\"ddoption\">".$topic."</a> - posted in <a href=\"https://forums.drunkit.co.uk/viewforum.php?f=$forum_id\" class=\"ddoption\">$forum</li>\n";	
        }
    }
    $messages .= "</ul>";
	
	// Now get the latest articles:
	$totalArticles = new SettingsFile("../etc/settings/Articles/Articles.txt");
    $totalArticles = $totalArticles->get("numberofarticles");
    $articles = "<ul>";
	for ($i = $totalArticles; $i > ($totalArticles - 8); $i--) {
        $article = new SettingsFile("../var/Articles/".$i.".txt");
        $articles .= "<li><a href=\"https://drunkit.co.uk/bin/article/id,".$i."/\" class=\"ddoption\">".$article->get("title")."</a> - ".$article->get("description")."</li>";
		if ((time() - $article->get("date")) < 604801) {
			$articles .= " - <b>New!</b>";
		}
    }
    $articles .= "</ul>";

	$announcement = @file("../var/Announcements/Announcements.txt");
	
	$quote = file("../home/quotes.txt");
	$quote = $quote[rand(0, (count($quote) - 1))];

	$userName = getUserName();
	
	$template = str_replace("{messages}", $messages, $template);
	$template = str_replace("{articles}", $articles, $template);
	$template = str_replace("{announcement}", $announcement[0], $template);
	$template = str_replace("{quote}", $quote, $template);
	

	print implode("",$template);

	$botTemplate = new Template("bot-template.html");
			
	$botTemplate->printTemplate();
?>
