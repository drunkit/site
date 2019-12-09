#!/usr/bin/perl

use strict;
use CGI;

require "/srv/http/drunkit/bin/common/modules.pl";

my $query = new CGI;

print $query->header(-charset=>"ISO-8859-15") unless ($query->param('area') eq 'changeTheme');

&printTemplate("top-template.html") unless $query->param('area') eq 'changeTheme';

&promptLogin unless &getUserName;


my $startingPath = &getToDocumentRoot($ENV{SCRIPT_NAME});
my $skinDir = $startingPath."etc/themes/default/components/ControlPanel/";
my $userLevel = getUserSetting("UserLevel");

if ($query->param('area') eq 'themes') {
	&themes;
}
elsif ($query->param('area') eq 'changeTheme') {
	&changeTheme;
}
elsif ($query->param('area') eq 'changePass') {
	&changePass;
}
elsif ($query->param('area') eq 'resetpassword') {
	&resetpassword;
}
elsif ($query->param('area') eq 'profile') {
	&profile;
}
elsif ($query->param('area') eq 'changeProfile') {
	&changeProfile;
}
elsif ($query->param('area') eq 'moderation') {
	&checkLevel(2);
	if ($query->param('usr')) {
		&profileModerator;
	}
	else {
		&profileModeratorChooseUser;
	}
}
elsif ($query->param('area') eq 'editannouncements') {
	&checkLevel(3);
	&editAnnouncements;
}
elsif ($query->param('area') eq 'doEditAnnouncements') {
	&checkLevel(3);
	&doEditAnnouncements;
}
elsif ($query->param('area') eq 'admin') {
	&checkLevel(3);
	if ($query->param('usr')) {
		&profileAdmin;
	}
	else {
		&profileAdminChooseUser;
	}
}
elsif ($query->param('area') eq 'changeModProfile') {
	&changeModProfile;
}
elsif ($query->param('area') eq 'changeUserPass') {
	&changeUserPass;
}
elsif ($query->param('area') eq 'password') {
	&password;
}
else {
	&controlPanel;
}

sub profileModerator {
	my $passedUserName = strtolower($query->param('usr'));
	my %userVariables = getUserSettingHash($passedUserName);
	$userVariables{profile} = escapeFromHex($userVariables{profile});
	my $parsedThemes = &parseTemplate($skinDir."modProfile.html","",-1);
	$parsedThemes =~ s/\[var userInfo=(.*?)\]/$userVariables{strtolower($1)}/gi;
	

	$parsedThemes =~ s/\[var userParam]/$passedUserName/gi;

	print $parsedThemes;

}

sub changeModProfile {
	&checkLevel(2);
	my $username = $query->param('usr');
	my $profile = $query->param('profile');
	$profile = escapeToHex($profile);
	writeUserSetting("Profile",$profile,$username);
	print &parseTemplate($skinDir."profileUpdated.html","",-1);
}


sub editAnnouncements {
	my $announcements = &returnAllArrayElements(0,"",openFile("../var/Announcements/Announcements.txt"));
	my $announcementEdit = &parseTemplate($skinDir."editAnnouncements.html","",-1);
	$announcementEdit =~ s/\[announcements\]/$announcements/gi;
	print $announcementEdit;
}

sub doEditAnnouncements {
	&checkLevel(3);
	open(FILE,"> ../var/Announcements/Announcements.txt");
	print FILE $query->param('announcements');
	close(FILE);
	print &parseTemplate($skinDir."editedAnnouncements.html","",-1);
}

sub profileAdmin {
	&checkLevel(3);
	my $parsedThemes = &parseTemplate($skinDir."adminProfile.html","",-1);
	my $passedUsername = $query->param('usr');
	my %userVariables = getUserSettingHash($passedUsername);
	my $selectList;
	my %userDescriptions = (1,"Poster",2,"Moderator",3,"Administrator");
	my $userLevels = 1;
	my $thisUserLevel = $userVariables{userlevel};
	while ($userLevels <= 3) {
		if ($thisUserLevel == $userLevels) {
			$selectList .= "<option value=".$userLevels." selected>".$userDescriptions{$userLevels}."</option>";
		}
		else {
			$selectList .= "<option value=".$userLevels.">".$userDescriptions{$userLevels}."</option>";
		}
		$userLevels++;
	}

	$userVariables{Profile} = escapeFromHex($userVariables{Profile});
	$parsedThemes =~ s/\[var userInfo=(.*?)\]/$userVariables{strtolower($1)}/gi;
	
	my $passedUserName = strtolower($query->param('usr'));

	$parsedThemes =~ s/\[var userParam]/$passedUserName/gi;

	$parsedThemes =~ s/\[controlPanel addOption=userLevel\]/$selectList/gi;

	print $parsedThemes;

}

sub profileModeratorChooseUser {
	my $parsedThemes = &parseTemplate($skinDir."modChooseUser.html","",-1);
	my $userList = getUserList();
	$parsedThemes =~ s/\[controlPanel addOption=users\]/$userList/gi;

	print $parsedThemes;
}

sub profileAdminChooseUser {
	my $parsedThemes = &parseTemplate($skinDir."adminChooseUser.html","",-1);
	my $userList = getUserList();
	$parsedThemes =~ s/\[controlPanel addOption=users\]/$userList/gi;

	print $parsedThemes;
}

sub changeProfile {
	my $userName = &getUserName;
	if (($query->param('usr')) && ($userLevel >= 3)) {
		$userName = $query->param('usr');
		writeUserSetting("UserLevel",$query->param('userLevel'),$userName);
	}
	my $alias = $query->param('FriendlyName');
	my $email = $query->param('Email');
	my $profile = escapeToHex($query->param('profile'));

	writeUserSetting("Profile",$profile,$userName);
	writeUserSetting("FriendlyName",$alias,$userName);
	writeUserSetting("Email",$email,$userName);

	print &parseTemplate($skinDir."profileUpdated.html","",-1);
}

sub profile {
	my $toParse = &parseTemplate($skinDir."editProfile.html","",-1);
	my %userVariables = getUserSettingHash();
	$userVariables{profile} = escapeFromHex($userVariables{profile});
	$toParse =~ s/\[var userInfo=(.*?)\]/$userVariables{strtolower($1)}/gi;
	print $toParse;
	
}

sub resetpassword {
	&checkLevel(3);
	my $parsedThemes = &parseTemplate($skinDir."resetpassword.html","",-1);

	my $userList = getUserList();
	
	$parsedThemes =~ s/\[controlPanel addOption=users\]/$userList/gi;

	print $parsedThemes;
}

sub changePass {
	if ((encrypt($query->param('oldPass')) ne &getUserSetting("Password")) && ($userLevel < 3)) {
		&error("Your old password does not match the one in our records. Please try again.");
	}
	elsif ($query->param('pass1') ne $query->param('pass2')) {
		&error("Your two new passwords do not match. Please try again");
	}
	elsif ($query->param('pass1') eq "") {
		&error("You haven't entered a new password. Please try again");
	}
	else {
		my $encPass = encrypt($query->param('pass1'));

		if (($userLevel == 3) && ($query->param('usr'))) {
			my $userFile = $startingPath."usr/".$query->param('usr').".txt";
			writeSetting($userFile,"Password",$encPass);
		} 
		else {
			writeUserSetting("Password",$encPass);
		}
		print &parseTemplate($skinDir."password-changed.html","",-1);
	}

}

sub password {
	print &parseTemplate($skinDir."password.html","",-1);
}

sub changeTheme {
	writeUserSetting("Template",$query->param('theme'));
	print "Location: controlPanel\n\n";
}

sub getUserList {
	my $userDir = $startingPath."usr/";
	
	opendir(DIR,$userDir);
		my @users = readdir(DIR);
	closedir(DIR);

	my $userList;

	foreach my $user (@users) {
		if ($user =~ m/(.*?)\.txt/gi) {
			my ($name, $null) = split(/\./,$user);
			$userList .= "<option value=\"$name\">".$name."</option>";
		}
	}
	
	return $userList;

}

sub themes {
	my $parsedThemes = &parseTemplate($skinDir."themes.html","",-1);

	my $themeDir = $startingPath."etc/themes";

	opendir(DIR,$themeDir);
		my @themes = readdir(DIR);
	closedir(DIR);

	my $themeList;

	foreach my $theme (@themes) {

		my $themeDesc = $themeDir."/".$theme."/theme.txt";
		open(FILE,$themeDesc);
			$themeDesc = <FILE>;
		close(FILE);
		$themeDesc = $theme unless $themeDesc;
		my $checked = " selected" if ($theme eq getUserSetting("Template"));
		$themeList .= "<option value=\"$theme\"$checked>$themeDesc</option>\n" unless (($theme eq "..") || ($theme eq ".") || ($themeDesc =~ m/\*\*\*HIDETHEME\*\*\*/gi));
	}

	$parsedThemes =~ s/\[controlPanel addOption=themes\]/$themeList/gi;
	print $parsedThemes;

}


sub controlPanel {
	print &parseTemplate($skinDir."controlPanel.html","",-1);
	if ($userLevel == 2) {
		print &parseTemplate($skinDir."moderator-controlPanel.html","",-1);
	}
	elsif ($userLevel == 3) {
		print &parseTemplate($skinDir."administrator-controlPanel.html","",-1);
	}
	print &parseTemplate($skinDir."poster-controlPanel.html","",-1);
}

&printTemplate("bot-template.html") unless ($query->param('area') eq 'changeTheme');

