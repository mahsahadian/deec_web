from pymongo import MongoClient
import os

from Algorithms import DEEC
from graph import build_graph, k_means
import matplotlib.pyplot as plt
from flask import Flask, request, render_template, abort, Response
import io
import base64
import numpy as np
import pandas as pd
w1 = np.random.uniform(0.8,1.0,(50,2))
w2 = np.random.uniform(0.0,0.2,(50,2))
X = np.concatenate((w1,w2),axis=0)
app = Flask(__name__)

global ch_listo, mk_listo, ap_listo, cf_listo
ch_listo, mk_listo, ap_listo, cf_listo = [], [], [], []
client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
db = client.basketdb

@app.route("/handleUpload", methods=['POST'])
def handleFileUpload():
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            data = pd.read_csv(photo)
            #photo.save(os.path.join('C:/Users/Public/Pictures', photo.filename))
    #return redirect(url_for('fileFrontPage'))
@app.route('/')
def index():
    _items = db.basketdb.find()
    #items = [item for item in _items]
    #total = sum([float(item["price"]) for item in items])
    # These coordinates could be stored in DB
    x1 = [0, 1, 2, 3, 4]
    y1 = [10, 30, 40, 5, 50]
    x2 = [0, 1, 2, 3, 4]
    y2 = [50, 30, 20, 10, 50]
    x3 = [0, 1, 2, 3, 4]
    y3 = [0, 30, 10, 5, 30]

    graph1_url = build_graph(x1, y1);
    graph2_url = build_graph(x2, y2);
    graph3_url = build_graph(x3, y3);

    clf = DEEC()
    clf.fit(X)

    for centroid in clf.centroids:
        plt.scatter(clf.centroids[centroid][0], clf.centroids[centroid][1],
                    marker="o", color="k", s=50, linewidths=2)
    colors = 10 * ["g", "r", "c", "b", "k"]
    for classification in clf.classifications:
        color = colors[classification]
        for featureset in clf.classifications[classification]:
            plt.scatter(featureset[0], featureset[1], marker="x", color=color, s=150, linewidths=5)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    image = 'data:image/png;base64,{}'.format(graph_url)
    return render_template('basket.html',
                           graph1=image,
                           graph2=graph2_url,
                           graph3=graph3_url)
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
