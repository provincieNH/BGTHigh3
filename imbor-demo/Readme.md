# BGTHigh3 - imbor-demo

We hebben voor 1 imbor object (Verhardingsobject) een deel van de data uit de provincie noord-holland Areaaldata 
database geconverteerd. Hiervoor is gebruik gemaakt van de 'alpha' versie van de IMBOR Ontologie die gemaakt wordt door CROW.
Een aantal eigenschappen hebben we nog aanvullend zelf gemodelleerd omdat dat voor de demo handig was.

Het FME script areaaldata_naar_imbor.fmw gebruikt een xmlformatter om een filegeodatabase te converteren naar rdf/xml formaat.

De jupyter notebooks maken gebruik van het package 'gastrodon' om sparql queries op lokale of remote endpoints te kunnen uitvoeren.
Ze zijn hier vooral gebruikt als hulpmiddel om de ontologie te bevragen voor de mapping en een snelle check uit te voeren op het
conversie resultaat.

imbor-data.rdf is een voorbeeld datasetje.

