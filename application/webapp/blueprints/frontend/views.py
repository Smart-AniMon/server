from flask import abort, render_template, request, redirect, session, url_for
from webapp.ext.database import instance
from .forms import FlagForm, LabelForm, SearchForm, AnimalForm
from flask_paginate import Pagination, get_page_parameter
from bson.objectid import ObjectId

ROWS_PER_PAGE = 5
filter = False

def index():
    return render_template("index.html")

def monitored():
    fields = [
        {'filter': 'id' , 'name': 'Módulo'},
        #{'filter': 'capture_date' , 'name': 'Data de Captura'}
    ]
    collection_monitored = 'monitored_animals'
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)

    form = SearchForm()
    form.filtro.choices = [(field['filter'], field['name']) for field in fields]
    global filter
    if request.method == 'POST':
        if form.search.data:
            session['filter_key'] = form.filtro.data
            session['filter_value'] = form.value.data
            filter = True
        elif form.clear.data:
            session['filter_key'] = ''
            session['filter_value'] = ''
            form.filtro.data = ''
            form.value.data = ''
            filter = False
    filtro = None
    if filter: 
        filtro = {session['filter_key'] : session['filter_value']}
        form.value.data = session['filter_value']
        form.value.render_kw = {'disabled': 'disabled'}
        form.search.render_kw = {'disabled': 'disabled'}
    result = get_documents(collection_monitored, filtro , (page-1)*ROWS_PER_PAGE)
    pagination = Pagination(page=page, per_page=ROWS_PER_PAGE, 
                                    total=result.count(), search=search, css_framework='bootstrap3', record_name='result')
    return render_template("monitored.html",form=form, pagination=pagination, monitored_animals=result, title="Animais Monitorados")

def classified():
    collection = 'identified_animals'
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    result = get_documents(collection, {'classified': True}, (page-1)*ROWS_PER_PAGE)
    pagination = Pagination(page=page, per_page=ROWS_PER_PAGE, 
                                    total=result.count(), search=search, css_framework='bootstrap3', record_name='result')
    return render_template("classified.html",pagination=pagination, classified_animals=result, title="Animais Classificados")

def identified():
    collection_identified = 'identified_animals'
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    result = get_documents(collection_identified, {'identified': True}, (page-1)*ROWS_PER_PAGE)
    pagination = Pagination(page=page, per_page=ROWS_PER_PAGE, 
                                    total=result.count(), search=search, css_framework='bootstrap3', record_name='result')
    return render_template("identified.html",pagination=pagination, identified_animals=result, title="Animais Identificados")

def not_identified():
    collection_identified = 'identified_animals'
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    result = get_documents(collection_identified, {'identified': False}, (page-1)*ROWS_PER_PAGE)
    pagination = Pagination(page=page, per_page=ROWS_PER_PAGE, 
                                    total=result.count(), search=search, css_framework='bootstrap3', record_name='result')
    return render_template("notidentified.html",pagination=pagination, identified_animals=result, title="Animais não Identificados")

def label():
    filtro = {'active': True}
    collection_labels = 'labels'
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)

    action = request.args.get('action')
    if action:
        obj = {'active': False}
        id_doc = request.args.get('_id')
        filter = {'_id': ObjectId(id_doc)}
        up_document(collection_labels, filter, obj)

    form = LabelForm()
    
    if request.method == 'POST':
        if form.inserir_label.data:
            labels = form.labels.data.splitlines()
            animal = form.animal.data
            new_label = dict()
            new_label['labels'] = labels
            new_label['animal'] = animal
            new_label['active'] = True
            add_document(collection_labels, new_label)
            form.labels.data = ''
            form.animal.data = ''
    result = get_documents(collection_labels, filtro, (page-1)*ROWS_PER_PAGE)
    pagination = Pagination(page=page, per_page=ROWS_PER_PAGE, 
                                    total=result.count(), search=search, css_framework='bootstrap3', record_name='result')
    return render_template("label.html",pagination=pagination,form=form, labels=result, title="Labels")

def notification():
    collection_notifications = 'notifications'
    collection_monitored = 'monitored_animals'
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)

    action = request.args.get('action')
    if action:
        obj = {'read': True}
        id_doc = request.args.get('_id')
        filter = {'_id': ObjectId(id_doc)}
        up_document(collection_notifications, filter, obj)
    notifications = get_documents(collection_notifications, {'read': False}, (page-1)*ROWS_PER_PAGE)
    result = []
    for notification in notifications:
        monitored_animal = get_one_document(collection_monitored, {'_id': notification['animal_id']})
        notification['date'] = monitored_animal['capture_date']
        result.append(notification)
    pagination = Pagination(page=page, per_page=ROWS_PER_PAGE, 
                                    total=notifications.count(), search=search, css_framework='bootstrap3', record_name='result')
    return render_template("notification.html", pagination=pagination, notifications=result, title="Notificações")

def flag():
    filtro = {'active': True}
    collection_flags = 'flags'
    collection_labels = 'labels'
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    
    action = request.args.get('action')
    if action:
        obj = {'active': False}
        id_doc = request.args.get('_id')
        filter = {'_id': ObjectId(id_doc)}
        up_document(collection_flags, filter, obj)
   
    form = FlagForm()
    labels = get_all(collection_labels, filtro)
    form.animals.choices = [(label['_id'], label['animal']) for label in labels]
    
    if request.method == 'POST':
        if form.inserir_flag.data:
            obj = {'_id': form.animals.data}
            label = get_one_document(collection_labels, obj)
            new_flag = dict()
            new_flag['labels'] = label['labels']
            new_flag['animal'] = label['animal']
            new_flag['active'] = True
            add_document(collection_flags, new_flag)
            form.animals.data = ''
    result = get_documents(collection_flags,filtro, (page-1)*ROWS_PER_PAGE)
    
    pagination = Pagination(page=page, per_page=ROWS_PER_PAGE, 
                                    total=result.count(), search=search, css_framework='bootstrap3', record_name='result')
    return render_template("flag.html",pagination=pagination, form=form, flags=result, title="Flags")

def history():
    collection_notifications = 'notifications'
    collection_monitored = 'monitored_animals'
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    notifications = get_documents(collection_notifications, None, (page-1)*ROWS_PER_PAGE)
    result = []
    for notification in notifications:
        monitored_animal = get_one_document(collection_monitored, {'_id': notification['animal_id']})
        notification['date'] = monitored_animal['capture_date']
        result.append(notification)

    pagination = Pagination(page=page, per_page=ROWS_PER_PAGE, 
                                    total=notifications.count(), search=search, css_framework='bootstrap3', record_name='result')
    return render_template("history.html", pagination=pagination, notifications=result, title="Histórico de Notificações")

def animal():
    collection_monitored = 'monitored_animals'
    collection_identified = 'identified_animals'

    id_doc = request.args.get('_id')
    back = request.args.get('back')

    filtro = {'_id': id_doc}
    form = AnimalForm()

    if request.method == 'POST':
        if form.back.data:
            return redirect(url_for('frontend.'+back))
    monitored_animal = get_one_document(collection_monitored, filtro)
    identified_animal = get_one_document(collection_identified, filtro)
    return render_template("animal.html",form=form, identified_animal=identified_animal, monitored_animal=monitored_animal, title="Informações do Animal")

def add_document(collection: str, document: dict()):
    instance.db[collection].insert_one(document)

def get_documents(collection: str, filter: object, skip: int):
    if filter is None:
        return instance.db[collection].find().skip(skip).limit(ROWS_PER_PAGE)
    return instance.db[collection].find(filter).skip(skip).limit(ROWS_PER_PAGE)

def up_document(collection: str, filter: str, obj_up: object):
    return instance.db[collection].update_one(filter, {'$set': obj_up} )

def get_one_document(collection: str, filter: object):
    if filter is None:
        return instance.db[collection].find_one()
    return instance.db[collection].find_one(filter)

def get_all(collection: str, filter: object):
    if filter is None:
        return instance.db[collection].find()
    return instance.db[collection].find(filter)
