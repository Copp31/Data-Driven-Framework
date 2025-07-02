

## 🎼 Missing Migrants: Data-Driven Composition Framework


This project offers a preliminary data analysis of the **Missing Migrants Project** dataset as a way to better understand the systemic violence and human loss surrounding global migration. The numbers—often treated as abstract or impersonal—are approached here as traces of real lives, dislocated by structural inequality, border regimes, and geopolitical indifference.

This work marks the beginning of a broader research and composition project developed in collaboration with **Bled Contemporary Music Week** (Slovenia, 2026). The ultimate goal is to write a musical score under constraint, where data-derived elements shape the sonic language itself.

The cleaned and analyzed data are translated into **MIDI files**, which will serve as a compositional base. These MIDI sequences will be mapped to parameters of **VST instruments**, **modulation effects**, or directly notated into score material—creating a space where **statistics become sonified structures**.

By grounding the musical process in datasets tied to human displacement, this project seeks to engage with questions of **audibility, ethics, and the limits of representation**.

Database : https://missingmigrants.iom.int/downloads

## ⚙️ Workflow

### 1. Load and Clean the Dataset

```python
df = pd.read_csv('../data/Missing_Migrants_Global_Figures_allData.csv')
df.columns = df.columns.str.strip().str.replace('"', '')
df['Number of Dead'] = df['Number of Dead'].fillna(0)
df['Total Number of Dead and Missing'] = df['Total Number of Dead and Missing'].fillna(0)
```

### 2. Generate Key Aggregates

```python
deaths_by_year = df.groupby('Incident Year')['Total Number of Dead and Missing'].sum()
top_routes = df.groupby('Migration Route')['Total Number of Dead and Missing'].sum().sort_values(ascending=False)
```

### 3. Save Reports

```python
with open("data/analyse_missing_migrants.txt", "w") as f:
    f.write(f"Total deaths: {df['Number of Dead'].sum()}")
```

Structured output is also exported as JSON for downstream use:

```python
json.dump({"deaths_by_year": deaths_by_year.to_dict()}, open("data/output.json", "w"))
```

---

## 🎵 MIDI Sonification

We transform structured data into a sequence of MIDI notes using a linear mapping.

### Example: children affected per year → pitch

```python
from migrant_data_to_midi import MigrantDataToMIDI

converter = MigrantDataToMIDI("data/analyse_croisee_missing_migrants.json")
converter.create_midi_from_field("children_by_year", "data/children_by_year.mid")
```

### MIDI Mapping Logic

```python
pitch = int(map_range(value, min_val, max_val, pitch_low, pitch_high))
track.append(Message('note_on', note=pitch, velocity=100, time=delta))
```

You can replace the `map_range()` logic or enforce scale quantization (e.g., C major) for musicality.

---


This approach blends **data journalism**, **music composition**, and **information ethics**.

---

## ✍️ Future Directions

* Visualize MIDI over time using DAW or WebMIDI tools
* Integrate with interactive installations or generative environments

