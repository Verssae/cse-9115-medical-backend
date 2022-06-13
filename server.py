from flask import Flask, redirect, render_template, request, Response
from werkzeug.datastructures import ImmutableMultiDict
from urllib.parse import urlparse
import converter
import json
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Please post info to (URL)/post </p>"


@app.route("/post",methods=['POST'])
def post():
    req_dict = json.loads(request.data)

    result_path = converter.convert(req_dict)
    
    o = urlparse(request.base_url)

    
    res = {"url": f"{o.hostname}:5000/{result_path}"}

    return json.dumps(res)





def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src, encoding="UTF-8").read()
    except IOError as exc:
        return str(exc)



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_resource(path):  # pragma: no cover
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
    }
    print(path)
    complete_path = os.path.join(root_dir(), path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)   