import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree


def join_nearest_points(
    gdA: gpd.GeoDataFrame, gdB: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    nA = np.array(list(gdA.geometry.apply(lambda x: (x.x, x.y))))
    nB = np.array(list(gdB.geometry.apply(lambda x: (x.x, x.y))))
    btree = cKDTree(nB)
    _, idx = btree.query(nA, k=1)
    gdB_nearest = gdB.iloc[idx].reset_index(drop=True)
    return pd.concat(
        [
            gdA.reset_index(drop=True).drop(columns="geometry"),
            gdB_nearest,
        ],
        axis=1,
    )
