.. _usage-json:

=====================
Waffle Status as JSON
=====================

Although :doc:`WaffleJS<javascript>` returns the status of all
:ref:`flags <types-flag>`, :ref:`switches <types-switch>`, and
:ref:`samples <types-sample>`, it does so by exposing a Javascript
object, rather than returning the data in a directly consumable format.

In cases where a directly consumable format is preferable,
Waffle also exposes this data as JSON via the ``waffle_status`` view.


Using the view
--------------

Using the ``waffle_status`` view requires adding Waffle to your URL
configuration. For example, in your ``ROOT_URLCONF``::

    urlpatterns = patterns('',
        (r'^', include('waffle.urls')),
    )

This adds a route called ``waffle_status``, which will return the current
status of each flag, switch, and sample as JSON, with the following structure:

.. code-block:: json

    {
        "flags": {
            "flag_active": {
                "is_active": true,
                "last_modified": "2020-01-01T12:00:00.000"
            },
            "flag_inactive": {
                "is_active": false,
                "last_modified": "2020-01-01T12:00:00.000"
            }
        },
        "switches": {
            "switch_active": {
                "is_active": true,
                "last_modified": "2020-01-01T12:00:00.000"
            },
            "switch_inactive": {
                "is_active": false,
                "last_modified": "2020-01-01T12:00:00.000"
            }
        },
        "samples": {
            "sample_active": {
                "is_active": true,
                "last_modified": "2020-01-01T12:00:00.000"
            },
            "sample_inactive": {
                "is_active": false,
                "last_modified": "2020-01-01T12:00:00.000"
            }
        }
    }
