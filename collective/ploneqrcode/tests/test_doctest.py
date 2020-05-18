# -*- coding: utf-8 -*-
from collective.ploneqrcode import testing
from plone.testing import layered
import doctest
import unittest

functional = [
    'controlpanel.txt',
]


def test_suite():

    tests = []

    for f in functional:
        tests.append(
            layered(
                doctest.DocFileSuite('tests/{0}'.format(f),
                                     package='collective.ploneqrcode',
                                     optionflags=testing.OPTIONFLAGS,
                                     ),
                layer=testing.FUNCTIONAL_TESTING,
            )
        )

    return unittest.TestSuite(tests)
