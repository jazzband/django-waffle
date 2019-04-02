Releasing New Versions
======================

These are the steps necessary to release a new version of Django Waffle.

1. Update the version number in the following files:

    a. `setup.py`
    b. `docs/conf.py`
    c. `waffle/__init__.py`

2. Update the changelog in `CHANGES`.

3. Merge these changes to the `master` branch.

4. Create a new release on GitHub. This will also create a Git tag, and trigger a push to PyPI.

5. Ensure the documentation build passes: https://readthedocs.org/projects/waffle/
