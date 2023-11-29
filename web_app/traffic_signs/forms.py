from django.forms import Form, FileField, TextInput


class VideoForm(Form):
    file = TextInput()
