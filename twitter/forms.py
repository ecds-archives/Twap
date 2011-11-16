from django import forms

class TagForm(forms.Form):
    """
    A form for searching and filtering hashtags.
    """
    search_help = 'Comma seperated list of partial search words.'
    s_widget = forms.TextInput(attrs={'class': 'text'})
    search = forms.CharField(max_length=50, help_text=search_help, required=False, widget=s_widget)
    ex_help = 'Comma seperated list of partial words to exclude.'
    ex_widget = forms.TextInput(attrs={'class': 'text'})
    exclude = forms.CharField(max_length=50, help_text=ex_help,required=False,widget=ex_widget)

class UserSearchForm(forms.Form):
    """
    Simple search for twitter usernames.
    """
    search_help = 'Username (full or partial) to search for.'
    s_widget = forms.TextInput(attrs={'class': 'text'})
    search = forms.CharField(max_length=50, help_text=search_help, label='Twitter Username', widget=s_widget)