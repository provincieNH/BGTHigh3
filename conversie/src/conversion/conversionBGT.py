import rdflib
from rdflib.namespace import FOAF
from .shared import *
from .gml_naar_dict import xml_naar_dict
import collections

def conversion(dict: collections.OrderedDict) -> rdflib.Graph:
    graph = rdflib.Graph()

    for Class, _value in dict.items():
        className = dict[Class]["imgeo:bgt-status"]["#text"]
        DocId = stringToId(dict[Class]["@gml:id"], "doc", className)
        idId = stringToId(dict[Class]["@gml:id"], "id", className)
        graph.add((idId, RDF.type, stringToClass(className)))
        graph.add((idId, FOAF.isPrimaryTopicOf, DocId))
    for key, value in dict[Class].items():
        if key == "imgeo:identificatie":
            nen3610Id = predefinedStringToIRI("nen3610:"+value['imgeo:NEN3610ID']['imgeo:lokaalID'])
            graph.add((idId, predefinedStringToIRI("nen3610:identificatie"),nen3610Id))
            graph.add((nen3610Id, predefinedStringToIRI("nen3610:namespace"), stringToLiteral(value['imgeo:NEN3610ID']['imgeo:namespace']) ))
            graph.add((nen3610Id, predefinedStringToIRI("nen3610:lokaalID"), stringToLiteral(value['imgeo:NEN3610ID']['imgeo:lokaalID']) ))

            continue
        if key == "imgeo:functie":
            graph.add((idId, predefinedStringToIRI(key), stringToLiteral(value["#text"])))
            continue
        if key == "class":
            graph.add((idId, RDF.type, stringToLiteral(value["#text"])))
            continue
        if key == "imgeo:plus-fysiekVoorkomen":
            graph.add((idId, RDF.type, stringToLiteral(value["#text"])))
            continue
        if "imgeo:kruinlijn" in key:
            if "@nilReason"in value:
                continue
            else:
                graph.add((idId, predefinedStringToIRI("imgeo:kruinlijn"), stringToLiteral("GEOMETRY")))
            continue
        if "imgeo:geometrie2d" in key:
            if "@nilReason"in value:
                continue
            else:
                graph.add((idId, predefinedStringToIRI("imgeo:geometry"), stringToLiteral("GEOMETRY")))
            continue

        if type(value) == collections.OrderedDict:
            continue

        if key == "creationDate":
            graph.add((idId, predefinedStringToIRI("imgeo:"+key), stringToLiteral(value["#text"])))
            continue
        if key == "imgeo:bronhouder" :
            IRI = getBronhouderIri(value)
            if IRI != "":
                graph.add((DocId, predefinedStringToIRI(key), stringToIRI(IRI)))
            continue
        if key == "imgeo:inOnderzoek" :
            graph.add((DocId, predefinedStringToIRI(key), stringToLiteral(value)))
            continue
        if key == "imgeo:LV-publicatiedatum" :
            graph.add((DocId, predefinedStringToIRI(key), stringToLiteral(value)))
            continue

        if "imgeo" in key :
            graph.add((idId, predefinedStringToIRI(key), stringToLiteral(value)))
            continue

    return graph

def convertBGT():
    file = open("output/output.nt", "wb+")
    bgt_gml ="resources/bgt_begroeidterreindeel.gml"

    for index, dict in enumerate(xml_naar_dict(bgt_gml)['CityModel']['cityObjectMember']):

        graph = conversion(dict)
        file.write(graph.serialize(format='nt'))
