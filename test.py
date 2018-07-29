# $ export FLASK_APP=flask-serve.py
# $ flask run [-p 5000]

from flask import Flask, jsonify, make_response, render_template
from flask import Markup
from flask import request
import json
import db

app = Flask(__name__)

gobleni = {
    '644': dict(name='Под чадъра', colours=56, model='1:1/1:4', size_w='69', size_h='45', price='109.50'),
    '656': dict(name='Фрегати 3D', colours=40, model='1:4', size_w='70', size_h='25', price='80')
}

category_display_names_en = {
    'religious': 'Религиозни мотиви',
    'landscapes': 'Пейзажи',
    'paintings': 'Картини',
    'stilllife': 'Натюрморти',
    'flowers': 'Цветя',
    'animals': 'Животни',
    'children': 'Детски картини',
    'mini': 'Миниатюри'
}

category_display_names = {
    'религиозни': 'Религиозни мотиви',
    'пейзаж': 'Пейзажи',
    'картина': 'Картини',
    'натюрморт': 'Натюрморти',
    'цветя': 'Цветя',
    'животни': 'Животни',
    'деца': 'Детски картини',
    'графика': 'Графики',
    'мини': 'Миниатюри'
}

# category_display_names = {
#     'религиозни': 'Религиозни мотиви',
#     'икона': '',
#     'пейзаж': 'Пейзажи',
#     'къща': '',
#     'зима': '',
#     'море': '',
#     'картина': 'Картини',
#     'портрет': '',
#     'българска': '',
#     'натюрморт': 'Натюрморти',
#     'плодове': '',
#     'цветя': 'Цветя',
#     'животни': 'Животни',
#     'кон': '',
#     'куче': '',
#     'детски': 'Детски картини',
#     'дисни': '',
#     'графика': 'Графики',
#     'мини': 'Миниатюри'
# }

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
    try:
        info = db.goblen_info(number)
        # TODO maybe add readable artist here?
    except KeyError:
        # TODO nicer 404 page
        return make_response(jsonify({'error': 'Not found'}), 404)

    name_display = info['name']
    category_display = category_display_names[category]
    print(info['author'])

    # if info['model'] == '1:1':
    #     model_label = '1 към 1'
    # elif info['model'] == '1:4':
    #     model_label = '1 към 4'
    # elif info['model'] == '1:1/1:4':
    #     model_label = '1 към 1 или 1 към 4'
    # else:
    #     model_label = ''

    return render_template('goblen.html', number=number,
        category=category, category_display=category_display,
        name=name, name_display=name_display,
        hudojnik = db.goblen_hudojnik(info['author']),
        subtitle = info['subtitle'], description = Markup(info['description']),
        colours=info['colours'],
        model=info['model'], size_w=info['size_w'], size_h=info['size_h'], price=info['price']/100,
        model2=info['model2'], size2_w=info['size2_w'], size2_h=info['size2_h'], price2=info['price2']/100)
        # TODO prices should really be handled in a general way, and beautified
        # TODO add ready offers too

@app.route('/goblen/<category>/<number>')
def goblen_incomplete_url(category, number):
    # TODO redirect instead?
    # goblen(category, number, gobleni[number]['name'])
    return goblen(category, number, gobleni[number]['name'])

@app.route('/hudojnik/<name>')
def hudojnik(name):
    info = db.hudojnik_info(name)
    gobleni = db.gobleni_ot(name)
    if gobleni is None:
        # TODO handle these
        print("NONE FROM DB")
    return render_template('hudojnik.html',
            artist = info['name'],
            description = Markup(info['description']),
            gobleni = gobleni,
            wiki_link = info['wiki_link'])

# This server's not-found repsonse
@app.errorhandler(404)
def not_found(error):
 return make_response(jsonify({'error': 'Not found'}), 404)
