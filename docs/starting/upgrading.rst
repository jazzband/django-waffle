.. _starting-upgrading:

=========
Upgrading
=========

From v0.10.x to v0.11
=====================

Jinja2 Templates
----------------

Waffle no longer supports `jingo's <http://jingo.readthedocs.org/>`
automatic helper import, but now ships with a `Jinja2
<http://jinja.pocoo.org/>` extension that supports multiple Jinja2
template loaders for Django. See the :ref:`installation docs
<installation-settings-templates>` for details on how to install this
extension.
