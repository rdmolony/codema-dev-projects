from pathlib import Path
from typing import Any

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point


from ops.convert import convert_dataframe_to_geodataframe
from ops.io import read_networkx_gpkg
from ops.join_nearest import join_nearest_points


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


def extract_network_lines(upstream: Any, product: Any) -> None:
    network = gpd.read_file(
        str(upstream["extract_dublin_mv_and_lv_network"]), driver="GPKG"
    )

    # explode converts multi-part geometries to single-part which is req by networkx
    network_lines = network.query("Level in [1, 2, 10, 11]").explode()
    network_lines.to_file(str(product), driver="GPKG")


def find_nearest_nodes_to_stations_on_network(upstream: Any, product: Any) -> None:
    lv_substations = (
        gpd.read_file(str(upstream["extract_dublin_substations"]))
        .query("`Voltage Class` == 'LV'")
        .reset_index(drop=True)
    )
    G = read_networkx_gpkg(str(upstream["extract_network_lines"]))

    nodes_as_points = gpd.GeoSeries(
        [Point(n) for n in G.nodes()], crs="EPSG:2157", name="geometry"
    )
    nearest_node_points = join_nearest_points(
        lv_substations[["geometry"]], nodes_as_points
    )
    nearest_node_ids = (
        nearest_node_points.geometry.apply(lambda x: str(x.coords[0]))
        .rename("nearest_node_ids")
        .to_frame()
    )
    nearest_node_ids.to_parquet(product)
