.. _usage-javascript:

==============
Using WaffleJS
==============

Waffle supports using :ref:`flags <types-flag>`, :ref:`switches
<types-switch>`, and :ref:`samples <types-sample>` in JavaScript
("WaffleJS") either via inline script or an external script.

.. warning::

    Unlike samples when used in Python, samples in WaffleJS **are only
    calculated once** and so are **consistent**.


The WaffleJS ``waffle`` object
==============================

WaffleJS exposes a global ``waffle`` object that gives access to flags,
switches, and samples.


Methods
-------

These methods can be used exactly like their Python equivalents:

- ``waffle.flag_is_active(flag_name)``
- ``waffle.switch_is_active(switch_name)``
- ``waffle.sample_is_active(sample_name)``


Members
-------

WaffleJS also directly exposes dictionaries of each type, where keys are
the names and values are ``true`` or ``false``:

- ``waffle.FLAGS``
- ``waffle.SWITCHES``
- ``waffle.SAMPLES``


Installing WaffleJS
===================


As an external script
---------------------

Using the ``wafflejs`` view requires adding Waffle to your URL
configuration. For example, in your ``ROOT_URLCONF``::

    urlpatterns = patterns('',
        (r'^', include('waffle.urls')),
    )

This adds a route called ``wafflejs``, which you can use with the
``url`` template tag:

.. code-blocK:: django

    <script src="{% url 'wafflejs' %}"></script>


As an inline script
-------------------

To avoid an extra request, you can also use the ``wafflejs`` template
tag to include WaffleJS as an inline script:

.. code-block:: django

    {% load waffle_tags %}
    <script>
      {% wafflejs %}
    </script>
