# Python Backend & QA Portfólió

Ez a repository két, ipari sztenderdeknek megfelelő ("production-grade") referencia projektet tartalmaz, amelyek célja a modern Python fejlesztési és tesztelési best practice-ek demonstrálása.

A projektek elszeparált mappákban találhatók, saját virtuális környezettel és függőségekkel rendelkeznek.

---

## 1. 🧪 Mini Pytest API Tests (`mini-pytest-api-tests/`)

Ez a projekt egy **professzionális, skálázható API tesztelési keretrendszert** valósít meg. Nem egy egyszerű szkriptgyűjtemény, hanem egy strukturált, könnyen bővíthető framework.

### 🔭 Cél
Bemutatni, hogyan lehet karbantartható, környezet-független és típusbiztos teszteket írni REST API-khoz.

### 🛠 Technikai Stack
- **Core**: Python 3.9+, `pytest`
- **HTTP Client**: `requests` (wrapper osztállyal, automatikus retry logikával)
- **Validáció**: `pydantic` (szigorú típusellenőrzés a válaszokra)
- **CI/CD**: GitHub Actions
- **Quality**: `ruff`, `mypy`, `black`

### 💡 Kiemelt Megoldások (Senior Level)
- **Környezetkezelés**: A konfiguráció (pl. base URL) környezeti változók (`ENV`) és YAML fájlok kombinációjából töltődik be. Ugyanaz a tesztkód futtatható `dev`, `staging` és `prod` környezeten is.
- **Robust Client**: Az API hívások egy saját `ApiClient` osztályon keresztül mennek, amely automatikusan kezeli a hitelesítést (Auth headers), a logolást és az újrapróbálkozást (retry) hálózati hibák esetén.
- **Deklaratív Validáció**: A JSON válaszokat nem dictionary-ként kezeljük, hanem Pydantic modellekké alakítjuk. Ez azonnal kibuktatja, ha az API megváltoztatja a választípusokat (pl. `int` helyett `string`-et küld).
- **Jelentéskészítés**: Automatikus HTML riport generálás a tesztfutásokról.

---

## 2. 📊 Log Parser & Reporter (`log-parser-reporter/`)

Ez a projekt egy **nagy teljesítményű log feldolgozó és analizáló eszközt** (CLI) valósít meg. Képes hatalmas méretű logfájlok feldolgozására anélkül, hogy azokat betöltené a memóriába.

### 🔭 Cél
Demonstrálni a streaming adatfeldolgozást, a hatékony algoritmusokat és a modern CLI fejlesztést.

### 🛠 Technikai Stack
- **CLI**: `typer`, `rich` (színes, interaktív kimenet)
- **Core**: Python Generator-ok (streaming), `pydantic`
- **Riport**: `jinja2` (HTML templating)
- **Algoritmusok**: `heapq` (Top-N számítás), statisztikai aggregációk

### 💡 Kiemelt Megoldások (Senior Level)
- **Streaming Architecture**: A rendszer soronként ("lazán") olvassa a fájlokat. Ez lehetővé teszi akár több gigabájtos logfájlok feldolgozását is minimális memóriahasználat mellett (O(1) memóriaigény a legtöbb metrikához).
- **Plug-in Rendszer**: A parserek (JSON, Regex/Text) egy közös `BaseParser` interfészt valósítanak meg. Új formátum támogatása (pl. CSV, Syslog) csak egy új osztály létrehozását igényli a meglévő kód módosítása nélkül (Open-Closed Principle).
- **Hibatűrés (Robustness)**: A rendszer nem áll le (crash) egyetlen hibás sor miatt sem. A hibás sorokat külön gyűjti (`events_failed.csv`) későbbi elemzésre, miközben a helyes adatokat feldolgozza.
- **Analitika**: Kiszámolja a P50/P95/P99 latencia értékeket és képes detektálni az anomáliákat (pl. hirtelen megugró hibaarány egy adott időablakban).

---

## 🚀 Közös Jellemzők (Quality Gates)

Mindkét projekt szigorú minőségbiztosítási eszközöket használ, amelyek garantálják a kód fenntarthatóságát:

1.  **Type Hinting**: Minden függvény szigorúan típusos (`mypy --strict`).
2.  **Linting & Formatting**: `ruff` és `black` biztosítja az egységes kódstílust.
3.  **Makefile**: Egyszerűsített parancsok (`make test`, `make lint`) a fejlesztői élmény javítására.
4.  **Reprodukálhatóság**: `pyproject.toml` definiálja a pontos függőségeket.

## 🏃‍♂️ Hogyan használd?

Lépj be az egyik projekt könyvtárába, és kövesd az ottani `README.md` utasításait:

```bash
# 1. API Tesztek
cd mini-pytest-api-tests
pip install -e .
pytest

# 2. Log Parser
cd log-parser-reporter
pip install -e .
python gen_samples.py
log-reporter report --input samples/
```
