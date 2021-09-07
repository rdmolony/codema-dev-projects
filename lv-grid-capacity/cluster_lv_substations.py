# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.5
#   kernelspec:
#     display_name: 'Python 3.9.6 64-bit (''lv-grid-capacity'': conda)'
#     name: python3
# ---

# %%
import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from shapely.geometry import MultiPoint
from sklearn.cluster import DBSCAN

from _cluster import cluster_points
from _convert import convert_dataframe_to_geodataframe
from _join_nearest import join_nearest_points


# %% tags=["parameters"]
upstream = [
    "download_esb_substation_capacities",
    "download_dublin_small_area_boundaries",
]
product = None

# %%
lv_substations = (
    pd.read_csv(upstream["download_esb_substation_capacities"])
    .pipe(
        convert_dataframe_to_geodataframe,
        x="Longitude",
        y="Latitude",
        from_crs="EPSG:4326",
        to_crs="EPSG:2157",
    )
    .query("`Voltage Class` == 'LV'")
)

# %%
small_area_boundaries = gpd.read_file(
    upstream["download_dublin_small_area_boundaries"]
).to_crs("EPSG:2157")

# %%
dublin_lv_substations = gpd.sjoin(lv_substations, small_area_boundaries, op="within")

# %%
cluster_coordinates = cluster_points(
    dublin_lv_substations,
    selected_model="KMeans",
    model_parameters={"n_clusters": 100},
)

# %%
lv_substation_clusters = join_nearest_points(
    dublin_lv_substations,
    cluster_coordinates,
)

# %%
lv_substation_clusters.to_file(product["gpkg"], driver="GPKG")
