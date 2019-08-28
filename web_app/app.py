from flask import Flask, render_template, request, jsonify, abort

# import os


from skimage.io import imread, util

from random import random

app = Flask(__name__)

MAX_SIZE = 200

@app.route('/_get_image_categories')
def get_image_categories():
    try:
        url = request.args.get('url', '', type=str)
        
        if not util.is_url(url):
            # abort(500, 'API error')
            return jsonify(error=501)  # , 'This image could not be loaded')#, 404

        img = imread(url)
        h, w, c = img.shape

        hotdog = str(round(100*random(), 2))
        banana = str(round(100*random(), 2))

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
