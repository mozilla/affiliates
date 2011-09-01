BEGIN;

DROP TABLE `banners_banner`;
DROP TABLE `banners_bannerimage`;
DROP TABLE `banners_bannerinstance`;

CREATE TABLE `banners_banner` (
    `badge_ptr_id` integer NOT NULL PRIMARY KEY
)
;
CREATE TABLE `banners_bannerimage` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `banner_id` integer NOT NULL,
    `size` varchar(20) NOT NULL,
    `color` varchar(20) NOT NULL,
    `image` varchar(250) NOT NULL
)
;
ALTER TABLE `banners_bannerimage` ADD CONSTRAINT `banner_id_refs_badge_ptr_id_8d816f3d` FOREIGN KEY (`banner_id`) REFERENCES `banners_banner` (`badge_ptr_id`);
CREATE TABLE `banners_bannerinstance` (
    `badgeinstance_ptr_id` integer NOT NULL PRIMARY KEY,
    `image_id` integer NOT NULL
)
;
ALTER TABLE `banners_bannerinstance` ADD CONSTRAINT `image_id_refs_id_9a6082f4` FOREIGN KEY (`image_id`) REFERENCES `banners_bannerimage` (`id`);
CREATE INDEX `banners_bannerimage_50ab1ff4` ON `banners_bannerimage` (`banner_id`);
CREATE INDEX `banners_bannerinstance_6682136` ON `banners_bannerinstance` (`image_id`);

CREATE TABLE `badges_badge` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `child_type` varchar(255) NOT NULL,
    `name` varchar(255) NOT NULL,
    `subcategory_id` integer NOT NULL,
    `preview_img` varchar(250) NOT NULL,
    `href` varchar(200) NOT NULL
)
;
ALTER TABLE `badges_badge` ADD CONSTRAINT `subcategory_id_refs_id_6c7aad94` FOREIGN KEY (`subcategory_id`) REFERENCES `badges_subcategory` (`id`);
CREATE TABLE `badges_badgeinstance` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `child_type` varchar(255) NOT NULL,
    `created` datetime NOT NULL,
    `user_id` integer NOT NULL,
    `badge_id` integer NOT NULL
)
;
ALTER TABLE `badges_badgeinstance` ADD CONSTRAINT `badge_id_refs_id_6f655f7e` FOREIGN KEY (`badge_id`) REFERENCES `badges_badge` (`id`);
ALTER TABLE `badges_badgeinstance` ADD CONSTRAINT `user_id_refs_id_ae3bd08f` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `badges_clickstats` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `badge_instance_id` integer NOT NULL,
    `month` integer NOT NULL,
    `year` integer NOT NULL,
    `clicks` integer NOT NULL,
    UNIQUE (`badge_instance_id`, `month`, `year`)
)
;

ALTER TABLE `banners_banner` ADD CONSTRAINT `badge_ptr_id_refs_id_c467fa8d` FOREIGN KEY (`badge_ptr_id`) REFERENCES `badges_badge` (`id`);
ALTER TABLE `banners_bannerinstance` ADD CONSTRAINT `badgeinstance_ptr_id_refs_id_2899f6ad` FOREIGN KEY (`badgeinstance_ptr_id`) REFERENCES `badges_badgeinstance` (`id`);

ALTER TABLE `badges_clickstats` ADD CONSTRAINT `badge_instance_id_refs_id_1b6aeead` FOREIGN KEY (`badge_instance_id`) REFERENCES `badges_badgeinstance` (`id`);
CREATE INDEX `badges_badge_913b3835` ON `badges_badge` (`subcategory_id`);
CREATE INDEX `badges_badgeinstance_fbfc09f1` ON `badges_badgeinstance` (`user_id`);
CREATE INDEX `badges_badgeinstance_80db5b24` ON `badges_badgeinstance` (`badge_id`);
CREATE INDEX `badges_clickstats_7196040b` ON `badges_clickstats` (`badge_instance_id`);
COMMIT;
