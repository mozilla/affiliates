Installing Firefox Affiliates
=============================

Installation
------------

These instructions assume you have ``git`` and ``pip`` installed. If you don't
have ``pip`` installed, you can install it with ``easy_install pip``.

1. Start by getting the source::

    $ git clone --recursive git://github.com/mozilla/affiliates.git
    $ cd affiliates

.. note:: Make sure you use ``--recursive`` when checking the repo out! If you
   didn't, you can load all the submodules with ``git submodule update --init
   --recursive``.

2. Create a virtual environment for the libraries. Skip the first step if you
   already have ``virtualenv`` installed::

    $ pip install virtualenv
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements/dev.txt

.. note:: The adventurous may prefer to use virtualenvwrapper_ instead of
   manually creating a virtualenv.

3. Set up a local MySQL database. The `MySQL Installation Documentation`_
   explains this fairly well.

4. Configure your local settings by copying
   ``affiliates/settings/local.py-dist`` to ``affiliates/settings/local.py``
   and customizing the settings in it::

    $ cp affiliates/settings/local.py-dist affiliates/settings/local.py

   The file is commented to explain what each setting does and how to customize
   them.

5. Download the latest product_details JSON files::

    $ python manage.py update_product_details

6. Initialize your database structure::

    $ python manage.py syncdb
    $ python manage.py migrate

7. Install Stylus_. If you have npm_ set up, just run::

    $ npm install -g stylus

.. note:: You may have to set the ``STYLUS_BIN`` setting to point towards the
   stylus binary if it doesn't end up on your path after installation.

.. _stylus: http://learnboost.github.io/stylus/
.. _npm: https://www.npmjs.org/

Running the Development Server
------------------------------

You can launch the development server like so::

    $ python manage.py runserver

Localization
------------

If you want to set up localization, check out the locale repo using svn::

    $ git svn clone https://svn.mozilla.org/projects/l10n-misc/trunk/affiliates/locale/ locale
    # or
    $ svn checkout https://svn.mozilla.org/projects/l10n-misc/trunk/affiliates/locale/ locale

.. _virtualenvwrapper: http://www.doughellmann.com/projects/virtualenvwrapper/
.. _MySQL Installation Documentation: http://dev.mysql.com/doc/refman/5.6/en/installing.html

Developing the Facebook App
---------------------------

If you want to work on the Facebook app side of Affiliates, you'll need to
create a development app on Facebook using your Facebook account.

1. Visit https://developers.facebook.com and click the Apps menu item in the top
   bar.

2. Click the "Create New App" button (might be slightly different if you haven't
   created an app before).

3. Give your app a name and unique namespace, like ``username_fxaffiliates``.

4. On the following App Basic Details page, check the "App on Facebook" option.
   Your settings will most likely be:

   * Canvas URL: http://localhost:8000/fb/
   * Secure Canvas URL: https://localhost:8000/fb/
   * Canvas Width: Fluid
   * Canvas Height: Fluid

5. Edit ``settings/local.py``. There should be several settings that start with
   ``FACEBOOK`` that you will need to fill in.

.. note:: The ``FACEBOOK_DEBUG`` and ``FACEBOOK_DEBUG_USER_ID`` settings are for
   a hack to work on the Facebook app without a test app. Ignore them if you are
   following these steps.

Once the above is done you should be able to start your development server and
view your test Facebook app.

.. note:: Unless you somehow set up HTTPS on your local development server, you
   will only be able to view the app over HTTP.
