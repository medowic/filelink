import yaml
import urllib.request

from waitress import serve
from os import mkdir
from os.path import exists
from sys import argv

no_update = [ "-o", "--no-updates"]
path_flag = ["-f", "--folder"]

def update():
    with urllib.request.urlopen('https://raw.githubusercontent.com/medowic/filelink/master/version/version.data') as response:
        version_main = response.read().decode('utf-8')
        version_main = version_main.strip()

    with open(f"version/version.data", "r", encoding="utf-8") as file:
        version_main_local = file.read()
        version_main_local = version_main_local.strip()

    if not version_main_local == version_main:
        print(f"\nNew version of Filelink available ({version_main}) [current: {version_main_local}]")
        print("You can download it from https://github.com/medowic/filelink")

with open("config/config.yaml", "r", encoding="utf-8") as file:
    cfg = yaml.load(file, Loader=yaml.SafeLoader)

host = str(cfg["server"]["address"])
port = int(cfg["server"]["port"])

if not exists("tmp"):
    mkdir("tmp")

for flag in path_flag:
    if flag in argv:
        path_index = argv.index(flag) + 1
        try:
            path = str(argv[path_index])
        except IndexError:
            path_set = False
        else:
            path_set = True
            break
    else: path_set = False

if not path_set:
    try:
        path = str(cfg["custom"]["path"])
    except (KeyError, TypeError):
        path = "files"

with open("tmp/path.tmp", "w", encoding="utf-8") as file:
    file.write(path)

for flag in no_update:
    if flag in argv:
        is_update = False
        break
    else: is_update = True

if is_update:
    update()

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