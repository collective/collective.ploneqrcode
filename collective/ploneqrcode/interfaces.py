# -*- coding: utf-8 -*-
from collective.ploneqrcode import MessageFactory as _
from plone.autoform import directives as form
from plone.formwidget.namedfile.widget import NamedImageFieldWidget
from plone.supermodel import model
from zope import schema
from zope.interface import Interface


class IPloneQRLayer(Interface):
    """ """


class IPloneQRControlPanel(model.Schema):
    enable_viewlet = schema.Bool(
        title=_(u'Enable Qr Code Viewlets'),
        description=_(u'''Provides QR code viewlet for dexterity'''
                      u'''content and shown below of title.'''),
        default=False)

    use_logo = schema.Bool(
        title=_(u'Use your logo?'),
        default=False)

    form.widget('your_logo', NamedImageFieldWidget)
    your_logo = schema.ASCII(
        title=_(u'You logo'),
        required=False,
    )

    scale = schema.Choice(
        title=_(u'Scale'),
        required=True,
        default='2',
        vocabulary="collective.ploneqrcode.scale",
    )
