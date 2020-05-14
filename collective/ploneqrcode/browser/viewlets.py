# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.ploneqrcode.interfaces import IPloneQRControlPanel
from plone import api
from plone.app.layout.viewlets import ViewletBase
from plone.memoize.view import memoize_contextless
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


class PloneQRCodeViewlet(ViewletBase):
    """Viewlet used to display the QrCode."""
    index = ViewPageTemplateFile('templates/qrfooter.pt')

    def update(self):
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IPloneQRControlPanel, check=False)
        self.portal = api.portal.get()

    def render(self):
        if self.settings.enable_viewlet:
            return self.index()
        return ''

    @memoize_contextless
    def portal_url(self):
        return self.portal.absolute_url()

    @memoize_contextless
    def get_qrcode(self):
        URI = self.context.absolute_url()
        img = self.portal.restrictedTraverse('@@ploneqrcode')(data=URI,
                out="html", scale=self.settings.scale)
        return img
