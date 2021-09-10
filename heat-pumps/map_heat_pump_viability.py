# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.12.0
# kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import geopandas as gpd
import pandas as pd

# + tags=["parameters"]
upstream = [
    "calculate_small_area_heat_pump_viability",
    "download_small_area_boundaries",
]
product = None
# -

small_area_heat_pump_viability = pd.read_csv(
    upstream["calculate_small_area_heat_pump_viability"]
)

small_area_boundaries = gpd.read_file(str(upstream["download_small_area_boundaries"]))

small_area_heat_pump_viability_map = small_area_boundaries.merge(
    small_area_heat_pump_viability
)

small_area_heat_pump_viability_map.plot(
    column="percentage_of_heat_pump_ready_dwellings", figsize=(20, 20), legend=True
)

small_area_heat_pump_viability_map.to_file(product["gpkg"])
