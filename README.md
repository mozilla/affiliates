Affiliates
==========

This is the new home for the Mozilla affiliates program.

Developer Setup
---------------

0. (Recommended) Set up a virtualenv for the project.
1. `git clone --recursive git://github.com/mozilla/affiliates.git`
2. `pip install -r requirements/dev.txt`
3. `pip install -r requirements/compiled.txt`
4. Set up a MySQL Database
5. Copy `settings/local.py-dist` to `settings/local.py` and edit it.
   * Enter the connection info for the database you set up.
   * Set `DEBUG` and `DEV` both to `True`.
6. Create the tables and add the necessary data
   * `python manage.py syncdb`
   * `python manage.py migrate`
   * `python manage.py syncdata fixtures/sites.json`
7. `python manage.py runserver`
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
