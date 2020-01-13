import rdflib
from .shared import *
from .gml_naar_dict import xml_naar_dict

def conversion(dict):
    graph = rdflib.Graph()
    graph.add((URIRef("http://www.example.org#a"),URIRef("http://www.example.org#a"),URIRef("http://www.example.org#a")) )
    return graph

def convertBGT():
    lines = ["","","",""]
    file = open("output/output.nt", "ab+")
    bgt_gml ="resources/bgt_begroeidterreindeel.gml"

    for dict in xml_naar_dict(bgt_gml):
        graph = conversion(dict)
        file.write(graph.serialize(format='nt'))
