from osgeo import ogr
from rdflib import Literal, URIRef
from rdflib.namespace import XSD
import re

def getBronhouderIri(bronhouder):
    if bronhouder.matches("^G\\d{4}$"):
        return "http://data.labs.pdok.nl/bbi/id/gemeente/" + bronhouder.substring(1)
    elif Bronhouder.MAPPING.containsKey(bronhouder):
        return Bronhouder.MAPPING.get(bronhouder)
    else:
        print("Unexpected bronhouder format: {}".format(bronhouder))
        return null

def getClassIri(waarde, baseIri, feature):
    if waarde == null or waarde.equals("niet-bgt"):
        return null
    else:
        return baseIri + getClassReference(waarde) + "_" + feature


def convertGMLShapetoWKT(gml):
    # Export geometry to WKT
    wkt = ogr.CreateGeometryFromGML(gml).ExportToWkt()
    return wkt

def StringToDate(inputString):
    date_object = datetime.strptime(inputString, '%d-%m-%Y').date()
    return inputString, XSD.date

def StringToInteger(inputString):
    return int(inputString), XSD.integer

def StringToURI(inputString):
    return inputString, XSD.anyURI

def StringToFloat(inputString):
    return float(inputString), XSD.float

def StringTolangString(inputString):
    return integer, XSD.language

def wktToLiteral(wkt):
    return wkt, URIRef("http://www.opengis.net/ont/geosparql#")

def StringToLiteral(inputString):
    dateRegex = "^\d{1,2}\/\d{1,2}\/\d{4}$"
    integerRegex = "^(-?[1-9]+\d*)$|^0$"
    floatRegex = "^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$"
    anyURIRegex = "@^(https?|ftp)://[^\s/$.?#].[^\s]*$@iS"
    langRegex = ""
    # Cases literal
    if re.search(dateRegex, inputString):
        out, datatype = StringToDate(inputString)
    elif re.search(integerRegex, inputString):
        out, datatype = StringToInteger(inputString)
    elif re.search(floatRegex, inputString):
        out, datatype = StringToFloat(inputString)
    elif re.search(anyURIRegex, inputString):
        out, datatype = StringToURI(inputString)
    elif re.search(langRegex, inputString):
        out = inputString
        datatype = XSD.string
        # out, datatype = StringTolangString(inputString)
    else:
        out = inputString
        datatype = XSD.string

    return Literal(out, datatype=datatype)

def StringToIRI(inputString):
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
