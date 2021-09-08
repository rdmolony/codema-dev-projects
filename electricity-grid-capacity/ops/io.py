from pathlib import Path
from typing import Union

import geopandas as gpd
import networkx as nx
import momepy


def read_networkx_gpkg(filepath: Union[Path, str]) -> nx.DiGraph:
    network = gpd.read_file(Path(filepath), driver="GPKG")
    G = momepy.gdf_to_nx(network, approach="primal")
    G_dm = nx.DiGraph(G)
    return G_dm
