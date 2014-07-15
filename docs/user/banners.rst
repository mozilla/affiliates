Banners
=======

A **banner** is a template from which users will generate **links**.
Administrators create banners using the admin interface located at
https://affiliates.mozilla.org/admin/.

There are three types of banners:

- **Image banners**, which show an image link when embedded.
- **Text banners**, which show a text link when embedded.
- **Update banners**, which show an image link when embedded. The image shown
  changes if the user has an up-to-date version of Firefox installed or not.

.. _access-banner-admin:

Accessing the Banner Admin
--------------------------
The steps below describe how to access the admin interface for banners:

1. Open https://affiliates.mozilla.org/admin/ in your browser.

2. If a popup saying "Authentication Required" and "Mozilla Corporation -
   LDAP Required" appears, enter in your Mozilla LDAP credentials and click OK.

3. You will be shown a login form asking for a username and password. These
   Affiliates-specific credentials should have been provided to you by an
   existing admin or developer. Enter the username and password you were given
   and click "Log in".

4. Once logged in, you will see the Admin dashboard. There are several boxes
   with lists of admin panels you can access; the banner admin panels are in
   the box titled "Banners".

Adding Image Banners to Affiliates
----------------------------------
If you want to add a brand new banner to Affiliates, you'll need to gather the
following:

* A name for the banner, and names for any new categories or subcategories that
  need to be created. Since these need to be localized, they need to be chosen
  early and submitted for localization by a developer.

* The URL for the Banner to redirect to.

* The actual images to use for the banner. At least one of these must be
  125x125 pixels, otherwise an empty preview will be shown for the banner on
  the site.

Once you've gathered all these and had the necessary strings translated, you
can upload the banners to the site via the admin interface:

1. Access the :ref:`Banner Admin <access-banner-admin>` using the directions
   above.

2. Enter the Image Banner Admin by clicking the "Image banners" link. Then
   click the button to "Add image banner".

3. Enter the name of the banner, and select the category it belongs under. Note
   that you **must** select a *subcategory*. The select box shows two levels
   of categories, with subcategories being indented underneath their parent
   category.

4. Enter the URL you wish users to be sent to when they click the banner under
   the "Destination" field.

5. Make sure the "Visible" checkbox is checked. If it is unchecked, the banner
   will not show up in the generator on the site.

6. Under the "Image banner variations" section, click the "Add another Image
   Banner Variation" link to add fields for a variation. Select the color and
   locale of the image you're adding, and use the file field to select the
   image file for that variation.

7. Once you have added all the variations for the banner, click the save button
   to submit your changes and save the banner to the database.

Once you've saved the banner, you should log in to the website to check if the
new banner is available, localized, and that you can create links using it
correctly.

Updating Existing Image Banners
-------------------------------
Sometimes, we need to update the image being used in an Image Banner. It is
vital to note: :strong:`any new images must be the same size as the image they
are replacing` [#f1]_.

It is *highly* recommended that, prior to replacing the images, you create some
banners using the images you intend to replace, and copy the embed codes for
them to a test page, like `jsfiddle`_. That way, once you're done, you can go
back and check to see if the replacement worked.

Once you have the new images, you can update the old images via the image
banner admin:

1. Access the :ref:`Banner Admin <access-banner-admin>` using the directions
   above.

2. Enter the Image Banner Admin by clicking the "Image banners" link. Locate
   the banner with the images you need to replace and click it's name to open
   the banner editing page.

3. Search through the list of "Image banner variations" at the bottom of the
   page to find the variations that need to be replaced. You can Ctrl-Click or
   Cmd-Click the image filenames shown in the "Image" column to open the images
   in a new tab and ensure they're the right ones to replace.

4. Use the file input in the "Image" column to select the replacement image for
   each variation that needs to be replaced.

5. Once all the replacements have been selected, click the save button to save
   your changes.

After saving, you should check the website to see that the images have been
updated, as well as checking the old banners you created beforehand to ensure
they've been replaced as well.

.. _jsfiddle: http://jsfiddle.net/
.. [#f1] This is because the filenames used for banner images are generated
         from, among other things, the image size. If the image size changes,
         the filename will change, and people who were using the old image will
         continue to use it instead of getting the updated image.
