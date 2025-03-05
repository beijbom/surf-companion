# Surf Companion

<https://beijbom--surfcompanion-surf-companion.modal.run/>

Log your rides, get stats and recommendations

## Developers

### Run once

* Install the `uv` python manager <https://docs.astral.sh/uv/getting-started/installation/>
* Create a modal account <https://modal.com/>
* Configure your modal account `uv run modal config`

### Run dev server

`uv run modal serve main.py`

### Deploy to prod

`uv run modal deploy main.py`

## Todo

* Auth / account management
* Add images to SurfSession schema. Refine the score categories and values.
* Add SurfSession dashboards
* Add Spot dashboards
* Pull in data from NOAA and other sources
* Add recommendations
