ALTER TABLE `users_registerprofile` CHANGE COLUMN `name` `display_name` varchar(255) NOT NULL;

ALTER TABLE `users_userprofile` ADD COLUMN `display_name` varchar(255) NOT NULL;
