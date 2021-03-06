# autofresh

autofresh is a simple Flask app that serves your static HTML files with JavaScript injected to refresh the page when its file is changed locally.

## Requirements
Python >=3.6 and Flask. Install with `pip install flask`.

Or with a virtual environment: `python3 -m venv venv && source venv/bin/activate && pip install flask`

## Use
Use the following command to launch autofresh and point to a directory of your choice. This will default to the `example_root` directory.

```
$ python3 autofresh.py -r /absolute/path/to/file/root
```

Your files will now be served at `http://127.0.0.1:5000`.

`example_root` contains the following files:
1. http://127.0.0.1:5000/index.html
1. http://127.0.0.1:5000/subdirectory/page.html
