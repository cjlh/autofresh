from argparse import ArgumentParser
import os
import threading
import time
import glob

from flask import Flask, jsonify, request, render_template_string, send_from_directory


CLIENT_REFRESH_PERIOD_SECONDS = 0.5
SERVER_FILE_CHECK_PERIOD_SECONDS = 0.5
LAST_MODIFIED = dict()
LAST_ACCESSED = dict()


REFRESH_SCRIPT = f"""
window.setInterval(function(){{
    fetch('/shouldRefresh?filename=' +
          (window.location.pathname === '/' ? '/index.html' : window.location.pathname))
        .then(response => response.json())
        .then(json => refresh(json['result']));
}}, {CLIENT_REFRESH_PERIOD_SECONDS * 1000});

function refresh(shouldRefresh) {{
    if (shouldRefresh === true) {{
        location.reload();
    }}
}}
"""


def update_last_modified_times(root):
    trim_length = len(root) - 1 if root[-1] == '/' else len(root)
    while True:
        for filename in glob.iglob(root + '**/**', recursive=True):
            LAST_MODIFIED[filename[trim_length:]] = os.path.getmtime(filename)
        time.sleep(SERVER_FILE_CHECK_PERIOD_SECONDS)


def init(root):
    t = threading.Thread(target=update_last_modified_times, args=(root,)).start()
    return Flask(__name__, template_folder=root)


parser = ArgumentParser()
parser.add_argument('-r')
args = parser.parse_args()
if args.r:
    app = init(args.r)
else:
    app = init(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'example_root'))


@app.route('/<path:filename>')
def serve_file(filename):
    LAST_ACCESSED[f'/{filename}'] = time.time()
    s = f"{{% include '{filename}' %}}" + f"\n<script>{REFRESH_SCRIPT}</script>"
    return render_template_string(s)


@app.route('/')
def index():
    return serve_file('index.html')


@app.route('/shouldRefresh')
def should_refresh():
    filename = request.args.get('filename')
    result = (filename in LAST_ACCESSED and filename in LAST_MODIFIED and
              LAST_ACCESSED[filename] < LAST_MODIFIED[filename])
    return jsonify(result=result)


app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run()
