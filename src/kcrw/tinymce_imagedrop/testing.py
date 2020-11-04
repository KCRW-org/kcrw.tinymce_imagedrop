# -*- coding: utf-8 -*-
try:
    from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
    BASES = (PLONE_APP_CONTENTTYPES_FIXTURE,)
except ImportError:
    BASES = ()
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import kcrw.tinymce_imagedrop


class KcrwTinymceImagedropLayer(PloneSandboxLayer):

    defaultBases = BASES

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=kcrw.tinymce_imagedrop)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'kcrw.tinymce_imagedrop:default')


KCRW_TINYMCE_IMAGEDROP_FIXTURE = KcrwTinymceImagedropLayer()


KCRW_TINYMCE_IMAGEDROP_INTEGRATION_TESTING = IntegrationTesting(
    bases=(KCRW_TINYMCE_IMAGEDROP_FIXTURE,),
    name='KcrwTinymceImagedropLayer:IntegrationTesting',
)


KCRW_TINYMCE_IMAGEDROP_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(KCRW_TINYMCE_IMAGEDROP_FIXTURE,),
    name='KcrwTinymceImagedropLayer:FunctionalTesting',
)
