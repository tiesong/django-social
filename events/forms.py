from django import forms

class EventForm(forms.Form):
    event_name = forms.CharField(label='Event Name', max_length=100)
    event_time = forms.CharField(max_length=100)
    event_date = forms.CharField(max_length=100)
    event_url = forms.CharField(label='Event URL', max_length=100)


