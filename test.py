# $ export FLASK_APP=flask-serve.py
# $ flask run [-p 5000]

from flask import Flask, jsonify, make_response, render_template
from flask import request
import json

app = Flask(__name__)

gobleni = {
    '644': dict(name='Под чадъра', colours=56, model='1:1/1:4', size_w='69', size_h='45', price='109.50'),
    '656': dict(name='Фрегати 3D', colours=40, model='1:4', size_w='70', size_h='25', price='80')
}

category_display_names = {
    'religious': 'Религиозни_мотиви',
    'landscapes': 'Пейзажи',
    'paintings': 'Картини',
    'stilllife': 'Натюрморти',
    'flowers': 'Цветя',
    'animals': 'Животни',
    'children': 'Детски картини',
    'mini': 'Миниатюри'
}

@app.route('/gallery')
def gallery_generic():
    return 'whateva'

@app.route('/gallery/<category>')
def gallery(category):
    gobleni = [644, 656]

    return render_template('gallery.html', category=category,
        category_display=category_display_names[category],
        gobleni=gobleni)

@app.route('/goblen/<category>/<number>/<name>')
def goblen(category, number, name):
    # TODO db lookup here
    try:
        info = gobleni[number]
    except KeyError:
        return make_response(jsonify({'error': 'Not found'}), 404)

    name_display = name.replace('-', ' ').title()
    category_display = category_display_names[category]

    if info['model'] == '1:1':
        model_label = '1 към 1'
    elif info['model'] == '1:4':
        model_label = '1 към 4'
    elif info['model'] == '1:1/1:4':
        model_label = '1 към 1 или 1 към 4'
    else:
        model_label = ''

    return render_template('goblen.html', category=category, number=number, name=name,
        name_display=name_display, category_display=category_display,
        colours=info['colours'], model=model_label, size_w=info['size_w'], size_h=info['size_h'], price=info['price'])

@app.route('/goblen/<category>/<number>')
def goblen_incomplete_url(category, number):
    # TODO redirect instead?
    # goblen(category, number, gobleni[number]['name'])
    return goblen(category, number, gobleni[number]['name'])

# This server's not-found repsonse
@app.errorhandler(404)
def not_found(error):
 return make_response(jsonify({'error': 'Not found'}), 404)
