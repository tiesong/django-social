from django import forms

class EventForm(forms.Form):
    event_name = forms.CharField(label='Title', max_length=100)
    event_datetime_start = forms.DateTimeField()
    event_datetime_end = forms.DateTimeField()
    event_url = forms.URLField(label='Event URL', max_length=100)
    event_description = forms.CharField(label='Description', max_length=5000)

class ImageUploadForm(forms.Form):
    image = forms.ImageField()


