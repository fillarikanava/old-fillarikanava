CREATE TABLE `schema_version` (
    `site_id` integer NOT NULL,
    `version` integer NOT NULL,
    `applied` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (`site_id`, `version`)
);

ALTER TABLE `schema_version`
	ADD CONSTRAINT site_id_refs_id FOREIGN KEY (`site_id`) REFERENCES `django_site`(`id`) ON DELETE CASCADE;
