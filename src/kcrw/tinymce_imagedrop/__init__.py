# -*- coding: utf-8 -*-
"""Init and utils."""
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('kcrw.tinymce_imagedrop')


def _patched_get_tinymce_options(context, field, request):
    from plone.app.widgets import utils
    from Products.CMFCore.utils import getToolByName
    portal_url = getToolByName(context, 'portal_url')()
    options = utils._ktid_orig_get_tinymce_options(context, field, request)
    config = options.setdefault('tiny', {})
    config['paste_data_images'] = True
    config['external_plugins'] = {
        'paste_plone_image': '{}/++resource++kcrw.tinymce_imagedrop/tinymce_image_paste.js'.format(portal_url)
    }
    return options


def patch_plone4_tinymce_config():
    from plone.app.widgets import utils
    from plone.app.widgets import dx
    from plone.app.widgets import at
    if getattr(utils, '_ktid_orig_get_tinymce_options', None) is None:
        utils._ktid_orig_get_tinymce_options = utils.get_tinymce_options
        utils.get_tinymce_options = _patched_get_tinymce_options
        dx.get_tinymce_options = _patched_get_tinymce_options
        at.get_tinymce_options = _patched_get_tinymce_options


try:
    from plone.app.widgets import dx
    patch_plone4_tinymce_config()
except ImportError:
    pass
