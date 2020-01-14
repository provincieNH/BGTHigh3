
""""

Gebruikt xmldict (https://github.com/martinblech/xmltodict)

Dit script is geschreven voor de omzetting van BGT in GML format naar linked data
"""

import xmltodict
from .shared import *
import datetime

dateTimeNOW = datetime.date(2020, 1, 14)

def first(ordered_dict):
    for key, item in ordered_dict.items():
        return key

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
        typeElement = first(_bgt_dict['cityObjectMember'])
        for key, value in _bgt_dict['cityObjectMember'][typeElement].items():
            if "imgeo:eindRegistratie" in key:
                date, _dType = stringToDate(_bgt_dict['cityObjectMember'][typeElement][key])
                if date < dateTimeNOW :
                    return {}
            if "imgeo:kruinlijn" in key:
                if "@nilReason"in value:
                    continue
                else:
                    _xml_geom = dict_xmliseren(value )
                    # pas aan in dict
                    try:
                        _bgt_dict['cityObjectMember'][typeElement][key] = _xml_geom

                    except Exception as e:
                        print('error while putting xml in dict: {0}'.format(e))
            if "imgeo:geometrie2d" in key:
                type = key.replace("imgeo:geometrie2d","")

                _xml_geom = dict_xmliseren(value )
                # pas aan in dict
                try:
                    _bgt_dict['cityObjectMember'][typeElement][key] = _xml_geom

                except Exception as e:
                    print('error while putting xml in dict: {0}'.format(e))

    except Exception as e:
        pass

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
    bgt_gml = r"D:\high3Repo\resources\bgt_begroeidterreindeel.gml"
    with open(bgt_gml) as f:
        data = f.readline()
        bgt_dict_initial = xml_naar_dict(data)

        bgt_dict_final = geometrie_terugzetten(bgt_dict_initial)

        print(bgt_dict_final)


if __name__ == "__main__":
    main()
