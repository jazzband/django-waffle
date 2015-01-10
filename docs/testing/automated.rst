.. _testing-automated:

=============================
Automated testing with Waffle
=============================

Feature flags present a new challenge for writing tests. The test
database may not have Flags, Switches, or Samples defined, or they may
be non-deterministic.

My philosophy, and one I encourage you to adopt, is that tests should
cover *both* code paths, with any feature flags on and off. To do
this, you'll need to make the code behave deterministically.

Here, I'll cover some tips and best practices for testing your app
while using feature flags. I'll talk specifically about Flags but this
can equally apply to Switches or Samples.


Unit tests
==========

Flags may be non-deterministic by nature. Who is making the request?
Is the Flag defined? Is it a dice-roll or a roll-out? These make
testing difficult.  There are a few strategies for making Flags behave
deterministically.


Create the Flag
---------------

The simplest option is to create the Flag with some deterministic
options, for example::

    from waffle.models import Flag
    Flag.objects.create(name='foo', everyone=True)

Because the ``Flag.everyone`` property makes the Flag predictable, you
can use it in tests to guarantee one code-path or the other is hit.


Mocking ``flag_is_active``
--------------------------

Creating the flag may not always be possible or the best option. You
can also use a library like Mock_ or Fudge_ to mock other parts of the
chain. For example::

    # tests.py
    from module import views  # Imports waffle
    import mock

    @mock.patch.object(views.waffle, 'flag_is_active')
    def test_something(flag_is_active):
        flag_is_active.return_value = True
        views.some_view()  # Will behave as if *every* Flag is True.

The downside of mocking methods like ``flag_is_active`` is that
*every* Flag will come back with the same value. That might be fine
for some situations.


Mocking Template Helpers
------------------------

Waffle's template helpers for Django or Jinja require some special
mocking. For Jinja::

    import mock
    import waffle.helpers

    @mock.patch.object(waffle.helpers, 'flag_is_active')
    def test_something(flag_is_active):
        flag_is_active.return_value = True

Or for Django::

    import mock
    from waffle.templatetags import waffle_tags

    @mock.patch.object(waffle_tags, 'flag_is_active')
    def test_something(flag_is_active):
        flag_is_active.return_value = True


External test suites
====================

Tests that run in a separate process, such as Selenium tests, may not
have access to the test database or the ability to mock Waffle values.

For tests that make HTTP requests to the system-under-test (e.g. with
Selenium_ or PhantomJS_) the ``WAFFLE_OVERRIDE`` :ref:`setting
<starting-configuring>` makes it possible to control the value of any
*Flag* via the querystring.

For example, for a flag named ``foo``, we can ensure that it is "on" for
a request::

    GET /testpage?foo=1 HTTP/1.1

or that it is "off"::

    GET /testpage?foo=0 HTTP/1.1


.. _mock: http://pypi.python.org/pypi/mock/
.. _fudge: http://farmdev.com/projects/fudge/
.. _Selenium: http://www.seleniumhq.org/
.. _PhantomJS: http://phantomjs.org/
