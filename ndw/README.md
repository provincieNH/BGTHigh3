# NDW
Deze map bevat [opendatadownloads van NDW](https://dexter.ndwcloud.nu/opendata) over wegintensiteiten en gemiddelde snelheden per meetpunt. 
De `.xlsx` bestanden staan opgeslagen in `/data`. 

In `/src/parse.py` staat een Python-parseerscript dat bovengenoemde bestanden inlaadt (met het Pythonpakket `openpyxl`) en verwerkt naar een RDF-graaf (met het pakket `rdflib`). 
Dit wordt opgeslagen als een turtle-bestand in `/data/ndw-data-handpicked.ttl`. 
Vanwege de demonstratie, is ervoor gekozen voor enkele provinciale wegen meetpunten te nemen. 

De gebruikte ontologie maakt gebruik van [GeoSparql](http://www.opengis.net/ont/geosparql#) en [Datacube](http://purl.org/linked-data/cube#) voor de interoperabiliteit van de export. 