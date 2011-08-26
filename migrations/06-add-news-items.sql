BEGIN;
CREATE TABLE `news_newsitem` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `created` datetime NOT NULL,
    `modified` datetime NOT NULL,
    `title` varchar(255) NOT NULL,
    `content` longtext NOT NULL,
    `enabled` bool NOT NULL
)
;
COMMIT;
