# Heat Pumps

Plot heat pump viability maps by classifying buildings with a Heat Loss Parameter of less than 2 as heat pump ready

## Setup

Via [conda](https://github.com/conda-forge/miniforge):

```bash
conda env create --name heat-pumps --file environment.yml
conda activate heat-pumps
```

Now run the pipeline:

```bash
ploomber build
```