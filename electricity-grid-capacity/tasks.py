from pathlib import Path
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


def extract_dublin_mv_and_lv_network(upstream: Any, product: Any) -> None:
    index_filepath = upstream["download_dublin_mv_index_ids"]
    dirpath = Path(upstream["check_electricity_grid_cad_data_exists"])

    mv_index_ids = pd.read_csv(index_filepath, squeeze=True, header=None)
    networks = [
        gpd.read_file(dirpath / "Dig Request Style" / "MV-LV Data" / f"{id}.dgn")
        for id in mv_index_ids
    ]
    network = gpd.GeoDataFrame(pd.concat(networks), crs="EPSG:29903").to_crs(epsg=2157)
    network.to_file(str(product), driver="GPKG")
