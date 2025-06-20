# 🛗 System Sterowania Windami

## Cel projektu

Aplikacja symuluje pracę **dwóch wind** w sześciopiętrowym biurowcu (Można to modyfikować).
Pozwala na:

* zgłaszanie wezwań z korytarzy (↑/↓),
* wybór pięter z poziomu kabiny,
* przełączanie algorytmu przydziału zgłoszeń w trakcie działania,
* podgląd stanu w czasie rzeczywistym w interfejsie **GUI** (Tkinter) lub **CLI**.

Nieliniowość systemu wynika z kolejkowania wezwań – pojedynczy call może diametralnie zmienić trasy obu wind i czasy oczekiwania pozostałych pasażerów.

---

## Architektura (MVC)

| Warstwa        | Klasy / moduły                                                                         | Odpowiedzialność                          |
| -------------- | -------------------------------------------------------------------------------------- | ----------------------------------------- |
| **Model**      | `Building`, `Elevator`, `FloorRequest`, `CabinRequest`, `ElevatorState`, `strategy.py` | logika domenowa i pełny stan symulacji    |
| **View**       | `ViewGUI`, `ViewCLI`                                                                   | prezentacja danych; **obserwator** modelu |
| **Controller** | `Controller`                                                                           | parsowanie poleceń i aktualizacja modelu  |

Plik **`main.py`** uruchamia wspólny model; użytkownik wybiera tryb `gui` lub `cli`.

---

## Wzorce projektowe

| Wzorzec      | Implementacja                                                               | Rola                                    |
| ------------ | --------------------------------------------------------------------------- | --------------------------------------- |
| **Strategy** | `DispatchStrategy` → `NearestElevatorStrategy`, `LeastBusyElevatorStrategy` | wybór windy dla nowego zgłoszenia       |
| **State**    | `ElevatorState`                                                             | zachowanie kabiny w każdym ticku        |
| **Observer** | `Building` → `ViewGUI` / `ViewCLI`                                          | powiadamianie widoków po każdej zmianie |
| **MVC**      | patrz tabela wyżej                                                          | luźne sprzężenie warstw                 |

---

## SOLID w praktyce

* **SRP** – każda klasa odpowiada za jeden aspekt (np. `Elevator` tylko za ruch).
* **OCP** – kolejne algorytmy przydziału dodajemy jako nowe klasy strategii.
* **LSP** – wszystkie strategie w pełni zastępowalne poprzez wspólny interfejs.
* **ISP** – brak „grubych” interfejsów; `DispatchStrategy` ma tylko `select_elevator`.
* **DIP** – `Building` zależy od abstrakcji `DispatchStrategy`, a nie od jej implementacji.

---

## Sposób działania

1. **Tick (1 s)**

   * obsługa kolejki korytarzowej przez aktywną strategię,
   * ruch każdej windy o jedno piętro lub cykl drzwi,
   * powiadomienie widoków.
2. **GUI** – przyciski hall-call, panel kabiny z przyciskami pięter, auto-tick co 1 s.
3. **CLI** – komendy: `fr`, `cr`, `strategy`, `tick`, `status`.

---

## Uruchomienie

```bash
python main.py gui    # interfejs graficzny
python main.py cli    # interfejs tekstowy
```

---

## Struktura katalogów

```
src/
 ├─ elevator.py          # logika kabiny (State)
 ├─ building.py          # model budynku + Observer
 ├─ strategy.py          # interfejs + 2 strategie (Strategy)
 ├─ controller.py        # CLI Controller
 ├─ view_cli.py          # widok tekstowy
 ├─ view_gui.py          # widok Tkinter
 ├─ requests.py          # value objects
 └─ main.py              # wybór GUI/CLI
docs/
 ├─ UML/
 │   ├─ diagram.png      # diagram klas
 │   └─ diagram.txt      # opcjonalny link do PlantUML
 └─ screenshots/         # zrzuty ekranu GUI i CLI
 
```

---

## UML klas

Diagram znajduje się w `docs/UML/diagram.png` (wersja PlantUML w `diagram.txt`).
Oznaczenia stereotypów: `«strategy»`, `«observer»`, `enum`, itp.

---

## Rezultat

Projekt spełnia wszystkie kryteria: modeluje złożony, nieliniowy problem przydziału wind, zachowuje zasady **SOLID**, wykorzystuje wzorce **Strategy, State, Observer, MVC**, a repozytorium zawiera kod źródłowy, diagram UML, opis i zrzuty ekranu z działania.
