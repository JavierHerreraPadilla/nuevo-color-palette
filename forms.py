from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.fields import SubmitField, FileField, IntegerField


class uploadForm(FlaskForm):
    file = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png','jpeg'], 'Images only!')])
    colors = IntegerField('Number of colors', default=3)
    submit = SubmitField('Upload')