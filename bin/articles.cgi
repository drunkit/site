#!/usr/bin/perl
use CGI;
use strict;
require "/srv/http/drunkit/bin/common/modules.pl";

my $query = new CGI;

my $startingPath = &getToDocumentRoot($ENV{SCRIPT_NAME});
my $articleDir = $startingPath."var/Articles/";
my $skinDir = $startingPath."etc/themes/default/components/Articles/";

#print $query->header(-charset=>"utf8");
print $query->header();

&printTemplate("top-template.html");

if ($query->param('a') eq 'view') {
	&viewArticle($query->param('id'));
}
elsif ($query->param('a') eq 'edit') {
	&editArticle($query->param('id'));	
}
elsif ($query->param('a') eq 'new') {
	&newArticle();
}
elsif (($query->param('a') eq 'viewall') || (!$query->param('a'))) {
	&viewAll;
}
elsif ($query->param('a') eq 'editArticle') {
	&writeArticle($query->param('a'));
}
elsif ($query->param('a') eq 'postComment') {
	&postComments($query->param('id'));
}
elsif ($query->param('a') eq 'writeComment') {
	&writeComments($query->param('id'),$query->param('comments'));
}
elsif ($query->param('a') eq 'newarticle') {
	&writeArticle($query->param('a'));
}
elsif ($query->param('a') eq 'unread') {
	&showUnread;
}
else {
	&viewAll;
}

&printTemplate("bot-template.html");


sub showUnread {
	my $articleSettingsFile = $startingPath."etc/settings/Articles/Articles.txt";
	my $numberOfArticles = &getSetting($articleSettingsFile,"NumberOfArticles");
	my $numberUnread = $numberOfArticles - &getUserSetting("articleView");
	my $numberLeftUnread = $numberOfArticles - $numberUnread;

	my $articlePreviewBuffer;
	while ($numberOfArticles > $numberLeftUnread) {
		$articlePreviewBuffer .= &parseTemplate($skinDir."viewAllSingleArticle.html",$articleDir.$numberOfArticles.".txt",$numberOfArticles);
		$numberOfArticles--;
	}
	my $outputBuffer = &parseTemplate($skinDir."UnreadArticles.html","",-1);
	$outputBuffer =~ s/\[drunkitArticles\]/$articlePreviewBuffer/gi;
	print $outputBuffer;

}

sub viewAll {
	my $articleSettingsFile = $startingPath."etc/settings/Articles/Articles.txt";
	my $numberOfArticles = &getSetting($articleSettingsFile,"NumberOfArticles");
	my $articlePreviewBuffer;
	while ($numberOfArticles > 0) {
		$articlePreviewBuffer .= &parseTemplate($skinDir."viewAllSingleArticle.html",$articleDir.$numberOfArticles.".txt",$numberOfArticles);
		$numberOfArticles--;
	}
	my $outputBuffer = &parseTemplate($skinDir."ListArticles.html","",-1);
	$outputBuffer =~ s/\[drunkitArticles\]/$articlePreviewBuffer/gi;
	print $outputBuffer;
}

sub writeArticle {
	return 1;
	&promptLogin unless &getUserName;
	my $numberOfArticles;
	if ($query->param('a') eq 'newarticle') {
		my $articleSettingsFile = $startingPath."etc/settings/Articles/Articles.txt";
		$numberOfArticles = &getSetting($articleSettingsFile,"NumberOfArticles");
		$numberOfArticles++;
		writeSetting($articleSettingsFile,"NumberOfArticles",$numberOfArticles);
	}
	else {
		$numberOfArticles = $query->param('article');
	}
	my $articleFile = $articleDir.$numberOfArticles.".txt";

	&writeSetting($articleFile,"NumberOfComments",0) if ($query->param('a') eq 'newarticle');
	&writeSetting($articleFile,"UserName",&getUserName) if ($query->param('a') eq 'newarticle');
	&writeSetting($articleFile,"Date",time) if ($query->param('a') eq 'newarticle');
	&writeSetting($articleFile,"Article",&escapeToHex($query->param('Article')));
	&writeSetting($articleFile,"Description",&escapeToHex($query->param('Description')));
	&writeSetting($articleFile,"Title",$query->param('Title'));

	print &parseTemplate($skinDir."thanksForPostingArticle.html",$articleFile,$numberOfArticles);
}


sub writeComments {
	&promptLogin unless &getUserName;
	my $articleId = shift;
	my $comment = shift;
	&error("No comment entered!") unless $comment;
	$comment = &escapeToHex($comment);
	my $articleFile = $articleDir.$articleId.".txt";
	my $comments = &getSetting($articleFile,"Comments");
	$comments .= ";".&getUserName.":".$comment;
	writeSetting($articleFile,"Comments",$comments);

	my $numberOfComments = &getSetting($articleFile,"NumberOfComments");
	$numberOfComments++;
	writeSetting($articleFile,"NumberOfComments",$numberOfComments);


	my $templateFile = $skinDir."thanksForPostingComments.html";;
	print &parseTemplate($templateFile,$articleFile,$articleId);
}

sub newArticle {
	&promptLogin unless &getUserName;
	print &parseTemplate($skinDir."newArticle.html","",-1);
}

sub postComments {
	&promptLogin unless &getUserName;
	my $articleId = shift;
	my $articleFile = $articleDir.$articleId.".txt";
	my $templateFile = $skinDir."PostComment.html";;
	print &parseTemplate($templateFile,$articleFile,$articleId);

}


sub viewArticle {
	my $articleId = shift;
	my $templateFile = $skinDir."viewArticle.html";
	my $articleFile = $articleDir.$articleId.".txt";
	my $parseInfo = &parseTemplate($templateFile,$articleFile,$articleId);
	my $comments = &getComments($articleFile);

	if (&getUserSetting("articleView") < $articleId) {
		&writeUserSetting("articleView",$articleId);
	}

	$parseInfo =~ s/\[insertComments\]/$comments/gi;

	print $parseInfo;
}

sub getComments {
	my $articleFile = shift;
	my $returnBuffer;
	my @comments = split(/\;/,&getSetting($articleFile,"Comments"));
	foreach my $comment (@comments) {
		my ($userName,$userComment) = split(/:/,$comment);
		$userName = strtolower($userName);
		if ($userComment) {
			my $lineBuffer;
			my @commentLine = openFile($skinDir."CommentLine.html");
			foreach my $line (@commentLine) {
				my %userHash = &getUserSettingHash($userName);
				$userComment = &formatTableHtml(&escapeFromHex($userComment));
				$line =~ s/\[username\]/$userName/gi;
				$line =~ s/\[comment\]/$userComment/gi;
				$line =~ s/\[var user=(.*?)\]/$userHash{strtolower($1)}/gi;
				$lineBuffer .= $line;
			}
			$returnBuffer = $lineBuffer.$returnBuffer;
		}

	}
	return $returnBuffer;
}

sub getCommentTemplate {
	my $userName = shift;
	my $comment = shift;
}

sub editArticle {
	&promptLogin unless &getUserName;
	my $articleId = shift;
	if ($articleId) {
		my $articleFile = $articleDir.$articleId.".txt";
		if ((&getSetting($articleFile,"UserName") eq &getUserName) || (&getUserSetting("UserLevel") >= 2)) {
			print &parseTemplate($skinDir."editArticle.html",$articleFile,$articleId);	
		}
		else {
			&error("Insufficient permissions to edit this article");
		}
	}
	else {
		my $articleSettingsFile = $startingPath."etc/settings/Articles/Articles.txt";
		my $numberOfArticles = &getSetting($articleSettingsFile,"NumberOfArticles");
		my $articleList;
		my $modArticleList;
		for (my $sofar = 1; ($sofar <= $numberOfArticles); $sofar++) {
			if (&getSetting($articleDir.$sofar.".txt","UserName") eq &getUserName) {
				$articleList .= &parseTemplate($skinDir."editArticleListLine.html",$articleDir.$sofar.".txt",$sofar);
			}
		}
		if (&getUserSetting("UserLevel") >= 2) {
			for (my $sofar = 1; ($sofar <= $numberOfArticles); $sofar++) {
				if (&getSetting($articleDir.$sofar.".txt","UserName") ne &getUserName) {
						$modArticleList .= &parseTemplate($skinDir."editArticleListLine.html",$articleDir.$sofar.".txt",$sofar);
				}
			}
		}
		my $modArticleListBuffer;
		if (&getUserSetting("UserLevel") >= 2) {
			 $modArticleListBuffer = &parseTemplate($skinDir."modArticlesListLine.html","",-1);
		}
		$modArticleListBuffer =~ s/\[editarticlelist\]/$modArticleList/gi;

		my $articleListBuffer = &parseTemplate($skinDir."editArticleList.html","",-1);

		$articleListBuffer =~ s/\[editarticlelist\]/$articleList/gi;
		$articleListBuffer =~ s/\[otherPeoplesArticles\]/$modArticleListBuffer/gi;

		print $articleListBuffer;

	}
}


