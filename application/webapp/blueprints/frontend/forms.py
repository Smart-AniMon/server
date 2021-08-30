from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, SelectMultipleField, \
    IntegerField, BooleanField
from wtforms.validators import DataRequired
from bson.objectid import ObjectId
from datetime import date
from wtforms.fields.html5 import DateField

class FlagForm(FlaskForm):
    animals = SelectField('Animal', coerce=ObjectId, validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    #animal = StringField('Animal', description='Infome o nome do animal relacionado.', validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    inserir_flag = SubmitField('Inserir')

class LabelForm(FlaskForm):
    labels = TextAreaField('Labels', description='Obs.: Informe uma label por linha.', validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    animal = StringField('Animal', description='Infome o nome do animal relacionado.', validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    inserir_label = SubmitField('Inserir')

class PreSearchForm(FlaskForm):
    filtro = SelectField('Campo', coerce=str, validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    search_pre = SubmitField('Pesquisar')

class SearchForm(FlaskForm):
    filtro = SelectField('Campo', coerce=str, validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    value = StringField('Valor')
    search = SubmitField('Filtrar')
    clear = SubmitField('Limpar filtro')

class SearchDateForm(FlaskForm):
    filtro = SelectField('Campo', coerce=str, validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    value  = DateField('Indique a data',format='%Y-%m-%d',default=date.today)
    search_date = SubmitField('Filtrar')
    clear_date = SubmitField('Limpar filtro')

class AnimalForm(FlaskForm):
    back = SubmitField('Voltar')
