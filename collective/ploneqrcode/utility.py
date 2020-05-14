# -*- coding: utf-8 -*-
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def get_scale(context):
    """Creates a vocabulary with the available scales.
    """
    items = [(str(i), str(i)) for i in xrange(1, 11)]
    terms = [SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in items]
    return SimpleVocabulary(terms)
