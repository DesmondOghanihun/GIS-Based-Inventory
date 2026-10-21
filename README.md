# A GIS-Based Inventory of Estuarine and Coastal Creek Systems in the Niger Delta: Baseline Data for Marine Ecosystem Management

This repository contains the open-source spatial framework, Python scripts, and baseline hydrological datasets developed to map and inventory 23 major estuarine and coastal creek systems across the core Niger Delta states (**Delta, Bayelsa, and Rivers**).

---

## 👥 Author & Affiliation
* **Ugegeh Desmond Oghanihun*** (Corresponding Author) — *desmond.ugegeh@unidel.edu.ng*

*Department of Marine Science, University of Delta, Agbor, Nigeria*

---

## 📝 Abstract
The Niger Delta region of Nigeria hosts one of Africa's most extensive and ecologically significant coastal wetland systems, characterized by intricate networks of estuaries, creeks, and river channels that support diverse marine ecosystems and coastal livelihoods. Despite their ecological and economic importance, comprehensive spatial inventories of these hydrological features remain limited, constraining effective marine ecosystem management and conservation planning. 

This study presents a **GIS-based inventory of 23 estuarine and coastal creek systems** across the core Niger Delta states of Delta, Bayelsa, and Rivers. Using open-source geospatial tools (`Python`, `GeoPandas`, `Matplotlib`) and integrating multiple data sources including KML-format hydrological features and administrative boundary shapefiles, we developed a high-resolution spatial framework mapping the distribution, connectivity, and geographic context of these critical marine-influenced waterways. 

The resulting cartographic product includes a multi-panel map with national and regional insets, a detailed main map with OpenStreetMap basemap integration, and a comprehensive legend employing color-shape differentiation for individual feature identification. This baseline dataset provides essential spatial information for marine ecosystem management, supporting applications in fisheries management, oil spill response planning, coastal zone regulation, and conservation prioritization.

---

## 🎯 Core Objectives & Significance
- **Spatial Mapping:** Create a high-resolution framework documenting 23 critical marine-influenced waterways.
- **Methodological Development:** Outline a reproducible, entirely open-source workflow for coastal mapping in data-scarce regions.
- **Environmental Management Support:** Provide actionable baseline data critical for oil spill trajectory modeling, environmental remediation, and coastal zone planning.
- **Conservation & Policy:** Support marine spatial planning and climate change vulnerability assessment against sea-level rise.

---

## 🛠️ Tech Stack & Dependencies
The methodology relies exclusively on open-source Python geospatial libraries. To execute the tracking script, ensure you have the following packages installed:

```bash
pip install geopandas matplotlib contextily shapely pandas
```

* **GeoPandas:** For handling vector data geometries, shapefiles, and KML layers.
* **Matplotlib:** For rendering multi-panel cartographic outputs, figures, and legends.
* **OpenStreetMap (via Contextily/Basemaps):** Integrated as the primary web map tiles background for geographic context.

---

## 📂 Repository Structure

```text
├── data/                       # Core GIS dataset directory
│   ├── *.kml                   # 23 discrete KML files mapping estuarine channels
│   └── [shapefiles]            # Regional administrative boundary maps
├── inventory2.py               # Main Python pipeline generating maps & inventories
├── .gitignore                  # Git configurations protecting large spatial caches
└── README.md                   # Project documentation
```

### Monitored Hydrological Systems (Data Folder)
The `data/` directory isolates and tracks individual KML layers for the 23 mapped systems, which include:
* *Escravos, Forçados, Benin, Ethiope, and Warri Rivers* (Delta State)
* *Brass, Nun, Sangana, Kulama, Dodo, and Middleton Rivers* (Bayelsa State)
* *Bonny, New Calabar, Sombreiro, and Andoni Rivers* (Rivers State)
* *...and other major interconnected coastal creeks.*

---

## 🚀 How to Run the Script
Ensure your terminal environment is mapped correctly to your workspace folder containing `inventory2.py` and the `data/` folder, then run:

```bash
python inventory2.py
```

### Expected Output
The script automatically reads the data directory, processes the geometries, overlays administrative boundaries, and outputs high-resolution cartographic figures (`.png`/`.pdf`) detailing:
1. **Figure 1:** Multi-panel map showing regional distribution with national/state inset alignments.
2. **Figure 2:** Statistical charts showing features categorized cleanly by administrative distribution.

---

## 🏷️ Keywords
`GIS Inventory` • `Estuaries` • `Coastal Creeks` • `Niger Delta` • `Marine Ecosystem Management` • `Open-Source GIS` • `Coastal Zone Management` • `Baseline Data`
