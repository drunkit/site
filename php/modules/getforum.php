<?php
include '/srv/http/drunkit/forums3/config.php';

function getMessagesArray () {
        global $dbhost;
        global $dbport;
        global $dbname;
        global $dbuser;
        global $dbpasswd;
        global $table_prefix;

        $server = $dbhost;
        $port = $dbport;
		$dbn = $dbname;
		$user = $dbuser;
		$pass = $dbpasswd;

#		$private1 = " AND f.auth_view < 1";
		$PostNumber = 10;
		$start = 0;

		$forum_lst = "1, 2, 3, 4";

		$dbConnect = mysqli_connect($server, $user, $pass, $dbn, $port) or print "Connection error".mysqli_error();
        mysqli_select_db($dbn, $dbConnect);

		$sql = "SELECT t.topic_title, p.topic_id, t.topic_last_post_id, p.post_time, f.forum_name, f.forum_id,
			       u.username, u.user_id, p.post_username, u2.username as user2, u2.user_id as id2
			 FROM phpbb_topics AS t,
			      phpbb_forums AS f,
			      phpbb_posts AS p,
			      phpbb_users AS u,
			      phpbb_users AS u2
			 WHERE f.forum_id       = t.forum_id
				 AND t.topic_poster   = u.user_id
			   AND p.post_id        = t.topic_last_post_id
			   AND p.poster_id      = u2.user_id
			   AND t.topic_moved_id = 0
			   AND f.forum_id in ( $forum_lst )
			   $private1
			 ORDER BY t.topic_last_post_id DESC
			 LIMIT $start, $PostNumber";


        	$query = @mysqli_query($dbConnect, $sql) or print 'Error: '.mysqli_error($dbConnect);
        	$output = array();
		while ($row = @mysqli_fetch_array($query)) {
			$output[] = $row;
		}
		return $output;
	}
?>
