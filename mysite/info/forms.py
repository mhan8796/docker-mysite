from django import forms

class CfSpaceForm(forms.Form):
    space_index = forms.CharField(label='', max_length=100, \
    	widget= forms.TextInput(attrs={
            'placeholder':'Search',
            'type':'text',
            'class':'form-control'
    		}))

class BbProjectForm(forms.Form):
    project_key = forms.CharField(label='', max_length=100, \
    	widget= forms.TextInput(attrs={
            'placeholder':'Search',
            'type':'text',
            'class':'form-control'
    		}))

class JrProjectForm(forms.Form):
    project_key = forms.CharField(label='', max_length=100, \
        widget= forms.TextInput(attrs={
            'placeholder':'Search',
            'type':'text',
            'class':'form-control'
            }))