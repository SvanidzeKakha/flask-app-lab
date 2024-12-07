from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, TextAreaField, SubmitField, BooleanField, DateTimeLocalField, SelectField
from wtforms.validators import DataRequired, Length
from datetime import datetime as dt

CATEGORIES = [('Technology', 'Technology'), ('Science', 'Science'), ('Lifestyle', 'Lifestyle')]

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()])
    is_active = BooleanField('Active Post')
    date_posted = DateTimeLocalField('Publication Date', format="%Y-%m-%dT%H:%M", default=dt.now())
    category = SelectField('Category', choices=CATEGORIES, validators=[DataRequired()])
    author_id = SelectField("Author", coerce=int)
    tags_id = SelectMultipleField("Tags", coerce=int)
    submit = SubmitField('Add Post')