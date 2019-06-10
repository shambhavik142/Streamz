#import elasticsearch
from elasticsearch import Elasticsearch 

# Connect to the elastic cluster
es=Elasticsearch([{'host':'localhost','port':9200}])
print es

#dummy data
#12 entries made
   

# create index called streams1
# added analysers for stemming and tokenizing
# remove stop words
res = es.indices.create(index ='streamz', body = {
   "settings": {
    "analysis": {
      "filter": {
        "english_stop": {
          "type":       "stop",
          "stopwords":  "_english_"
        },
        "light_english_stemmer": {
          "type":       "stemmer",
          "language":   "light_english" 
        },
        "english_possessive_stemmer": {
          "type":       "stemmer",
          "language":   "possessive_english"
        }
      },
      "analyzer": {
        "english": {
          "tokenizer":  "standard",
          "filter": [
            "english_possessive_stemmer",
            "lowercase",
            "english_stop",
            "light_english_stemmer", 
            "asciifolding" ,
          ]
        }
      }
    }
  }
})


