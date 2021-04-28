# autofresh

Auto-refreshing web server for local static web development

## Requirements
Just Flask. Install with `pip install flask`.

## Use
Use the following command to launch autofresh and point to a directory of your choice. This will default to the `example_root` directory.

```
$ python autofresh.py -r /absolute/path/to/file/root
```

Your files will now be served at `http://127.0.0.1:5000`.

`example_root` contains the following files:
1. http://127.0.0.1:5000/index.html
1. http://127.0.0.1:5000/sudirectory/page.html