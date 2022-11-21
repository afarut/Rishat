from django import forms
  
DEMO_CHOICES =(
    ("1", "Naveen"),
    ("2", "Pranav"),
    ("3", "Isha"),
    ("4", "Saloni"),
)
class MultipleChoiceForm(forms.Form):
    order = forms.MultipleChoiceField(choices = DEMO_CHOICES)
    discount = forms.CharField(required=False)

    #def __init__(self, choices, *args, **kwargs):
    #    super(MultipleChoiceForm, self).__init__(*args, **kwargs)
    #    lst = tuple([(str(i), choices[i]) for i in range(len(choices))])