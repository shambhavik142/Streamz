#import libraries
import web
import json
import requests

# Import Elasticsearch package 
from elasticsearch import Elasticsearch 


# function to upload details to server
#details consists of id,channel,uploader,category,title,description and tags

def send_details(details):
  ids=json.loads(details)['id']
  # Connect to the elastic cluster
  es=Elasticsearch([{'host':'localhost','port':9200}])
  res = es.index(index='streamz',doc_type='video',body=details,id=ids)  #index_name=streams1, doc_type=videos
  return res


# function to search by keywords
#search based on category,channel,uploader,title,tags
def send_search(keyword,age,country):
  txt=str(keyword)
  country=str(country)
  age=int(age)

  videos=[]
  es=Elasticsearch([{'host':'localhost','port':9200}])
  res= es.search(index='streamz',body={"query": {
    
    "bool": {
                    "must":[

                    
                    
                    { "range": {
                        "age": {
                "lt": age
            }
        }
        },
        {"bool":
        {"must_not":[
        {"match": {"countries":country}}]}},
    
                    {
                    "bool":

                    {
                    "should" : [
                    { "match" : {"category" : txt} },
                    { "match" : {"description" : txt} },
                    {"match":{ "uploader" : txt }},
                    {"match": {"tags": txt}},
                    {"match": {"title":{"query":txt,"analyzer": "english"}}},
                    ]

                    }
                    }
                    ]
                    }
                    }
                    })
  for hit in res['hits']['hits']:
    videos.append(hit['_source']['id'])
  ids = {'id': videos}
  return json.dumps(ids)


  
 # function to delete from server 
def delete(index):
  #print index
  es=Elasticsearch([{'host':'localhost','port':9200}])
  res = es.delete(index='streamz', doc_type='video', id=index)
  return res	
    
def update_details(details):
  ids=json.loads(details)['id']
  uploader=json.loads(details)['uploader']
  category=json.loads(details)['category']
  title=json.loads(details)['video_name']
  description=json.loads(details)['description']
  tags=json.loads(details)['tags']
  countries=json.loads(details)['countries']
  age=json.loads(details)['age']
  #Connect to the elastic cluster
  es=Elasticsearch([{'host':'localhost','port':9200}])
  body={"doc":{'id':int(ids),'uploader':uploader,'category':category,'title':title,'description':description,'tags':tags,'countries':countries,'age':age}}
  res=es.update(index='streamz',doc_type='video',id=ids,body=body)
  return res

def update_likes(ids,likes,dislikes,score):

  es=Elasticsearch([{'host':'localhost','port':9200}])
  res=es.update(index='streamz',doc_type='video',id=ids,body={"doc": {'likes':likes,'dislikes':dislikes,'score':score}})
  params={'status':"Updated"}
  return json.dumps(params)



def trending(age,country):
  age=int(age)
  country=str(country)
  videos=[]
  es=Elasticsearch([{'host':'localhost','port':9200}])
  res= es.search(index='streamz',body={

  "query": {
    
    "bool": {
                 "must":[
                    
                    { "range": {
                        "age": {
                "lt": age
            }
        }
        }
        ],
        "must_not":[
        {"match": {"countries":country}}]
        }
        },

        "sort" : [
      {"score" : {"order" : "desc", "mode" : "avg"}},]
                    
        }
        )


  for hit in res['hits']['hits']:
    videos.append(hit['_source']['id'])
  ids = {'trend_video': videos}
  return json.dumps(ids)


def sort_category(category,age,country):
  category=str(category) 
  videos=[]
  es=Elasticsearch([{'host':'localhost','port':9200}])
  res= es.search(index='streamz',body={

   "query": {
    
    "bool": {
                    "must":[
                    { "range": {
                        "age": {
                "lt": age
            }
        }
        },
        {"bool":
        {"must_not":[
        {"match": {"countries":country}}]}},
    
                    {
                    "bool":

                    {
                    "must" : 
                    
                    { "match" : {"category" : category} },
            
                    

                    }
                    }
                    ]
                    }
                    }
                    }
                   
                  
                    )
  for hit in res['hits']['hits']:
    videos.append(hit['_source']['id'])
  ids = {'id': videos}
  return json.dumps(ids)

def recommendation(ids,age,country):

  es=Elasticsearch([{'host':'localhost','port':9200}])
  res = es.get(index='streamz',doc_type='video',id=ids)
  category=res['_source']['category']
  uploader=res['_source']['uploader']
  recom=[]

  res1= es.search(index='streamz',body={

  "query": {
    
    "bool": {
                    "must":[

                    
                    
                    { "range": {
                        "age": {
                "lt": age
            }
        }
        },
        {"bool":
        {"must_not":[
        {"match": {"countries":country}}]}},
    
                    {
                    "bool":

                    {
                    "should" : [
                    { "match" : {"category" : category} },
                    {"match":{ "uploader" : uploader }},
                    
                    ]

                    }
                    }
                    ]
                    }
                    }
                    }
                   
                  
                    )
  for hit in res1['hits']['hits']:
    recom.append(hit['_source']['id'])                    
  ids = {'recom_id':recom}
  print ids
  return json.dumps(ids)