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

Waffle provides three context managers (that can also be used as
decorators) in ``waffle.testutils`` that make testing easier.

- ``override_flag``
- ``override_sample``
- ``override_switch``

All three are used the same way::

    with override_flag('flag_name', active=True):
        # Only 'flag_name' is affected, other flags behave normally.
        assert waffle.flag_is_active(request, 'flag_name')

Or::

    @override_sample('sample_name', active=True)
    def test_with_sample():
        # Only 'sample_name' is affected, and will always be True. Other
        # samples behave normally.
        assert waffle.sample_is_active('sample_name')

All three will restore the relevant flag, sample, or switch to its
previous state: they will restore the old values and will delete objects
that did not exist.


External test suites
====================

Tests that run in a separate process, such as Selenium tests, may not
have access to the test database or the ability to mock Waffle values.

For tests that make HTTP requests to the system-under-test (e.g. with
Selenium_ or PhantomJS_) the ``WAFFLE_OVERRIDE`` :ref:`setting
<starting-configuring>` makes it possible to control the value of any
*Flag* via the querystring.

.. highlight:: http

For example, for a flag named ``foo``, we can ensure that it is "on" for
a request::

    GET /testpage?foo=1 HTTP/1.1

or that it is "off"::

    GET /testpage?foo=0 HTTP/1.1


.. _mock: http://pypi.python.org/pypi/mock/
.. _fudge: http://farmdev.com/projects/fudge/
.. _Selenium: http://www.seleniumhq.org/
.. _PhantomJS: http://phantomjs.org/
