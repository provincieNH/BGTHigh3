# Required:
# $ pip install openpyxl

import glob
import os

import openpyxl
from rdflib import BNode, Graph, Literal, Namespace, URIRef, RDFS, XSD, RDF

ONTO = Namespace("http://ndw.nu/ns/intensiteitsmetingen#")
MEETLOCATIE = Namespace("http://noordholland.nl/ns/ndw/id/meetlocatie/")
METING = Namespace("http://noordholland.nl/ns/ndw/id/meting/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")


def parse(file):
    workbook = openpyxl.open(file, data_only=True, read_only=True)

    overzicht = workbook["Overzicht"]
    intensiteit = workbook["Intensiteit"]
    gemiddelde_snelheid = workbook["Gemiddelde snelheid"]

    meetlocaties = list()

    for volgnummer, id_, naam, lat, long in overzicht["A7:E50"]:
        meetlocaties.append(
            {
                "volgnummer": volgnummer.value,
                "id": id_.value,
                "naam": naam.value,
                "lat": lat.value,
                "long": long.value,
            }
        )

        geometrie = BNode()

        yield MEETLOCATIE[id_.value], RDFS.label, Literal(naam.value)
        yield MEETLOCATIE[id_.value], ONTO.identificatie, Literal(id_.value)
        yield MEETLOCATIE[id_.value], GEO.hasGeometry, geometrie

        long = float(str(long.value).replace(",", "."))
        lat = float(str(lat.value).replace(",", "."))

        yield geometrie, GEO.asWKT, Literal(
            f"POINT ({long} {lat})", datatype=GEO.wktLiteral
        )

    # 27 rijen per meetlocatie, beginnend op 4, met 10 witregels ertussen
    offset = 6
    spacing = 13
    duration = 24  # uren in de dag duh

    for i, locatie in enumerate(meetlocaties, start=0):
        begin = offset + (i * (duration + spacing))
        eind = begin + duration - 1

        bereik = (begin, eind)
        bereik = f"A{bereik[0]}:H{bereik[1]}"

        for (
            uuropdeweg,
            intensiteitswaarde,
            voertuiglengte1,
            voertuiglengte2,
            voertuiglengte3,
            voertuiglengte4,
            voertuiglengte5,
            voertuiglengte_onbekend,
        ) in intensiteit[bereik]:
            meting = BNode()

            v1 = float(str(intensiteitswaarde.value).replace(",", ".")) if intensiteitswaarde is not None else None
            v2 = float(str(voertuiglengte1.value).replace(",", ".")) if voertuiglengte1 is not None else None
            v3 = float(str(voertuiglengte2.value).replace(",", ".")) if voertuiglengte2 is not None else None
            v4 = float(str(voertuiglengte3.value).replace(",", ".")) if voertuiglengte3 is not None else None
            v5 = float(str(voertuiglengte4.value).replace(",", ".")) if voertuiglengte4 is not None else None
            v6 = float(str(voertuiglengte5.value).replace(",", ".")) if voertuiglengte5 is not None else None
            v7 = float(str(voertuiglengte_onbekend.value).replace(",", ".")) if voertuiglengte_onbekend is not None else None

            yield meting, RDF.type, ONTO.Intensiteitsmeting

            yield meting, ONTO.periodeStart, Literal(
                uuropdeweg.value.split(" - ")[0], datatype=XSD.string
            )
            yield meting, ONTO.intensiteitswaarde, Literal(v1, datatype=XSD.decimal)
            yield meting, ONTO.perVoertuiglengte1, Literal(v2, datatype=XSD.decimal)
            yield meting, ONTO.perVoertuiglengte2, Literal(v3, datatype=XSD.decimal)
            yield meting, ONTO.perVoertuiglengte3, Literal(v4, datatype=XSD.decimal)
            yield meting, ONTO.perVoertuiglengte4, Literal(v5, datatype=XSD.decimal)
            yield meting, ONTO.perVoertuiglengte5, Literal(v6, datatype=XSD.decimal)
            yield meting, ONTO.perOnbekendeVoertuiglengte, Literal(v7, datatype=XSD.decimal)

            yield MEETLOCATIE[locatie["id"]], ONTO.heeftMeting, meting

    for i, locatie in enumerate(meetlocaties, start=0):
        begin = offset + (i * (duration + spacing - 1))
        eind = begin + duration - 1

        bereik = (begin, eind)
        bereik = f"A{bereik[0]}:G{bereik[1]}"

        for (
            uuropdeweg,
            gem_snelheid,
            voertuiglengte1,
            voertuiglengte2,
            voertuiglengte3,
            voertuiglengte4,
            voertuiglengte5,
        ) in gemiddelde_snelheid[bereik]:
            meting = BNode()

            v1 = float(str(gem_snelheid.value).replace(",", ".")) if gem_snelheid.value is not None else None
            v2 = float(str(voertuiglengte1.value).replace(",", ".")) if voertuiglengte1.value is not None else None
            v3 = float(str(voertuiglengte2.value).replace(",", ".")) if voertuiglengte2.value is not None else None
            v4 = float(str(voertuiglengte3.value).replace(",", ".")) if voertuiglengte3.value is not None else None
            v5 = float(str(voertuiglengte4.value).replace(",", ".")) if voertuiglengte4.value is not None else None
            v6 = float(str(voertuiglengte5.value).replace(",", ".")) if voertuiglengte5.value is not None else None

            yield meting, RDF.type, ONTO.GemiddeldeSnelheidsmeting
            yield meting, ONTO.periodeStart, Literal(
                uuropdeweg.value.split(" - ")[0], datatype=XSD.string
            )
            yield meting, ONTO.gemiddeldeSnelheid, Literal(v1, datatype=XSD.decimal)
            yield meting, ONTO.perVoertuiglengte1, Literal(v2, datatype=XSD.decimal)
            yield meting, ONTO.perVoertuiglengte2, Literal(v3, datatype=XSD.decimal)
            yield meting, ONTO.perVoertuiglengte3, Literal(v4, datatype=XSD.decimal)
            yield meting, ONTO.perVoertuiglengte4, Literal(v5, datatype=XSD.decimal)
            yield meting, ONTO.perVoertuiglengte5, Literal(v6, datatype=XSD.decimal)

            yield MEETLOCATIE[locatie["id"]], ONTO.heeftMeting, meting


if __name__ == "__main__":
    g = Graph()
    g.bind("geo", GEO)
    g.bind("nh", MEETLOCATIE)
    g.bind("ndw", ONTO)
    # g.bind('metin', ONTO )

    for file in glob.glob("ndw/data/*.xlsx"):
        # file = "ndw/data/N247samen.xlsx"
        print(f"Processing {os.path.basename(file)}")
        for triple in parse(file):
            if triple[-1] is not None:
                g.add(triple)

        g.serialize(f"ndw/data/export-{os.path.basename(file)}.ttl", format="ttl")
