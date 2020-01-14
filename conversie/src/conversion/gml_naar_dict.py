
""""

Gebruikt xmldict (https://github.com/martinblech/xmltodict)

Dit script is geschreven voor de omzetting van BGT in GML format naar linked data
"""

import xmltodict

def xml_naar_dict(gmlLine):
    """
    Leest een gml bestand en zet deze om naar een dict.


    Todo: geometrie plat slaan?
    """

    _features = {}
    try:
        _features = xmltodict.parse(gmlLine)

    except Exception as e:
        print(e)

    return _features

def geometrie_terugzetten(bgt_dict):
    """
    Verandert geometrie weer terug in xml

    :param bgt_dict:
    :return bgt_dict_xml_geom:
    """

    _bgt_dict = bgt_dict
    _new_dict = {}
    if _bgt_dict == {}:
        return _bgt_dict

    try:
        # zet om
        _xml_geom = dict_xmliseren(_bgt_dict['cityObjectMember']['PlantCover']['imgeo:geometrie2dBegroeidTerreindeel'] )
        # pas aan in dict

        try:
            _bgt_dict['cityObjectMember']['PlantCover']['imgeo:geometrie2dBegroeidTerreindeel'] = _xml_geom
        except Exception as e:
            print('error while putting xml in dict: {0}'.format(e))
    except Exception as e:
        print(e)

    #
    # # maak dict met alleen maar geometrieën
    # bgt_dict_xml_geom = {}


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
    bgt_gml = r"D:\high3Repo\resources\bgt_begroeidterreindeel.gml"
    with open(bgt_gml) as f:
        data = f.readline()
        bgt_dict_initial = xml_naar_dict(line)

        bgt_dict_final = geometrie_terugzetten(bgt_dict_initial)

        print(bgt_dict_final)


if __name__ == "__main__":
    main()
