import spacy
import nltk
nlp=spacy.load("en_core_web_sm")

# Read contents from file in local folder - spaCy
with open ("input/draft1.txt","r") as file:
    text=file.read()
print("Original text:\n",text)

# Convert content to Lowercase
text=text.lower()
print("\nLowercase text:\n",text)

# Remove Punctuations from content- spaCy
temp_text=""
for x in text:
    if x.isalnum() or x.isspace(): #alnum includes alphabets, numbers & combo of both(ex, KPI9)
        temp_text=temp_text+x
text=temp_text
print("\nLowercase text without Punctuation:\n",text)

# Identify Lemmas- NLP spaCy
doc=nlp(text)
words=[] 
lemmas=[] 
for token in doc: 
    if token.text.isalnum():
        words.append(token.text) 
        lemmas.append(token.lemma_)
print("\nOriginal words and their lemmas:\n",list(zip(words,lemmas)))

# Remove Stopwords from content- NLP NLTK
filtered_words=[]
filtered_lemmas=[]
for item in doc:
    if not item.is_stop and item.text.isalnum(): #considers strings excluding stop words
        filtered_words.append(item.text)
        filtered_lemmas.append(item.lemma_)
print("\nFiltered content:\n"," ".join(filtered_words))

#Measure Frequency of Filtered words- Pandas
lemma_dict={} #create an empty dictionary
for term, lemma in zip(filtered_words,filtered_lemmas):
    if lemma not in lemma_dict:
        lemma_dict[lemma]=[term]
    else:
        lemma_dict[lemma].append(term)
for lemma in lemma_dict:
    variants=lemma_dict[lemma]
    frequency=len(variants)
    unique_variants=list(set(variants))
    dominant_variant=max(set(variants),key=variants.count)
    print("Lemma:",lemma)
    print("Frequency:",frequency)
    print("Variants:",variants)
    print("Unique variants:",unique_variants)
    print("Frequently appearing variant:",dominant_variant)