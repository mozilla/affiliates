CREATE TABLE `badges_badgelocale` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `locale` varchar(32) NOT NULL,
    `badge_id` integer NOT NULL
)
;
ALTER TABLE `badges_badgelocale` ADD CONSTRAINT `badge_id_refs_id_3c2e885b` FOREIGN KEY (`badge_id`) REFERENCES `badges_badge` (`id`);
