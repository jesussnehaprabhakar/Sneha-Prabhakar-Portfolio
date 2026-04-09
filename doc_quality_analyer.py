import spacy
nlp=spacy.load("en_core_web_sm")
with open ("input/draft1.txt","r") as file:
    text=file.read()
    print("Original text:\n",text)
   