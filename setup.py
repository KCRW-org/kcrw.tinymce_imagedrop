# -*- coding: utf-8 -*-
"""Installer for the kcrw.tinymce_imagedrop package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='kcrw.tinymce_imagedrop',
    version='1.0.1',
    description="A Plone add-on that adds image drag and drop to TinyMCE 4 in Plone.",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone CMS',
    author='Alec Mitchell',
    author_email='alecpm@gmail.com',
    url='https://github.com/collective/kcrw.tinymce_imagedrop',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/kcrw.tinymce_imagedrop',
        'Source': 'https://github.com/collective/kcrw.tinymce_imagedrop',
        'Tracker': 'https://github.com/collective/kcrw.tinymce_imagedrop/issues',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['kcrw'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires="==2.7, >=3.6",
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'plone.api',
        'plone.app.widgets',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = kcrw.tinymce_imagedrop.locales.update:update_locale
    """,
)
