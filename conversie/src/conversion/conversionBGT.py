import rdflib
from .shared import *
from .gml_naar_dict import xml_naar_dict
import collections



## DictionaryKeys
# class
# imgeo:geometrie2dBegroeidTerreindeel
# imgeo:begroeidTerreindeelOpTalud
# imgeo:kruinlijnBegroeidTerreindeel
# imgeo:plus-fysiekVoorkomen
# @xmlns
# @gml:id
# creationDate
# imgeo:LV-publicatiedatum
# imgeo:relatieveHoogteligging
# imgeo:inOnderzoek
# imgeo:tijdstipRegistratie
# imgeo:identificatie
# imgeo:bronhouder
# imgeo:bgt-status
# imgeo:plus-status
# <class 'str'> @xmlns http://www.opengis.net/citygml/vegetation/2.0
# <class 'str'> @gml:id b714098fc-4c7a-11e8-951f-610a7ca84980
# <class 'str'> imgeo:LV-publicatiedatum 2018-04-27T14:26:17.000
# <class 'str'> imgeo:relatieveHoogteligging 0
# <class 'str'> imgeo:inOnderzoek false
# <class 'str'> imgeo:tijdstipRegistratie 2018-04-27T13:58:35.000
# <class 'str'> imgeo:bronhouder G0307
# <class 'str'> imgeo:begroeidTerreindeelOpTalud false




def conversion(dict: collections.OrderedDict) -> rdflib.Graph:
    graph = rdflib.Graph()
    for Class, _value in dict.items():
        print(Class)

        id = stringToId(dict[Class]["@gml:id"])
        graph.add((id, RDF.type, stringToClass(Class)))
    for key, value in dict[Class].items():
        if type(value) == collections.OrderedDict:
            for keyLayer2, valueLayer2 in value.items():
                print("KEY: ", key, "Key: ", keyLayer2, "Value: ",valueLayer2)



            continue
        if key == "imgeo:bronhouder" :
            IRI = getBronhouderIri(value)
            if IRI != "":
                graph.add((id, predefinedStringToIRI(key), stringToIRI(IRI)))
            continue
        if key.split(":")[0] == "imgeo" :
            graph.add((id, predefinedStringToIRI(key), stringToLiteral(value)))
            continue

    return graph

def convertBGT():
    file = open("output/output.nt", "wb+")
    bgt_gml ="resources/bgt_begroeidterreindeel.gml"

    for index, dict in enumerate(xml_naar_dict(bgt_gml)['CityModel']['cityObjectMember']):

        graph = conversion(dict)
        file.write(graph.serialize(format='nt'))
