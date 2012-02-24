Affiliates
==========

This is the new home for the Mozilla affiliates program.

Deployment Notes
----------------

* Do not run syncdb when setting up a new copy of Affiliates. All database setup is taken care of by schematic migrations.
* Post-push steps:
  * `git submodule update --init` - Update or initialize any new submodules.
  * `./vendor/src/schematic/schematic migrations` - Run new migrations.
  * `manage.py compress_assets` - Generate bundled CSS and JS.

Developer Setup
---------------

0. (Recommended) Set up a virtualenv for the project.
1. `git clone --recursive git://github.com/mozilla/affiliates.git`
2. pip install -r requirements/dev.txt
3. Set up a MySQL Database
4. Copy `settings/local.py-dist` to `settings/local.py` and edit it.
   * Enter the connection info for the database you set up.
   * Set `DEBUG` and `DEV` both to `True`.
5. Run schematic migrations
   * __DO NOT RUN `syncdb`.__ Migrations handle initial setup.
   * You can use the vendor libraries: `./vendor/src/schematic/schematic migrations`
6. `python manage.py runserver`
   * Run `python manage.py createsuperuser` if you want to create an admin account.

Contributing
------------
Patches are welcome! Affiliates is a [playdoh][gh-playdoh]-based web
application.

[gh-playdoh]: https://github.com/mozilla/playdoh


License
-------
This software is licensed under the [New BSD License][BSD]. For more
information, read the file ``LICENSE``.

[BSD]: http://creativecommons.org/licenses/BSD/
