import rdflib
from rdflib.namespace import FOAF, RDFS
from .shared import *
from .gml_naar_dict import xml_naar_dict, geometrie_terugzetten
import collections
from zipfile import ZipFile

__verbose = False


def conversionPand(graph, dict, idId) :
    bnodeNummerAanduidingsReeks = rdflib.BNode()
    graph.add((idId, predefinedStringToIRI("imgeo:nummeraanduidingreeks"), bnodeNummerAanduidingsReeks))
    text = dict["imgeo:Nummeraanduidingreeks"]["imgeo:nummeraanduidingreeks"]["imgeo:Label"]["imgeo:tekst"]
    numbers = text.split("-")
    if len(numbers) == 2:
        graph.add((bnodeNummerAanduidingsReeks,RDFS.label,stringToLiteral(numbers[0])))
        graph.add((bnodeNummerAanduidingsReeks,RDFS.label,stringToLiteral(numbers[1])))
    if "imgeo:identificatieBAGVBOHoogsteHuisnummer" in dict["imgeo:Nummeraanduidingreeks"]:
        hoogsteNummer = dict["imgeo:Nummeraanduidingreeks"]["imgeo:identificatieBAGVBOHoogsteHuisnummer"]
        graph.add((bnodeNummerAanduidingsReeks,predefinedStringToIRI("imgeo:identificatieBAGVBOHoogsteHuisnummer"),stringToLiteral(hoogsteNummer)))
    elif len(numbers) == 1:
        graph.add((bnodeNummerAanduidingsReeks,predefinedStringToExportToWktIRI("imgeo:laagsteHuisnummer"),stringToLiteral(numbers[0])))

    laagsteNummer = dict["imgeo:Nummeraanduidingreeks"]["imgeo:identificatieBAGVBOLaagsteHuisnummer"]

    graph.add((bnodeNummerAanduidingsReeks,RDFS.label,stringToLiteral(text)))
    graph.add((bnodeNummerAanduidingsReeks,predefinedStringToIRI("imgeo:Nummeraanduidingreeksnummeraanduidingreeks"),stringToLiteral(text)))
    graph.add((bnodeNummerAanduidingsReeks,predefinedStringToIRI("imgeo:identificatieBAGVBOLaagsteHuisnummer"),stringToLiteral(laagsteNummer)))


    return graph

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
        graph.add((DocId, RDF.type, predefinedStringToIRI("imgeo:Objectregistratie")))
        graph.add((idId, FOAF.isPrimaryTopicOf, DocId))
    for key, value in dict[Class].items():
        if key == "imgeo:identificatie":
            nen3610Id = predefinedStringToIRI("nen3610:"+value['imgeo:NEN3610ID']['imgeo:lokaalID'])
            graph.add((idId, predefinedStringToIRI("nen3610:identificatie"),nen3610Id))
            graph.add((nen3610Id, predefinedStringToIRI("nen3610:namespace"), stringToLiteral(value['imgeo:NEN3610ID']['imgeo:namespace']) ))
            graph.add((nen3610Id, predefinedStringToIRI("nen3610:lokaalID"), stringToLiteral(value['imgeo:NEN3610ID']['imgeo:lokaalID']) ))
            graph.add((nen3610Id, RDF.type, predefinedStringToIRI("nen3610def:NEN3610Identificatie")))
            continue
        if key == "function":
            ReplacetypeName = typeName
            if typeName == "Wegdeel":
                ReplacetypeName = "Weg"
            if value["#text"].lower() != "waardeonbeExportToWktkend":
                graph.add((idId, predefinedStringToIRI("imgeo:functie"), predefinedStringToIRI("imgeobegrip:" + value["#text"].title().replace(" ", "")+"_Functie"+ReplacetypeName)))
            continue
        if "imgeo:plus-functie" == key:
            if value["#text"].lower() != "waardeonbekend":
                graph.add((idId, predefinedStringToIRI("imgeo:functie"), predefinedStringToIRI("imgeobegrip:" + value["#text"].title().replace(" ", "")+"_Functie"+ReplacetypeName)))
            continue
        if "surfaceMaterial" in key:
            if value["#text"].lower() != "waardeonbekend":
                graph.add((idId, RDF.type, stringToClass( value["#text"].title().replace(" ", ""))))
            continue
        if "imgeo:plus-fysiekVoorkomen" in key:
            if value["#text"].lower() != "waardeonbekend":
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
                    Bnode = stringToId(dict[Class]["@gml:id"]+"-geometry-kruinlijn", "id", className)
                    graph.add((idId, predefinedStringToIRI("geometry:hasGeometry"), Bnode))
                    graph.add((Bnode, predefinedStringToIRI("geometry:asWKT"), wktToLiteral(wkt)))
                    graph.add((Bnode, RDF.type, predefinedStringToIRI("geometry:Geometry")))
            continue
        if "imgeo:geometrie2d" in key:
            if "@nilReason"in value:
                continue
            else:
                wkt = convertGMLShapetoWKT(value)
                if wkt != "":
                    Bnode = stringToId(dict[Class]["@gml:id"]+"-geometry2d", "id", className)
                    graph.add((idId, predefinedStringToIRI("geometry:hasGeometry"), Bnode))
                    graph.add((Bnode, predefinedStringToIRI("geometry:asWKT"), wktToLiteral(wkt)))
                    graph.add((Bnode, RDF.type, predefinedStringToIRI("geometry:Geometry")))
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
            if value and int(value) > 0:
                graph.add((idId,predefinedStringToIRI("imgeo:Pand"), predefinedStringToIRI("bag:"+value)))
            continue
        if key == "imgeo:overbruggingIsBeweegbaar" :
            graph.add((DocId, predefinedStringToIRI(key), stringToLiteral(value)))
            continue

        if key == "imgeo:nummeraanduidingreeks" :
            if type(value) == type([]):
                for element in value:
                    graph = conversionPand(graph, element, idId)
            if type(value) == type({}):
                graph = conversionPand(graph, value, idId)
            continue
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

def convertFile(zip, file, sample):
    with zip.open(file) as f:
        try:
            line = f.readline()
        except:
            line = ""
        j = 0
        i = 0
        if sample:
            maxLines = 250000
        else:
            maxLines = 900000000
        while len(line) > 0 and i < maxLines:
            Outfile = open("output/output_"+str(file[:-4])+"_"+str(j)+".nt", "wb+")
            j += 1
            i = 0
            while i < 250000 and len(line) > 0:
                bgt_dict_initial = xml_naar_dict(line)
                bgt_dict_final = geometrie_terugzetten(bgt_dict_initial)
                if bgt_dict_final != {}:
                    graph = conversion(bgt_dict_final['cityObjectMember'])
                    try:
                        pass
                    except:
                        print("FAILED TO CREATE GRAPH CONTINUEING")
                        continue
                    Outfile.write(graph.serialize(format='nt'))

                i += 1
                line = f.readline()



def convertBGT():
    file_name ="resources/bgt-citygml-nl-nopbp.zip"
    FileRoundTwo = []
    with ZipFile(file_name, 'r') as zip:
        listOfFileNames = zip.namelist()
        for file in listOfFileNames:
            if file not in [  "bgt_pand.gml"]: # ,
                FileRoundTwo.append(file)
                continue
            else:
                convertFile(zip, file, False)
        for file in FileRoundTwo:
            convertFile(zip, file, False)
