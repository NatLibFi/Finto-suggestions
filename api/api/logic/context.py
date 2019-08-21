"""
  Contex.py is used to simplify the managing of context for skos data

  Usage:

  from .context import listContext
  ...
  VAR.serialize(format='YOUR_FORMAT', context=listContext(), indent=N)

"""

import string, os, json

def listContext():
  contextInUseCommon = {
  'yso': 'http://www.yso.fi/onto/yso/',
  'ysa': 'http://www.yso.fi/onto/ysa/',
  'ysemeta': 'http://www.yso.fi/onto/yse-meta/',
  'ysameta': 'http://www.yso.fi/onto/ysa-meta/',
  'foaf': 'http://xmlns.com/foaf/0.1/',
  'skos': 'http://www.w3.org/2004/02/skos/core#',
  'dct': 'http://purl.org/dc/terms/',
  'ysometa': 'http://www.yso.fi/onto/yso-meta/',
  'allars': 'http://www.yso.fi/onto/allars/',
  'koko': 'http://www.yso.fi/onto/koko/',
  'isothes': 'http://purl.org/iso25964/skos-thes#',
  'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
  'owl': 'http://www.w3.org/2002/07/owl#',
  'dc11': 'http://purl.org/dc/elements/1.1/',
  'context': 'http://schema.org/',
  'type': '@type',
  'uri': '@id',
  'type': '@type',
  'lang': '@language',
  'value': '@value',
  'graph': '@graph',
  'label': 'rdfs:label',
  'prefLabel': 'skos:prefLabel',
  'altLabel': 'skos:altLabel',
  'hiddenLabel': 'skos:hiddenLabel',
  'broader': 'skos:broader',
  'narrower': 'skos:narrower',
  'related': 'skos:related',
  'inScheme': 'skos:inScheme',
  'exactMatch': 'skos:exactMatch',
  'closeMatch': 'skos:closeMatch',
  'broadMatch': 'skos:broadMatch',
  'narrowMatch': 'skos:narrowMatch',
  'relatedMatch': 'skos:relatedMatch'
}
  return contextInUseCommon




