# BGTHigh3

Centrale repository voor de High 3 week georganiseerd door Provincie Noord-Holland en Kadaster.

In deze centrale repo zitten de volgende onderdelen:
 - Het model, [Readme](model/README.md)
 - Het Extract Transform Load (ETL)script, [Readme](conversie/README.md)
 - imbor-demo, [Readme](imbor-demo/Readme.md)
 - NDW data
 - presentaties, de presentaties die tijdens de afsluitende bijeenkomst zijn gepresenteerd.
 
 ### Resultaten
 De Data story is te vinden op de [labs ogeving van het kadaster](https://labs.kadaster.nl/stories/bgt-high3/index.html)
 De databrowser is [hier](https://labs.kadaster.nl/browsers/areaal/) te vinden
 
### Wat hebben we geleerd
De belangrijkste zaken zijn:
- In vergelijking met een paar jaar geleden is het omzetten een stuk makkelijker geworden
- Het linken van datasets gaat eigenlijk heel makkelijk (als je het eenmaal onder de knie hebt)
- Het combineren van data op basis van zowel ligging als attributen is heel flexibel en krachtig
       bijvoorbeeld de vraag ‘geef me alle objecten die gerelateerd zijn aan de N247’
- Deze werkvorm met een multidisciplinair team was leuk, leerzaam en productief

### Redenen om door te gaan met BGT als Linked data
- Harmonisatie van informatiemodellen zodat we de hele keten integraal kunnen bevragen: NEN3610 - BGT - IMGeo - IMBor - Contracteisen

- BGT beschikbaar als linked data betekent dat we minder dubbel hoeven bij te houden. We kunnen het BGT object eenvoudiger ‘uitbreiden’ met imbor/provinciale informatie.

- elimineren van ‘horizontaal berichtenverkeer’ (als we mutatieverzoeken via bv. ogc api kunnen implementeren)

- Het opent de weg naar __slimme toepassingen__ omdat de data integraal bevraagbaar is.
