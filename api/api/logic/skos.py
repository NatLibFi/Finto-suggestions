from rdflib import Graph, URIRef, Literal, Namespace, RDF, XSD
from rdflib.namespace import SKOS
import os

yso = Namespace('http://www.yso.fi/onto/yso/')
# ysa = Namespace('http://www.yso.fi/onto/ysa/')
ysemeta = Namespace("http://www.yso.fi/onto/yse-meta/")
ysameta = Namespace("http://www.yso.fi/onto/ysa-meta/")
foaf = Namespace('http://xmlns.com/foaf/0.1/')
skos = Namespace("http://www.w3.org/2004/02/skos/core#")
dct = Namespace('http://purl.org/dc/terms/')

def initGraph():
  g = Graph()
  # g.bind('dc', dct)
  # g.bind('isothes', isothes)
  # g.bind('ysa', ysa)
  g.bind('ysa-meta', ysameta)
  g.bind('foaf', foaf)
  g.bind('skos', skos)
  return g

def suggestionToTriple(suggestion, graph = None):
  g = None
  if graph is None:
    g = initGraph()
  else:
    g = graph

  if suggestion is not None:
    uri = yso['p{}'.format(50000 + suggestion.id)]
    g.add((uri, RDF.type, SKOS.Concept))

    for tag in suggestion.tags:
      if 'maantieteellinen' in tag.label.lower():
        g.add(((URIRef(uri), RDF.type, URIRef(ysameta + 'GeographicalConcept'))))

    suggestion_system_url = os.environ.get('SUGGESTION_SYSTEM_ISSUE_URL', None)

    g.add((URIRef(uri), RDF.type, URIRef(skos + 'Concept')) )
    g.add((URIRef(uri), RDF.type, URIRef(ysemeta + 'Concept')) )
    g.add((URIRef(uri), foaf.homepage, URIRef(f'{suggestion_system_url}/{suggestion.id}')))
    g.add((URIRef(uri), dct.created, Literal(suggestion.created.date(), datatype=XSD.date)))

    if suggestion.preferred_label.fi.value:
      g.add((URIRef(uri), skos.prefLabel, Literal(suggestion.preferred_label.fi.value, lang='fi')))

    if suggestion.preferred_label.sv.value:
      g.add((URIRef(uri), skos.prefLabel, Literal(suggestion.preferred_label.sv.value, lang='sv')))

    if suggestion.preferred_label.en:
      g.add((URIRef(uri), skos.prefLabel, Literal(suggestion.preferred_label.en, lang='en')))

    for group in suggestion.groups:
      g.add((URIRef(uri), skos.member, URIRef(group.uri)))

    for match in suggestion.broader_labels:
      g.add((URIRef(uri), skos.broadMatch, URIRef(match.uri)))

    g.add((URIRef(uri), skos.note, suggestion.scopeNote))

    for label in suggestion.alternative_labels:
      g.add((URIRef(uri), skos.altLabel, URIRef(label.uri)))

    for match in suggestion.narrower_labels:
      g.add((URIRef(uri), skos.narrowMatch, URIRef(match.uri)))

    for match in suggestion.related_labels:
      g.add((URIRef(uri), skos.relatedMatch, URIRef(match.uri)))