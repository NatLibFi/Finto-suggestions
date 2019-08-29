from rdflib import Graph, URIRef, Literal, Namespace, RDF, XSD, plugin, term
from rdflib.namespace import SKOS, DC
from rdflib.serializer import Serializer
import json, rdflib_jsonld
import os
import string
from flask import jsonify
import ast
from .context import listContext
import urllib as ul
import requests
from collections import Counter
import logging
import copy

yso = Namespace('http://www.yso.fi/onto/yso/')
ysa = Namespace('http://www.yso.fi/onto/ysa/')
ysemeta = Namespace('http://www.yso.fi/onto/yse-meta/')
ysameta = Namespace('http://www.yso.fi/onto/ysa-meta/')
foaf = Namespace('http://xmlns.com/foaf/0.1/')
skos = Namespace('http://www.w3.org/2004/02/skos/core#')
dct = Namespace('http://purl.org/dc/terms/')
ysometa = Namespace('http://www.yso.fi/onto/yso-meta/')
allars = Namespace('http://www.yso.fi/onto/allars/')
koko = Namespace('http://www.yso.fi/onto/koko/')
isothes = Namespace('http://purl.org/iso25964/skos-thes#')
rdfs = Namespace('http://www.w3.org/2000/01/rdf-schema#')
owl = Namespace('http://www.w3.org/2002/07/owl#')
dc11 = Namespace('http://purl.org/dc/elements/1.1/')

def initGraph():
  g = Graph()
  g.bind('yso', yso)
  g.bind('ysa', ysa)
  g.bind('skos', skos)
  g.bind('allars', allars)
  g.bind('ysometa', ysometa)
  g.bind('ysometa', ysometa)
  g.bind('ysameta', ysameta)
  g.bind('ysemeta', ysemeta)
  g.bind('koko', koko)
  g.bind('dc', dct)
  g.bind('foaf', foaf)
  return g

def suggestionToGraph(suggestion, graph = None):
    g = None
    
    try:
      if graph is None:
        g = initGraph()
      else:
        g = graph
    except Exception as ex:
      print(str(ex))

    try:
      if suggestion is not None:
        uri = yso['p{}'.format(50000 + suggestion["id"])]
        g.add((uri, RDF.type, SKOS.Concept))

        try:
          for tag in suggestion["tags"]:
            if 'maantieteellinen' in tag["label"].lower():
              g.add(((URIRef(uri), RDF.type, URIRef(ysometa + 'GeographicalConcept'))))
        except Exception as ex:
          print(str(ex))

        try:
          suggestion_system_url = os.environ.get('SUGGESTION_SYSTEM_ISSUE_URL', None)
        except Exception as ex:
          print(str(ex))

        g.add((URIRef(uri),  RDF.type, URIRef(ysometa + 'Concept')))

        try:
          g.add(( URIRef(uri), foaf.homepage, URIRef(f'{suggestion_system_url}/api/suggestions/{suggestion["id"]}/skos')))
        except Exception as ex:
          print(str(ex))

        try:
          g.add((URIRef(uri), dct.created, Literal(suggestion["created"].date(), datatype=XSD.date)))
          g.add((URIRef(uri), dct.modified, Literal(suggestion["modified"].date(), datatype=XSD.date)))
        except Exception as ex:
          print(str(ex))

        try:
          for lang in ("fi", "sv", "en"):
            if lang in suggestion["preferred_label"] and suggestion["preferred_label"][lang].get('value'):
              g.add((URIRef(uri), skos.prefLabel, Literal(suggestion["preferred_label"][lang]["value"].strip(), lang=lang)))
        except Exception as ex:
          print(str(ex))

        try:
          for group in suggestion["groups"]:
            if group.get('uri'):
              g.add((URIRef(uri), skos.member, term.URIRef(group.get('uri'))))

          for match in suggestion["broader_labels"]:
            if match.get('uri'):
              g.add((URIRef(uri), skos.broadMatch, URIRef(match.get('uri'))))

          if suggestion.get('scopeNote'):
            g.add((URIRef(uri), skos.scopeNote, Literal(suggestion["scopeNote"].strip())))

          for aLabel in suggestion["alternative_labels"]:
            if aLabel.get('value'):
              g.add((URIRef(uri), skos.altLabel, Literal(aLabel["value"].strip())))
            
          for match in suggestion["narrower_labels"]:
            if match.get('uri'):
              g.add((URIRef(uri), skos.narrowMatch, URIRef(match.get('uri'))))
        
          for match in suggestion["related_labels"]:
            if match.get('uri'):
              g.add((URIRef(uri), skos.relatedMatch, URIRef(match.get('uri'))))
        except Exception as ex:
          print(str(ex))
          
    except Exception as totalEx:
      print(str(totalEx))  

    return g

