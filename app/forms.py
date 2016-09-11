from wtforms import Form, StringField, validators

class GameForm(Form):
    user_input = StringField("User Input", [validators.DataRequired()])