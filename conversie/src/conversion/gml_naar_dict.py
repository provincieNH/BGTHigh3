
"""

Gebruikt xmldict (https://github.com/martinblech/xmltodict)

Dit script is geschreven voor de omzetting van BGT in GML format naar linked data
"""

import xmltodict
from .shared import *

def first(ordered_dict):
    """
    Retrieves the first key from an dictionary.
    """
    for key, item in ordered_dict.items():
        return key

def xml_naar_dict(gmlLine):
    """
    Leest een gml bestand en zet deze om naar een dict.
    """

    _features = {}
    try:
        _features = xmltodict.parse(gmlLine)
    except Exception as e:
        if e.args[0] != 'no element found: line 2, column 0':
            print(e.args[0])

    return _features

def geometrie_terugzetten(bgt_dict):
    """
    Verandert geometrie weer terug in xml

    :param bgt_dict:
    :return bgt_dict_xml_geom:
    """

    _bgt_dict = bgt_dict
    _new_dict = {}
    # Check for empty dictionary. IF empty or incorrect information skip dict.
    if _bgt_dict == {} or 'cityObjectMember' not in bgt_dict:
        return {}

    # We retrieve the first and only element from the dictionary.
    # The typeElement is needed for the nested dictionary
    typeElement = first(_bgt_dict['cityObjectMember'])
    for key, value in _bgt_dict['cityObjectMember'][typeElement].items():
        # Converting the two geometries(kruinlijn and geometrie2d) back from the nested dictionary
        # to an gml, needed for later conversion to WKT.
        if "imgeo:kruinlijn" in key:
            # Skipping if no geometry present.
            if "@nilReason" in value:
                continue
            _xml_geom = dict_xmliseren(value )
            _bgt_dict['cityObjectMember'][typeElement][key] = _xml_geom
        if "imgeo:geometrie2d" in key:
            # Skipping if no geometry present.
            if "@nilReason" in value:
                continue
            type = key.replace("imgeo:geometrie2d","")
            _xml_geom = dict_xmliseren(value )
            _bgt_dict['cityObjectMember'][typeElement][key] = _xml_geom

    _bgt_dict['cityObjectMember'][typeElement]["type"] = type

    return _bgt_dict

def dict_xmliseren(geom_dict):
    """
    Unparsed dict met geometrie naar xml

    :param geom_dict:
    :return geom_dict_xmliseerd:
    """
    _geom_dict = geom_dict

    geom_dict_xmliseerd = {}

    try:
        geom_dict_xmliseerd = xmltodict.unparse(_geom_dict)
    except Exception as e:
        print(e)

    return geom_dict_xmliseerd



def main():
    """
    Runs the above script and converts a single line of the gml to an dict.
    With returned geometry.
    """
    bgt_gml = r"D:\high3Repo\resources\bgt_begroeidterreindeel.gml"
    with open(bgt_gml) as f:
        data = f.readline()
        bgt_dict_initial = xml_naar_dict(data)

        bgt_dict_final = geometrie_terugzetten(bgt_dict_initial)

        print(bgt_dict_final)


if __name__ == "__main__":
    main()
