'''
Build a news headline recommonder system 
'''
## import dependencies 
import os 
import scipy 
import pandas as pd
import embeddinghub as eh
from sentence_transformers import SentenceTransformer

## load BERT model for embedding generation
model = SentenceTransformer('bert-base-nli-mean-tokens')

## load the data and create a list of headlines 
BASE_DIR = '/Users/gouravbais/Downloads/'
TEXT_DATA_DIR = os.path.join(BASE_DIR, 'million-news-dataset')
NEWS_FILE_NAME = "abcnews-date-text.csv"

## read the csv file
input_df = pd.read_csv(os.path.join(TEXT_DATA_DIR, NEWS_FILE_NAME))
input_df = input_df.head(20000)
print(input_df.head(20))

## create a list of headlines
sentences = input_df['headline_text'].values.tolist()

# Each sentence is encoded as a 1-D vector with 78 columns
sentence_embeddings = model.encode(sentences)
print('BERT embeddings length:', len(sentence_embeddings[0]))
print('BERT embedding vector:', sentence_embeddings[0])

## create a dictionary of embeddings 
embeddings = dict(zip(sentences, sentence_embeddings))

## create a python client for EmbeddingHub 
hub = eh.connect(eh.LocalConfig("data/"))

## create a space for storing the data
space = hub.create_space("demo", dims=768)

## write wmbeddings in the space 
space.multiset(embeddings)

#-------------------------------------##---------------------------------------------#

## get space where data is stored
space = hub.get_space("demo")

## retrieve data from the space
embed = space.multiget(embeddings.keys())

## map data with sentences
getEmbeddings = dict(zip(embeddings.keys(), embed))

## query to generate headings for 
query = "share market"

queries = [query]
## generate embeddings for the query 
query_embeddings = model.encode(queries)
## top number of matches you want as results
number_top_matches = 3 #@param {type: "number"}
print("Semantic Search Results")

for query, query_embedding in zip(queries, query_embeddings):
    ## calculate distance of query embeddings with all sentence embeddings
    distances = scipy.spatial.distance.cdist([query_embedding], sentence_embeddings, "cosine")[0]
    
    ## sort the results
    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])
    print(type(results))

    print("\n\n======================\n\n")
    print("Query:", query)
    print("\nTop 5 most similar sentences in corpus:")
    
    for idx, distance in results[0:number_top_matches]:
        print(sentences[idx].strip(), "(Cosine Score: %.4f)" % (1-distance))



