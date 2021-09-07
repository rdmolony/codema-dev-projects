# Electricity Grid Capacity

## Caveat

To reproduce this project you must:

1. Have access to the closed-access ESB CAD Network data
2. Create a new folder called `data/raw/` and copy this dataset into it

## Setup

Install via [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/):
```bash
conda env create -f environment.yml -n electricity-grid
```

Now run via [ploomber](https://github.com/ploomber/ploomber):
```bash
ploomber build
```