import rdflib
from rdflib.namespace import FOAF, RDFS
from .shared import *
from .gml_naar_dict import xml_naar_dict, geometrie_terugzetten
import collections
from zipfile import ZipFile

__verbose = False

def conversion(dict: collections.OrderedDict) -> rdflib.Graph:
    if dict == {}:
        return
    graph = rdflib.Graph()
    for Class, _value in dict.items():
        typeName = dict[Class]["type"]
        if "class" in dict[Class]:
            className = dict[Class]["class"]["#text"].title().replace(" ", "")
        else:
            className = typeName

        idId = stringToId(dict[Class]["@gml:id"], "id", className)
        DocId = stringToId(dict[Class]["@gml:id"], "doc", className)
        if className != typeName:
            graph.add((idId, RDF.type, stringToClass(className+"_"+typeName)))
        graph.add((idId, RDF.type, stringToClass(typeName)))
        graph.add((idId, FOAF.isPrimaryTopicOf, DocId))
    for key, value in dict[Class].items():
        if key == "imgeo:identificatie":
            nen3610Id = predefinedStringToIRI("nen3610:"+value['imgeo:NEN3610ID']['imgeo:lokaalID'])
            graph.add((idId, predefinedStringToIRI("nen3610:identificatie"),nen3610Id))
            graph.add((nen3610Id, predefinedStringToIRI("nen3610:namespace"), stringToLiteral(value['imgeo:NEN3610ID']['imgeo:namespace']) ))
            graph.add((nen3610Id, predefinedStringToIRI("nen3610:lokaalID"), stringToLiteral(value['imgeo:NEN3610ID']['imgeo:lokaalID']) ))

            continue
        if key == "function":
            ReplacetypeName = typeName
            if typeName == "Wegdeel":
                ReplacetypeName = "Weg"
            if value["#text"] != "Waardeonbekend":
                graph.add((idId, predefinedStringToIRI("imgeo:functie"), predefinedStringToIRI("imgeobegrip:" + value["#text"].title().replace(" ", "")+"_Functie"+ReplacetypeName)))
            continue
        if "imgeo:plus-functie" == key:
            if value["#text"] != "Waardeonbekend":
                graph.add((idId, predefinedStringToIRI("imgeo:functie"), predefinedStringToIRI("imgeobegrip:" + value["#text"].title().replace(" ", "")+"_Functie"+ReplacetypeName)))
            continue
        if "surfaceMaterial" in key:
            if value["#text"] != "Waardeonbekend":
                graph.add((idId, RDF.type, stringToClass( value["#text"].title().replace(" ", ""))))
            continue
        if "imgeo:plus-fysiekVoorkomen" in key:
            if value["#text"] != "Waardeonbekend":
                graph.add((idId, RDF.type, stringToClass( value["#text"].title().replace(" ", ""))))
            continue
        # if key == "imgeo:plus-fysiekVoorkomen":
        #     graph.add((idId, RDF.type, predefinedStringToIRI("imgeobegrip:" + value["#text"])))
        #     continue
        if "imgeo:kruinlijn" in key:
            if "@nilReason"in value:
                continue
            else:
                wkt = convertGMLShapetoWKT(value)
                if wkt != "":
                    Bnode = rdflib.BNode()
                    graph.add((idId, predefinedStringToIRI("geometry:hasGeometry"), Bnode))
                    graph.add((Bnode, predefinedStringToIRI("geometry:asWKT"), wktToLiteral(wkt)))
            continue
        if "imgeo:geometrie2d" in key:
            if "@nilReason"in value:
                continue
            else:
                wkt = convertGMLShapetoWKT(value)
                if wkt != "":
                    Bnode = rdflib.BNode()
                    graph.add((idId, predefinedStringToIRI("geometry:hasGeometry"), Bnode))
                    graph.add((Bnode, predefinedStringToIRI("geometry:asWKT"), wktToLiteral(wkt)))
            continue

        if type(value) == collections.OrderedDict:
            continue

        if key == "creationDate":
            graph.add((DocId, predefinedStringToIRI("imgeo:"+key), stringToLiteral(value["#text"])))
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
        if key == "imgeo:bgt-status" :
            graph.add((idId, predefinedStringToIRI(key), predefinedStringToIRI('bgtBegrip:'+value)))
            continue
        if key == "imgeo:eindRegistratie" :
            graph.add((DocId, predefinedStringToIRI(key), stringToLiteral(value)))
            continue
        if "OpTalud" in key :
            graph.add((idId, predefinedStringToIRI("imgeo:opTalud"), stringToLiteral(value)))
            continue
        if key == "imgeo:relatieveHoogteligging" :
            graph.add((idId, predefinedStringToIRI(key), stringToLiteral(value)))
            continue
        if key == "imgeo:tijdstipRegistratie" :
            graph.add((DocId, predefinedStringToIRI(key), stringToLiteral(value)))
            continue
        if key == "imgeo:naam" :
            if value:
                graph.add((idId, RDFS.label, stringToLiteral(value)))
            continue
        if key == "imgeo:identificatieBAGPND" :
            if value:
                graph.add((idId,predefinedStringToIRI("imgeo:Pand"), predefinedStringToIRI("bag:"+value)))
        if "imgeo" in key :
            print(key, value)
            if value:
                try:
                    graph.add((idId, predefinedStringToIRI(key), stringToLiteral(value)))
                except:
                    print("failed to add", type(value))
            if __verbose:
                print(key, value)
            continue
        if __verbose:
            print(key, value)

    return graph

def _convertBGT():
    Outfile = open("output/output.nt", "wb+")
    file_name ="resources/bgt_begroeidterreindeel.gml"
    with open(file_name) as f:
        line = f.readline()
        while len(line) > 0:
            bgt_dict_initial = xml_naar_dict(line)
            bgt_dict_final = geometrie_terugzetten(bgt_dict_initial)
            if bgt_dict_final != {}:
                graph = conversion(bgt_dict_final['cityObjectMember'])
                Outfile.write(graph.serialize(format='nt'))
            line = f.readline()


def convertBGT():
    file_name ="resources/bgt-citygml-nl-nopbp.zip"
    with ZipFile(file_name, 'r') as zip:
        listOfFileNames = zip.namelist()
        for file in listOfFileNames:
            # SKIPPING FILENAMES FOR TESTING
            # if file not in [ "bgt_wegdeel.gml"]: #"bgt_begroeidterreindeel.gml", "bgt_pand.gml"
            #     continue
            with zip.open(file) as f:
                line = f.readline()
                j = 0
                i = 0
                while len(line) > 0 and i < 100000:
                    Outfile = open("output/output_"+str(file[:-4])+"_"+str(j)+".nt", "wb+")
                    j += 1
                    i = 0
                    while i < 100000:
                        bgt_dict_initial = xml_naar_dict(line)
                        bgt_dict_final = geometrie_terugzetten(bgt_dict_initial)
                        if bgt_dict_final != {}:
                            graph = conversion(bgt_dict_final['cityObjectMember'])
                            Outfile.write(graph.serialize(format='nt'))
                        line = f.readline()
                        i += 1
