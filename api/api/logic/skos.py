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

    for pref_label in suggestion.preferred_label:
        g.add((URIRef(uri), URIRef(skos + 'prefLabel'), Literal(suggestion.preferred_label['pref_label'], lang=pref_label)))

    for group in suggestion.group:
      g.add((URIRef(group.uri), skos.member, URIRef(uri)))

    #Ehdotettu yläkäsite YSOssa (LT) : broadMatch (missing from parser)
    # for broader_labels

    #Tarkoitusta täsmentävä selite : note
    # for scopeNote from suggestion.scopeNote:

    #Vaihtoehtoiset termit ja ilmaisut : altLabel
    # for alt_label in suggestion.alternative_labels:

    #Alakäsitteet (ST) : narrowMatch (missing from parser)

    #Assosiatiiviset (RT) : relatedMatch (missing from parser)

