# -*- coding: utf-8 -*-
from collective.ploneqrcode.testing import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles
from zope.component import getMultiAdapter
import unittest


class ControlPanelTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.cp = getattr(self.portal, 'portal_controlpanel')

    def test_installed(self):
        # entry is in the control panel
        installed = [a.getAction(self)['id'] for a in self.cp.listActions()]
        self.assertIn('ploneqrcode', installed)

    def test_uninstalled(self):
        setup_tool = getattr(self.portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile(
            'profile-collective.ploneqrcode:uninstall')

        # entry is removed from the control panel
        installed = [a.getAction(self)['id'] for a in self.cp.listActions()]
        self.assertNotIn('ploneqrcode', installed)

    def test_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name='ploneqrcode-settings')
        view = view.__of__(self.portal)
        self.failUnless(view())

    def test_view_protected(self):
        # view can not be accessed by anonymous users
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                          '@@ploneqrcode-settings')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
