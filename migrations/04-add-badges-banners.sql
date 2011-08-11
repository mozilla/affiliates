BEGIN;
CREATE TABLE `django_admin_log` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `action_time` datetime NOT NULL,
    `user_id` integer NOT NULL,
    `content_type_id` integer,
    `object_id` longtext,
    `object_repr` varchar(200) NOT NULL,
    `action_flag` smallint UNSIGNED NOT NULL,
    `change_message` longtext NOT NULL
)
;
ALTER TABLE `django_admin_log` ADD CONSTRAINT `user_id_refs_id_c8665aa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `django_admin_log` ADD CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);
CREATE INDEX `django_admin_log_fbfc09f1` ON `django_admin_log` (`user_id`);
CREATE INDEX `django_admin_log_e4470c6e` ON `django_admin_log` (`content_type_id`);

CREATE TABLE `badges_category` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(255) NOT NULL
)
;

CREATE TABLE `badges_subcategory` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `parent_id` integer NOT NULL,
    `name` varchar(255) NOT NULL,
    `preview_img` varchar(250) NOT NULL
)
;
ALTER TABLE `badges_subcategory` ADD CONSTRAINT `parent_id_refs_id_246a2df6` FOREIGN KEY (`parent_id`) REFERENCES `badges_category` (`id`);
CREATE INDEX `badges_subcategory_63f17a16` ON `badges_subcategory` (`parent_id`);

CREATE TABLE `banners_banner` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(255) NOT NULL,
    `subcategory_id` integer NOT NULL,
    `preview_img` varchar(250) NOT NULL
)
;
ALTER TABLE `banners_banner` ADD CONSTRAINT `subcategory_id_refs_id_ec76f334` FOREIGN KEY (`subcategory_id`) REFERENCES `badges_subcategory` (`id`);

CREATE TABLE `banners_bannerimage` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `banner_id` integer NOT NULL,
    `size` varchar(20) NOT NULL,
    `color` varchar(20) NOT NULL,
    `image` varchar(250) NOT NULL
)
;
ALTER TABLE `banners_bannerimage` ADD CONSTRAINT `banner_id_refs_id_8d816f3d` FOREIGN KEY (`banner_id`) REFERENCES `banners_banner` (`id`);

CREATE TABLE `banners_bannerinstance` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `created` datetime NOT NULL,
    `modified` datetime NOT NULL,
    `banner_id` integer NOT NULL,
    `image_id` integer NOT NULL
)
;
ALTER TABLE `banners_bannerinstance` ADD CONSTRAINT `image_id_refs_id_9a6082f4` FOREIGN KEY (`image_id`) REFERENCES `banners_bannerimage` (`id`);
ALTER TABLE `banners_bannerinstance` ADD CONSTRAINT `user_id_refs_id_b973abe9` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `banners_bannerinstance` ADD CONSTRAINT `banner_id_refs_id_ebcf3362` FOREIGN KEY (`banner_id`) REFERENCES `banners_banner` (`id`);
CREATE INDEX `banners_banner_913b3835` ON `banners_banner` (`subcategory_id`);
CREATE INDEX `banners_bannerimage_50ab1ff4` ON `banners_bannerimage` (`banner_id`);
CREATE INDEX `banners_bannerinstance_fbfc09f1` ON `banners_bannerinstance` (`user_id`);
CREATE INDEX `banners_bannerinstance_50ab1ff4` ON `banners_bannerinstance` (`banner_id`);
CREATE INDEX `banners_bannerinstance_6682136` ON `banners_bannerinstance` (`image_id`);

CREATE TABLE `django_session` (
    `session_key` varchar(40) NOT NULL PRIMARY KEY,
    `session_data` longtext NOT NULL,
    `expire_date` datetime NOT NULL
)
;
CREATE INDEX `django_session_c25c2c28` ON `django_session` (`expire_date`);
COMMIT;