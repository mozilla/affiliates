Fancy Tag
=========

Overview
--------

``fancy_tag`` is a template tag decorator designed to replace Django's built in
``simple_tag`` decorator. It's backwards compatible with ``simple_tag`` and adds
new calling options like named arguments.

Features
--------

* Keyword arguments - arguments can be explicitly assigned to parameter
  specific parameters in the template tag function

* Variable length arguments - The "``*args``" and "``**kwargs``" notation

* The trailing "``as <varname>``" to assign the output of the template tag to
  a variable in the template's context.

Installation
------------

1. Add the fancy_tag package to your Python path


2. Instead of::

    @register.simple_tag
    def some_tag(arg1, arg2):
        return '%s %s' % (arg1, arg2)


   Use::

    @fancy_tag(register)
    def some_tag(arg1, arg2):
        return '%s %s' % (arg1, arg2)

Examples
--------

Keyword Arguments
~~~~~~~~~~~~~~~~~

Python Code::

    @fancy_tag(register)
    def say_cheese(name, thing_to_say='cheese'):
        return 'Hey, %s! Say %s!' % (name, thing_to_say)

Template Code::

    {% say_cheese "Jacob" %} -> "Hey, Jacob! Say Cheese!"
    {% say_cheese "Malcolm" thing_to_say="Vegemite" %} -> "Hey Malcolm! Say Vegemite!"

Variable Length Arguments
~~~~~~~~~~~~~~~~~~~~~~~~~

Python Code::

    @fancy_tag(register)
    def greet_people(*args):
        return 'Hello, %s' % ', '.join(args)


Template Code::

    {% greet_people "Larry" "Darryl" "Darryl" %}

Produces:

Hello, Larry, Darryl, Darryl

Variable Length Keyword Arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python Code::

    @fancy_tag(register)
    def watch_your_mouth(s, **kwargs):
        for key, value in kwargs.items():
            s = s.replace(key, value)
        return s

Template Code::

    {% watch_your_mouth "You damn dirty ape!" "damn"="doggone" "dirty"="handsome" %}

Produces:

You doggone handsome ape!"

Assigning Output To A Variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python Code::

    @fancy_tag(register)
    def now(format_string):
        df = DateFormat(datetime.now())
        return df.format(format_string)

Template Code::

    {% now as just_now %}
    Oh no, it's already {{ just_now }}!

Produces:

Oh no, it's already February 20th, 2010!

Accessing the Template Context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python Code::

    @fancy_tag(register, takes_context)
    def say_hello_to_user(context, phrase):
        return u'%s, %s!' % (phrase, context['user'])

Template Context::

    {'user': 'Tobias'}  # Provided by a template context processor, for example

Template Code::

    {% say_hello_to_user "Hallo" %}

Produces:

Hallo, Tobias!

Testing
-------

With Django in your python path, run ``tests/run_tests.py`` or use 
`tox <http://tox.testrun.org/>`_ to run the tests using multiple
Python and Django versions.

Source
------

http://github.com/trapeze/fancy_tag

License
-------

fancy_tag is Copyright (c) 2010-2012 Sam Bull, Trapeze. It is free software, and
may be redistributed under the terms specified in the LICENSE file.

Credits
-------

fancy_tag is maintained by `Sam Bull <sam@pocketuniverse>`_, with support from
`Trapeze <http://trapeze.com>`_.
