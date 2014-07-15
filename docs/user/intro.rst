Introduction
============

What is Firefox Affiliates?
---------------------------
Firefox Affiliates is a website that allows users to generate **links** that can
be embedded on a website. Affiliates then measures the number of people
clicking on these links and logs that data for the user who generated the
link.

Administrators of Firefox Affiliates create things called **banners**, which
serve as templates that users generate links from. There are several types of
banners:

- **Image banners**, which show an image link when embedded.
- **Text banners**, which show a text link when embedded.
- **Update banners**, which show an image link when embedded. The image shown
  changes if the user has an up-to-date version of Firefox installed or not.

Banners are organized under **categories** and **subcategories**. When you go
through the link generation flow, the first step is to choose a category.
Within each category is a set of banners to choose from. Once you've chosen a
banner, you must choose which **variation** of the banner to use. Variations
are all related to the same subject (and thus are part of the same banner),
but vary in size, color, and language.


What data does Firefox Affiliates store?
----------------------------------------
For each link that a user generates, Affiliates stores the number of times
someone has followed the link, called **link clicks**. The number of link
clicks per day is stored for the past 90 days from the present. After 90 days,
the link click count is aggregated into a single count of the total link clicks
for the link since it was created.

In practice, what this means is that *per-day link click counts for any link
are only available for the past 90 days*. If you wanted the total link clicks
for a date more than 90 days in the past, you're out of luck!

The total number link clicks since a link was created is always available, of
course.
