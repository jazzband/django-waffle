.. _usage-templates:
.. highlight:: django

=========================
Using Waffle in templates
=========================

Waffle makes it easy to test :ref:`flags <types-flag>`, :ref:`switches
<types-switch>`, and :ref:`samples <types-sample>` in templates to flip
features on the front-end. It includes support for both Django's
built-in templates and for Jinja2_.

.. warning::

    Before using samples in templates, see the warning in the
    :ref:`Sample chapter <types-sample>`.


.. _templates-django:

Django Templates
================

Load the ``waffle_tags`` template tags::

    {% load waffle_tags %}

In Django templates, Waffle provides three new block types, ``flag``,
``switch``, and ``sample``, that function like ``if`` blocks. Each block
supports an optional ``else`` to be rendered if the flag, switch, or
sample in inactive.


Flags
-----

::

    {% flag "flag_name" %}
        flag_name is active!
    {% else %}
        flag_name is inactive
    {% endflag %}


Switches
--------

::

    {% switch "switch_name" %}
        switch_name is active!
    {% else %}
        switch_name is inactive
    {% endswitch %}


Samples
-------

::

    {% sample "sample_name" %}
        sample_name is active!
    {% else %}
        sample_name is inactive
    {% endsample %}


.. _templates-jinja:

Jinja Templates
===============

When used with Jinja2_, Waffle provides a ``waffle`` object in the Jinja
template context that can be used with normal ``if`` statements. Because
these are normal ``if`` statements, you can use ``else`` or ``if not``
as normal.


Flags
-----

::

    {% if waffle.flag('flag_name') %}
        flag_name is active!
    {% endif %}


Switches
--------

::

    {% if waffle.switch('switch_name') %}
        switch_name is active!
    {% endif %}


Samples
-------

::

    {% if waffle.sample('sample_name') %}
        sample_name is active!
    {% endif %}


.. _Jinja2: http://jinja.pocoo.org/
