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

def codeExplicator(codeTxt: str):
  print('\n')
  print('****** By command: ')
  print(codeTxt)  
  print('******')

def uriCleaner(uriToBeCleaned):
  cleanedUri = requests.get(uriToBeCleaned).url
  return cleanedUri

def suggestionToTriple(suggestion, asJson = False, graph = None):
    if asJson is True:
        print("Toimii")
        g = None
                
        if graph is None:
            g = initGraph()
        else:
            g = graph

        if suggestion is not None:
            uri = yso['pXXX{}'.format(50000 + suggestion["id"])]
            # g.add((uri, RDF.type, SKOS.Concept))
            g.add((uri, RDF.type, SKOS.Concept))

            for tag in suggestion["tags"]:
                if 'maantieteellinen' in tag["label"].lower():
                    g.add(((URIRef(uri), RDF.type, URIRef(ysometa + 'GeographicalConcept'))))

            suggestion_system_url = os.environ.get('SUGGESTION_SYSTEM_ISSUE_URL', None)
            g.add((URIRef(uri), RDF.type, URIRef(ysometa + 'ConceptAAA')))


    # Nyt:
    # type: [
    # "http://finto.fi/yso/fi/ConceptAAA",
    # "skos:ConceptQQQ"
    # ],


    # Pitaisi olla:
    # "http://www.yso.fi/onto/yso-meta/Concept",
    # "skos:Concept"


    #OK
            g.add((URIRef(uri),  RDF.type, URIRef(skos + 'ConceptQQQ')))

            g.add((URIRef(uri), foaf.homepage, URIRef(f'{suggestion_system_url}/{suggestion["id"]}')))

            #Tässä kohtaa, jos ottaa uriCleanerin pois, graph-osa häviää json-ld-tulosteesta kokonaan????
            g.add((URIRef(uriCleaner(uri)), dct.created, Literal(suggestion["created"].date(), datatype=XSD.date)))

            if "fi" in suggestion["preferred_label"].keys() and "value" in suggestion["preferred_label"]["fi"].keys():
                g.add((URIRef(uri), skos.prefLabel, Literal(suggestion["preferred_label"]["fi"]["value"], lang='fi')))
                
            if "fi" in suggestion["preferred_label"].keys():
                codeExplicator("suggestion")

            if "sv" in suggestion["preferred_label"].keys() and "value" in suggestion["preferred_label"]["sv"].keys():
                g.add((URIRef(uri), skos.prefLabel, Literal(suggestion["preferred_label"]["sv"]["value"], lang='sv')))

            if "en" in suggestion["preferred_label"].keys():
                g.add((URIRef(uri), skos.prefLabel, Literal(suggestion["preferred_label"]["en"], lang='en')))

            for group in suggestion["groups"]:
    #Toimii            g.add((URIRef(uri), skos.member, URIRef(cleanedUri)))
                g.add((URIRef(uri), skos.member, URIRef(group["uri"])))
                # g.add((URIRef(ul.parse.quote(uri)), skos.member, URIRef(group["uri"])))

            for match in suggestion["broader_labels"]:
                g.add((URIRef(uri), skos.broadMatch, URIRef(match["uri"])))

            g.add((URIRef(uri), skos.note, Literal(suggestion["scopeNote"])))

            for aLabel in suggestion["alternative_labels"]:
                g.add((URIRef(uri), skos.altLabel, Literal(aLabel["value"]))) #)) Literal(altLabel["value"]) 
                
            for match in suggestion["narrower_labels"]:
                g.add((URIRef(uri), skos.narrowMatch, URIRef(match["uri"])))
            
            for match in suggestion["related_labels"]:
                print("Mitä tähän tulostuu?")
                print(match["uri"])
                #rdflib.term.URIRef(uri)
                print('Entä tämä sitten?')
                print(URIRef(match["uri"]))
                u = URIRef(match["uri"])
                # u = URIRef(u'www.jotain.url')
                # g.add((URIRef(uri), skos.relatedMatch, match["uri"]))
                #Testi g.add((URIRef(uri), skos.relatedMatch, u))
                g.add((URIRef(uri), skos.relatedMatch, u))
        
        # print( g.serialize(format='json-ld', context=listContext(), indent=4).decode('utf8').replace("'", ''))
        # print(uri)
        # print(uriCleaner(uri))
        # for s, p, o in g:
        #     print((s, p, o))
        #Periaatteessa toimiva gg = g.serialize(format='json-ld', context=listContext(), indent=4).decode('utf8').replace("'", '')
        # gg = g.serialize(format='json-ld', context=listContext(), indent=4).decode('utf8').replace("'", '')
        gg = g.serialize(format='json-ld', context=listContext(), indent=4).decode('utf8').replace("'", '')

        

        print('*** Ensin pelkkä g')
        for s, p, o in g:
            print('####')
            print((s))
            print((p))
            print((o))
            print('####')
        print('*** Sitten gg')    
        print(gg)


        return gg


    else:
        print("Ei toimi")

        # from functools import singledispatch

        # @singledispatch
        # def keys_to_strings(ob):
        #     return ob

        # @keys_to_strings.register(dict)
        # def _handle_dict(ob):
        #     return {str(v): keys_to_strings(v) for k, v in ob.items()}

        # @keys_to_strings.register(list)
        # def _handle_list(ob):
        #     return [keys_to_strings(v) for v in ob]
        
        # suggestions2 = json.dumps(_handle_list(suggestion))
        
        # suggestion = str(suggestion)

                    # replaceQuotes = serialized_object.replace("'", '"')
        # cleanedSuggestion = json.dumps(suggestion)
            # return cleanedJson
#         var myObj = {mykey: "my value"}
#    ,myObjJSON = JSON.stringify(myObj);
        # # inititialising json object 
        # ini_string = {'nikhil': 1, 'akash' : 5,  
        #             'manjeet' : 10, 'akshat' : 15} 
        
        # # printing initial json 
        # suggestion = json.dumps(suggestion) 
        # print ("initial 1st dictionary", suggestion) 
        # print ("type of ini_object", type(suggestion)) 
        
        # # converting string to json 
        # final_dictionary = json.loads(suggestion) 
        
        # # printing final result 
        # print ("final dictionary", str(final_dictionary)) 
        # print ("type of final_dictionary", type(final_dictionary)) 

# "\"
# \""   

        # data = []
        # for line in suggestion:
        #     data.append(json.loads(line))

        # print(data)

        # loaded_json = json.loads(str(suggestion))
        # for x in loaded_json:
        #     print("%s: %d" % (x, loaded_json[x]))

        # class Test(object):
        #     def __init__(self, data):
        #         self.__dict__ = json.loads(data)

        # test1 = Test(suggestion)
        # print(test1)
        # first_json = json.dumps(suggestion)
        # print(first_json)

        # d = {"first_name": "Alfred", "last_name":"Hitchcock"}

# def func(*args):
#     mylist=[]
#     z = {'x':(123,"SE",2,1),'q':(124,"CI",1,1)}
#     for x,y in z.items():
#         for t in args:
#             if t in y:
#                 mylist.append(x)
#     return mylist
# print (func(1,"CI"))



        # for key,val in suggestion.items():
        #     print("{} = {}".format(key, val))
    
        finalDict = {}
        level1Dict = {}
        level2Dict = {}
        level3Dict = {}
        # for x, y in suggestion:
        #     # for t in args:
        #     # if t in y:
        #     # myDict.update(x, y)
        #     # myDict.add(x, y)
        #     myDict[x] = y

        print(type(suggestion))
        for key in suggestion:
            print("Avain on: ")
            print(key)
            print("Arvo on: ")
            print(suggestion.get(key))
            if type(suggestion.get(key)) is dict:
                print("on Dikti")
                level1Dict = suggestion.get(key)
                for subKey1 in level1Dict:
                    print("Sublevelillä 1 Avain on: ")
                    print(subKey1)
                    print("Sublevelillä 2 Arvo on: ")
                    print(level1Dict.get(subKey1))
            # print("Aarvo on ") + suggestion.get(key))
            # print(suggestion.get(key))
            # print(value)
        # for key, value in suggestion:
        #     myDict[key] = value


        # for key in myDict.keys:
        #     print("Avain on: " + key)
        #     print("Arvo on: " + myDict.get(key))
    # print (func(1,"CI"))


# current_dict = {'corse': 378, 'cielo': 209, 'mute': 16}
# print(current_dict)
# def replace_value_with_definition(key_to_find, definition):
#     for key in current_dict.keys():
#         if key == key_to_find:
#             current_dict[key] = definition

# replace_value_with_definition('corse', 'Definition of "corse"')
# print(current_dict)




        return suggestion






