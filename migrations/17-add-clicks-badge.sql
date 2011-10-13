ALTER TABLE `badges_badgeinstance` ADD `clicks` INT NOT NULL;

-- Populate the clicks field with existing data
UPDATE `badges_badgeinstance` AS `bi`
SET `clicks` = (
	SELECT SUM(`cs`.`clicks`)
	FROM `badges_clickstats` AS `cs`
	WHERE `bi`.`id` = `cs`.`badge_instance_id`
	GROUP BY `cs`.`badge_instance_id`
);
