from flask import Flask, render_template, request, jsonify, abort

from PIL import Image
from skimage.io import imread, util
import os
import numpy as np
from random import random

app = Flask(__name__)

MAX_SIZE = 200
H_SIZE, W_SIZE = 224, 224#300, 300

weights_path = os.path.join(
    os.path.abspath('./'),
    # 'ai/weights/epochs_001-val_acc_0.980.hdf5'
    # 'ai/weights/epochs_003-val_auc_0.886.hdf5'#epochs_011-val_auc_1_0.528.hdf5'
    'ai/weights/mn2_epochs_014-val_auc_0.989.hdf5'
)

import ai.model
model = ai.model.get_model4(weights_path)

@app.route('/_get_image_categories')
def get_image_categories():
    try:
        url = request.args.get('url', '', type=str)
        
        if not util.is_url(url):
            # abort(500, 'API error')
            return jsonify(error=501)  # , 'This image could not be loaded')#, 404

        img = imread(url)
        h, w, c = img.shape

        img = np.stack([
            np.array(
                Image.fromarray(
                    img
                )
                .convert("RGB")
                .resize(
                    (H_SIZE, W_SIZE),
                    Image.ANTIALIAS
                )
            )
        ], axis=0)

        nhnb = None
        try:
            nhnb = model.predict(img)
        except Exception as e:
            abort(500, 'API error')
        nhnb = nhnb[0]
        # print(nhnb)
        hotdog = str(round(100*nhnb[0], 2))
        banana = str(round(100*nhnb[1], 2))

        return jsonify(
            # src=url,
            hotdog=hotdog,
            banana=banana,
            w=w,
            h=h
        )
    except Exception as e:
        # TODO
        print(e)
        return jsonify(error=501)#, 'This image could not be loaded')#, 404
        # abort(500, 'API error')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    #jsonify(error=404, text=(str(e))), 404


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        print(request.form['imageurl'])
    return render_template('main.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
