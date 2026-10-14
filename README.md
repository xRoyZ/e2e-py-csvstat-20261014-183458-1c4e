# csvstat

`csvstat` ist ein schlankes Kommandozeilenwerkzeug, das eine CSV-Datei einliest
und pro Spalte Statistiken ausgibt: numerische Spalten erhalten Anzahl der Werte,
Minimum, Maximum, Mittelwert und die Zahl der fehlenden Werte, Textspalten die
Anzahl der eindeutigen Werte. Spaltentrenner, Spaltenauswahl und JSON-Ausgabe
lassen sich über Optionen steuern; fehlende, leere oder nur eine Kopfzeile
enthaltende Dateien werden mit einer verständlichen Meldung auf stderr und dem
Exit-Code 1 beantwortet. Das Werkzeug hat keine Laufzeit-Abhängigkeiten, schreibt
keine Kopien der Eingabedaten auf die Festplatte und stellt keine
Netzwerkverbindungen her.

## Tech-Stack

- Python 3.11+ (getestet mit Python 3.13)
- `argparse` aus der Standardbibliothek für die Kommandozeilenschnittstelle
- `csv` inklusive `csv.Sniffer` aus der Standardbibliothek zum Einlesen und zur
  Trennzeichenerkennung
- `pytest` und `ruff` als Entwicklungs-Abhängigkeiten
- Keine Laufzeit-Abhängigkeiten

## Installation

```bash
python -m pip install -e ".[dev]"
```

## Ausführen

Werkzeug als Modul starten:

```bash
python -m csvstat --help
```

Nach der Installation steht zusätzlich das Konsolen-Skript `csvstat` zur
Verfügung:

```bash
csvstat --help
```

## Testen

```bash
python -m pytest
```

## Lint

```bash
python -m ruff check .
python -m ruff format --check .
```

## Verwendung der CLI

```
csvstat <datei> [--delimiter <zeichen>] [--columns <a,b>] [--json]
```

| Option                 | Bedeutung                                                                 |
| ---------------------- | ------------------------------------------------------------------------- |
| `<datei>`              | Pfad zur CSV-Datei (erforderlich).                                        |
| `--delimiter <zeichen>` | Feldtrenner, z. B. `;`. Ohne Angabe wird er automatisch erkannt (Komma als Rückfall). |
| `--columns <a,b>`      | Nur diese Spalten ausgeben, in der Reihenfolge der Kopfzeile.             |
| `--json`               | Ausgabe als JSON statt als Texttabelle.                                   |

Exit-Codes: `0` bei Erfolg; `1` bei einem `CsvstatError` (Meldung auf stderr,
ohne Traceback); `2` bei einem Syntaxfehler der Kommandozeile.

Beispiele:

```bash
# Alle Spalten als Texttabelle
csvstat data.csv

# Semikolon-getrennte Datei, nur die Spalten name und alter
csvstat data.csv --delimiter ';' --columns name,alter

# JSON-Ausgabe
csvstat data.csv --json
```

## Funktionsumfang

- Einlesen einer CSV-Datei mit automatischer oder expliziter Trennzeichenwahl.
- Pro Spalte Statistiken berechnen (numerisch: Anzahl, Minimum, Maximum,
  Mittelwert, fehlende Werte; Text: Anzahl eindeutiger Werte).
- Spaltenauswahl über `--columns`, in der Reihenfolge der Kopfzeile.
- Ausgabe als ausgerichtete Texttabelle oder als JSON.
- Klare Fehlermeldungen mit Exit-Code 1 für fehlende, leere, nur eine Kopfzeile
  enthaltende und spaltenlose Eingaben.

> Hinweis: Dieses Repository enthält derzeit das lauffähige CLI-Gerüst. Die
> Parser-Optionen, der Ablauf und die Fehlerbehandlung des Einstiegspunkts sind
> fertig; die Statistik-, Lese-, Auswahl- und Ausgabe-Module werden in
> nachfolgenden Tickets mit ihrer Funktionalität gefüllt.
