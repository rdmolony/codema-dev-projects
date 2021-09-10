from typing import Any

import pandas as pd


def calculate_small_area_heat_pump_viability(upstream: Any, product: Any) -> None:
    use_columns = ["small_area", "heat_loss_parameter"]

    buildings = pd.read_parquet(upstream["download_buildings"]).loc[:, use_columns]

    is_heat_pump_ready = buildings["heat_loss_parameter"] < 2

    number_of_heat_pump_ready_dwellings_per_small_area = (
        pd.concat([buildings["small_area"], is_heat_pump_ready], axis=1)
        .groupby("small_area", sort=False)["heat_loss_parameter"]
        .sum()
    )

    total_dwellings_per_small_area = buildings["small_area"].value_counts(sort=False)

    small_area_heat_pump_viability = (
        number_of_heat_pump_ready_dwellings_per_small_area.divide(
            total_dwellings_per_small_area
        )
        .multiply(100)
        .round(2)
        .rename("percentage_of_heat_pump_ready_dwellings")
        .to_frame()
    )

    small_area_heat_pump_viability.to_csv(product)
