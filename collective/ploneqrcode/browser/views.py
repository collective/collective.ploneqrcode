# -*- coding: utf-8 -*-
from PIL import Image
from Products.Five import BrowserView
from collective.ploneqrcode.interfaces import IPloneQRControlPanel
from io import BytesIO
from plone.memoize.view import memoize_contextless
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
import base64
import pyqrcode


class QrCodeConvert(BrowserView):
    """  """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.response = self.request.response

        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IPloneQRControlPanel, check=False)

        self.supported = ['png', 'base64', 'html']
        self.scale_percent_thumb = 30
        self.oRet = BytesIO()

    def resizeImg(self, img, size):
        rsize_out = BytesIO()

        w, h = size
        dim = (int(w * self.scale_percent_thumb / 100), int(h * self.scale_percent_thumb / 100))
        img.thumbnail(dim, Image.ANTIALIAS)
        img.save(rsize_out, "PNG")
        return Image.open(rsize_out)

    def newImg(self, img1, img2):
        n_img = BytesIO()

        wBase, hBase = img1.size
        wpercent = (wBase / float(img2.size[0]))
        hsize = int((float(img2.size[1]) * float(wpercent)))
        dim = (int(wBase * wpercent / 100), int(hBase * wpercent / 100))

        image_copy = img1.copy()
        position = ((img1.width - img2.width)/2, (image_copy.height -img2.height)/2)
        image_copy.paste(img2, position, img2)
        image_copy.save(n_img, "PNG")
        return n_img

    @memoize_contextless
    def _toPng(self, qrcode, **kwargs):
        qrcode.png(self.oRet, scale=kwargs.get('scale'),
          module_color=(tuple(map(int, kwargs.get('color').split(', ')))),
          background=tuple(map(int, kwargs.get('background').split(', '))))

        if self.settings.use_logo:
            lg = Image.open(BytesIO(base64.b64decode(self.settings.your_logo.split('datab64:')[1]))).convert("RGBA")
            img = Image.open(self.oRet).convert("RGBA")
            self.oRet = self.newImg(img, self.resizeImg(lg, img.size))
        return self.oRet.getvalue()

    def _toBase64(self, qrcode, **kwargs):
        self._toPng(qrcode, **kwargs)
        oQR = base64.b64encode(self.oRet.getvalue())
        return oQR

    def _toHtml(self, qrcode, **kwargs):
        b64 = self._toBase64(qrcode, **kwargs)
        html_img = '<img class="ploneqrcode" src="data:image/png;base64,{}">'.format(b64)
        return html_img

    def __call__(self, data, scale='5', color='0, 0, 0, 225',
            background='255, 255, 255, 255', out='png'):

        kwargs = {}
        kwargs['scale'] = scale
        kwargs['color'] = color
        kwargs['background'] = background
        kwargs['out'] = out

        if data:
            qrcode = pyqrcode.create(data)

            if out.lower() in self.supported:
               return getattr(self, '_to{}'.format(out.title()))(qrcode, **kwargs)
