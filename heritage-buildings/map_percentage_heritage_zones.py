import geopandas as gpd
import pandas as pd
import seaborn as sns

sns.set()

# + tags=["parameters"]
upstream = [
    "download_buildings",
    "download_dublin_small_area_boundaries",
    "extract_dublin_niah_houses",
    "extract_dublin_smr_houses",
]
product = None
# -

small_area_boundaries = gpd.read_file(upstream["download_dublin_small_area_boundaries"])

buildings = pd.read_parquet(upstream["download_buildings"])

niah_houses = gpd.read_file(upstream["extract_dublin_niah_houses"])

smr_houses = gpd.read_file(upstream["extract_dublin_smr_houses"])

total_niah_houses_per_small_area = (
    niah_houses.groupby("small_area", sort=False)
    .size()
    .rename("total_niah_dwellings")
    .reindex(small_area_boundaries["small_area"])
    .fillna(0)
)

total_smr_houses_per_small_area = (
    smr_houses.groupby("small_area", sort=False)
    .size()
    .rename("total_niah_dwellings")
    .reindex(small_area_boundaries["small_area"])
    .fillna(0)
)

total_heritage = total_niah_houses_per_small_area.add(
    total_smr_houses_per_small_area
).rename("total_heritage_dwellings")

total_buildings_per_small_area = (
    buildings.groupby("small_area", sort=False)
    .size()
    .rename("total_dwellings")
    .reindex(small_area_boundaries["small_area"])
)

small_area_totals = pd.concat(
    [total_heritage, total_buildings_per_small_area], axis=1
).fillna(0)

percentage_heritage = (
    total_heritage.divide(total_buildings_per_small_area)
    .multiply(100)
    .rename("percentage_of_heritage_dwellings")
)

small_area_heritage_map = pd.concat(
    [small_area_boundaries.set_index("small_area"), percentage_heritage], axis=1
)

ax = small_area_heritage_map.query("percentage_of_heritage_dwellings > 0").plot(
    column="percentage_of_heritage_dwellings", figsize=(20, 20), legend=True
)
small_area_heritage_map.query("percentage_of_heritage_dwellings == 0").plot(
    ax=ax, facecolor="none"
)

small_area_heritage_map.to_file(str(product["gpkg"]), driver="GPKG")
