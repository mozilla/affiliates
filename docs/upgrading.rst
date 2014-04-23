Upgrading from Affiliates 1.0
=============================

There are a few manual steps required to upgrade an instance of Affiliates v1.0
(tagged as v1.0) to the next version.

1. Migrate to new Data Model
----------------------------

1. Create a copy of your old database and add it to your MySQL instance. Edit
   ``affiliates/settings.local.py`` to add this copy to the ``DATABASES``
   setting under the name ``oldbackup``.

2. Merge/checkout up to the latest commit.

3. Manually edit the database and remove tables from the ``banners``,
   ``badges``, and ``news`` apps (these tables start with the app name and an
   underscore, e.g. ``banners_bannerinstance``).

4. Run fake migrations to reset the ``banners`` app and then re-run the
   migrations for create tables for the ``links`` app and ``banners`` app:

   .. code-block:: sh

      ./manage.py migrate --fake --delete-ghost-migrations banners zero
      ./manage.py migrate --delete-ghost-migrations

5. Run the data migration command, passing in the name you used for the backup
   database:

   .. code-block:: sh

      ./manage.py migrate_v1_links oldbackup

At this point your database should be migrated successfully. You should look
through the data to ensure that it has been migrated properly, and keep a
backup of your old data in case you ever find an issue with the new data.
