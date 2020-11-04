# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from kcrw.tinymce_imagedrop.testing import \
    KCRW_TINYMCE_IMAGEDROP_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that kcrw.tinymce_imagedrop is properly installed."""

    layer = KCRW_TINYMCE_IMAGEDROP_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if kcrw.tinymce_imagedrop is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'kcrw.tinymce_imagedrop'))

    def test_browserlayer(self):
        """Test that IKcrwTinymceImagedropLayer is registered."""
        from kcrw.tinymce_imagedrop.interfaces import (
            IKcrwTinymceImagedropLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IKcrwTinymceImagedropLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = KCRW_TINYMCE_IMAGEDROP_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['kcrw.tinymce_imagedrop'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if kcrw.tinymce_imagedrop is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'kcrw.tinymce_imagedrop'))

    def test_browserlayer_removed(self):
        """Test that IKcrwTinymceImagedropLayer is removed."""
        from kcrw.tinymce_imagedrop.interfaces import \
            IKcrwTinymceImagedropLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IKcrwTinymceImagedropLayer,
            utils.registered_layers())
