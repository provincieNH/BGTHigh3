
""""

Gebruikt xmldict (https://github.com/martinblech/xmltodict)

Dit script is geschreven voor de omzetting van BGT in GML format naar linked data
"""

import xmltodict

def xml_naar_dict(gml):
    """
    Leest een gml bestand en zet deze om naar een dict.


    Todo: geometrie plat slaan?
    """

    _features = {}
    try:
        with open(gml) as f:
            data = f.read()
            _features = xmltodict.parse(data)

    except Exception as e:
        print(e)

    return _features

def main():

    bgt_gml = r"D:\high3Repo\resources\bgt_begroeidterreindeel.gml"
    bgt_dict = xml_naar_dict(bgt_gml)

    print(bgt_dict)


if __name__ == "__main__":
    main()