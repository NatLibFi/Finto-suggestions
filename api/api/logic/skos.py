from rdflib import Graph, URIRef, Literal, Namespace, RDF, XSD, plugin, term
from rdflib.namespace import SKOS, DC
from rdflib.serializer import Serializer
import json
import os
import string
from flask import jsonify
import ast
from .context import listContext
#
# from rdflib.collection import collection
import urllib as ul
import requests
from collections import Counter
# from plugin import register, Parser

asJson = True

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
#   print("******")
#   print("Situation immediately after an initalization")
#   print( g.serialize(format='json-ld', context=listContext(), indent=4).decode('utf8').replace("'", ''))
#   print("******")
  return g

def quoteAdder(strObj: str):
    dq = "'"
    newstr = dq + strObj + dq
    newstr.replace("'", '"')
    print(newstr)
    print(type(newstr))
    return newstr

def codeExplicator(codeTxt: str):
  print('\n')
  print('****** By command: ')
  print(codeTxt)  
  print('******')

def uriCleaner(uriToBeCleaned):
  cleanedUri = requests.get(uriToBeCleaned).url
  return cleanedUri

# def suggestionToTriple(suggestion, asJson = False, graph = None):
def suggestionToTriple(suggestion, graph = None):
    # if asJson is True:
    # print("Toimii")
    g = None
            
    if graph is None:
        g = initGraph()
    else:
        g = graph

    if suggestion is not None:
        uri = yso['p{}'.format(50000 + suggestion["id"])]
        # g.add((uri, RDF.type, SKOS.Concept))
        g.add((quoteAdder(uri), RDF.type, SKOS.Concept))

        for tag in suggestion["tags"]:
            if 'maantieteellinen' in tag["label"].lower():
                g.add(((URIRef(quoteAdder(uri)), RDF.type, URIRef(quoteAdder(ysometa + 'GeographicalConcept')))))

        suggestion_system_url = os.environ.get('SUGGESTION_SYSTEM_ISSUE_URL', None)
        # g.add((URIRef(uri), RDF.type, URIRef(ysometa + 'ConceptAAA')))


        g.add((URIRef(quoteAdder(uri)),  RDF.type, URIRef(quoteAdder(ysometa + 'Concept'))))

#         skos + 'ConceptQQQ'
#         type: [
# "http://www.yso.fi/onto/yso-meta/Concept",
# "skos:Concept"
# ],

        g.add(( URIRef(quoteAdder(uri)), foaf.homepage, URIRef(quoteAdder(f'{suggestion_system_url}/{suggestion["id"]}'))))

        #Tässä kohtaa, jos ottaa uriCleanerin pois, graph-osa häviää json-ld-tulosteesta kokonaan????
        g.add((URIRef(quoteAdder(uri)), dct.created, Literal(suggestion["created"].date(), datatype=XSD.date)))
        g.add((URIRef(quoteAdder(uri)), dct.modified, Literal(suggestion["modified"].date(), datatype=XSD.date)))

        if "fi" in suggestion["preferred_label"].keys() and "value" in suggestion["preferred_label"]["fi"].keys():
            g.add((URIRef(quoteAdder(uri)), skos.prefLabel, Literal(suggestion["preferred_label"]["fi"]["value"], lang='fi')))
            
        # if "fi" in suggestion["preferred_label"].keys():
        #     codeExplicator("suggestion")

        if "sv" in suggestion["preferred_label"].keys() and "value" in suggestion["preferred_label"]["sv"].keys():
            g.add((URIRef(quoteAdder(uri)), skos.prefLabel, Literal(suggestion["preferred_label"]["sv"]["value"], lang='sv')))

        if "en" in suggestion["preferred_label"].keys():
            g.add((URIRef(quoteAdder(uri)), skos.prefLabel, Literal(suggestion["preferred_label"]["en"], lang='en')))

        for group in suggestion["groups"]:

#Toimii            g.add((URIRef(uri), skos.member, URIRef(cleanedUri)))
            g.add((URIRef(quoteAdder(uri)), skos.member, term.URIRef(quoteAdder(group.get('uri')))))

        for match in suggestion["broader_labels"]:
            g.add((URIRef(quoteAdder(uri)), skos.broadMatch, URIRef(quoteAdder(match.get('uri')))))
            # g.add((URIRef(quoteAdder(uri)), skos.broadMatch, Literal(match.get('value'))))

        g.add((URIRef(quoteAdder(uri)), skos.note, Literal(suggestion["scopeNote"])))

        for aLabel in suggestion["alternative_labels"]:
            g.add((URIRef(quoteAdder(uri)), skos.altLabel, Literal(aLabel["value"]))) #)) Literal(altLabel["value"]) 
            
        for match in suggestion["narrower_labels"]:
            g.add((URIRef(quoteAdder(uri)), skos.narrowMatch, URIRef(quoteAdder(match.get('uri')))))
        
        for match in suggestion["related_labels"]:
            g.add((URIRef(quoteAdder(uri)), skos.relatedMatch, URIRef(quoteAdder(match.get('uri')))))

#         # Datetimes need to be converted to string 
#         suggestion['created'] = str(suggestion['created'])
#         suggestion['modified'] = str(suggestion['modified'])
#         # Datetimes are in the right format (string), now it is time to create a json
#         suggestionInJson = json.dumps(suggestion)
#         # Json uses double quotes
#         suggestionInJsonWihtDQ = suggestionInJson.replace("'", '"')
#         # suggestionInJsonWihtDQ = json.loads(suggestionInJsonWihtDQ)
#         print(suggestionInJsonWihtDQ)
#         print("suggestionInJsonWihtDQ:n tyyppi on nyt:")
#         print(type(suggestionInJsonWihtDQ))
    # print(g)
    g_as_string = str(g)
    print(g_as_string)
    gg = json.dumps(g_as_string)
    # print(gg)
    gg = gg[:-1:]
    gg = gg[1 : : ]
    ggg = g.serialize(format='turtle', context=listContext(), indent=4).decode(' ')
    print("suggestion on tyyppiä")
    print(type(suggestion))
    print(suggestion)
    print("***")
    print("ggg on tyyppiä")
    print(type(ggg))
    # print (ggg)
    #     dq = "'"
    # newstr = dq + strObj + dq
    # newstr.replace("'", '"')
    # print(newstr)
    # print(type(newstr))
    # return newstr

    # OOKOO gggg = ggg.replace(r"'", '"').replace("\n", "")
    gggg = ggg.replace(r"''", '"').replace(r"'", '').replace("\n", "") #.replace('"', '') #.replace('\\"', '"')
    # gggg = gg[:-1:]
    # gggg = gg[1 : : ]
    print("gg")
    print(gg)
    print("ggg")
    print(ggg)
    print("gggg")
    print(gggg)

    return gggg


    # else:
    #     print("Ei toimi")




# ### ÄLÄ tuhoa alla olevaa



#         # print("Ehdotus on tyyppiä :")
#         # print(type(suggestion))
#         # for key in suggestion:
#         #     print("Avain levelillä 0 on: ")
#         #     print(key)
#         #     print("Avain levelillä 0 on: ")
#         #     print(suggestion.get(key))
#         #     print("Value on tyyppiä :")
#         #     print(type(suggestion.get(key)))
#         #     if type(suggestion.get(key)) is int:
#         #         print("Mikä tässä on pielessä: " + typeConverter(suggestion.get(key)))
#         #         # if type(typeConverter(suggestion.get(key))) is str:
#         #         #     print("Muuttui stringiksi ")
#         #     if type(suggestion.get(key)) is dict:
#         #         print("on Dikti")
#         #         level1Dict = suggestion.get(key)
#         #         for subKey1 in level1Dict:
#         #             print("Sublevelillä 1 Avain on: ")
#         #             print(subKey1)
#         #             print("Sublevelillä 1 Arvo on: ")
#         #             print(level1Dict.get(subKey1))
#         #             print("Value on tyyppiä :")
#         #             print(type(level1Dict.get(subKey1)))
#         #             if type(level1Dict.get(subKey1)) is dict:
#         #                 print("on Dikti")
#         #                 level2Dict = level1Dict.get(subKey1)
#         #                 for subKey2 in level2Dict:
#         #                     print("Sublevelillä 2 Avain on: ")
#         #                     print(subKey2)
#         #                     print("Sublevelillä 2 Arvo on: ")
#         #                     print(level2Dict.get(subKey2))
#         #                     print("Value on tyyppiä :")
#         #                     print(type(level2Dict.get(subKey2)))
#         #                     if type(level2Dict.get(subKey2)) is dict:
#         #                         print("on Dikti")
#         #                         level3Dict = level2Dict.get(subKey2)
#         #                         for subKey3 in level3Dict:
#         #                             print("Sublevelillä 3 Avain on: ")
#         #                             print(subKey3)
#         #                             print("Sublevelillä 3 Arvo on: ")
#         #                             print(level3Dict.get(subKey3))

# ### ÄLÄ tuhoa ylläolevaa

#         # Datetimes need to be converted to string 
#         suggestion['created'] = str(suggestion['created'])
#         suggestion['modified'] = str(suggestion['modified'])
#         # Datetimes are in the right format (string), now it is time to create a json
#         suggestionInJson = json.dumps(suggestion)
#         # Json uses double quotes
#         suggestionInJsonWihtDQ = suggestionInJson.replace("'", '"')
#         # suggestionInJsonWihtDQ = json.loads(suggestionInJsonWihtDQ)
#         print(suggestionInJsonWihtDQ)
#         print("suggestionInJsonWihtDQ:n tyyppi on nyt:")
#         print(type(suggestionInJsonWihtDQ))


#         ghi = initGraph()

#         # uri = yso['pXXX{}'.format(50000 + suggestion["id"])]
#         #     # g.add((uri, RDF.type, SKOS.Concept))
#         # ghi.add((uri, RDF.type, SKOS.Concept))

#         # for tag in suggestionInJsonWihtDQ["tags"]:
#         #     if 'maantieteellinen' in tag["label"].lower():
#         #         ghi.add(((URIRef(uri), RDF.type, URIRef(ysometa + 'GeographicalConcept'))))

#         #     suggestion_system_url = os.environ.get('SUGGESTION_SYSTEM_ISSUE_URL', None)
#         #     ghi.add((URIRef(uri), RDF.type, URIRef(ysometa + 'ConceptAAA')))


#         #     ghi.add((URIRef(uri),  RDF.type, URIRef(skos + 'ConceptQQQ')))

#         #     ghi.add((URIRef(uri), foaf.homepage, URIRef(f'{suggestion_system_url}/{suggestion["id"]}')))

#         #     #Tässä kohtaa, jos ottaa uriCleanerin pois, graph-osa häviää json-ld-tulosteesta kokonaan????
#         #     ghi.add((URIRef(uriCleaner(uri)), dct.created, Literal(suggestion["created"])))









#         # for subj, pred, obj in ghi:
#         #     print(subj)
#         #     print(pred)
#         #     print(obj)
#         #     if (subj, pred, obj) not in g:
#         #         raise Exception("It better be!")

#         # ghi_ser = ghi.serialize(format='json-ld', context=listContext(), indent=4)



#         # Harjoitusalue päättyy

#         # return ghi
#         return suggestionInJsonWihtDQ






