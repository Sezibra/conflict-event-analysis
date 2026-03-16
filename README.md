# Conflict Event Data Analysis and Geospatial Visualization

Spatial and temporal analysis of violence against civilians during the Ethiopia/Tigray conflict (November 2020 to November 2022), using the UCDP Georeferenced Event Dataset.

## Research Question

How does violence against civilians cluster spatially and temporally during the Tigray conflict?

## Background

The Tigray conflict began on November 3, 2020, when fighting broke out between Ethiopia's federal government forces and the Tigray People's Liberation Front (TPLF). The conflict escalated through 2021 with multiple armed actors, including Eritrean forces and Amhara regional militias, operating across northern Ethiopia. A Cessation of Hostilities Agreement was signed on November 2, 2022.

## Data

UCDP Georeferenced Event Dataset (GED) v25.1, downloaded from https://ucdp.uu.se/downloads. The full dataset contains 385,918 events of organized violence globally (1989 to 2024). Filtered to Ethiopia during the study period: 1,764 events.

UCDP categorizes organized violence into three types:
- State-based conflict (type 1): fighting between armed groups where at least one is a government. 1,203 events.
- Non-state conflict (type 2): fighting between armed groups with no government involvement. 7 events.
- One-sided violence (type 3): deliberate killing of civilians by an organized armed group. 554 events, 9,324 fatalities.

UCDP data is not redistributed in this repository. See data/README.md for download instructions.

## Methods

- Data cleaning and temporal aggregation with pandas
- Exploratory data analysis: event counts by type, region, actor, and conflict phase
- Geospatial visualization with geopandas and folium
- Spatial clustering with DBSCAN (scikit-learn), using haversine distance at 50km radius

## Key Findings

1. The dataset contains 554 events of one-sided violence against civilians with an estimated 9,324 deaths over two years.

2. Government forces (Ethiopia and Eritrea) committed the majority of documented violence against civilians: 428 of 554 events (77%). The Government of Ethiopia was the perpetrator in 208 events, the Government of Eritrea in 158, and joint Ethiopian-Eritrean forces in 62. TPLF committed 54 events, OLA 45, and Fano militia 25.

3. DBSCAN identified 9 spatial clusters. One cluster in Tigray contains 385 events (69% of all one-sided violence) with 8,444 fatalities. The remaining clusters are in Oromiya (OLA insurgency), Amhara (TPLF counteroffensive), and Benishangul-Gumuz. Only 30 events (5.4%) were classified as noise.

4. Violence shifted geographically across three conflict phases. Phase 1 (Nov 2020 to Jun 2021) concentrated in Tigray during the federal offensive. Phase 2 (Jul to Dec 2021) spread to Amhara and Afar as TPLF forces advanced beyond Tigray. Phase 3 (Jan to Nov 2022) saw violence return toward Tigray before the ceasefire.

5. The four most affected regions were Tigray (728 events), Oromiya (615), Amhara (277), and Afar (94). Oromiya's high count reflects a separate OLA insurgency running in parallel with the Tigray conflict.

## Sample Outputs

### Monthly conflict events by violence type
![Monthly events](outputs/monthly_events_by_type.png)

### Violence against civilians by perpetrator and region
![Perpetrator heatmap](outputs/perpetrator_region_heatmap.png)

### Geographic shift across conflict phases
![Phase maps](outputs/onesided_by_phase_maps.png)

### DBSCAN spatial clusters
![DBSCAN clusters](outputs/dbscan_clusters_map.png)

## Project Structure

    conflict-event-analysis/
        README.md
        requirements.txt
        .gitignore
        notebooks/
            01_exploratory_analysis.ipynb
            02_geospatial_analysis.ipynb
            03_figures_and_findings.ipynb
        src/
            data_loader.py
        data/               (not tracked in git)
        outputs/            (figures, maps, tables)

## How to Reproduce

1. Clone this repository
2. Download UCDP GED v25.1 from https://ucdp.uu.se/downloads and place the CSV in data/
3. Install dependencies: pip install -r requirements.txt

## References

- Sundberg, R. and Melander, E. (2013). Introducing the UCDP Georeferenced Event Dataset. Journal of Peace Research, 50(4), 523-532.
- Gleditsch, K.S. and Weidmann, N.B. (2012). Richardson in the Information Age: GIS and Spatial Data in International Studies. Annual Review of Political Science, 15, 461-481.
- Deutschmann, E. et al. (eds.) (2020). Computational Conflict Research. Springer.
- Hegre, H. et al. (2019). ViEWS: A Political Violence Early-Warning System. Journal of Peace Research, 56(2), 155-174.
- Davies, S., Pettersson, T., Sollenberg, M., and Oberg, M. (2025). Organized violence 1989-2024. Journal of Peace Research, 62(4).
