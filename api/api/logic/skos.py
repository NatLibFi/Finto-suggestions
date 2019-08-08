from rdflib import Graph, URIRef, Literal, Namespace, RDF, XSD, plugin
from rdflib.namespace import SKOS, DC
from rdflib.serializer import Serializer
import json
import os
import string
#Ylläolevat toimivat ja ÄLÄ muuta näitä ellei ole ihan pakko

class MikasTest:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

yso = Namespace('http://www.yso.fi/onto/yso/')
ysa = Namespace('http://www.yso.fi/onto/ysa/')
ysemeta = Namespace("http://www.yso.fi/onto/yse-meta/")
ysameta = Namespace("http://www.yso.fi/onto/ysa-meta/")
foaf = Namespace('http://xmlns.com/foaf/0.1/')
skos = Namespace("http://www.w3.org/2004/02/skos/core#")
dct = Namespace('http://purl.org/dc/terms/')
ysometa = Namespace("http://www.yso.fi/onto/yso-meta/")
allars = Namespace("http://www.yso.fi/onto/allars/")
koko = Namespace('http://www.yso.fi/onto/koko/')

contextInUse = {
  "context": "http://schema.org/",
  "type": "@type",
  "uri": "@id",
  "type": "@type",
  "lang": "@language",
  "value": "@value",
  "graph": "@graph",
  "label": "rdfs:label",
  "prefLabel": "skos:prefLabel",
  "altLabel": "skos:altLabel",
  "hiddenLabel": "skos:hiddenLabel",
  "broader": "skos:broader",
  "narrower": "skos:narrower",
  "related": "skos:related",
  "inScheme": "skos:inScheme",
  "exactMatch": "skos:exactMatch",
  "closeMatch": "skos:closeMatch",
  "broadMatch": "skos:broadMatch",
  "narrowMatch": "skos:narrowMatch",
  "relatedMatch": "skos:relatedMatch"
}

def initGraph():
  g = Graph()
  g.bind('yso', yso)
  g.bind('ysa', ysa)
  g.bind('skos', skos)
  g.bind('allars', allars)
  g.bind('ysometa', ysometa)
  g.bind('ysameta', ysameta)
  g.bind('ysemeta', ysemeta)
  g.bind('koko', koko)
  g.bind('dc', dct)
  g.bind('foaf', foaf)
  return g

def suggestionToTriple(suggestion, graph = None):
    g = None
    if graph is None:
        g = initGraph()
    else:
        g = graph

    if suggestion is not None:
        uri = yso['p{}'.format(50000 + suggestion["id"])]
        g.add((uri, RDF.type, SKOS.Concept))

        for tag in suggestion["tags"]:
            if 'maantieteellinen' in tag["label"].lower():
                g.add(((URIRef(uri), RDF.type, URIRef(ysameta + 'GeographicalConcept'))))

        suggestion_system_url = os.environ.get('SUGGESTION_SYSTEM_ISSUE_URL', None)

        g.add((URIRef(uri), RDF.type, URIRef(skos + 'Concept')) )
        g.add((URIRef(uri), RDF.type, URIRef(ysemeta + 'Concept')) )
        g.add((URIRef(uri), foaf.homepage, URIRef(f'{suggestion_system_url}/{suggestion["id"]}')))

        g.add((URIRef(uri), dct.created, Literal(suggestion["created"].date(), datatype=XSD.date)))

        if "fi" in suggestion["preferred_label"].keys() and "value" in suggestion["preferred_label"]["fi"].keys():
            g.add((URIRef(uri), skos.prefLabel, Literal(suggestion["preferred_label"]["fi"]["value"], lang='fi')))

        if "fi" in suggestion["preferred_label"].keys():
            print('halloota', suggestion)

        if "sv" in suggestion["preferred_label"].keys() and "value" in suggestion["preferred_label"]["sv"].keys():
            g.add((URIRef(uri), skos.prefLabel, Literal(suggestion["preferred_label"]["sv"]["value"], lang='sv')))

        if "en" in suggestion["preferred_label"].keys():
            g.add((URIRef(uri), skos.prefLabel, Literal(suggestion["preferred_label"]["en"], lang='en')))

        for group in suggestion["groups"]:
            g.add((URIRef(uri), skos.member, URIRef(group["uri"])))

        for match in suggestion["broader_labels"]:
            g.add((URIRef(uri), skos.broadMatch, URIRef(match["uri"])))

        g.add((URIRef(uri), skos.note, Literal(suggestion["scopeNote"])))

        for label in suggestion["alternative_labels"]:
            g.add((URIRef(uri), skos.altLabel, URIRef(label["uri"])))

        for match in suggestion["narrower_labels"]:
            g.add((URIRef(uri), skos.narrowMatch, URIRef(match["uri"])))

        for match in suggestion["related_labels"]:
            g.add((URIRef(uri), skos.relatedMatch, URIRef(match["uri"])))

    #Testing via short rdf and parsing
  #   testrdf = """
  #   PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
  #   PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
  #   PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  #   PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  # """

  #   gg = Graph().parse(data=testrdf, format='json-ld')
  #   ggg = (gg.serialize(format='json-ld', indent=4))
  #   return ggg

    #Testing ends
   
# The following is cunnently in use
    g = g.serialize(format='turtle', context=contextInUse, indent=4).decode('utf-8')
    # g = g.serialize(format='json-ld', indent=4)    
    return g



# The following "works"
# from rdflib import Graph, URIRef, Literal, Namespace, RDF, XSD
# from rdflib.namespace import SKOS
# import os

# yso = Namespace('http://www.yso.fi/onto/yso/')
# # ysa = Namespace('http://www.yso.fi/onto/ysa/')
# ysemeta = Namespace("http://www.yso.fi/onto/yse-meta/")
# ysameta = Namespace("http://www.yso.fi/onto/ysa-meta/")
# foaf = Namespace('http://xmlns.com/foaf/0.1/')
# skos = Namespace("http://www.w3.org/2004/02/skos/core#")
# dct = Namespace('http://purl.org/dc/terms/')

# def initGraph():
#   g = Graph()
#   # g.bind('dc', dct)
#   # g.bind('isothes', isothes)
#   # g.bind('ysa', ysa)
#   g.bind('ysa-meta', ysameta)
#   g.bind('foaf', foaf)
#   g.bind('skos', skos)
#   return g

# def suggestionToTriple(suggestion, graph = None):
#   g = None
#   if graph is None:
#     g = initGraph()
#   else:
#     g = graph

#   if suggestion is not None:
#     uri = yso['p{}'.format(50000 + suggestion.id)]
#     g.add((uri, RDF.type, SKOS.Concept))

#     for tag in suggestion.tags:
#       if 'maantieteellinen' in tag.label.lower():
#         g.add(((URIRef(uri), RDF.type, URIRef(ysameta + 'GeographicalConcept'))))

#     suggestion_system_url = os.environ.get('SUGGESTION_SYSTEM_ISSUE_URL', None)

#     g.add((URIRef(uri), RDF.type, URIRef(skos + 'Concept')) )
#     g.add((URIRef(uri), RDF.type, URIRef(ysemeta + 'Concept')) )
#     g.add((URIRef(uri), foaf.homepage, URIRef(f'{suggestion_system_url}/{suggestion.id}')))
#     g.add((URIRef(uri), dct.created, Literal(suggestion.created.date(), datatype=XSD.date)))

#     if suggestion.preferred_label.fi.value:
#       g.add((URIRef(uri), skos.prefLabel, Literal(suggestion.preferred_label.fi.value, lang='fi')))

#     if suggestion.preferred_label.sv.value:
#       g.add((URIRef(uri), skos.prefLabel, Literal(suggestion.preferred_label.sv.value, lang='sv')))

#     if suggestion.preferred_label.en:
#       g.add((URIRef(uri), skos.prefLabel, Literal(suggestion.preferred_label.en, lang='en')))

#     for group in suggestion.groups:
#       g.add((URIRef(uri), skos.member, URIRef(group.uri)))

#     for match in suggestion.broader_labels:
#       g.add((URIRef(uri), skos.broadMatch, URIRef(match.uri)))

#     g.add((URIRef(uri), skos.note, suggestion.scopeNote))
#     # g.add((URIRef(uri), skos.note, 'Mikas testing'))

#     for label in suggestion.alternative_labels:
#       g.add((URIRef(uri), skos.altLabel, URIRef(label.uri)))

#     for match in suggestion.narrower_labels:
#       g.add((URIRef(uri), skos.narrowMatch, URIRef(match.uri)))

#     for match in suggestion.related_labels:
#       g.add((URIRef(uri), skos.relatedMatch, URIRef(match.uri)))

