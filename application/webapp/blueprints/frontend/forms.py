from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, SelectMultipleField, DateField, \
    IntegerField, BooleanField
from wtforms.validators import DataRequired
from bson.objectid import ObjectId

class FlagForm(FlaskForm):
    animals = SelectField('Animal', coerce=ObjectId, validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    #animal = StringField('Animal', description='Infome o nome do animal relacionado.', validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    inserir_flag = SubmitField('Inserir')

class LabelForm(FlaskForm):
    labels = TextAreaField('Labels', description='Obs.: Informe uma label por linha.', validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    animal = StringField('Animal', description='Infome o nome do animal relacionado.', validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    inserir_label = SubmitField('Inserir')

