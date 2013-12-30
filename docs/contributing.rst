.. _contributing-chapter:

======================
Contributing to Waffle
======================

Waffle is pretty simple to hack, and has a decent test suite! Here's how to
hack Waffle, add tests, run them, and contribute changes.


Set Up
======

Setting up an environment is easy! You'll want ``virtualenv`` and ``pip``, then
just create a new virtual environment and install the requirements::

    $ mkvirtualenv waffle
    $ pip install -r requirements.txt

Done!


Running Things
==============

Waffle comes with a helper shell script to run tests and create schema
migrations: ``run.sh``. To run the tests, just::

    $ ./run.sh test

Run the script with no arguments to see all the options.


Writing Patches
===============

Patches should have tests. And follow PEP-8/existing styles. That's about it!
If you need help writing or running tests, let me know!

I will probably run your tests with and without the rest of the patch.


Submitting Patches
==================

Open a pull request on GitHub! If you want to make sure I'll merge the patch
upstream, open an issue first to discuss it.
