from typing import Any

import geopandas as gpd
import pandas as pd

from ops.convert import convert_dataframe_to_geodataframe


def extract_dublin_substations(upstream: Any, product: Any) -> None:
    lv_substations = pd.read_csv(upstream["download_esb_substation_capacities"]).pipe(
        convert_dataframe_to_geodataframe,
        x="Longitude",
        y="Latitude",
        from_crs="EPSG:4326",
        to_crs="EPSG:2157",
    )
    small_area_boundaries = gpd.read_file(
        str(upstream["download_dublin_small_area_boundaries"])
    ).to_crs("EPSG:2157")
    dublin_lv_substations = gpd.sjoin(
        lv_substations, small_area_boundaries, op="within"
    )
    dublin_lv_substations.to_file(str(product), driver="GPKG")
