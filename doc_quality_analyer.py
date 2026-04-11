import spacy
import pandas as pd
nlp=spacy.load("en_core_web_sm")

# Read contents from file in local folder
with open ("input/draft1.txt","r") as file:
    text=file.read()
print("Original text:\n",text)

# Convert content to Lowercase
text=text.lower()
print("\nLowercase text:\n",text)

# Remove Punctuations from content
temp_text=""
for x in text:
    if x.isalnum() or x.isspace(): #alnum includes alphabets, numbers & combo of both(ex, KPI9)
        temp_text=temp_text+x
text=temp_text
print("\nLowercase text without Punctuation:\n",text)

# Identify Lemmas
doc=nlp(text)
words=[] 
lemmas=[] 
for token in doc: 
    if token.text.isalnum():
        words.append(token.text) 
        lemmas.append(token.lemma_)
print("\nOriginal words and their lemmas:\n",list(zip(words,lemmas)))