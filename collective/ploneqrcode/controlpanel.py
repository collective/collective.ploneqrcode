# -*- coding: utf-8 -*-
from collective.ploneqrcode import MessageFactory as _
from collective.ploneqrcode.interfaces import IPloneQRControlPanel
from plone.app.registry.browser import controlpanel


class PloneQRCodeForm(controlpanel.RegistryEditForm):
    schema = IPloneQRControlPanel
    label = _(u'ploneqrcode settings')
    description = _(u'Settings for collective.ploneqrcode')


class PloneQRCodeControlPanel(controlpanel.ControlPanelFormWrapper):
    form = PloneQRCodeForm
