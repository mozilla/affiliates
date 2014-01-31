# How to Contribute

Welcome, and thanks for considering contributing! In order to make our
review/development process easier, we have some guidelines to help you figure
out how to contribute to Affiliates.


## Reporting Issues

We use [Bugzilla][] to track issues and bugs for Firefox Affiliates. Any issues
with the website should be filed under the Firefox Affiliates product.

[Bugzilla]: https://bugzilla.mozilla.org/describecomponents.cgi?product=Firefox%20Affiliates


## Terminology

<dl>
  <dt>Mothership</dt>
  <dd>
    The main portion of the Affiliates website, accessible at
    https://affiliates.mozilla.org.
  </dd>
  <dt>Social Integration / Facebook App</dt>
  <dd>
    Facebook app implemented in the `facebook` Django app that links with the
    mothership for certain stats.
  </dd>
  <dt>Banner</dt>
  <dd>
    An image link, text link, or other type of link that users can generate
    using Affiliates.
  </dd>
</dl>


## Development Guidelines

* Servers pull code from `master`. Development should happen in feature branches
  and pull requests should merge back to `master` except in special cases.
* Python code should be covered by unit tests. JavaScript code is covered by
  either [end-to-end tests][] or by manual testing.
* Python code should follow Mozilla's [general Webdev guidelines](py-bootcamp).
  The same goes for our [JavaScript guidelines](js-bootcamp) and
  [CSS guidelines](css-bootcamp).
  * As allowed by PEP8, we use 99-characters-per-line for Python code and
    72-characters-per-line for documentation/comments. Feel free to break these
    guidelines for readability if necessary.
* Affiliates is based on [Playdoh][]. The [Playdoh Documentation][] explain
  the features of Playdoh and how to develop a site based on it.

[end-to-end tests]: https://github.com/mozilla/Affiliates-Tests
[py-bootcamp]: http://mozweb.readthedocs.org/en/latest/coding.html#python
[js-bootcamp]: http://mozweb.readthedocs.org/en/latest/js-style.html#js-style
[css-bootcamp]: http://mozweb.readthedocs.org/en/latest/css-style.html
[Playdoh]: https://github.com/mozilla/playdoh/
[Playdoh Documentation]: http://playdoh.readthedocs.org/en/latest/


## Adding a Library

Due to licensing and deployment constraints, adding a library to Affiliates
requires a few things:

1. Add the library to the requirements files in the `requirements` folder.
   `prod.txt` is for libraries required in production, `dev.txt` is for
   libraries required for local development or running tests, and
   `compiled.txt` is for libraries that need to be compiled.
2. If the library isn't compiled, install it in `vendor-local` using the
   following Pip command (assuming we want to install the `chocobo` library from
   PyPI):

   ```sh
   pip install --no-install --build=vendor-local/packages -I chocobo
   ```
3. Add the path to your newly installed package to `vendor-local/vendor.pth`.
   For example, if it was installed in `vendor-local/packages/chocobo`, you'd
   add the line `pacakages/chocobo` to `vendor.pth`.

**Note:** Keep the installation changes in a separate commit from the rest of
your work to make code review easier.


## Additional Resources

* IRC: #affiliates on [irc.mozilla.org](https://wiki.mozilla.org/IRC).
* Planning/roadmap/meetings: [Affiliates on MozillaWiki](https://wiki.mozilla.org/Websites/Affiliates)
* [What is deployed on Affiliates servers?](http://mzl.la/affiliates-deployed)
