from django import forms

class CfSpaceForm(forms.Form):
    space_index = forms.CharField(label='', max_length=100, \
    	widget= forms.TextInput(attrs={
    		'placeholder':'Enter space name/key/ID',
    		'type':'search',
    		'name':'search',
    		'class':'form_input'
    		}))

class BbProjectForm(forms.Form):
    project_key = forms.CharField(label='', max_length=100, \
    	widget= forms.TextInput(attrs={
    		'placeholder':'Enter project key',
    		'type':'search',
    		'name':'search',
    		'class':'form_input'
    		}))