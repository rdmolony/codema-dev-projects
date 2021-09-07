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

from ops.cluster import cluster_points
from ops.convert import convert_dataframe_to_geodataframe
from ops.join_nearest import join_nearest_points


# %% tags=["parameters"]
upstream = [
    "extract_dublin_substations",
    "check_electricity_grid_cad_data_is_uploaded",
]
product = None

# %%
dublin_lv_substations = gpd.read_file(upstream["extract_dublin_substations"]).query(
    "`Voltage Class` == 'LV'"
)

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
