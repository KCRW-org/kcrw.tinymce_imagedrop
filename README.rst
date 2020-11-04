.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://img.shields.io/pypi/v/kcrw.tinymce_imagedrop.svg
    :target: https://pypi.python.org/pypi/kcrw.tinymce_imagedrop/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/kcrw.tinymce_imagedrop.svg
    :target: https://pypi.python.org/pypi/kcrw.tinymce_imagedrop
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/kcrw.tinymce_imagedrop.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/kcrw.tinymce_imagedrop.svg
    :target: https://pypi.python.org/pypi/kcrw.tinymce_imagedrop/
    :alt: License


======================
kcrw.tinymce_imagedrop
======================

``tinymce_imagedrop`` is a Plone add-on that enabled dragging images into TinyMCE 4 to automatically create Image content
in the Plone site and renders them in the WYSIWYG using UID references. The add-on support Plone 5.x and Plone 4.3 with
TinyMCE 4 enabled via ``plone.app.widgets``.

Features
--------

- Provides a Javascript Plugin for TinyMCE for that enables uploading images to a Plone view
- Provides a Plone view ``create-dropped-images`` which creates Image content in the nearest container where allowed
- The view can be overriden to customize the image type, the creation location, and the markup used by default for the images.

Installation
------------

Install kcrw.tinymce_imagedrop by adding it to your buildout::

    [buildout]

    ...

    eggs =
        kcrw.tinymce_imagedrop


and then running ``bin/buildout``. On Plone 5+ you must install the add-on from the Add-ons control panel,
on Plone 4.3 (with ``plone.app.widgets``) it will be enabled automatically via a monkey patch when added
to your buildout.


Contribute
----------

- Issue Tracker: https://github.com/KCRW-org/kcrw.tinymce_imagedrop/issues
- Source Code: https://github.com/KCRW-org/kcrw.tinymce_imagedrop


License
-------

The project is licensed under the GPLv2.


Credits
-------

This add-on was created by Alec Mitchell <alecpm@gmail.com> with support from KCRW_


.. _KCRW: http://www.kcrw.com/
