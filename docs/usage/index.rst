.. _usage-index:

============
Using Waffle
============

Waffle provides a simple API to check the state of :ref:`flags
<types-flag>`, :ref:`switches <types-switch>`, and :ref:`samples
<types-sample>` in views and templates, and even on the client in
JavaScript.

.. toctree::
   :titlesonly:

   views
   decorators
   mixins
   templates
   javascript
   json
   cli

Public Methods
==============

The following public methods are available in `waffle/__init__.py`:

:flag_is_active:
    Determines if a flag is active for a given request. Returns a boolean value.
:switch_is_active:
    Determines if a switch is active. Returns a boolean value.
:sample_is_active:
    Determines if a sample is active. Returns a boolean value.
