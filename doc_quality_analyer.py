import spacy
import nltk
import pandas as pd
nlp=spacy.load("en_core_web_sm")

# Read contents from file in local folder - spaCy
with open ("input/draft1.txt","r") as file:
    text=file.read()
print("Original text:\n",text)

# Convert content to Lowercase
text=text.lower()
print("\nLowercase text:\n",text)

# Remove Punctuations and Numbers from content- spaCy
temp_text=""
for x in text:
    if x.isalpha() or x.isspace(): #alnum includes alphabets, numbers & combo of both(ex, KPI9)
        temp_text=temp_text+x
text=temp_text
print("\nContent without Punctuation & Numbers:\n",text)

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
table=[] #Display output as Table
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
    # print("Lemma:",lemma)
    # print("Frequency:",frequency)
    # print("Variants:",variants)
    # print("Unique variants:",unique_variants)
    # print("Frequently appearing variant:",dominant_variant)
    table.append([lemma,frequency,variants,unique_variants,dominant_variant])
df=pd.DataFrame(table,columns=["Lemma","Frequency","Variants","Unique Variants","Dominant Variant"])
print(df)

#Identify frequently used Phrases
#Unigram
print("\nUnigram\n")
unigram_dict={}
for unigram in filtered_words:
    if unigram not in unigram_dict:
        unigram_dict[unigram]=1
    else:
        unigram_dict[unigram]+=1
number=1
for unigram in unigram_dict:
    print(number,unigram,":",unigram_dict[unigram])
    number+=1

#Bigram
pairs=[] #create list of pairs
print("\nNumber of filtered words: ",len(filtered_words))
print("Number of possible pairs: ",len(filtered_words)-1)
for i in range(len(filtered_words)-1):
    pair=filtered_words[i]+" "+filtered_words[i+1]
    pairs.append(pair)
    unique_pairs=list(set(pairs))
bigram_dict={}
for pair in pairs:
    if pair not in bigram_dict:
        bigram_dict[pair]=1
    else:
        bigram_dict[pair]+=1
print("\nBigram\n")
number=1
for pair in bigram_dict:
    print(number,pair,":",bigram_dict[pair])
    number+=1