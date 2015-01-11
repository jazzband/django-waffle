.. _testing-index:

===================
Testing with Waffle
===================

"Testing" takes on at least two distinct meanings with Waffle:

- Testing your application with automated tools
- Testing your feature with users

For the purposes of this chapter, we'll refer to the former as
"automated testing" and the latter as "user testing" for clarity.

.. toctree::
   :maxdepth: 1

   automated
   user


Automated testing
=================

Automated testing encompasses things like unit and integration tests,
whether they use the Python/Django unittest framework or an external
tool like Selenium.

Waffle is often non-deterministic, i.e. it introduces true randomness to
the system-under-test, which is a nightmare for automated testing. Thus,
Waffle includes tools to re-introduce determinism in automated test
suites.

:ref:`Read more about automated testing <testing-automated>`.


User testing
============

User testing occurs on both a (relatively) large scale with automated
metric collection and on a small, often one-to-one—such as testing
sessions with a user and research or turning on a feature within a
company or team.

Waffle does what it can to support these kinds of tests while still
remaining agnostic about metrics platforms.

:ref:`Read more about user testing <testing-user>`.
