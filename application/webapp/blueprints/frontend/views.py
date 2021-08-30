from flask import abort, render_template, request, redirect, session, url_for
from webapp.ext.database import instance
from .forms import FlagForm, LabelForm, SearchForm, AnimalForm, PreSearchForm, SearchDateForm
from flask_paginate import Pagination, get_page_parameter
from bson.objectid import ObjectId

import datetime
import re

ROWS_PER_PAGE = 5
filter_monitored = False
filter_date_monitored = False
filter_search_monitored = False
filter_classified = False
filter_identified = False
filter_notidentified = False
filter_notification = False
filter_date_notification = False
filter_search_notification = False


def index():
    return render_template("index.html")

def monitored():
    fields = [
        {'filter': 'id' , 'name': 'Módulo'},
        {'filter': 'capture_date_maior' , 'name': 'Data de Captura (>=)'},
        {'filter': 'capture_date_menor' , 'name': 'Data de Captura (<=)'}
    ]
    collection_monitored = 'monitored_animals'
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    
    form = PreSearchForm()
    form_date = SearchDateForm()
    form_string = SearchForm()
    
    form.filtro.choices = [(field['filter'], field['name']) for field in fields]
    form_date.filtro.choices = [(field['filter'], field['name']) for field in fields]
    form_string.filtro.choices = [(field['filter'], field['name']) for field in fields]
    global filter_monitored
    global filter_date_monitored
    global filter_search_monitored
    if request.method == 'POST':
        if form.search_pre.data:
            session['filter_key'] = form.filtro.data
            filter_monitored = True
        elif form_date.clear_date.data or form_string.clear.data:
            session['filter_key'] = ''
            session['filter_value'] = ''
            form.filtro.data = ''
            filter_monitored = False
            filter_date_monitored = False
            filter_search_monitored = False
        elif form_date.search_date.data:
            filter_search_monitored = True
            value = form_date.value.data
            if value is None:
                value = datetime.datetime.now()
            date_format = value.isoformat()
            session['filter_value'] = datetime.datetime.fromisoformat(date_format)
        elif form_string.search.data:
            filter_search_monitored = True
            session['filter_value'] = form_string.value.data
    filtro = None
    if filter_monitored:
        key_search = session['filter_key']
        if key_search == 'id':
            form_string.filtro.data = key_search
            form_string.filtro.render_kw = {'disabled': 'disabled'}
        else:
            filter_date_monitored = True
            form_date.filtro.data = key_search
            form_date.filtro.render_kw = {'disabled': 'disabled'}
    if filter_search_monitored:
        value_search = session['filter_value']
        key_search = session['filter_key']
        if key_search == 'id':
            form_string.filtro.data = key_search
            form_string.filtro.render_kw = {'disabled': 'disabled'}
            form_string.value.data = value_search
            form_string.value.render_kw = {'disabled': 'disabled'}
            form_string.search.render_kw = {'disabled': 'disabled'}
            filtro = {key_search : re.compile(value_search, re.IGNORECASE)}
        else:
            form_date.filtro.data = key_search
            form_date.filtro.render_kw = {'disabled': 'disabled'}
            form_date.value.data = value_search
            #form_date.value.render_kw = {'disabled': 'disabled'}
            #form_date.search_date.render_kw = {'disabled': 'disabled'}
            
            if value_search is None:
                value_search = datetime.datetime.now()
            if key_search == 'capture_date_maior':
                date_format = value_search.isoformat()
                d = datetime.datetime.fromisoformat(date_format)
                filtro = {'capture_date' : {'$gte': d}}
            else:
                date_format = value_search.isoformat()
                d = datetime.datetime.fromisoformat(date_format)
                filtro = {'capture_date' : {'$lte': d}}
                
    result = get_documents(collection_monitored, filtro , (page-1)*ROWS_PER_PAGE)
    pagination = Pagination(page=page, per_page=ROWS_PER_PAGE, 
                                    total=result.count(), search=search, css_framework='bootstrap3', record_name='result')
    return render_template("monitored.html",form=form,form_date=form_date, form_string=form_string, filter_monitored=filter_monitored,
                                            filter_date=filter_date_monitored, pagination=pagination, monitored_animals=result, 
                                            title="Capturas Realizadas")

def classified():
    fields = [
        {'filter': 'animal' , 'name': 'Animal'},
        {'filter': 'description' , 'name': 'Descrição da Label'},
    ]
    collection_identified = 'identified_animals'
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)

    form = SearchForm()
    form.filtro.choices = [(field['filter'], field['name']) for field in fields]
    global filter_classified
    if request.method == 'POST':
        if form.search.data:
            session['filter_key'] = form.filtro.data
            session['filter_value'] = form.value.data
            filter_classified = True
        elif form.clear.data:
            session['filter_key'] = ''
            session['filter_value'] = ''
            form.filtro.data = ''
            form.value.data = ''
            filter_classified = False
    filtro = {'classified': True}
    if filter_classified:
        key_search = session['filter_key']
        value_search = session['filter_value']
        list_search = []
        if key_search == 'description':
            documents = get_all(collection_identified, {'classified': True})
            for document in documents:
                for label in document['classified_labels']:
                    if  value_search.upper() in label[key_search].upper():
                        print('label[key_search].upper()')
                        list_search.append(document['_id'])
            filtro = {'_id': {'$in': list_search} }
        elif key_search == 'animal': 
            filtro = {session['filter_key']: re.compile(session['filter_value'], re.IGNORECASE), 'classified': True} 
        form.value.data = session['filter_value']
        form.filtro.render_kw = {'disabled': 'disabled'}
        form.value.render_kw = {'disabled': 'disabled'}
        form.search.render_kw = {'disabled': 'disabled'}
    result = get_documents(collection_identified, filtro, (page-1)*ROWS_PER_PAGE)
    pagination = Pagination(page=page, per_page=ROWS_PER_PAGE, 
                                    total=result.count(), search=search, css_framework='bootstrap3', record_name='result')
    return render_template("classified.html",form=form, pagination=pagination, classified_animals=result, title="Animais Classificados")

def identified():
    fields = [
        {'filter': 'description' , 'name': 'Descrição'},
    ]
    collection_identified = 'identified_animals'
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)

    form = SearchForm()
    form.filtro.choices = [(field['filter'], field['name']) for field in fields]
    global filter_identified
    if request.method == 'POST':
        if form.search.data:
            session['filter_key'] = form.filtro.data
            session['filter_value'] = form.value.data
            filter_identified = True
        elif form.clear.data:
            session['filter_key'] = ''
            session['filter_value'] = ''
            form.filtro.data = ''
            form.value.data = ''
            filter_identified = False
    filtro = {'identified': True}
    if filter_identified:
        key_search = session['filter_key']
        value_search = session['filter_value']
        list_search = []
        documents = get_all(collection_identified, {'identified': True})
        for document in documents:
            for label in document['labels']:
                if label[key_search].upper() == value_search.upper():
                    list_search.append(document['_id'])
        filtro = {'_id': {'$in': list_search} } 
        form.value.data = value_search
        form.value.render_kw = {'disabled': 'disabled'}
        form.search.render_kw = {'disabled': 'disabled'}
        form.filtro.render_kw = {'disabled': 'disabled'}

    result = get_documents(collection_identified, filtro, (page-1)*ROWS_PER_PAGE)
    pagination = Pagination(page=page, per_page=ROWS_PER_PAGE, 
                                    total=result.count(), search=search, css_framework='bootstrap3', record_name='result')
    return render_template("identified.html",form=form, pagination=pagination, identified_animals=result, title="Animais Identificados")

def not_identified():
    fields = [
        {'filter': 'description' , 'name': 'Descrição'},
    ]
    collection_identified = 'identified_animals'
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)

    form = SearchForm()
    form.filtro.choices = [(field['filter'], field['name']) for field in fields]
    global filter_notidentified
    
    if request.method == 'POST':
        if form.search.data:
            session['filter_key'] = form.filtro.data
            session['filter_value'] = form.value.data
            filter_notidentified = True
        elif form.clear.data:
            session['filter_key'] = ''
            session['filter_value'] = ''
            form.filtro.data = ''
            form.value.data = ''
            filter_notidentified = False
    filtro = {'identified': False}
    if filter_notidentified:
        key_search = session['filter_key']
        value_search = session['filter_value']
        list_search = []
        documents = get_all(collection_identified, {'identified': False})
        for document in documents:
            for label in document['labels']:
                if label[key_search].upper() == value_search.upper():
                    list_search.append(document['_id'])
        filtro = {'_id': {'$in': list_search} } 
        form.value.data = value_search
        form.value.render_kw = {'disabled': 'disabled'}
        form.search.render_kw = {'disabled': 'disabled'}
    result = get_documents(collection_identified, filtro, (page-1)*ROWS_PER_PAGE)
    pagination = Pagination(page=page, per_page=ROWS_PER_PAGE, 
                                    total=result.count(), search=search, css_framework='bootstrap3', record_name='result')
    return render_template("notidentified.html",form=form, pagination=pagination, identified_animals=result, title="Não Identificadas")

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
    return render_template("label.html",pagination=pagination,form=form, labels=result, title="Labels para Classificação")

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
    result = get_documents(collection_notifications, {'read': False}, (page-1)*ROWS_PER_PAGE)
    pagination = Pagination(page=page, per_page=ROWS_PER_PAGE, 
                                    total=result.count(), search=search, css_framework='bootstrap3', record_name='result')
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
    return render_template("flag.html",pagination=pagination, form=form, flags=result, title="Flags para Notificação")

def history():
    fields = [
        {'filter': 'description' , 'name': 'Labels Encontradas'},
        {'filter': 'labels' , 'name': 'Labels Pesquisadas'},
        {'filter': 'animal' , 'name': 'Animal'},
        {'filter': 'capture_date_maior' , 'name': 'Data de Captura (>=)'},
        {'filter': 'capture_date_menor' , 'name': 'Data de Captura (<=)'}
    ]
    collection_notifications = 'notifications'
    search = False
    q = request.args.get('q')
    if q:
        search = True

    form = PreSearchForm()
    form_date = SearchDateForm()
    form_string = SearchForm()

    form.filtro.choices = [(field['filter'], field['name']) for field in fields]
    form_date.filtro.choices = [(field['filter'], field['name']) for field in fields]
    form_string.filtro.choices = [(field['filter'], field['name']) for field in fields]
    
    global filter_notification
    global filter_date_notification
    global filter_search_notification
    if request.method == 'POST':
        if form.search_pre.data:
            session['filter_key'] = form.filtro.data
            filter_notification = True
        elif form_date.clear_date.data or form_string.clear.data:
            session['filter_key'] = ''
            session['filter_value'] = ''
            form.filtro.data = ''
            filter_notification = False
            filter_date_notification = False
            filter_search_notification = False
        elif form_date.search_date.data:
            filter_search_notification = True
            value = form_date.value.data
            if value is None:
                value = datetime.datetime.now()
            date_format = value.isoformat()
            session['filter_value'] = datetime.datetime.fromisoformat(date_format)
        elif form_string.search.data:
            filter_search_notification = True
            session['filter_value'] = form_string.value.data
    filtro = None
    if filter_notification:
        key_search = session['filter_key']
        if key_search == 'description' or key_search == 'labels' or key_search == 'animal':
            form_string.filtro.data = key_search
            form_string.filtro.render_kw = {'disabled': 'disabled'}
        else:
            filter_date_notification = True
            form_date.filtro.data = key_search
            form_date.filtro.render_kw = {'disabled': 'disabled'}
    if filter_search_notification:
        value_search = session['filter_value']
        key_search = session['filter_key']
        if key_search == 'description' or key_search == 'labels' or key_search == 'animal':
            form_string.filtro.data = key_search
            form_string.filtro.render_kw = {'disabled': 'disabled'}
            form_string.value.data = value_search
            #form_string.value.render_kw = {'disabled': 'disabled'}
            #form_string.search.render_kw = {'disabled': 'disabled'}
            if key_search == 'description':
                list_search = []
                documents = get_all(collection_notifications, None)
                for document in documents:
                    for label in document['identified_flags']:
                        if value_search.upper() in label[key_search].upper():
                            list_search.append(ObjectId(document['_id']))
                filtro = {'_id': {'$in': list_search} }
            elif key_search == 'labels':
                list_search = []
                documents = get_all(collection_notifications, None)
                for document in documents:
                    flag = document['flags']
                    for label in flag[key_search]:
                        if value_search.upper() in label.upper():
                            list_search.append(ObjectId(document['_id']))
                filtro = {'_id': {'$in': list_search} }
            elif key_search == 'animal':
                list_search = []
                documents = get_all(collection_notifications, None)
                for document in documents:
                    flag = document['flags']
                    animal = flag[key_search]
                    if value_search.upper() in animal.upper():
                        list_search.append(ObjectId(document['_id']))
                filtro = {'_id': {'$in': list_search} }
        else:
            form_date.filtro.data = key_search
            form_date.filtro.render_kw = {'disabled': 'disabled'}
            form_date.value.data = value_search
            #form_date.value.render_kw = {'disabled': 'disabled'}
            #form_date.search_date.render_kw = {'disabled': 'disabled'}
            if value_search is None:
                value_search = datetime.datetime.now()
                print(value_search)
            if key_search == 'capture_date_maior':
                date_format = value_search.isoformat()
                d = datetime.datetime.fromisoformat(date_format)
                filtro = {'date' : {'$gte': d}}
            else:
                date_format = value_search.isoformat()
                d = datetime.datetime.fromisoformat(date_format)
                filtro = {'date' : {'$lte': d}}

    page = request.args.get(get_page_parameter(), type=int, default=1)
    result = get_documents(collection_notifications, filtro, (page-1)*ROWS_PER_PAGE)
    pagination = Pagination(page=page, per_page=ROWS_PER_PAGE, 
                                    total=result.count(), search=search, css_framework='bootstrap3', record_name='result')
    return render_template("history.html", form=form,form_date=form_date, form_string=form_string, filter_monitored=filter_notification,
                                           filter_date=filter_date_notification, pagination=pagination, notifications=result, 
                                           title="Histórico de Notificações")

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
