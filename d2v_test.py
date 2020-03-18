#Import all the dependencies
import nltk, re, pprint
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import os
import numpy as np
from tqdm import tqdm
from scipy import spatial
import spacy
from spacy.tokens import Token
Token.set_extension('tag', default=False)
nltk.download('punkt')
#find html files
html_ar = []
def create_custom_tokenizer(nlp):
    from spacy import util
    from spacy.tokenizer import Tokenizer
    from spacy.lang.tokenizer_exceptions import TOKEN_MATCH
    prefixes =  nlp.Defaults.prefixes + ('^<i>',)
    suffixes =  nlp.Defaults.suffixes + ('</i>$',)
    # remove the tag symbols from prefixes and suffixes
    prefixes = list(prefixes)
    prefixes.remove('<')
    prefixes = tuple(prefixes)
    suffixes = list(suffixes)
    suffixes.remove('>')
    suffixes = tuple(suffixes)
    infixes = nlp.Defaults.infixes
    rules = nlp.Defaults.tokenizer_exceptions
    token_match = TOKEN_MATCH
    prefix_search = (util.compile_prefix_regex(prefixes).search)
    suffix_search = (util.compile_suffix_regex(suffixes).search)
    infix_finditer = (util.compile_infix_regex(infixes).finditer)
    return Tokenizer(nlp.vocab, rules=rules,
                     prefix_search=prefix_search,
                     suffix_search=suffix_search,
                     infix_finditer=infix_finditer,
                     token_match=token_match)
for root, dirs, filename in os.walk("htmlfiles"):
    for filename in [f for f in filename if f.endswith(".htm")]:
        print(os.path.join(root, filename))
        file = open(root+"/"+filename,encoding="utf8")
        s = file.read() 
        s = s.replace("\n", " ")
        s = s.replace("<", "")
        s = s.replace(">", "")
        s = s.replace('"',"")
        s = s.replace("'","")
        s = s.replace("[","")
        s = s.replace("]","")
        # s = s.replace("{","")
        # s = s.replace("}","")
        html_ar.append(s)

nlp = spacy.load('en_core_web_sm')
nlp.max_length = 3000000
tokenizer = create_custom_tokenizer(nlp)
nlp.tokenizer = tokenizer
#print("html:",html_ar)
tagged_data = [TaggedDocument(words=nlp(_d.lower()), tags=[str(i)]) for i, _d in tqdm(enumerate(html_ar))]

        
#print(tagged_data)
max_epochs = 20
vec_size = 20
alpha = 0.03
batch_size = 20
model = Doc2Vec(size=vec_size,
                alpha=alpha, 
                min_alpha=0.00025,
                min_count=10,
                dm =0,
                workers=8)
  
model.build_vocab(tagged_data)
#uncomment for training again
for epoch in range(max_epochs):
    print('iteration {0}'.format(epoch))
    model.train(tagged_data,
                total_examples=model.corpus_count,
                epochs=model.iter)
    # decrease the learning rate
    model.alpha -= 0.0002
    # fix the learning rate, no decay
    model.min_alpha = model.alpha

model.save("d2v.model")
print("Model Saved")
model = Doc2Vec.load("d2v.model")

#Amazon
f = open("amazon_testfiles/am_n_login.htm", encoding="utf8")
s = f.read()
s = s.replace("\n", " ")
s = s.replace("<", "")
s = s.replace(">", "")
s = s.replace("[","")
s = s.replace("]","")
test_data = word_tokenize(s.lower())
a1 = model.infer_vector(test_data)
print("a1_infer", a1)
f = open("amazon_testfiles/am_login.htm", encoding="utf8")
s = f.read()
s = s.replace("\n", " ")
s = s.replace("<", "")
s = s.replace(">", "")
s = s.replace("[","")
s = s.replace("]","")
test_data = word_tokenize(s.lower())
a2 = model.infer_vector(test_data)
print("a2_infer", a2)
f = open("amazon_testfiles/am_anders.htm", encoding="utf8")
s = f.read()
s = s.replace("\n", " ")
s = s.replace("<", "")
s = s.replace(">", "")
s = s.replace("[","")
s = s.replace("]","")
test_data = word_tokenize(s.lower())
a3 = model.infer_vector(test_data)
print("a3_infer", a3)
# dist = np.linalg.norm(a1-a2)
# print("distance am:",dist)
sim = spatial.distance.cosine(a1, a2)
print("distance dicht (cosine):",sim)
sim = spatial.distance.cosine(a1, a3)
print("distance ver (cosine):",sim)

#Bol
f = open("bol_testfiles/bol_ingelogd.htm", encoding="utf8")
s = f.read()
s = s.replace("\n", " ")
s = s.replace("<", "")
s = s.replace(">", "")
s = s.replace("[","")
s = s.replace("]","")
test_data = word_tokenize(s.lower())
b1 = model.infer_vector(test_data)
print("bol1_infer", b1)
f = open("bol_testfiles/bol_n_ingelogd.htm", encoding="utf8")
s = f.read()
s = s.replace("\n", " ")
s = s.replace("<", "")
s = s.replace(">", "")
s = s.replace("[","")
s = s.replace("]","")
test_data = word_tokenize(s.lower())
b2 = model.infer_vector(test_data)
print("bol2_infer", b2)
f = open("bol_testfiles/bol_anders.htm", encoding="utf8")
s = f.read()
s = s.replace("\n", " ")
s = s.replace("<", "")
s = s.replace(">", "")
s = s.replace("[","")
s = s.replace("]","")
test_data = word_tokenize(s.lower())
b3 = model.infer_vector(test_data)
print("bol3_infer", b3)
# dist = np.linalg.norm(b1-b2)
# print("distance dicht:",dist)
# dist = np.linalg.norm(b1-b3)
# print("distance ver:",dist)
sim = spatial.distance.cosine(b1, b2)
print("distance dicht (cosine):",sim)
sim = spatial.distance.cosine(b1, b3)
print("distance ver (cosine):",sim)

#Youtube
f = open("yt_testfiles/yt_n_login.htm", encoding="utf8")
s = f.read()
s = s.replace("\n", " ")
s = s.replace("<", "")
s = s.replace(">", "")
s = s.replace("[","")
s = s.replace("]","")
test_data = word_tokenize(s.lower())
yt1 = model.infer_vector(test_data)
print("yt1_infer",yt1)
f = open("yt_testfiles/yt_login.htm", encoding="utf8")
s = f.read()
s = s.replace("\n", " ")
s = s.replace("<", "")
s = s.replace(">", "")
s = s.replace("[","")
s = s.replace("]","")
test_data = word_tokenize(s.lower())
yt2 = model.infer_vector(test_data)
print("yt2_infer", yt2)
f = open("yt_testfiles/yt_anders.htm", encoding="utf8")
s = f.read()
s = s.replace("\n", " ")
s = s.replace("<", "")
s = s.replace(">", "")
s = s.replace("[","")
s = s.replace("]","")
test_data = word_tokenize(s.lower())
yt3 = model.infer_vector(test_data)
print("yt3_infer", yt3)
# dist = np.linalg.norm(a1-a2)
# print("distance am:",dist)
sim = spatial.distance.cosine(yt1, yt2)
print("distance dicht (cosine):",sim)
sim = spatial.distance.cosine(yt1, yt3)
print("distance ver (cosine):",sim)