import secrets
import string
import yaml

from flask import Flask, Response, send_from_directory, request, session, abort, render_template, url_for, redirect
from os import environ, listdir
from os.path import getsize, isdir

with open("config/config.yaml", "r", encoding="utf-8") as file:
    cfg = yaml.load(file, Loader=yaml.SafeLoader)

with open("tmp/path.tmp", "r", encoding="utf-8") as file:
    path = file.read()

app = Flask(__name__)
app.secret_key = secrets.token_hex(64)

try:
    secure = str(cfg["custom"]["passkey"])
except (KeyError, TypeError):
    alphabet = string.ascii_letters + string.digits
    secure = ''.join(secrets.choice(alphabet) for _ in range(64))

try:
    provider = str(cfg["custom"]["username"])
except (KeyError, TypeError):
    try:
        provider = environ['USERNAME']
    except KeyError:
        provider = environ['USER']
        if provider == "root":
            provider = "admin"

print(f" * Host: {provider}")
print(f" * Passkey: {secure}\n")

def sizer(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    else:
        return f"{size_bytes:.2f} TB"

def show(site):
    with open(site, "r", encoding="utf-8") as file:
        return file.read()

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template("403.html"), 403

@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500

@app.route('/')
def index():
    return show("w3/index.html") + f"""<title>Filelink - {provider}</title>""" + f"""<h6>Hosted by: {provider}</h6></body></html>"""

@app.route('/success')
def success():
    files = ""
    num = 1
    if not session.get('authorized'):
        return abort(403)
    if not listdir(path):
        return show("w3/success.html") + f"""<h5>no files available</h5>""" + f"""<h6>Hosted by: {provider}</h6></body></html>"""
    for i in listdir(path):
        if isdir(f"{path}/{i}"):
            pass
        else:
            size = sizer(getsize(f"{path}/{i}"))
            files += f"""<h5>{num}. <a href="/download/{i}">{i}</a> ({size})</h5>"""
            num += 1
    return show("w3/success.html") + f"""<title>Files - {provider}</title>""" + files + f"""<h6>{num-1} files. Hosted by: {provider}</h6></body></html>"""

@app.route('/access')
def access():
    key = request.args.get('passkey')
    if key and key == secure:
        session['authorized'] = True
    if session.get('authorized'):
        return redirect(url_for("success"))
    session['allow_get_key'] = True
    return show("w3/access.html")

@app.route('/get-key')
def get_key():
    if not session.get('allow_get_key'):
        return abort(403)
    session.pop('allow_get_key')
    return Response(secure, mimetype='text/plain')

@app.route('/check-key', methods=['POST'])
def check_password():
    user_pass = request.form.get('password', '')
    if user_pass == secure:
        session['authorized'] = True
        return "OK"
    return "FAIL", 403

@app.route('/download/<name>', methods=['GET'])
def download_file(name):
    if not session.get('authorized'):
        return abort(403)
    return send_from_directory(path, name, as_attachment=True)