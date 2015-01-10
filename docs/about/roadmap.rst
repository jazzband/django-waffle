.. _about-roadmap:

=======
Roadmap
=======

.. note::

    This roadmap is subject to change, but represents the rough
    direction I plan to go. For specific issues, see the current
    milestones_.


Waffle is already a useful library used in many production systems, but
it is not done evolving.


Present through 0.12
=====================

The immediate future is finishing common segment features and bug fixes.


0.10.2/0.11
-----------

0.10.2_ was primarily a docs overhaul with a major fix to how caching
works. It will probably not be released on its own but combined with
0.11_.

0.11 includes a couple of significant refactors designed to pay down
some of the debt that's accrued in the past few years. It also includes
finally making a decision about auto-create/data-in-settings. There are
also a few small tools like template syntax sugar and and integration
testing tools.


0.12
----

0.12_ is about closing some long-standing feature gaps, like segmenting
by IP and User-Agent.


Toward 1.0
==========

There are no solid criteria for what makes 1.0 right now, but after
0.12, most outstanding issues will be resolved and Waffle will be in
very good shape. There are no plans for a 0.13, so it seems likely that
the next step after 0.12 would be some clean-up and finally a 1.0.


Beyond 1.0
==========

*tl;dr: Waffle2 may be a complete break from Waffle.*

Waffle is one of the first Python libraries I created, you can see that
in the amount of code I left in ``__init__.py``. It is also 4 years old,
and was created during a different period in my career, and in Django.

There are some philosophical issues with how Waffle is designed. Adding
new methods of segmenting users requires at least one new column each,
and increasing the cyclomatic complexity. Caching is difficult. The
requirements are stringent and no longer realistic (they were created
before Django 1.5). The distinction between Flags, Samples, and Switches
is confusing and triples the API surface area (Flags can easily act as
Switches, less easily as Samples). It is not extensible.

Some challenges also just accrue over time. Dropping support for Django
1.4, the current Extended Support Release, would significantly simplify
a few parts.

There is a simplicity to Waffle that I've always appreciated vs, say,
Gargoyle_. Not least of which is that Waffle works with the built-in
admin (or any other admin you care to use). I don't have to write any
code to start using Waffle, other than an ``if`` block. Just add a row
and click some checkboxes. Most batteries are included. These are all
things that any new version of Waffle must maintain.

Still, if I *want* to write code to do some kind of custom segment that
isn't common-enough to belong in Waffle, shouldn't I be able to? (And,
if all the core segmenters were built as the same kind of extension, we
could lower the bar for inclusion.) If I only care about IP address and
percentage, it would be great to skip all the other checks that just
happen to be higher in the code.

I have rough sketches of what this looks like, but there are still some
significant sticking points, particularly around shoehorning all of this
into the existing Django admin. I believe it's *possible*, just
potentially *gross*. (Then again, if it's gross underneath but exposes a
pleasant UI, that's not ideal, but it's OK.)

The other big sticking point is that this won't be a simple ``ALTER
TABLE wafle_flag ADD COLUMN`` upgrade; things will break. 

I've been thinking what Waffle would be like if I designed it from
scratch today with slightly different goals, like extensibility. Beyond
1.0, it's difficult to see continuing to add new features without this
kind of overhaul.


.. _milestones: https://github.com/jsocol/django-waffle/milestones
.. _0.10.2: https://github.com/jsocol/django-waffle/milestones/0.10.2
.. _0.11: https://github.com/jsocol/django-waffle/milestones/0.11
.. _0.12: https://github.com/jsocol/django-waffle/milestones/0.12
.. _Gargoyle: https://github.com/disqus/gargoyle
