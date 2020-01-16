from osgeo import ogr, osr
import rdflib
from datetime import datetime
from rdflib import Literal, URIRef, RDF
from rdflib.namespace import XSD
import re

## GLOBAL VARIABLES:
##
# Namespaces
nen3610=rdflib.Namespace("http://definities.geostandaarden.nl/def/nen3610#")
nen3610def=rdflib.Namespace("http://definities.geostandaarden.nl/def/nen3610/")
nen3610id=rdflib.Namespace("http://definities.geostandaarden.nl/id/nen3610/")
imgeo=rdflib.Namespace("http://definities.geostandaarden.nl/def/imgeo#")
imgeobegrip=rdflib.Namespace("http://definities.geostandaarden.nl/imgeo/id/begrip/")
bgt=rdflib.Namespace('http://bgt.basisregistraties.overheid.nl/bgt/')
bgtdef=rdflib.Namespace("http://bgt.basisregistraties.overheid.nl/def/bgt#")
bgtBegrip=rdflib.Namespace("http://bgt.basisregistraties.overheid.nl/id/begrip/")
bag=rdflib.Namespace("http://bag.basisregistraties.overheid.nl/bag/id/pand/")
dc=rdflib.Namespace("http://purl.org/dc/terms/")
skos=rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
foaf=rdflib.Namespace("http://xmlns.com/foaf/0.1/")
geometry=rdflib.Namespace("http://www.opengis.net/ont/geosparql#")

# Verbosity of the printStatements
__verbose = False

# Conversion scheme for spatial reference: RD -> WGS84
source = osr.SpatialReference()
source.ImportFromEPSG(28992)

target = osr.SpatialReference()
target.ImportFromEPSG(4258)

transform = osr.CoordinateTransformation(source, target)

# Helper function responsible for the conversion of an GML RD geometry to an WKT WGS84 geometry
def convertGMLShapetoWKT(gml):
    # Export geometry to WKT
    wkt = ogr.CreateGeometryFromGML(gml)

    if wkt:
        # IF we have an valid WKT we first convert the WKT to a linear geometry.
        wktLinear = wkt.GetLinearGeometry()
        wktLinear.Transform(transform)
        return wktLinear.ExportToWkt()
    else:
        return ""

# Checks if the bronhouder exists, and converts it to an IRI. A waardelijst of the bronhouders would add missing bronhouders to the list.
def getBronhouderIri(bronhouder):
    if re.search("^G\\d{4}$",bronhouder):
        return "http://data.labs.pdok.nl/bbi/id/gemeente/" + bronhouder[1:]
    else:
        if __verbose:
            print("Unexpected bronhouder format: {}".format(bronhouder))
        return ""

# Checks if there is an Waarde as string and checks if the waarde can be converted to an class-IRI
def getClassIri(waarde, baseIri, feature):
    if waarde == null or waarde.equals("niet-bgt"):
        return null
    else:
        return baseIri + getClassReference(waarde) + "_" + feature

# Converts a string with dateTime to a date specific object.
def stringToDate(inputString):
    if len(inputString.split("T")) > 1:
        date_object = datetime.strptime(inputString, '%Y-%m-%dT%H:%M:%S.%f').date()
    else:
        date_object = datetime.strptime(inputString, '%Y-%m-%d').date()
    return date_object, XSD.date

# Due to the changes in ID-IRI's we use a specialized function that converts a string to an ID-IRI.
def stringToId(inputString, docOrId, classType):
    """Transforms a input to an IRI for an object.

    Keyword arguments:
    inputString -- String, the string that holds the Id
    docOrId -- String, decides if the IRI defines a document of an object(doc) or the Object (id)
    classType -- String, the specialized classtype.

    Output:
    IRI
    """
    input = docOrId+ "/" + classType+ "/"+inputString
    return bgt[input]


def predefinedStringToIRI(inputString):
    """ Transforms an predefined string to an IRI.
    predefined strings consist out of the prefix and suffix split by an ':'.
    Example:
        imgeo:Pand -> http://definities.geostandaarden.nl/def/imgeo#Pand
        bgtdef:Pand -> http://bgt.basisregistraties.overheid.nl/def/bgt#Pand

    Input
     - predefined string

    Output
     - IRI
    """
    prefix, suffix = inputString.split(":")
    if prefix == "imgeo":
        return imgeo[suffix]
    if prefix == "nen3610":
        return nen3610[suffix]
    if prefix == "nen3610def":
        return nen3610def[suffix]
    if prefix == "bgt":
        return bgt[suffix]
    if prefix == "bgtBegrip":
        return bgtBegrip[suffix]
    if prefix == "imgeobegrip":
        return imgeobegrip[suffix]
    if prefix == "geometry":
        return geometry[suffix]
    if prefix == "bag":
        return bag[suffix]
    if prefix =="nen3610id":
        return nen3610id[suffix]

# Converts string to integer, with correct datatype
def stringToInteger(inputString):
    return int(inputString), XSD.integer

# Converts string to URI, with correct datatype
def stringToURI(inputString):
    return inputString, XSD.anyURI

# Converts string to boolean, with correct datatype
def stringToBoolean(inputString):
    return inputString, XSD.boolean

# Converts string to Float, with correct datatype
def stringToFloat(inputString):
    return float(inputString), XSD.float

# Converts string to languageString, with correct datatype
def stringTolangString(inputString):
    return integer, XSD.language

# Converts an wkt string to an WKTLiteral
def wktToLiteral(wkt):
    return Literal(wkt, datatype=URIRef("http://www.opengis.net/ont/geosparql#wktLiteral"))

# Converts an string to the correct Literal type, using regexes
def stringToLiteral(inputString):
    dateRegex = "([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))"
    integerRegex = "^(-?[1-9]+\d*)$|^0$"
    floatRegex = "^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$"
    anyURIRegex = "@^(https?|ftp)://[^\s/$.?#].[^\s]*$@iS"
    booleanRegex = "true|false"

    # Cases literal
    # Important to NOTE:
    # These searches are set on occurence, with strings being the final type.
    # Everything that can not be classified as a different type will fall into there.
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
    else:
        out = inputString
        datatype = XSD.string

    return Literal(out, datatype=datatype)

# Converts a completeString to an IRI. Different to the predefinedStringToIRI
# That one only converts strings with a prefix. This will convert everything to an IRI.
def stringToIRI(inputString):
    return URIRef(inputString)
