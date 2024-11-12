from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired, Length

CATEGORIES = [('Technology', 'Technology'), ('Science', 'Science'), ('Lifestyle', 'Lifestyle')]

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()])
    is_active = BooleanField('Active Post')
    publish_date = DateField('Publication Date', format='%Y-%m-%d', validators=[DataRequired()])
    category = SelectField('Category', choices=CATEGORIES, validators=[DataRequired()])
    submit = SubmitField('Add Post')
