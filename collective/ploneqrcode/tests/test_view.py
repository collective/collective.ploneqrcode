# -*- coding: utf-8 -*-
import unittest
from plone import api
from collective.ploneqrcode.testing import FUNCTIONAL_TESTING
import re
import io
from PIL import Image
from zope.interface import alsoProvides
from plone.app.customerize import registration
from collective.ploneqrcode.interfaces import IPloneQRLayer


class ViewMixin:
    def test_view_is_registered(self):
        registered = [v.name for v in registration.getViews(IPloneQRLayer)]
        self.assertIn('ploneqrcode.belowcontentbody', registered)


class BaseViewTestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IPloneQRLayer)


class TestCase(ViewMixin, BaseViewTestCase):

    def setUp(self):
        """Shared test environment set-up, ran before every test."""
        super(TestCase, self).setUp()
        self.qrcode = api.content.get_view("ploneqrcode", self.portal, self.request)

    def test_qrcode_png(self):
        qcode = self.qrcode(data='Foo data')
        Image.open(io.BytesIO(qcode))

    def test_qrcode_html(self):
        rgx = re.compile(r'''<img\s+([^>]*)src="*"(.*?)[^>]*>''', re.IGNORECASE)
        qcode = self.qrcode(data='Foo data', out='html')
        rs = rgx.search(qcode).group()

        self.assertEqual(rs, qcode)
        self.assertIn('class="ploneqrcode"', rs)

    def test_qrcode_base64(self):
        expected_str = "iVBORw0KGgoAAAANSUhEUgAAAKUAAAClAQAAAAAVUAB3AAABIklEQVR4"\
                       "nO2WMY6EMAxFP6JIyRFyE7gYUpD2YjM3yREoKRDeb4+E2OyW+9EUYwkp"\
                       "vBRx7G87sD9sw4e+P10BdLZkjJi5RNHSYvZcZ9Jhz/ErpTPSkz6kA9zq"\
                       "bqF7BujDbTQ9bqER31K3iUFuoi6grh2CxJQ2ihLQsLUPR5pq0VAm0upG"\
                       "pcKOQUv9xuOwIDGveetMTItRNnRkRG/JxNQW9+Gr+n49lSqjXoA8PvpZ"\
                       "eKOkfuhkTCTbDK5xkFC3ByKlO85sCmloxw4gc79IKZVqoZ2Oq6Smr5pn"\
                       "P3PZYFq19Oxnrzl0qU0JLTFjET5claqhPoeizfDjRLqBRl2sfW3eDyq6"\
                       "eBWyzfy4sYJ6fC2eRRxGchrvvrAlN6/B/6e/7UPfnn4Dd2eWDAQLIPMA"\
                       "AAAASUVORK5CYII="

        rgx = re.compile(r'^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$')
        qcode = self.qrcode(data='Foo data', out='base64')

        self.assertTrue(rgx.search(qcode))
        self.assertEqual(qcode, expected_str)
