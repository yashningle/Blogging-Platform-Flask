
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):

    title = StringField(
        "Post Title",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    content = TextAreaField(
        "Post Content",
        validators=[
            DataRequired(),
            Length(min=10)
        ]
    )

    category_id = SelectField(
        "Category",
        coerce=int,
        validators=[DataRequired()]
    )

    submit = SubmitField("Publish Post")
