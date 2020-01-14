from osgeo import ogr
import rdflib
from datetime import datetime
from rdflib import Literal, URIRef, RDF
from rdflib.namespace import XSD
import re

## GLOBAL VARIABLES:
bgt=rdflib.Namespace('http://bgt.basisregistraties.overheid.nl/bgt/')
bgtdef=rdflib.Namespace("http://bgt.basisregistraties.overheid.nl/def/bgt#")
dc=rdflib.Namespace("http://purl.org/dc/terms/")
skos=rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
imgeo=rdflib.Namespace("http://definities.geostandaarden.nl/def/imgeo#")
imgeobegrip=rdflib.Namespace("http://definities.geostandaarden.nl/imgeo/id/begrip/")
foaf=rdflib.Namespace("http://xmlns.com/foaf/0.1/")
nen3610=rdflib.Namespace("http://definities.geostandaarden.nl/def/nen3610#")
bgtBegrip=rdflib.Namespace("http://bgt.basisregistraties.overheid.nl/id/begrip/")
geometry=rdflib.Namespace("http://www.opengis.net/ont/geosparql#")

def getBronhouderIri(bronhouder):
    if re.search("^G\\d{4}$",bronhouder):
        return "http://data.labs.pdok.nl/bbi/id/gemeente/" + bronhouder[1:]
    else:
        print("Unexpected bronhouder format: {}".format(bronhouder))
        return ""

def getClassIri(waarde, baseIri, feature):
    if waarde == null or waarde.equals("niet-bgt"):
        return null
    else:
        return baseIri + getClassReference(waarde) + "_" + feature


def convertGMLShapetoWKT(gml):
    # Export geometry to WKT
    wkt = ogr.CreateGeometryFromGML(gml)
    if wkt:
        return wkt.ExportToWkt()
    else:
        return ""

def stringToDate(inputString):
    if len(inputString.split("T")) > 1:
        date_object = datetime.strptime(inputString, '%Y-%m-%dT%H:%M:%S.%f').date()
    else:
        date_object = datetime.strptime(inputString, '%Y-%m-%d').date()
    return inputString, XSD.date

def stringToClass(inputString):
    return bgtdef[inputString]

def stringToId(inputString, docOrId, classType):
    input = docOrId+ "/" + classType+ "/"+inputString
    return bgt[input]

def predefinedStringToIRI(inputString):
    prefix, suffix = inputString.split(":")
    if prefix == "imgeo":
        return imgeo[suffix]
    if prefix == "nen3610":
        return nen3610[suffix]
    if prefix == "bgt":
        return bgt[suffix]
    if prefix == "bgtBegrip":
        return bgtBegrip[suffix]
    if prefix == "imgeobegrip":
        return imgeobegrip[suffix]
    if prefix == "geometry":
        return geometry[suffix]

def stringToInteger(inputString):
    return int(inputString), XSD.integer

def stringToURI(inputString):
    return inputString, XSD.anyURI

def stringToBoolean(inputString):
    return inputString, XSD.boolean

def stringToFloat(inputString):
    return float(inputString), XSD.float

def stringTolangString(inputString):
    return integer, XSD.language

def wktToLiteral(wkt):
    return Literal(wkt, datatype=URIRef("http://www.opengis.net/ont/geosparql#"))

def stringToLiteral(inputString):
    dateRegex = "([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))"
    integerRegex = "^(-?[1-9]+\d*)$|^0$"
    floatRegex = "^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$"
    anyURIRegex = "@^(https?|ftp)://[^\s/$.?#].[^\s]*$@iS"
    booleanRegex = "true|false"
    langRegex = ""
    # Cases literal

    if re.search(dateRegex, inputString):
        out, datatype = stringToDate(inputString)
    elif re.search(booleanRegex, inputString):
        out, datatype = stringToBoolean(inputString)
    elif re.search(integerRegex, inputString):
        out, datatype = stringToInteger(inputString)
    elif re.search(floatRegex, inputString):
        out, datatype = stringToFloat(inputString)
    elif re.search(anyURIRegex, inputString):
        out, datatype = stringToURI(inputString)
    elif re.search(langRegex, inputString):
        out = inputString
        datatype = XSD.string
        # out, datatype = StringTolangString(inputString)
    else:
        out = inputString
        datatype = XSD.string

    return Literal(out, datatype=datatype)

def stringToIRI(inputString):
    return URIRef(inputString)


# def getBegripIri(waarde, eigenschap, plusWaarde, feature):
#     if waarde == null:
#         return null
#     searchWaarde = waarde
#     if featureBegripMapping.contains(feature):
#         featurePart = featureBegripMapping.get(feature)
#     else:
#         feature
#     if plusWaarde != null:
#         featurePart += "Plus"
#         searchWaarde = plusWaarde
#
#     searchString = (eigenschap + featurePart).toLowerCase();
#
#     subjects = imgeoConcepts.filter(null, SKOS.PREF_LABEL, VF.createLiteral(searchWaarde)).subjects();
#     if subjects.size() == 0:
#         LOG.warn("Could not find value {} for attribute {} in Geonovum concepts.", searchWaarde, eigenschap)
#         return null
#
#     if subjects.size() > 1:
#         try:
#             # filtered = subjects.stream().filter(s -> s.stringValue().toLowerCase().contains(searchString))
#             if filtered.size() == 2:
#                 if plusWaarde != null:
#                     filteredResult = filtered.stream()
#                             .filter(s -> s.stringValue().contains("Plus"))
#                             .collect(Collectors.toList())
#                             .get(0)
#                             .stringValue();
#                 else:
#                     filteredResult = filtered.stream()
#                             .filter(s -> !(s.stringValue().contains("Plus")))
#                             .collect(Collectors.toList())
#                             .get(0)
#                             .stringValue();
#
#                 return filteredResult
#
#             return Iterables.getOnlyElement(filtered).stringValue();
#         except:
#             raise Exception("Expecting one element but found multiple in: ".format(subjects));
#
#     else:
#         return Iterables.getOnlyElement(subjects).stringValue();
