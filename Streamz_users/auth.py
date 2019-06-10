import web
import model
import json
import requests
import hashlib

urls = ('/login', 'Login',
        '/logout', 'Logout',
        '/register', 'Register',
	'/profile', 'Profile',
	'/updateprofile', 'UpdateProfile',
        '/getdob', 'GetDob',
        '/getcountry', 'GetCountry',
        '/getprofilepic', 'GetProfilePic',
        '/getcoverpic', 'GetCoverPic',
        '/getsubscription', 'GetSubscription',
        '/updatelike','UpdateLike',
        '/updatedislike','UpdateDislike',
        '/updatenonelike','UpdateNonelike',
        '/getlikestatus','GetLikeStatus',
        '/getfirstname','GetFirstname',
        '/subscribe','Subscribe',
        '/unsubscribe','Unsubscribe',
        '/getsubscribestatus','GetSubscribeStatus',
        '/comment','Comment',
        '/getcommentlist','GetCommentList',
        '/getlikestatuscount','GetLikeStatusCount',
        '/getsubscribestatuscount','GetSubscribeStatusCount',
        '/updatesubscribestatus','UpdateSubscribeStatus',
        '/updatechannellikestatuscount','UpdateChannelLikesStatusCount',
        '/getuserstats','GetUserStats',
        '/addhistory','AddHistory',
        '/gethistory','GetHistory',
        '/deletevideo','DeleteVideo',
        )

class DeleteVideo:
    
        def POST(self):
                data=web.data()
                id=json.loads(data)['id']
                s=model.delete_video(id)
                return s

class AddViews:
        def POST(self):
                data=web.data()
                un=json.loads(data)['username']
                vid=json.loads(data)['videoid']
                s=model.add_views(un,vid)
                return s

class GetHistory:
        def POST(self):
                data=web.data()
                un=json.loads(data)['username']
                s=model.get_history(un)
                return s

class AddHistory:
        def POST(self):
                data=web.data()
                un=json.loads(data)['username']
                vid=json.loads(data)['videoid']
                s=model.add_history(un,vid)
                return s

class GetUserStats:
        def POST(self):
                data=web.data()
                un=json.loads(data)['username']
                s=model.get_user_stats(un)
                return s

class UpdateChannelLikesStatusCount:
        def POST(self):
                data=web.data()
                upl=json.loads(data)['uploader']
                lkscnt=json.loads(data)['likescount']
                dlkscnt=json.loads(data)['dislikescount']
                s=model.update_channel_likescount_count(upl,lkscnt,dlkscnt)
                return s

class UpdateSubscribeStatus:
        def POST(self):
                data=web.data()
                upl=json.loads(data)['uploader']
                sbs=json.loads(data)['subscribers']
                s=model.update_subscribestatus(upl,sbs)
                return s

class GetSubscribeStatusCount:
        def POST(self):
                data=web.data()
                upl=json.loads(data)['uploader']
                s=model.get_subscribe_count(upl)
                return s

class Subscribe:
        def POST(self):
                data=web.data()
                un=json.loads(data)['username']
                upl=json.loads(data)['uploader']
                s=model.subscribe(un,upl)
                return s

class Unsubscribe:
        def POST(self):
                data=web.data()
                un=json.loads(data)['username']
                upl=json.loads(data)['uploader']
                s=model.unsubscribe(un,upl)
                return s

class GetLikeStatusCount:
        def POST(self):
                data=web.data()
                vid=json.loads(data)['videoid']
                s=model.get_likestatus_count(vid)
                return s


class GetCommentList:
        def POST(self):
                data=web.data()
                vid=json.loads(data)['videoid']
                s=model.get_comment(vid)
                return s

class Comment:
        def POST(self):
                data=web.data()
                vid=json.loads(data)['videoid']
                un=json.loads(data)['username']
                cmt=json.loads(data)['comment']
                s=model.comment(vid,un,cmt)
                return s

class GetFirstname:
        def POST(self):
                data=web.data()
                un=json.loads(data)['username']
                s=model.get_firstname(un)
                return s

class GetSubscription:
        def POST(self):
                data=web.data()
                un=json.loads(data)['username']
                s=model.get_subscription(un)
                return s

class GetSubscribeStatus:
        def POST(self):
                data=web.data()
                un=json.loads(data)['username']
                upl=json.loads(data)['uploader']
                s=model.get_subscribestatus(un,upl)
                return s



class GetLikeStatus:
        def POST(self):
                data=web.data()
                un=json.loads(data)['username']
                vid=json.loads(data)['videoid']
                s=model.get_likestatus(un,vid)
                return s


class UpdateLike:
        def POST(self):
                data=web.data()
                un=json.loads(data)['username']
                vid=json.loads(data)['videoid']
                s=model.update_like(un,vid)
                return s

class UpdateDislike:
        def POST(self):
                data=web.data()
                un=json.loads(data)['username']
                vid=json.loads(data)['videoid']
                s=model.update_dislike(un,vid)
                return s

class UpdateNonelike:
        def POST(self):
                data=web.data()
                un=json.loads(data)['username']
                vid=json.loads(data)['videoid']
                s=model.update_nonelike(un,vid)
                return s


class GetProfilePic:
    
        def POST(self):
                data=web.data()
                un=json.loads(data)['username']
                s=model.get_profilepic(un)
                return s

class GetCoverPic:
    
        def POST(self):
                data=web.data()
                un=json.loads(data)['username']
                s=model.get_coverpic(un)
                return s

class Register:
   
        def POST(self):
                data = web.data()
                fn=json.loads(data)['firstname']
                ln=json.loads(data)['lastname']
                ph=json.loads(data)['phone']
                eml=json.loads(data)['email']
                un=json.loads(data)['username']
                pwd=json.loads(data)['password']
                pwd1= hashlib.md5(pwd).hexdigest()
                dt=json.loads(data)['joined']
                p=model.new_user(fn,ln,ph,eml,un,pwd1,0,0,0,dt)
                return p
        

class Login:
    
        def POST(self):
                data=web.data()
                un=json.loads(data)['username']
                pwd=json.loads(data)['password']
                passhash = hashlib.md5(pwd).hexdigest()
                id=model.check_user(un,passhash)
                return id
	

class Profile:
    
        def POST(self):
                data=web.data()
                user=json.loads(data)['username']
                s=model.get_user(user)
                return s


class UpdateProfile:
    
        def POST(self):
                web.header('Access-Control-Allow-Origin','*')
                web.header('Access-Control-Allow-Credentials', 'true')
                data = web.input()
                profilepicname=data['profilepic_name']
                coverpicname=data['coverpic_name']
                fn=data['firstname']
                ln=data['lastname']
                abt=data['about']
                ph=data['phone']
                eml=data['email']
                un=data['username']
                db=data['dob']
                cntry=data['country']

                if profilepicname!="":
                        fout = open('static/profilepic' +'/'+ profilepicname,'w')
                        fout.write(data['profilepic_file']) 
                        fout.close() 
                if coverpicname!="":
                        fout = open('static/coverpic' +'/'+ coverpicname,'w')
                        fout.write(data['coverpic_file']) 
                        fout.close()
                s=model.update_user('static/profilepic/' + profilepicname,'static/coverpic/' + coverpicname,fn,ln,ph,eml,un,db,cntry,abt)

		return s

class GetDob:
    
        def POST(self):
                data=web.data()
                un=json.loads(data)['username']
                s=model.get_dob(un)
                return s

class GetCountry:
    
        def POST(self):
                data=web.data()
                un=json.loads(data)['username']
                s=model.get_country(un)
                return s

app = web.application(urls, globals())

if __name__ == '__main__':
        app.run()
