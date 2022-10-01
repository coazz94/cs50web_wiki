from django import forms



class Search_Field(forms.Form):
    search_label = forms.CharField(label="" , widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))


class NewPageForm(forms.Form):
    pagename = forms.CharField(label="", required = True, 
    widget= forms.Textarea
    (attrs={'placeholder':'Enter Title','value':'TEst','class':'col-lg-4','style':'margin-top:1rem;height:2rem'}))


    content = forms.CharField(label="",required= True,
    widget= forms.Textarea
    (attrs={'placeholder':'Enter markdown content','class':'col-lg-5','style':'top:1rem;height:40%'}))


class EditPage(forms.Form):
    content = forms.CharField(label="",required= True,
    widget= forms.Textarea
    (attrs={'placeholder':'Enter markdown content','class':'col-lg-5','style':'top:1rem;height:40%'}))

