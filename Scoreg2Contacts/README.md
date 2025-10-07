# Scoreg2Kontaktdatenabfrage
## Kurzbeschreibung
Dieses Tool kann verwendet werden, um sämtliche Mitglieder oder deren Eltern als VCard Kontakte abzuspeichern, um so schnell alle Telefonnummern und Email-Adressen auf dem Handy zu haben.

## Installation
Man muss python3.12 installiert haben.
Nun kann man die benötigten Dependencies installieren: `pip install -r requirements.txt`

## Verwendung
Als Basis für dieses Programm benötigt man einen kompletten Scoreg-Auszug. Diesen kann man sich direkt im Scoreg unter dem "Excel-Symbol"->"Vollständige Ansicht" herunterladen (siehe unten).
<img width="210" height="111" alt="image" src="https://github.com/user-attachments/assets/6400be6f-2161-4b35-8e29-893bc3f80ddb" />

Dann kann man mithilfe des folgenden Befehls das Programm starten:
```
python3 main.py --output-file out.pdf --input-file <path_to_scoreg_table> --stufen <comma_seperated_list_of_stufen> --parents
```

Die Parents-Flag gibt an, ob man die Eltern der TeilnehmerInnen als Kontakte erzeugen will ODER die TeilnehmerInnen selbst.

Für den Parameter `stufen` können folgende Stufenausdrücke beliebig kombiniert werden:
- BIEBER
- WICHTEL
- WOELFLINGE
- GUIDES
- SPAEHER
- CAVELIERS
- EXPLORERS
- RANGER
- ROVER
