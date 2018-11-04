Releasing New Versions
======================

These are the steps necessary to release a new version of Django Waffle.

1. Update the version number in the following files:

    a. `setup.py`
    b. `docs/conf.py`

2. Update the changelog in `CHANGES`.

3. Merge these changes to the `master` branch.

4. Create a new release on GitHub. This will also create a Git tag.

5. Ensure the documentation build passes: https://readthedocs.org/projects/waffle/

6. Ensure the Travis build, for the `master` branch, has passed: https://travis-ci.org/django-waffle/django-waffle/branches

7. Build and push to PyPI:

    .. code-block:: bash

        $ python setup.py sdist bdist_wheel
        $ python setup.py sdist bdist_wheel upload -r pypi
