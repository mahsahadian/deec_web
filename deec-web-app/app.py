import datetime

from pymongo import MongoClient
from Algorithms import DEEC
import matplotlib.pyplot as plt
from flask import Flask, request, render_template
import io
import base64
import numpy as np
import pandas as pd
app = Flask(__name__)
global ch_listo, mk_listo, ap_listo, cf_listo
ch_listo, mk_listo, ap_listo, cf_listo = [], [], [], []
client = MongoClient('localhost', 27017)
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
    w1 = np.random.uniform(0.8, 1.0, (50, 2))
    w2 = np.random.uniform(0.0, 0.2, (50, 2))
    X = np.concatenate((w1, w2), axis=0)
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
    return render_template('basket.html',graph1=image)
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
