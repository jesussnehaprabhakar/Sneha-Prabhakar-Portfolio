import enchant
import nltk
import pandas as pd
import spacy
pd.set_option("display.max_rows",None) 
nlp=spacy.load("en_core_web_sm")
error=[]

# Read contents from file in local folder - spaCy
with open ("input/draft1.txt","r",encoding="utf-8") as file:
    text=file.read()
#print("Original text:\n",text)

# Convert content to Lowercase
text=text.lower()
#print("\nLowercase text:\n",text)

# Remove Punctuations and Numbers from content- spaCy
temp_text=""
for x in text:
    if x.isalpha() or x.isspace(): #alnum includes alphabets, numbers & combo of both(ex, KPI9)
        temp_text=temp_text+x
text=temp_text
#print("\nContent without Punctuation & Numbers:\n",text)

# Identify Lemmas- NLP spaCy
doc=nlp(text)
try:
    word=[] 
    lemmas=[] 
    for token in doc: 
        if token.text.isalnum():
            word.append(token.text) 
            lemmas.append(token.lemma_)
    #print("\nOriginal words and their lemmas:\n",list(zip(words,lemmas)))

    # Remove Stopwords from content- NLP NLTK
    filtered_words=[]
    filtered_lemmas=[]
    for item in doc:
        if not item.is_stop and item.text.isalnum(): #considers strings excluding stop words
            filtered_words.append(item.text)
            filtered_lemmas.append(item.lemma_)
    #print("\nFiltered content:\n"," ".join(filtered_words))

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
        table.append([lemma,frequency,unique_variants,dominant_variant])
    sort_lemma=sorted(table,key=lambda l:l[1],reverse=True)
    df=pd.DataFrame(sort_lemma,columns=["Lemma","Frequency","Unique Variants","Dominant Variant"])
    df_filtered=df[df["Frequency"]>1].reset_index(drop=True)
    df_filtered.index=df_filtered.index+1
    print(df_filtered)
    error.append(["Lemma","Success",""])
except Exception as e:
    error.append(["Lemma","Failed",str(e)])

#Identify frequently used Phrases
#Unigram
#print("\nUnigram")
#print("Number of filtered words:",len(filtered_words))
try:
    unigram_dict={}
    for unigram in filtered_words:
        if unigram not in unigram_dict:
            unigram_dict[unigram]=1
        else:
            unigram_dict[unigram]+=1
    sort_unigram=sorted(unigram_dict.items(),key=lambda u:u[1],reverse=True) 
    #key= needs a function reference, not a static number, so lambda used
    df_unigram=pd.DataFrame(sort_unigram,columns=["Repeated Words","Frequency"])
    df_ug_filtered=df_unigram[df_unigram["Frequency"]>1].reset_index(drop=True)
    df_ug_filtered.index=df_ug_filtered.index+1
    print(df_ug_filtered)
    error.append(["Unigram","Success",""])
except Exception as e:
    error.append(["Unigram","Failed",str(e)])

#Bigram
#print("\nBigram")
#print("Number of filtered words:",len(filtered_words))
#print("Number of possible pairs:",len(filtered_words)-1)
try:
    bigram=[] #create list of pairs
    for i in range(len(filtered_words)-1):
        pair=filtered_words[i]+" "+filtered_words[i+1]
        bigram.append(pair)
        unique_pairs=list(set(bigram))
    bigram_dict={}
    for pair in bigram:
        if pair not in bigram_dict:
            bigram_dict[pair]=1
        else:
            bigram_dict[pair]+=1
    sort_bigram=sorted(bigram_dict.items(),key=lambda b:b[1],reverse=True) 
    df_bigram=pd.DataFrame(sort_bigram,columns=["Repeated Phrases(2 words)","Frequency"])
    df_bg_filtered=df_bigram[df_bigram["Frequency"]>1].reset_index(drop=True)
    df_bg_filtered.index=df_bg_filtered.index+1
    print(df_bg_filtered)
    error.append(["Bigram","Success",""])
except Exception as e:
    error.append(["Bigram","Failed",str(e)])

#Trigram
#print("\nTrigram")
#print("Number of filtered words:",len(filtered_words))
#print("Number of possible triplets:",len(filtered_words)-2)
try:
    trigram=[] #create list of 3-words phrase
    for i in range(len(filtered_words)-4):
        triplet=filtered_words[i]+" "+filtered_words[i+1]+" "+filtered_words[i+2]
        trigram.append(triplet)
        unique_triplets=list(set(triplet))
    trigram_dict={}
    for triplet in trigram:
        if triplet not in trigram_dict:
            trigram_dict[triplet]=1
        else:
            trigram_dict[triplet]+=1
    sort_trigram=sorted(trigram_dict.items(),key=lambda t:t[1],reverse=True) 
    df_trigram=pd.DataFrame(sort_trigram,columns=["Repeated phrases(3 words)","Frequency"])
    df_tg_filtered=df_trigram[df_trigram["Frequency"]>1].reset_index(drop=True)
    df_tg_filtered.index=df_tg_filtered.index+1
    print(df_tg_filtered)
    error.append(["Trigram","Success",""])
except Exception as e:
    error.append(["Trigram","Failed",str(e)])

#Review words which are not in standard English format
d=enchant.Dict("en_US")
try:
    review_dict={}
    for word,lemma in zip(filtered_words,filtered_lemmas):
        if not d.check(lemma.lower()):
            review_dict[word.lower()]=review_dict.get(word.lower(),0)+1
    sort_review=sorted(review_dict.items(),key=lambda r:r[1],reverse=True)
    df_review=pd.DataFrame(sort_review,columns=["Non-Dictionary words","Frequency"])
    df_review.index=df_review.index+1
    print(df_review)
    error.append(["Review Required","Success",""])
except Exception as e:
    error.append(["Review Required","Failed",str(e)])

#Error Handling
df_error=pd.DataFrame(error,columns=["Module Name","Status","Error Message"])
df_error.index=df_error.index+1
print(df_error)

#Print output to Excel
with pd.ExcelWriter("document_analysis.xlsx") as writer:
    df_filtered.to_excel(writer,sheet_name="Lemma",index=False)
    df_ug_filtered.to_excel(writer,sheet_name="Unigram",index=False)
    df_bg_filtered.to_excel(writer,sheet_name="Bigram",index=False)
    df_tg_filtered.to_excel(writer,sheet_name="Trigram",index=False)
    df_review.to_excel(writer,sheet_name="Review Required",index=False)
    df_error.to_excel(writer,sheet_name="Error Handling",index=False)