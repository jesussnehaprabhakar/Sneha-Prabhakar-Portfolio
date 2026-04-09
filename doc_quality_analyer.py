import spacy
nlp=spacy.load("en_core_web_sm")
with open ("input/draft1.txt","r") as file:
    text=file.read()
    print("Original text:\n",text)
text=text.lower()
print("\nLowercase text:\n",text)
temp_text=""
for x in text:
    if x.isalnum() or x.isspace():
        temp_text=temp_text+x
text=temp_text
print("\nLowercase text without Punctuation:\n",text) 