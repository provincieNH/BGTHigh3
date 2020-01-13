import rdflib
from .shared import *

def lineToDict(line):
    # TODO
    return line

def conversion(dict):
    graph = rdflib.Graph()
    graph.add((URIRef("http://www.example.org#a"),URIRef("http://www.example.org#a"),URIRef("http://www.example.org#a")) )
    return graph


def convertBGT():
    lines = ["","","",""]
    file = open("output/output.nt", "ab+")
    for line in lines:
        dict = lineToDict(line)
        graph = conversion(dict)
        file.write(graph.serialize(format='nt'))
