import requests
import json
import datetime
from datetime import date

def new_user(firstname,lastname,phone,email,username,password,date):
    params = {'firstname': firstname,'lastname':lastname,'phone':phone,'email':email,'username':username,'password':password,'joined':date} 
    p=requests.post('http://0.0.0.0:9090/register', data=json.dumps(params))
    return p.json()
    #return json.dumps(params)

def check_user(username,password):
    params = {'username': username,'password':password} 
    p=requests.post('http://0.0.0.0:9090/login', data=json.dumps(params))
    return p.json()

def get_profile(username):
    params = {'username':username} 
    p=requests.post('http://0.0.0.0:9090/profile', data=json.dumps(params))
    return p.json()

def get_dob(username):
    params = {'username':username} 
    p=requests.post('http://0.0.0.0:9090/getdob', data=json.dumps(params))
    return p.json()

def get_country(username):
    params = {'username':username} 
    p=requests.post('http://0.0.0.0:9090/getcountry', data=json.dumps(params))
    return p.json()

def get_profilepic(username):
    params = {'username':username} 
    p=requests.post('http://0.0.0.0:9090/getprofilepic', data=json.dumps(params))
    return p

def get_coverpic(username):
    params = {'username':username} 
    p=requests.post('http://0.0.0.0:9090/getcoverpic', data=json.dumps(params))
    return p
     
def update_profile(firstname,lastname,username,about,phone,email,country,dob,x,y):
    paramspic = {'profilepic_file': x.myprofilepic.file.read(),'profilepic_name':x.myprofilepic.filename,'coverpic_file': y.mycoverpic.file.read(),'coverpic_name':y.mycoverpic.filename,'firstname':firstname,'lastname':lastname,'username':username,'phone':phone,'email':email,'country':country,'dob':dob,'about':about}
    p = requests.post('http://0.0.0.0:9090/updateprofile', files=paramspic)
    return p
    #return json.dumps(params)



"""--------------------------------------Search---------------------------------"""


def send_search(search_text,age,country):
    params = {'keyword': search_text,'user_age':age,'user_country':country} 
    p=requests.post('http://0.0.0.0:7070/search', data=json.dumps(params))
    return p.json()
    r#eturn json.dumps(params)



"""--------------------------------------Comments---------------------------------"""

def send_comment(videoid,username,comment_text):
    params = {'videoid':videoid,'username':username,'comment':comment_text} 
    p=requests.post('http://0.0.0.0:9090/comment', data=json.dumps(params))
    return p.json()
    #return json.dumps(params)

def get_commentlist(videoid):
    params = {'videoid':videoid} 
    p=requests.post('http://0.0.0.0:9090/getcommentlist', data=json.dumps(params))
    return p.json()

"""--------------------------------------Video Upload-----------------------------------------"""

def delete_video(id):

    params = {'id': id}
    p=requests.post('http://0.0.0.0:7070/deletevideo', data=json.dumps(params))
    p=requests.post('http://0.0.0.0:9090/deletevideo', data=json.dumps(params))
    p=requests.post('http://0.0.0.0:5050/deletevideo', data=json.dumps(params))
    return p.json()

def get_uploads(username):
    params = {'username': username} 
    p=requests.post('http://0.0.0.0:5050/getuploads', data=json.dumps(params))
    return p.json()
    #return json.dumps(params)

def get_videodesc(id):
    params = {'vid': id} 
    p=requests.post('http://0.0.0.0:5050/getvideodesc', data=json.dumps(params))
    return p.json()
    #return json.dumps(params)


def upload_video(x,th,uploader):
    file1 = {'file': x.myfile.file.read(),'name':x.myfile.filename,'thumbnail_file': th.mythumbnail.file.read(),'thumbnail_name':th.mythumbnail.filename,'uploader':uploader}
    p = requests.post("http://0.0.0.0:5050/upload", files=file1)
    return p.json()


def upload_video_info(id,name,description,tags,countries,category,uploader,age,th,st):

    params = {'id':int(id),'video_name':name,'description':description,'tags':tags,'category':category,'countries':json.dumps(countries),'uploader':uploader,'age':int(age)} 
    p=requests.post('http://0.0.0.0:7070/details', data=json.dumps(params))

    paramsth = {'thumbnail_file': th.mythumbnail.file.read(),'thumbnail_name':th.mythumbnail.filename,'subtitles_file': st.mysubtitles.file.read(),'subtitles_name':st.mysubtitles.filename,'id':id,'video_name':name,'description':description,'tags':tags,'category':category,'countries':json.dumps(countries),'age':age}
    q = requests.post('http://0.0.0.0:5050/updatevideo', files=paramsth)
    return paramsth
    #return paramsth  

def update_video(id,name,description,tags,countries,category,uploader,age,th,st):

    params = {'id':int(id),'video_name':name,'description':description,'tags':tags,'category':category,'countries':json.dumps(countries),'uploader':uploader,'age':age} 
    p=requests.post('http://0.0.0.0:7070/updatevideo', data=json.dumps(params))

    paramsth = {'thumbnail_file': th.mythumbnail.file.read(),'thumbnail_name':th.mythumbnail.filename,'subtitles_file': st.mysubtitles.file.read(),'subtitles_name':st.mysubtitles.filename,'id':id,'video_name':name,'description':description,'tags':tags,'category':category,'countries':json.dumps(countries),'age':age}
    q = requests.post('http://0.0.0.0:5050/updatevideo', files=paramsth)
    return q

def get_video(id):
    params = {'vid': id} 
    p=requests.post('http://0.0.0.0:5050/getvideo', data=json.dumps(params))
    return p
    #return json.dumps(params)

def get_subtitle(id):
    params = {'vid': id} 
    p=requests.post('http://0.0.0.0:5050/getsubtitle', data=json.dumps(params))
    return p
    #return json.dumps(params)

def get_thumbnail(id):
    params = {'vid': id} 
    p=requests.post('http://0.0.0.0:5050/getthumbnail', data=json.dumps(params))
    return p

def get_videoname(id):
    params = {'vid': id} 
    p=requests.post('http://0.0.0.0:5050/getvideoname', data=json.dumps(params))
    return p.json()

def get_description(id):
    params = {'vid': id} 
    p=requests.post('http://0.0.0.0:5050/getdescription', data=json.dumps(params))
    return p.json()

def get_uploader(id):
    params = {'vid': id} 
    p=requests.post('http://0.0.0.0:5050/getuploader', data=json.dumps(params))
    return p.json()

def get_views(id):
    params = {'vid': id} 
    p=requests.post('http://0.0.0.0:5050/getviews', data=json.dumps(params))
    return p.json()

def calculate_Age(db):
    db=datetime.datetime.strptime(db, '%Y-%m-%d').date()
    today = date.today()
    age=today.year - db.year - ((today.month, today.day) < (db.month, db.day))
    return age

"""--------------------------------------Video Upload-----------------------------------------"""
def update_like(username,videoid):
    params = {'username': username,'videoid':videoid} 
    p=requests.post('http://0.0.0.0:9090/updatelike', data=json.dumps(params))
    return p.json()
    #return params

def update_dislike(username,videoid):
    params = {'username': username,'videoid':videoid} 
    p=requests.post('http://0.0.0.0:9090/updatedislike', data=json.dumps(params))
    return p.json()
    #return params

def update_nonelike(username,videoid):
    params = {'username': username,'videoid':videoid} 
    p=requests.post('http://0.0.0.0:9090/updatenonelike', data=json.dumps(params))
    return p.json()
    #return params

def get_likestatus(username,videoid):
    params = {'username': username,'videoid':videoid}
    p=requests.post('http://0.0.0.0:9090/getlikestatus', data=json.dumps(params))
    return p.json()
    #return params

def get_likestatus_count(videoid):
    params = {'videoid':videoid}
    p=requests.post('http://0.0.0.0:9090/getlikestatuscount', data=json.dumps(params))
    return p.json()
    #return params

def get_subscribestatus_count(uploader):
    params = {'uploader':uploader}
    p=requests.post('http://0.0.0.0:9090/getsubscribestatuscount', data=json.dumps(params))
    return p.json()
    #return params


def subscribe(username,uploader):
    params = {'username': username,'uploader':uploader}
    p=requests.post('http://0.0.0.0:9090/subscribe', data=json.dumps(params))
    return p.json()
    #return params

def unsubscribe(username,uploader):
    params = {'username': username,'uploader':uploader}
    p=requests.post('http://0.0.0.0:9090/unsubscribe', data=json.dumps(params))
    return p.json()
    #return params

def get_subscribestatus(username,uploader):
    params = {'username': username,'uploader':uploader}
    p=requests.post('http://0.0.0.0:9090/getsubscribestatus', data=json.dumps(params))
    return p.json()
    #return params

def get_subscription(username):
    params = {'username':username} 
    p=requests.post('http://0.0.0.0:9090/getsubscription', data=json.dumps(params))
    return p.json()

def get_firstname(username):
    params = {'username':username} 
    p=requests.post('http://0.0.0.0:9090/getfirstname', data=json.dumps(params))
    return p.json()

"""--------------------------------------------------------------------------------------------------------"""
def update_likestatus(videoid,likes,dislikes):
    params = {'videoid':videoid,'likes':likes,'dislikes':dislikes} 
    q=requests.post('http://0.0.0.0:7070/updatelikestatus', data=json.dumps(params))
    p=requests.post('http://0.0.0.0:5050/updatelikestatus', data=json.dumps(params))
    return q

    return p.json()

def update_subscribestatus(uploader,subscribers):
    params = {'uploader':uploader,'subscribers':subscribers}
    q=requests.post('http://0.0.0.0:7070/updatesubscribestatus', data=json.dumps(params))
    p=requests.post('http://0.0.0.0:9090/updatesubscribestatus', data=json.dumps(params))
    return p.json()

def update_channel_likes_count(uploader):
    params = {'uploader':uploader}
    p=requests.post('http://0.0.0.0:5050/getchannellikescount', data=json.dumps(params))
    p=p.json()
    q=requests.post('http://0.0.0.0:9090/updatechannellikestatuscount', data=json.dumps(p))
    return q

def get_user_stats(username):
    params = {'username':username} 
    p=requests.post('http://0.0.0.0:9090/getuserstats', data=json.dumps(params))
    return p.json()

def add_history(username,videoid):
    params = {'username':username,'videoid':videoid} 
    p=requests.post('http://0.0.0.0:9090/addhistory', data=json.dumps(params))
    return p.json()

def get_history(username):
    params = {'username':username}
    p=requests.post('http://0.0.0.0:9090/gethistory', data=json.dumps(params))
    return p.json()

def get_trending(age,country):
    params={'user_age':age,'user_country':country}
    p=requests.post('http://0.0.0.0:7070/gettrending', data=json.dumps(params))
    return p.json()

def get_category_videoids(category,age,country):
    params = {'category': category,'user_age':age,'user_country':country}
    p=requests.post('http://0.0.0.0:7070/getcategoryvideo', data=json.dumps(params))
    return p.json()

def get_recommendation(videoid,age,country):
    params = {'videoid':videoid,'user_age':age,'user_country':country} 
    p=requests.post('http://0.0.0.0:7070/getrecommendation', data=json.dumps(params))
    return p.json()
    #return json.dumps(params)

def get_agerestriction(videoid):
    params = {'videoid':videoid}
    p=requests.post('http://0.0.0.0:5050/getagerestriction', data=json.dumps(params))
    return p.json()

def get_countryrestriction(videoid):
    params = {'videoid':videoid}
    p=requests.post('http://0.0.0.0:5050/getcountryrestriction', data=json.dumps(params))
    return p.json()

def update_views(videoid):
    params = {'videoid':videoid}
    p=requests.post('http://0.0.0.0:5050/updateviews', data=json.dumps(params))
    return p.json()
