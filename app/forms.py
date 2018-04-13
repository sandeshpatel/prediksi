from django import forms

from martor.fields import MartorFormField
from app.models import Post, Simple  


class SimpleForm(forms.Form): # use forms.ModelForm instead forms.Form and erase all following entry  
    title = forms.CharField(widget=forms.TextInput())
    description = MartorFormField()
    #wiki = MartorFormField()

    class Meta(): # it is created by sk
    	model = Simple 
    	fields = '__all__'


class PostForm(forms.ModelForm):


    
    class Meta():
        model = Post
        fields = '__all__'
    