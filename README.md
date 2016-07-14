# Non-blocking execution cell magic

In the jupyter notebook:
```
>>> %bg result = long_call()
```

Immediately returns while the call runs. Uses threading as the calls are assumed to be IO-bound, e.g. waiting for queries or remote jobs to run.
