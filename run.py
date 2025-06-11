import yaml

from waitress import serve
from os import mkdir
from os.path import exists
from sys import argv

with open("config/config.yaml", "r", encoding="utf-8") as file:
    cfg = yaml.load(file, Loader=yaml.SafeLoader)

host = str(cfg["server"]["address"])
port = int(cfg["server"]["port"])

if not exists("tmp"):
    mkdir("tmp")
    
try:
    path = str(argv[1])
except IndexError:
    try:
        path = str(cfg["custom"]["path"])
    except (KeyError, TypeError):
        path = "files"

with open("tmp/path.tmp", "w", encoding="utf-8") as file:
    file.write(path)

print("\nFilelink Server\n")
print("Debug:")

if host == "0.0.0.0":
    print(f" * Running on all addresses ({host})")
    print(f" * Running on http://127.0.0.1:{port}")
else:
    print(f" * Running on http://{host}:{port}")

print("\nConfiguration:")
print(f" * Folder: {path}")

from main import app
serve(app, host=host, port=port)
