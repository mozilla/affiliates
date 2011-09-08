BEGIN;
CREATE TABLE `badges_leaderboard` (
    `ranking` integer UNSIGNED NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `clicks` integer UNSIGNED NOT NULL
);
ALTER TABLE `badges_leaderboard` ADD CONSTRAINT `user_id_refs_id_84a206a2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE INDEX `badges_leaderboard_fbfc09f1` ON `badges_leaderboard` (`user_id`);
COMMIT;
