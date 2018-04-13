from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app.forms import  PostForm, SimpleForm
from app.models import Post
import json



def home_redirect_view(request):
    return redirect('simple_form')


def simple_form_view(request):
    form = SimpleForm()

    if request.method == 'POST': # it is created by sk
        form = SimpleForm(request.POST)
        if form.is_valid():
            #form.save()
            #title = form.cleaned_data['title']

            print(form.cleaned_data['title'])
            print(form.cleaned_data['description'])
            #print(form.cleaned_data['wiki'])

            #return HttpResponse('%s successfully  saved!' % title)
            return HttpResponse('successfully  saved!')
    else:
        context = {'form': form, 'title': 'Simple Form'}

    context = {'form': form, 'title': 'Simple Form'}
    return render(request, 'custom_form.html', context)

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


@csrf_exempt
def words_view(request):
    if request.method == 'POST':
        text = json.loads(request.body)['text']
        tries = fileparse(text)
        print(text)
        json_string = '{"first_name": "Guido", "last_name":"Rossum"}'
        return HttpResponse(json.dumps(tries.__dict__)) # Sending an success response
    else:
        return HttpResponse("Request method is not a GET")


#@login_required
def post_form_view(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            #title = form.cleaned_data['title']

            print(form.cleaned_data['title'])
            print(form.cleaned_data['description'])
            #print(form.cleaned_data['wiki'])

            #return HttpResponse('%s successfully  saved!' % title)
            return HttpResponse('successfully  saved!')
    else:
        context = {'form': form, 'title': 'Post Form'}
    return render(request, 'custom_form.html', context)


def test_markdownify(request):
    post = Post.objects.last()

    if post is not None:
        context = {'post': post}
    else:
        context = {
            'post': {
                'title': 'Fake Post',
                'description': """It **working**! :heart: [Python Learning](https://python.web.id)"""
            }
        }
    return render(request, 'test_markdownify.html', context)




def get_keywords(text):
    #!/usr/bin/env python
    df = {}
    with open('/home/san-d/foss/martor_demo/app/doc_freq_36lac.txt') as file:
        for line in file:
            tokens = line.split()
            df[tokens[0]] = int(tokens[1])
    print(len(df))
            

    import numpy as np
    idf = {}
    for word in df:
        idf[word] = np.log(3620000 /(1+ df[word])) #3620000 is the number of document processed




    tf = {}
    
    for word in text.split():
        word = word.lower()
        if word in df:
            if word in tf:
                tf[word] += 1
            else:
                tf[word] = 1



    tfidf = {}
    for word in tf:
        tfidf[word] = tf[word] * idf[word]


    import operator
    keywords = ""
    tfidf_sorted = sorted(tfidf.items(), key=operator.itemgetter(1))[::-1]
    for i in range(7):
        keywords += tfidf_sorted[i][0] + ' '

    return keywords



class Node:
    def __init__(self):
        self.next = {}  #Initialize an empty hash (python dictionary)

        self.word_marker = False 
        # There can be words, Hot and Hottest. When search is performed, usually state transition upto leaf node is peformed and characters are printed. 

        # Then in this case, only Hottest will be printed. Hot is intermediate state. Inorder to mark t as a state where word is to be print, a word_marker is used



    def add_item(self, string):
        ''' Method to add a string the Trie data structure'''
        
        if len(string) == 0:
            self.word_marker = True 
            return 
        
        key = string[0] #Extract first character

        string = string[1:] #Create a string by removing first character


        # If the key character exists in the hash, call next pointing node's add_item() with remaining string as argument

        if key in self.next:
            self.next[key].add_item(string)
        # Else create an empty node. Insert the key character to hash and point it to newly created node. Call add_item() in new node with remaining string.

        else:
            node = Node()
            self.next[key] = node
            node.add_item(string)


    def dfs(self, sofar=None):
        '''Perform Depth First Search Traversal'''
        
        # When hash of the current node is empty, that means it is a leaf node. 

        # Hence print sofar (sofar is a string containing the path as character sequences through which state transition occured)

        if self.next.keys() == []:
            print("Match:",sofar)
            return
            
        if self.word_marker == True:
            print("Match:",sofar)

        # Recursively call dfs for all the nodes pointed by keys in the hash

        for key in self.next.keys():
            self.next[key].dfs(sofar+key)

    def search(self, string, sofar=""):
        '''Perform auto completion search and print the autocomplete results'''
        # Make state transition based on the input characters. 

        # When the input characters becomes exhaused, perform dfs() so that the trie gets traversed upto leaves and print the state characters

        if len(string) > 0:
            key = string[0]
            string = string[1:]
            #if key in self.next:
            if key in self.next:
                sofar = sofar + key
                self.next[key].search(string,sofar)
                
            else:
                print("No match")
        else:
            if self.word_marker == True:
                print("Match:",sofar)

            for key in self.next.keys():
                self.next[key].dfs(sofar+key)


def fileparse(search_text):
    from googlesearch import search
    import requests
    from bs4 import BeautifulSoup
    import re
    regex = re.compile(r"\W")
    root = Node()
    text = []
    keywords = get_keywords(search_text)
    for url in search(keywords, stop=20):
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            for sent_array in [s.findAll(text=True) for s in soup.findAll('p')]:
                #sent_array is a list of sentances of a paragraph
                for sentance in [regex.sub(" ", sent).split() for sent in sent_array]:
                    text.extend(sentance)
                    #print(sentance)
                    try:
                        text.extend([sentance[i] + ' ' + sentance[i+1] for i in range(len(sentance)-1)])
                    except:
                        pass
        except:
            pass
    for word in text:
        if 1<len(word)< 50:
            root.add_item(word.lower())
            #print(word)
    return root
