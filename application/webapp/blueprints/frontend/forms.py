from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, SelectMultipleField, DateField, \
    IntegerField, BooleanField
from wtforms.validators import DataRequired

class FlagForm(FlaskForm):
    labels = TextAreaField('Labels a serem monitoradas', description='Obs.: Informe uma label por linha.', validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    animal = StringField('Animal', description='Infome o nome do animal relacionado.', validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    inserir_flag = SubmitField('Inserir')

