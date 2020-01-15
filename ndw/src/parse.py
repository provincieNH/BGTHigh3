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
QB = Namespace('http://purl.org/linked-data/cube#')

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

        yield MEETLOCATIE[id_.value], RDF.type, ONTO.Meetlocatie
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

    yield ONTO.Meetlocatie, RDF.type, RDFS.Class
    yield ONTO.Meetlocatie, RDFS.subClassOf, GEO.Feature
    yield ONTO.Meetlocatie, RDFS.label, Literal("Meetlocatie", lang='nl')

    yield ONTO.identificatie, RDF.type, RDF.Property
    yield ONTO.identificatie, RDFS.label, Literal("identificatie", lang='nl')

    yield ONTO.voertuig, RDF.type, RDF.Property
    yield ONTO.voertuig, RDF.type, QB.DimensionProperty
    yield ONTO.voertuig, RDFS.label, Literal("voertuig", lang='nl')

    yield ONTO.intensiteit, RDF.type, RDF.Property
    yield ONTO.intensiteit, RDF.type, QB.MeasureProperty
    yield ONTO.intensiteit, RDFS.label, Literal("intensiteit", lang='nl')

    yield ONTO.snelheid, RDF.type, RDF.Property
    yield ONTO.snelheid, RDF.type, QB.MeasureProperty
    yield ONTO.snelheid, RDFS.label, Literal("snelheid", lang='nl')

    yield ONTO.Voertuig, RDF.type, RDFS.Class
    yield ONTO.Voertuig, RDFS.label, Literal("Voertuigklasse", lang='nl')

    yield ONTO.AlleVoertuigen, RDF.type, ONTO.Voertuig
    yield ONTO.AlleVoertuigen, RDFS.label, Literal("Alle voertuigen", lang='nl')

    yield ONTO.Voertuiglengte1, RDF.type, ONTO.Voertuig
    yield ONTO.Voertuiglengte1, RDFS.label, Literal("Voertuig tussen 1,85 m en 2,40 m", lang='nl')

    yield ONTO.Voertuiglengte2, RDF.type, ONTO.Voertuig
    yield ONTO.Voertuiglengte2, RDFS.label, Literal("Voertuig tussen 2,40 m en 5,60 m", lang='nl')

    yield ONTO.Voertuiglengte3, RDF.type, ONTO.Voertuig
    yield ONTO.Voertuiglengte3, RDFS.label, Literal("Voertuig tussen 5,60 m en 11,50 m", lang='nl')

    yield ONTO.Voertuiglengte4, RDF.type, ONTO.Voertuig
    yield ONTO.Voertuiglengte4, RDFS.label, Literal("Voertuig tussen 11,50 m en 12,20 m", lang='nl')

    yield ONTO.Voertuiglengte5, RDF.type, ONTO.Voertuig
    yield ONTO.Voertuiglengte5, RDFS.label, Literal("Voertuig groter dan 12,20 m", lang='nl')

    yield ONTO.VoertuiglengteOnbekend, RDF.type, ONTO.Voertuig
    yield ONTO.VoertuiglengteOnbekend, RDFS.label, Literal("Voertuig met onbepaalde lengte", lang='nl')

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
            # meting = BNode()

            v0 = str(intensiteitswaarde.value).replace(",", ".") if intensiteitswaarde is not None else None
            v1 = str(voertuiglengte1.value).replace(",", ".") if voertuiglengte1 is not None else None
            v2 = str(voertuiglengte2.value).replace(",", ".") if voertuiglengte2 is not None else None
            v3 = str(voertuiglengte3.value).replace(",", ".") if voertuiglengte3 is not None else None
            v4 = str(voertuiglengte4.value).replace(",", ".") if voertuiglengte4 is not None else None
            v5 = str(voertuiglengte5.value).replace(",", ".") if voertuiglengte5 is not None else None
            v6 = str(voertuiglengte_onbekend.value).replace(",", ".") if voertuiglengte_onbekend is not None else None

            # yield meting, RDF.type, ONTO.Intensiteitsanalyse

            # yield meting, ONTO.periodeStart, Literal(
            #     uuropdeweg.value.split(" - ")[0], datatype=XSD.string
            # )
            # yield meting, ONTO.intensiteitswaarde, Literal(v1, datatype=XSD.decimal)
            # yield meting, ONTO.perVoertuiglengte1, Literal(v2, datatype=XSD.decimal)
            # yield meting, ONTO.perVoertuiglengte2, Literal(v3, datatype=XSD.decimal)
            # yield meting, ONTO.perVoertuiglengte3, Literal(v4, datatype=XSD.decimal)
            # yield meting, ONTO.perVoertuiglengte4, Literal(v5, datatype=XSD.decimal)
            # yield meting, ONTO.perVoertuiglengte5, Literal(v6, datatype=XSD.decimal)
            # yield meting, ONTO.perOnbekendeVoertuiglengte, Literal(v7, datatype=XSD.decimal)

            # yield MEETLOCATIE[locatie["id"]], ONTO.heeftMeting, meting

            slice_ = BNode()
            yield slice_, RDF.type, QB.Slice
            yield slice_, QB.sliceStructure, ONTO.slicePerVoertuig
            yield slice_, ONTO.periode, Literal(uuropdeweg.value.split(" - ")[0], datatype=XSD.string)
            yield slice_, ONTO.meetlocatie, MEETLOCATIE[locatie['id']]

            v0_node = BNode()
            yield v0_node, RDF.type, QB.Observation
            yield v0_node, ONTO.intensiteit, Literal(v0, datatype=XSD.decimal)
            yield v0_node, ONTO.voertuig, ONTO.AlleVoertuigen

            v1_node = BNode()
            yield v1_node, RDF.type, QB.Observation
            yield v1_node, ONTO.intensiteit, Literal(v1, datatype=XSD.decimal)
            yield v1_node, ONTO.voertuig, ONTO.Voertuiglengte1

            v2_node = BNode()
            yield v2_node, RDF.type, QB.Observation
            yield v2_node, ONTO.intensiteit, Literal(v2, datatype=XSD.decimal)
            yield v2_node, ONTO.voertuig, ONTO.Voertuiglengte2

            v3_node = BNode()
            yield v3_node, RDF.type, QB.Observation
            yield v3_node, ONTO.intensiteit, Literal(v3, datatype=XSD.decimal)
            yield v3_node, ONTO.voertuig, ONTO.Voertuiglengte3

            v4_node = BNode()
            yield v4_node, RDF.type, QB.Observation
            yield v4_node, ONTO.intensiteit, Literal(v4, datatype=XSD.decimal)
            yield v4_node, ONTO.voertuig, ONTO.Voertuiglengte4

            v5_node = BNode()
            yield v5_node, RDF.type, QB.Observation
            yield v5_node, ONTO.intensiteit, Literal(v5, datatype=XSD.decimal)
            yield v5_node, ONTO.voertuig, ONTO.Voertuiglengte5

            v6_node = BNode()
            yield v6_node, RDF.type, QB.Observation
            yield v6_node, ONTO.intensiteit, Literal(v6, datatype=XSD.decimal)
            yield v6_node, ONTO.voertuig, ONTO.VoertuiglengteOnbekend

            yield slice_, QB.observation, v0_node
            yield slice_, QB.observation, v1_node
            yield slice_, QB.observation, v2_node
            yield slice_, QB.observation, v3_node
            yield slice_, QB.observation, v4_node
            yield slice_, QB.observation, v5_node
            yield slice_, QB.observation, v6_node

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
            # meting = BNode()

            v0 = str(gem_snelheid.value).replace(",", ".") if gem_snelheid.value is not None else None
            v1 = str(voertuiglengte1.value).replace(",", ".") if voertuiglengte1.value is not None else None
            v2 = str(voertuiglengte2.value).replace(",", ".") if voertuiglengte2.value is not None else None
            v3 = str(voertuiglengte3.value).replace(",", ".") if voertuiglengte3.value is not None else None
            v4 = str(voertuiglengte4.value).replace(",", ".") if voertuiglengte4.value is not None else None
            v5 = str(voertuiglengte5.value).replace(",", ".") if voertuiglengte5.value is not None else None

            # yield meting, RDF.type, ONTO.GemiddeldeSnelheidsanalyse
            # yield meting, ONTO.periodeStart, Literal(
            #     uuropdeweg.value.split(" - ")[0], datatype=XSD.string
            # )
            # yield meting, ONTO.gemiddeldeSnelheid, Literal(v0, datatype=XSD.decimal)
            # yield meting, ONTO.perVoertuiglengte1, Literal(v1, datatype=XSD.decimal)
            # yield meting, ONTO.perVoertuiglengte2, Literal(v2, datatype=XSD.decimal)
            # yield meting, ONTO.perVoertuiglengte3, Literal(v3, datatype=XSD.decimal)
            # yield meting, ONTO.perVoertuiglengte4, Literal(v4, datatype=XSD.decimal)
            # yield meting, ONTO.perVoertuiglengte5, Literal(v5, datatype=XSD.decimal)

            # yield MEETLOCATIE[locatie["id"]], ONTO.heeftMeting, meting

            slice_ = BNode()
            yield slice_, RDF.type, QB.Slice
            yield slice_, QB.sliceStructure, ONTO.slicePerVoertuig
            yield slice_, ONTO.periode, Literal(uuropdeweg.value.split(" - ")[0], datatype=XSD.string)
            yield slice_, ONTO.meetlocatie, MEETLOCATIE[locatie['id']]

            v0_node = BNode()
            yield v0_node, RDF.type, QB.Observation
            yield v0_node, ONTO.snelheid, Literal(v0, datatype=XSD.decimal)
            yield v0_node, ONTO.voertuig, ONTO.AlleVoertuigen

            v1_node = BNode()
            yield v1_node, RDF.type, QB.Observation
            yield v1_node, ONTO.snelheid, Literal(v1, datatype=XSD.decimal)
            yield v1_node, ONTO.voertuig, ONTO.Voertuiglengte1

            v2_node = BNode()
            yield v2_node, RDF.type, QB.Observation
            yield v2_node, ONTO.snelheid, Literal(v2, datatype=XSD.decimal)
            yield v2_node, ONTO.voertuig, ONTO.Voertuiglengte2

            v3_node = BNode()
            yield v3_node, RDF.type, QB.Observation
            yield v3_node, ONTO.snelheid, Literal(v3, datatype=XSD.decimal)
            yield v3_node, ONTO.voertuig, ONTO.Voertuiglengte3

            v4_node = BNode()
            yield v4_node, RDF.type, QB.Observation
            yield v4_node, ONTO.snelheid, Literal(v4, datatype=XSD.decimal)
            yield v4_node, ONTO.voertuig, ONTO.Voertuiglengte4

            v5_node = BNode()
            yield v5_node, RDF.type, QB.Observation
            yield v5_node, ONTO.snelheid, Literal(v5, datatype=XSD.decimal)
            yield v5_node, ONTO.voertuig, ONTO.Voertuiglengte5

            yield slice_, QB.observation, v0_node
            yield slice_, QB.observation, v1_node
            yield slice_, QB.observation, v2_node
            yield slice_, QB.observation, v3_node
            yield slice_, QB.observation, v4_node
            yield slice_, QB.observation, v5_node


if __name__ == "__main__":
    g = Graph()
    g.bind("geo", GEO)
    g.bind("nh", MEETLOCATIE)
    g.bind("ndw", ONTO)
    g.bind('qb', QB )

    for file in glob.glob("ndw/data/*.xlsx"):
        # file = "ndw/data/N247samen.xlsx"
        print(f"Processing {os.path.basename(file)}")
        for triple in parse(file):
            if triple[-1] is not None:
                g.add(triple)

    g.serialize(f"ndw/data/ndw-data-handpicked.ttl", format="ttl")
