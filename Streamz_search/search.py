#import packages
import web
import model
import json

### Url mappings
#insertion,search,deletion

urls = (
	'/details','Details',
    '/search', 'Search',
    '/deletevideo','Delete',
    '/updatevideo','Update',
    '/updatelikestatus','UpdateLikestatus',
    '/gettrending','Trending',
    '/getcategoryvideo','Category',
    '/getrecommendation','Recommendation',
    
)
# sorting and filtering to be added
# This is the backend server.
#
#



# search by keyword
class Search:
    def GET(self):
        """no function"""

    def POST(self):
        
        info= web.data()
        ids = model.send_search(json.loads(info)['keyword'],json.loads(info)['user_age'],json.loads(info)['user_country']) 
        #print ids
        return ids


# delete by id
class Delete:


    def POST(self):
        
        index= web.data()
        id=json.loads(index)['id']
        res = model.delete(id)
        return res

#insert video details
class Details:
    def POST(self):
        
        data= web.data()
        ids=json.loads(data)['id']
        #channel=json.loads(data)['channel']
        uploader=json.loads(data)['uploader']
        category=json.loads(data)['category']
        title=json.loads(data)['video_name']
        description=json.loads(data)['description']
        tags=json.loads(data)['tags']
        countries=json.loads(data)['countries']
        age=json.loads(data)['age']
        age=int(age)
        likes=0
        dislikes=0
        subcount=0
        score=0
        details=json.dumps({'id':int(ids),'uploader':uploader,'category':category,'title':title,'description':description,'tags':tags,'countries':countries,'age':age,'likes':likes,'dislikes':dislikes,'subcount':subcount,'score':score})
        #print details
        res = model.send_details(details)
        return res
        
class Update:

    def POST(self):
        
        data= web.data()
        res = model.update_details(data)
        return res

class UpdateLikestatus:
    

    def POST(self):
        
        data= web.data()
        ids=json.loads(data)['videoid']
        likes=json.loads(data)['likes']
        dislikes=json.loads(data)['dislikes']
        score=(likes+dislikes)
        res = model.update_likes(ids,likes,dislikes,score) 
        return res  
        
class Trending:

    def POST(self):
        
        info= web.data()
        ids = model.trending(json.loads(info)['user_age'],json.loads(info)['user_country']) 
        #print ids
        return ids

class Category:

    def POST(self):
        
        info= web.data()
        ids = model.sort_category(json.loads(info)['category'],json.loads(info)['user_age'],json.loads(info)['user_country']) 
        #print ids
        return ids
		
class Recommendation:
    def POST(self):
        info= web.data()
        ids = model.recommendation(json.loads(info)['videoid'],json.loads(info)['user_age'],json.loads(info)['user_country']) 
        #print ids
        return ids

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
