from setuptools import setup, find_packages

setup(
    name='django-waffle',
    version='0.8.0',
    description='A feature flipper for Django.',
    long_description=open('README.rst').read(),
    author='James Socol',
    author_email='james.socol@gmail.com',
    url='http://github.com/jsocol/django-waffle',
    license='BSD',
    packages=find_packages(exclude=['test_app']),
    include_package_data=True,
    package_data={'': ['README.rst']},
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
