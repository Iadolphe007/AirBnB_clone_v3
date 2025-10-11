## AirBnB Clone v3 Flask routes

This folder contains small Flask applications demonstrating various routes and template rendering for the HBnB project.

### Run

Any file here is runnable directly, for example:

```bash
python3 0-hello_route.py
# open http://127.0.0.1:5000/
```

Common defaults: host `0.0.0.0`, port `5000`.

### Files overview

- `0-hello_route.py` → `/` → "Hello HBNB!"
- `1-hbnb_route.py` → adds `/hbnb`
- `2-c_route.py` → dynamic route `/c/<text>`
- `3-python_route.py` → optional dynamic `/python/(<text>)`
- `4-number_route.py` → integer route `/number/<n>`
- `5-number_template.py` → renders template if `<n>` is int
- `6-number_odd_or_even.py` → renders odd/even page
- `7-states_list.py` → list states from storage
- `8-cities_by_states.py` → nested listing
- `9-states.py` → dynamic state/city view
- `10-hbnb_filters.py` → renders `10-hbnb_filters.html` with filters

Templates live in `templates/` and styles in `static/`.

[!TIP]
Switch storage backends via `HBNB_TYPE_STORAGE` like the API. The views load data through `models.storage`.
