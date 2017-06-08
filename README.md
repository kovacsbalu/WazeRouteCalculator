# WazeRouteCalculator

[![Build Status](https://travis-ci.org/kovacsbalu/WazeRouteCalculator.svg?branch=master)](https://travis-ci.org/kovacsbalu/WazeRouteCalculator)
[![Coverage Status](https://coveralls.io/repos/github/kovacsbalu/WazeRouteCalculator/badge.svg?branch=master)](https://coveralls.io/github/kovacsbalu/WazeRouteCalculator?branch=master)

Calculate actual route time and distance with waze api

## Installation

```
pip install WazeRouteCalculator
```
## Example

```python
import WazeRouteCalculator

from_address = 'Budapest, Hungary'
to_address = 'Gyor, Hungary'
region = 'EU'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region)
route.calc_route_info()
```

```
python example.py
From: Budapest, Hungary - to: Gyor, Hungary
Time 69.27 minutes, distance 120.91 km.
```

`from_address` and `to_address` are required. `region` is optional, and defaults to "EU". `region` can be one of:

- EU (Europe)
- US or NA (North America)
- IL (Israel)

The Waze API has separate URLs for each region, and so identifying the correct region is crucial.
