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

Running Django apps without a Django project is a pain, so we use invoke to
pave over all that. Almost everything runs through ``invoke``. To see a list of
the commands, run ``invoke -l``::

    Available commands:

        migrate  Update a testing database with south.
        schema   Create a schema migration for any changes.
        serve    Start the Django dev server.
        shell    Start a Django shell with the test settings.
        syncdb   Create a database for testing in the shell or server.
        test     Run the Waffle test suite.

To run the tests, just run ``invoke test``.

To manually test out the app and admin, you'll want to run ``invoke syncdb`` then
``invoke migrate``, then you can run ``invoke serve`` to start the Django dev server,
or ``invoke shell`` to open the Django shell.


Writing Patches
===============

Patches should have tests. And follow PEP-8/existing styles. That's about it!
If you need help writing or running tests, let me know!

I will probably run your tests with and without the rest of the patch.


Submitting Patches
==================

Open a pull request on GitHub! If you want to make sure I'll merge the patch
upstream, open an issue first to discuss it.
