BEGIN;
CREATE TABLE `auth_permission` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(50) NOT NULL,
    `content_type_id` integer NOT NULL,
    `codename` varchar(100) NOT NULL,
    UNIQUE (`content_type_id`, `codename`)
)
;
CREATE TABLE `auth_group_permissions` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `group_id` integer NOT NULL,
    `permission_id` integer NOT NULL,
    UNIQUE (`group_id`, `permission_id`)
)
;
ALTER TABLE `auth_group_permissions` ADD CONSTRAINT `permission_id_refs_id_a7792de1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);
CREATE TABLE `auth_group` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(80) NOT NULL UNIQUE
)
;
ALTER TABLE `auth_group_permissions` ADD CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);
CREATE TABLE `auth_user_user_permissions` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `permission_id` integer NOT NULL,
    UNIQUE (`user_id`, `permission_id`)
)
;
ALTER TABLE `auth_user_user_permissions` ADD CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);
CREATE TABLE `auth_user_groups` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `group_id` integer NOT NULL,
    UNIQUE (`user_id`, `group_id`)
)
;
ALTER TABLE `auth_user_groups` ADD CONSTRAINT `group_id_refs_id_f0ee9890` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);
CREATE TABLE `auth_user` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `username` varchar(30) NOT NULL UNIQUE,
    `first_name` varchar(30) NOT NULL,
    `last_name` varchar(30) NOT NULL,
    `email` varchar(75) NOT NULL,
    `password` varchar(255) NOT NULL,
    `is_staff` bool NOT NULL,
    `is_active` bool NOT NULL,
    `is_superuser` bool NOT NULL,
    `last_login` datetime NOT NULL,
    `date_joined` datetime NOT NULL
)
;
ALTER TABLE `auth_user_user_permissions` ADD CONSTRAINT `user_id_refs_id_f2045483` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `auth_user_groups` ADD CONSTRAINT `user_id_refs_id_831107f1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `auth_message` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `message` longtext NOT NULL
)
;
ALTER TABLE `auth_message` ADD CONSTRAINT `user_id_refs_id_9af0b65a` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE INDEX `auth_permission_e4470c6e` ON `auth_permission` (`content_type_id`);
CREATE INDEX `auth_message_fbfc09f1` ON `auth_message` (`user_id`);
COMMIT;
BEGIN;
CREATE TABLE `django_content_type` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(100) NOT NULL,
    `app_label` varchar(100) NOT NULL,
    `model` varchar(100) NOT NULL,
    UNIQUE (`app_label`, `model`)
)
;
ALTER TABLE `auth_permission` ADD CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);
COMMIT;
BEGIN;
CREATE TABLE `django_site` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `domain` varchar(100) NOT NULL,
    `name` varchar(50) NOT NULL
)
;
COMMIT;
BEGIN;
CREATE TABLE `djcelery_intervalschedule` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `every` integer NOT NULL,
    `period` varchar(24) NOT NULL
)
;
CREATE TABLE `djcelery_crontabschedule` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `minute` varchar(64) NOT NULL,
    `hour` varchar(64) NOT NULL,
    `day_of_week` varchar(64) NOT NULL
)
;
CREATE TABLE `djcelery_periodictasks` (
    `ident` smallint NOT NULL PRIMARY KEY,
    `last_update` datetime NOT NULL
)
;
CREATE TABLE `djcelery_periodictask` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(200) NOT NULL UNIQUE,
    `task` varchar(200) NOT NULL,
    `interval_id` integer,
    `crontab_id` integer,
    `args` longtext NOT NULL,
    `kwargs` longtext NOT NULL,
    `queue` varchar(200),
    `exchange` varchar(200),
    `routing_key` varchar(200),
    `expires` datetime,
    `enabled` bool NOT NULL,
    `last_run_at` datetime,
    `total_run_count` integer UNSIGNED NOT NULL,
    `date_changed` datetime NOT NULL
)
;
ALTER TABLE `djcelery_periodictask` ADD CONSTRAINT `crontab_id_refs_id_ebff5e74` FOREIGN KEY (`crontab_id`) REFERENCES `djcelery_crontabschedule` (`id`);
ALTER TABLE `djcelery_periodictask` ADD CONSTRAINT `interval_id_refs_id_f2054349` FOREIGN KEY (`interval_id`) REFERENCES `djcelery_intervalschedule` (`id`);
CREATE TABLE `djcelery_workerstate` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `hostname` varchar(255) NOT NULL UNIQUE,
    `last_heartbeat` datetime
)
;
CREATE TABLE `djcelery_taskstate` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `state` varchar(64) NOT NULL,
    `task_id` varchar(36) NOT NULL UNIQUE,
    `name` varchar(200),
    `tstamp` datetime NOT NULL,
    `args` longtext,
    `kwargs` longtext,
    `eta` datetime,
    `expires` datetime,
    `result` longtext,
    `traceback` longtext,
    `runtime` double precision,
    `worker_id` integer,
    `hidden` bool NOT NULL
)
;
ALTER TABLE `djcelery_taskstate` ADD CONSTRAINT `worker_id_refs_id_4e3453a` FOREIGN KEY (`worker_id`) REFERENCES `djcelery_workerstate` (`id`);
CREATE INDEX `djcelery_periodictask_17d2d99d` ON `djcelery_periodictask` (`interval_id`);
CREATE INDEX `djcelery_periodictask_7aa5fda` ON `djcelery_periodictask` (`crontab_id`);
CREATE INDEX `djcelery_workerstate_eb8ac7e4` ON `djcelery_workerstate` (`last_heartbeat`);
CREATE INDEX `djcelery_taskstate_52094d6e` ON `djcelery_taskstate` (`name`);
CREATE INDEX `djcelery_taskstate_f0ba6500` ON `djcelery_taskstate` (`tstamp`);
CREATE INDEX `djcelery_taskstate_20fc5b84` ON `djcelery_taskstate` (`worker_id`);
COMMIT;
BEGIN;
CREATE TABLE `users_userprofile` (
    `user_id` integer NOT NULL PRIMARY KEY,
    `created` datetime NOT NULL,
    `modified` datetime NOT NULL,
    `name` varchar(255) NOT NULL,
    `email` varchar(75) NOT NULL UNIQUE,
    `address_1` varchar(255),
    `address_2` varchar(255),
    `city` varchar(255),
    `state` varchar(255),
    `locale` varchar(7) NOT NULL,
    `country` varchar(2) NOT NULL,
    `accept_email` bool NOT NULL
)
;
CREATE TABLE `users_registerprofile` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `activation_key` varchar(40) NOT NULL,
    `name` varchar(255) NOT NULL,
    `email` varchar(75) NOT NULL UNIQUE,
    `password` varchar(255) NOT NULL,
    `user_id` integer UNIQUE
)
;
ALTER TABLE `users_userprofile` ADD CONSTRAINT `user_id_refs_id_d653ba24` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `users_registerprofile` ADD CONSTRAINT `user_id_refs_id_2e4278d2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;
