import base64
import json
from Acquisition import aq_chain, aq_inner
from plone import api
from plone.protect import CheckAuthenticator, PostOnly
from Products.Five.browser import BrowserView
from zope.interface import Interface

try:
    from plone.dexterity.interfaces import IDexterityContent
    from plone.namedfile.file import NamedBlobImage
except ImportError:
    class IDexterityContent(Interface):
        pass


class CreateDroppedImages(BrowserView):
    """Upload images"""

    img_type = "Image"
    img_template = """
    <p>
      <img src="resolveuid/{uid}/@@images/image" data-val="{uid}" data-linktype="image" class="image-inline" />
    </p>"""

    def get_image_container(self):
        container = None
        for parent in aq_chain(aq_inner(self.context)):
            types = getattr(parent.aq_explicit, 'getLocallyAllowedTypes', ()) and parent.getLocallyAllowedTypes()
            if self.img_type in types or getattr(parent, 'meta_type', None) == 'Plone Site':
                container = parent
                break
        return container

    def set_image(self, item, img_data):
        if IDexterityContent.providedBy(item):
            image = NamedBlobImage(data=img_data)
            item.image = image
        else:
            item.setImage(img_data)

    def __call__(self):
        request = self.request
        response = request.response
        PostOnly(request)
        CheckAuthenticator(request)
        files = request.get('files', '[]')
        if files is not None:
            files = json.loads(files)
            files = [base64.b64decode(f) for f in files if f]

        uids = []
        container = self.get_image_container()
        if container is not None:
            for data in files:
                item = api.content.create(
                    container, self.img_type, id='pasted-image', safe_id=True,
                    title="Pasted Image"
                )
                if item is None:
                    continue
                uids.append(item.UID())
                self.set_image(item, data)

        response.setHeader('Content-Type', 'application/json; charset=utf-8')
        return json.dumps({
            'images': [self.img_template.format(uid=uid) for uid in uids if uid]
        })
