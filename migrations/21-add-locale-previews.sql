-- Get rid of old preview images
ALTER TABLE `badges_subcategory` DROP COLUMN `preview_img`;
ALTER TABLE `badges_badge` DROP COLUMN `preview_img`;


-- Add in new preview image tables
CREATE TABLE `badges_badgepreview` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `image` varchar(250) NOT NULL,
    `locale` varchar(32) NOT NULL,
    `badge_id` integer NOT NULL,
    UNIQUE (`locale`, `badge_id`)
);
ALTER TABLE `badges_badgepreview` ADD CONSTRAINT `badge_id_refs_id_ac77c140` FOREIGN KEY (`badge_id`) REFERENCES `badges_badge` (`id`);
CREATE INDEX `badges_badgepreview_80db5b24` ON `badges_badgepreview` (`badge_id`);
