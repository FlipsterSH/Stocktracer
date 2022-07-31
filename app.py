from flask import Flask, request
import json
from main import *


app = Flask(__name__)


@app.route("/") #bare setter opp webpagen
def index():
    return app.send_static_file("index.html")


@app.route("/update") #sender dictionary med all data og messages
def update():
    data = update1()
    return json.dumps(data)


@app.route("/graphinfo") #sender dictionary med to lister, liste over priser og liste over dager
def graphinfo():
    graph_id = request.args.get("graph_id", None)
    if graph_id:
        data = get_graph(graph_id)
        return json.dumps(data)
    return json.dumps({"pricelist": [], "daylist": []})


@app.route("/myindex") #
def myindex():
    data = my_index()
    return json.dumps(data)


if __name__ == "__main__":
    app.run()