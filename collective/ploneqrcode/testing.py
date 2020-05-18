# -*- coding: utf-8 -*-
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
import doctest


class PloneQRCodeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import plone.api
        self.loadZCML(package=plone.api)
        import collective.ploneqrcode
        self.loadZCML(package=collective.ploneqrcode)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.ploneqrcode:default')

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Folder', 'test-folder', title=u"Test Folder")
        folder = portal['test-folder']
        folder.invokeFactory('Document', 'test-doc', title=u"Test Document")
        folder.setDefaultPage('test-doc')
        setRoles(portal, TEST_USER_ID, ['Member'])


FIXTURE = PloneQRCodeLayer()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE, ),
    name='collective.ploneqrcode:Integration',
)

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE, ),
    name='collective.ploneqrcode:Functional',
)

OPTIONFLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
