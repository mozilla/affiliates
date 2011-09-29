ALTER TABLE `banners_bannerimage` ADD COLUMN `locale` varchar(32) NOT NULL;

/* Update locale field in user profile table to match. */

ALTER TABLE `users_userprofile` CHANGE `locale` `locale` varchar(32) NOT NULL;
