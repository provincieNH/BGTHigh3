# BGTHigh3 - imbor-demo

### scope
We hebben voor 1 imbor object (Verhardingsobject) een deel van de data uit de provincie noord-holland Areaaldata 
database geconverteerd. Hiervoor is gebruik gemaakt van de 'alpha' versie van de IMBOR Ontologie die gemaakt wordt door CROW.
Een aantal eigenschappen hebben we nog aanvullend zelf gemodelleerd omdat dat voor de demo handig was.

### aanpak
We hebben er in de demo ook voor gekozen om de imbor objecten als 'extensie' van BGT objecten aan te maken. Dus het imbor
object bevat alleen de imbor eigenschappen en verwijst via geo:sfEquals naar het BGT object waar de geometrie en andere BGT eigenschappen zijn vastgelegd.

### files
Het FME script areaaldata_naar_imbor.fmw gebruikt een xmlformatter om een filegeodatabase te converteren naar rdf/xml formaat.

De jupyter notebooks maken gebruik van het package 'gastrodon' om sparql queries op lokale of remote endpoints te kunnen uitvoeren.
Ze zijn hier vooral gebruikt als hulpmiddel om de ontologie te bevragen voor de mapping en een snelle check uit te voeren op het
conversie resultaat.

imbor-data.rdf is een voorbeeld datasetje.

