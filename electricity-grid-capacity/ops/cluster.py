from typing import Any
from typing import Dict

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiPoint
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans


def cluster_points(
    gdf: gpd.GeoDataFrame, selected_model: str, model_parameters: Dict[str, Any]
):
    _model_map = {"KMeans": KMeans, "DBSCAN": DBSCAN}
    x = gdf.geometry.x
    y = gdf.geometry.y
    coords = pd.concat([x, y], axis=1).to_numpy()
    model = _model_map[selected_model](**model_parameters)
    model.fit(coords)
    cluster_labels = model.labels_
    num_clusters = len(set(cluster_labels))
    clusters = gpd.GeoDataFrame(
        geometry=[MultiPoint(coords[cluster_labels == n]) for n in range(num_clusters)]
    )
    centermost_points = (
        clusters.assign(geometry=lambda gdf: gdf.geometry.centroid)
        .reset_index()
        .rename(columns={"index": "cluster_id"})
    )
    return centermost_points
