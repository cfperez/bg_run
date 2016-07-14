# Non-blocking execution cell magic

In the jupyter notebook:
```
In [1]: %bg result = long_call()
```

Immediately returns while the call runs and updates variable `result` when finished. Uses threading as the calls are assumed to be IO-bound, e.g. waiting for queries or remote jobs to run.

```
In [2]: future = %bg long_call()
```
Returns a future (see concurrent.futures).

## Installation

1. `pip install git+https://github.com/cfperez/bg_run`
2. In notebook: `%load_ext bg_run`

