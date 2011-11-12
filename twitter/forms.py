from django import forms

class TagForm(forms.Form):
    """
    A form for searching and filtering hashtags.
    """
    search_help = 'Comma seperated list of partial search words.'
    search = forms.CharField(max_length=50, help_text=search_help, required=False)
    ex_help = 'Comma seperated list of partial words to exclude.'
    exclude = forms.CharField(max_length=50, help_text=ex_help,required=False)