Upgrading from Affiliates 1.0
=============================

There are a few manual steps required to upgrade an instance of Affiliates v1.0
(tagged as v1.0) to the next version.

1. Migrate to new Data Model
----------------------------

1. Merge/checkout up to the tag ``v2.0-migrate-data``. This commit and its
   ancestors contain the data migration scripts that migrate data from the old
   data model to the new one.

2. Run the migrations:

   .. code-block:: sh

      ./manage.py migrate

3. Merge/checkout up to the tag ``v2.0-migrate-remove-models``. This commit
   removes a few apps that had their models deleted in the previous commit.

4. Reset the ``links`` and ``banners`` apps to their new initial migrations
   with the following two commands:

   .. code-block:: sh

      ./manage.py migrate --fake --delete-ghost-migrations links 0001
      ./manage.py migrate --fake --delete-ghost-migrations banners 0001

At this point your database should be through the data migration; you can now
checkout the latest commit on master and run the migrations normally.
