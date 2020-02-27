import os

from rdflib import Graph, URIRef, Literal, Namespace, RDF, XSD
from rdflib.namespace import SKOS


yso = Namespace('http://www.yso.fi/onto/yso/')
ysa = Namespace('http://www.yso.fi/onto/ysa/')
ysemeta = Namespace('http://www.yso.fi/onto/yse-meta/')
foaf = Namespace('http://xmlns.com/foaf/0.1/')
skos = Namespace('http://www.w3.org/2004/02/skos/core#')
dct = Namespace('http://purl.org/dc/terms/')
allars = Namespace('http://www.yso.fi/onto/allars/')
koko = Namespace('http://www.yso.fi/onto/koko/')
isothes = Namespace('http://purl.org/iso25964/skos-thes#')
rdfs = Namespace('http://www.w3.org/2000/01/rdf-schema#')
owl = Namespace('http://www.w3.org/2002/07/owl#')
dc11 = Namespace('http://purl.org/dc/elements/1.1/')
ehdotus = Namespace(f'{os.environ.get("SUGGESTION_SYSTEM_ISSUE_URL", "http://ehdotus.finto.fi")}/suggestion/')


def initGraph():
    g = Graph()
    g.bind('yso', yso)
    g.bind('ysa', ysa)
    g.bind('skos', skos)
    g.bind('allars', allars)
    g.bind('ysemeta', ysemeta)
    g.bind('koko', koko)
    g.bind('dc', dct)
    g.bind('foaf', foaf)
    g.bind('ehdotus', ehdotus)
    return g


def suggestionToGraph(suggestion, graph=None):
    g = None

    if graph is None:
        g = initGraph()
    else:
        g = graph

    if suggestion is not None:
        uri = yso['p{}'.format(50000 + suggestion["id"])]
        g.add((uri, RDF.type, SKOS.Concept))
        g.add((uri, RDF.type, ysemeta.Concept))

        for tag in suggestion["tags"]:
            if 'maantieteellinen' in tag["label"].lower():
                g.add((uri, RDF.type, ysemeta.GeographicalConcept))
                break

        g.add((uri, foaf.homepage, ehdotus['{}'.format(suggestion["id"])]))

        g.add((uri, dct.created, Literal(
            suggestion["created"].date(), datatype=XSD.date)))
        g.add((uri, dct.modified, Literal(
            suggestion["modified"].date(), datatype=XSD.date)))

        if suggestion["preferred_label"]:
            for lang in suggestion["preferred_label"]:
                try:
                    g.add((uri, skos.prefLabel, Literal(
                        suggestion["preferred_label"][lang]["value"].strip(), lang=lang)))
                except (TypeError, AttributeError):
                    g.add((uri, skos.prefLabel, Literal(
                        suggestion["preferred_label"][lang].strip(), lang=lang)))

        for group in suggestion["groups"]:
            if group.get('uri'):
                g.add((uri, skos.member, URIRef(group.get('uri'))))

        for match in suggestion["broader_labels"]:
            if match.get('uri'):
                g.add((uri, skos.broadMatch, URIRef(match.get('uri'))))

        if suggestion.get('scopeNote'):
            g.add((uri, skos.scopeNote, Literal(
                suggestion["scopeNote"].strip())))

        for aLabel in suggestion["alternative_labels"]:
            if aLabel.get('value'):
                g.add((uri, skos.altLabel, Literal(aLabel["value"].strip())))

        for match in suggestion["narrower_labels"]:
            if match.get('uri'):
                g.add((uri, skos.narrowMatch, URIRef(match.get('uri'))))

        for match in suggestion["related_labels"]:
            if match.get('uri'):
                g.add((uri, skos.relatedMatch, URIRef(match.get('uri'))))

    return g
