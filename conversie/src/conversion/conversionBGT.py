import rdflib
from rdflib.namespace import FOAF, RDFS
from .shared import *
from .gml_naar_dict import xml_naar_dict, geometrie_terugzetten, first
import collections
from zipfile import ZipFile
import os
import shutil

__verbose = False

# Converts the numberaanduidingreeks, available on a Pand to statementens
def conversionPand(graph, dict, idId) :
    """
    Adds the information about the surrounding BAG panden to the BGT object.

    :param  graph: Graph storing a single BGT object.
            dict: Part of the dictionary with the information about the surrounding BAG panden.
            idId: Id of the BGT object.
    :return bgt_dict_xml_geom:
    """

    # Creating an blankNode storing the bag nummeraanduidingreeks properties.
    bnodeNummer = rdflib.BNode()

    # Adding link from bgt-Object -> bagNummeraanduidingsReeks.
    graph.add((idId, predefinedStringToIRI("imgeo:nummeraanduidingreeks"), bnodeNummer))

    # Getting the label for the surrounding numbers
    text = dict["imgeo:nummeraanduidingreeks"]["imgeo:Label"]["imgeo:tekst"]

    # Splitting the text to get the lowest and the highest number.
    numbers = text.split("-")

    # If the reeks consists out of two numbers: lowest-highest number. We will add both numbers to the dataset.
    if len(numbers) == 2:
        # bagNummeraanduidingsReeks -> number1 and bagNummeraanduidingsReeks -> number2
        graph.add((bnodeNummer,predefinedStringToIRI("imgeo:laagsteHuisnummer"),stringToLiteral(numbers[0])))
        graph.add((bnodeNummer,predefinedStringToIRI("imgeo:hoogsteHuisnummer"),stringToLiteral(numbers[1])))

        # Checking if the highest number exists in the dictionary. This will only occur if the there is a highest and a lowest number,
        # else there will only be a lowest number.
        if "imgeo:identificatieBAGVBOHoogsteHuisnummer" in dict:
            hoogsteNummerPand = dict["imgeo:identificatieBAGVBOHoogsteHuisnummer"]
            # bagNummeraanduidingsReeks -> BagPandID hoogste nummer.
            graph.add((bnodeNummer,predefinedStringToIRI("imgeo:identificatieBAGVBOHoogsteHuisnummer"),predefinedStringToIRI("bag:"+hoogsteNummerPand)))

    # If the string only consists out of a single number will will only add in the lowest number
    elif len(numbers) == 1:
        graph.add((bnodeNummer,predefinedStringToIRI("imgeo:laagsteHuisnummer"),stringToLiteral(numbers[0])))

    # We will also add in the bagPandId of the lower house number.
    laagsteNummerPand = dict["imgeo:identificatieBAGVBOLaagsteHuisnummer"]
    graph.add((bnodeNummer,predefinedStringToIRI("imgeo:identificatieBAGVBOLaagsteHuisnummer"),predefinedStringToIRI("bag:"+laagsteNummerPand)))

    # Finally we add the metadata information. What type it is, an rdfs label and the string for the nummeraanduidingreeksNummeraanduidingreeks
    graph.add((bnodeNummer,RDF.type,predefinedStringToIRI("nen3610def:Nummeraanduidingreeksnummeraanduidingreeks")))
    graph.add((bnodeNummer,RDFS.label,stringToLiteral(text)))
    graph.add((bnodeNummer,predefinedStringToIRI("imgeo:Nummeraanduidingreeksnummeraanduidingreeks"),stringToLiteral(text)))

    return graph

#
def conversion(dict: collections.OrderedDict) -> rdflib.Graph:
    """ Main conversion script. In this script with the help of helperfunctions from the shared.py script
    we convert the dictionary to a small graph.

    :param  dict: The dictionary with the information about the BGT object.
    :return rdflib graph
    """

    # Returning if the dictionary is empty
    if dict == {}:
        return

    # Creating an empty graph to store in the data.
    graph = rdflib.Graph()

    #First and only element
    Class = first(dict)

    # Getting the information dictionary.
    DictClass = dict[Class]
    typeName = DictClass["type"]

    # It could be that a class has a subclass in their name as well. Combining these gives the correct id IRI.
    if "class" in DictClass:
        className = DictClass["class"]["#text"].title().replace(" ", "")
    else:
        # We will just use the typeName.
        className = typeName

    # Retrieving the local ID from the dictionary. This is always in the same location
    # So we can use dictionary strings to get it.
    # If it is not available it should fail, as we need this ID for the IRI.
    idString = DictClass["imgeo:identificatie"]['imgeo:NEN3610ID']['imgeo:lokaalID']

    # Creating the id's for both the object and the Objectregistratie.
    idId = stringToId(idString, "id", className)
    DocId = stringToId(idString, "doc", className)

    # Adding the correct classes with the necessary types.
    if className != typeName:
        graph.add((idId, RDF.type, predefinedStringToIRI("imgeo:"+className+"_"+typeName)))
    graph.add((idId, RDF.type, predefinedStringToIRI("imgeo:"+typeName)))
    graph.add((DocId, RDF.type, predefinedStringToIRI("imgeo:Objectregistratie")))

    # We link the Objectregistratie to the object
    graph.add((idId, FOAF.isPrimaryTopicOf, DocId))

    # Now we will add the properties to the respective classes.
    for key, value in DictClass.items():
        # NEN3610 identificatie, link to the nen3610.
        if key == "imgeo:identificatie":
            # Creating an nen3610ID
            nen3610Id = predefinedStringToIRI("nen3610id:"+idString)
            # Link to the object
            graph.add((idId, predefinedStringToIRI("nen3610:identificatie"),nen3610Id))

            # Add the localId and namespace to the nen3610 object.
            graph.add((nen3610Id, predefinedStringToIRI("nen3610:namespace"), stringToLiteral(value['imgeo:NEN3610ID']['imgeo:namespace']) ))
            graph.add((nen3610Id, predefinedStringToIRI("nen3610:lokaalID"), stringToLiteral(value['imgeo:NEN3610ID']['imgeo:lokaalID']) ))

            # Give the object an type. We do not want any objects without a type.
            graph.add((nen3610Id, RDF.type, predefinedStringToIRI("nen3610def:NEN3610Identificatie")))
            continue

        # MOST ELEMENTS BELOW WILL WORK SIMILAR.
        # If we match the key we will add the corresponding triple to the graph.
        ## If something different occurs it will be explained in the comments.

        # Add function of the object
        if key == "function":
            ReplacetypeName = typeName

            # Due to naming schemes we clean the Wegdeel -> Weg. Doing this with codelist has to be implemented just yet.
            if typeName == "Wegdeel":
                ReplacetypeName = "Weg"
            # Only when the there is a value and it is known we want to add it to the graph.
            if value["#text"].lower() != "waardeonbekend":
                graph.add((idId, predefinedStringToIRI("imgeo:functie"), predefinedStringToIRI("imgeobegrip:" + value["#text"].title().replace(" ", "")+"_Functie"+ReplacetypeName)))
            continue

        # Some objects also have an plus-function.
        if "imgeo:plus-functie" == key:
            if value["#text"].lower() != "waardeonbekend":
                # Only when the there is a value and it is known we want to add it to the graph.
                graph.add((idId, predefinedStringToIRI("imgeo:functie"), predefinedStringToIRI("imgeobegrip:" + value["#text"].title().replace(" ", "")+"_Functie"+ReplacetypeName)))
            continue

        if "surfaceMaterial" in key:
            if value["#text"].lower() != "waardeonbekend":
                # Only when the there is a value and it is known we want to add it to the graph.
                graph.add((idId, RDF.type, predefinedStringToIRI("imgeo:"+ value["#text"].title().replace(" ", ""))))
            continue
        if "imgeo:plus-fysiekVoorkomen" in key:
            if value["#text"].lower() != "waardeonbekend":
                # Only when the there is a value and it is known we want to add it to the graph.
                graph.add((idId, RDF.type, predefinedStringToIRI("imgeo:"+ value["#text"].title().replace(" ", ""))))
            continue


        if "imgeo:kruinlijn" in key:
            # Only when the there is a value and it is known we want to add it to the graph.
            if "@nilReason"in value:
                continue
            else:
                # Converts to wkt
                wkt = convertGMLShapetoWKT(value)

                # Checking just in case if the wkt is empty
                if wkt != "":

                    Bnode = stringToId(idString+"-geometry-kruinlijn", "id", className)
                    graph.add((idId, predefinedStringToIRI("geometry:hasGeometry"), Bnode))
                    graph.add((Bnode, predefinedStringToIRI("geometry:asWKT"), wktToLiteral(wkt)))
                    graph.add((Bnode, RDF.type, predefinedStringToIRI("geometry:Geometry")))
            continue

        # The geometry 2D
        if "imgeo:geometrie2d" in key:

            # Check for @nilReason, empty gml. Not needed in the graph.
            if "@nilReason"in value:
                continue
            else:
                # Converts to wkt
                wkt = convertGMLShapetoWKT(value)

                # Checking just in case if the wkt is empty
                if wkt != "":
                    Bnode = stringToId(idString+"-geometry2d", "id", className)
                    graph.add((idId, predefinedStringToIRI("geometry:hasGeometry"), Bnode))
                    graph.add((Bnode, predefinedStringToIRI("geometry:asWKT"), wktToLiteral(wkt)))
                    graph.add((Bnode, RDF.type, predefinedStringToIRI("geometry:Geometry")))
            continue

        # Add in nummeraanduidingreeks to the graph
        # There could be a list of nummeraanduidingreeksen so we first check for a list and then run the
        # script for converting it to linked data.
        if key == "imgeo:nummeraanduidingreeks" :
            if type(value) == type([]):
                for element in value:
                    graph = conversionPand(graph, element["imgeo:Nummeraanduidingreeks"], idId)
            if type(value) == type({}):
                graph = conversionPand(graph, value["imgeo:Nummeraanduidingreeks"], idId)
            continue


        # We should have cleared all the necessary dictionaries. All others will be skipped.
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

        # We possibily missed a property. We will print the property and key to the user when the Verbosity is turned on.
        # Which we can then implemented in the script.
        if "imgeo" in key :
            if value:
                try:
                    graph.add((idId, predefinedStringToIRI(key), stringToLiteral(value)))
                except:
                    print("failed to add", type(value))
            if __verbose:
                print(key, value)
            continue

        # Finally if we missed anything we will print it here.
        if __verbose:
            print(key, value)

    # Finally we will return the graph to be serialized.
    return graph



def convertFile(zip, file, sample, output_path):
    """
    Opens the zipfile retrieves the file and streams through the xml line by line.

    :param  zip: Zipfile object
            file: Filename in the zipfile
            Sample -- boolean : Boolean for retrieving a sample vs the complete dataset.
    """
    with zip.open(file) as f:
        # tries to read the first line.
        line = readlineFailure(f, 50)
        SampleFile = True
        part = 1

        #While there is a line to read, e.g. the linelength is larger than 0.
        while len(line) > 0 and SampleFile:
            if sample:
                SampleFile = False

            # Open a new file to write to.
            Outfile = open(os.path.join(output_path, "output_" + str(file[:-4]) + "_"+str(part)) + ".nt", "wb+")

            # Set a few variables.
            part += 1
            i = 0

            # Trying to write a part of the converted lines to a file.
            # Due to the size of the files, this will limit the amount of data in a single file.
            # Saving time restarting when the script fails. And limits the writing time
            while len(line) > 0 and i < 250000:
                # Gets the nested dictionary from the line, with the gml for the geo set back.
                bgt_dict_final = geometrie_terugzetten(xml_naar_dict(line))

                # If the dictionary is not empty we will convert the document and write to file.
                if bgt_dict_final != {}:
                    # We only a part of the nested dictionary.
                    graph = conversion(bgt_dict_final['cityObjectMember'])
                    Outfile.write(graph.serialize(format='nt'))
                i += 1

                # Read the next line.
                line = readlineFailure(f, 500000)

# Function for failure save readlines. Tries to read a line and breaks after a certain amout of tries.
def readlineFailure(f, tries):
    """
    Tries to read a line and if it fails to read a line it will try a number of times.

    :param  f: document
            tries: Number of tries.
    :returns line
    """
    breakLoop = 0
    while True:
        try:
            line = f.readline()
            return line
        except:
            next(f)
            breakLoop += 1
        if breakLoop > tries:
            print("FAILED TO READ XML STOPPING PROCESS")
            return ""


def convertBGT(bgt_zip_path, output_path):
    """
    Reads an zipfile and converts every document in the zipfile.

    :param source: path containing BGT zip
    :return:
    """

    FileRoundTwo = []

    for file_name in os.listdir(bgt_zip_path):
        with ZipFile(os.path.join(bgt_zip_path, file_name), 'r') as zip:
            listOfFileNames = zip.namelist()
            for file in listOfFileNames:
                convertFile(zip, file, False, output_path)

        print("finished conversion")

    shutil.make_archive("outputZipped/zippedBGT.zip", 'zip', "output/")
