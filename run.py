import yaml
from waitress import serve

with open("config/config.yaml", "r", encoding="utf-8") as file:
    cfg = yaml.load(file, Loader=yaml.SafeLoader)

host = str(cfg["server"]["address"])
port = int(cfg["server"]["port"])

print("Filelink Server\n")
print(f"Server started at http://{host}:{port}\n")

from main import app
serve(app, host=host, port=port)
