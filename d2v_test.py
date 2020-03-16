#Import all the dependencies
import nltk, re, pprint
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import os
import numpy as np
from tqdm import tqdm
nltk.download('punkt')
#find html files
html_ar = []
for root, dirs, filename in os.walk("htmlfiles"):
    for filename in [f for f in filename if f.endswith(".htm")]:
        print(os.path.join(root, filename))
        file = open(root+"/"+filename,encoding="utf8")
        s = file.read() 
        s = s.replace("\n", " ")
        s = s.replace("<", "")
        s = s.replace(">", "")
        html_ar.append(s)
#print("html:",html_ar)
tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in tqdm(enumerate(html_ar))]

        
print(tagged_data)
max_epochs = 100
vec_size = 200
alpha = 0.025

model = Doc2Vec(size=vec_size,
                alpha=alpha, 
                min_alpha=0.00025,
                min_count=1,
                dm =0,
                workers=4)
  
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

f = open("amazon1.htm", encoding="utf8")
s = f.read()
s = s.replace("\n", " ")
s = s.replace("<", "")
s = s.replace(">", "")
test_data = word_tokenize(s.lower())
a1 = model.infer_vector(test_data)
print("a1_infer", a1)
f = open("amazon2.htm", encoding="utf8")
s = f.read()
s = s.replace("\n", " ")
s = s.replace("<", "")
s = s.replace(">", "")
test_data = word_tokenize(s.lower())
a2 = model.infer_vector(test_data)
print("a2_infer", a2)
dist = np.linalg.norm(a1-a2)
print("distance am:",dist)

f = open("bol_i.htm", encoding="utf8")
s = f.read()
s = s.replace("\n", " ")
s = s.replace("<", "")
s = s.replace(">", "")
test_data = word_tokenize(s.lower())
b1 = model.infer_vector(test_data)
print(b1)
print("bol1_infer", b1)
f = open("bol_i.htm", encoding="utf8")
s = f.read()
s = s.replace("\n", " ")
s = s.replace("<", "")
s = s.replace(">", "")
test_data = word_tokenize(s.lower())
b2 = model.infer_vector(test_data)
print(b2)
print("bol2_infer", b2)
f = open("bol_a.htm", encoding="utf8")
s = f.read()
s = s.replace("\n", " ")
s = s.replace("<", "")
s = s.replace(">", "")
test_data = word_tokenize(s.lower())
b3 = model.infer_vector(test_data)
print("bol3_infer", b3)
dist = np.linalg.norm(b1-b2)
print("distance dicht:",dist)
dist = np.linalg.norm(b1-b3)
print("distance ver:",dist)