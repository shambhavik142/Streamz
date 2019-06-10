import web
import requests
import model
from web import form
import json
import datetime
from datetime import date
import ast

urls = (
	'/', 'Index',
	'/register', 'Register',
	'/home', 'Homepage',
	'/play/(\d+)','Play',
	'/uploadvideo','Uploadvideo',
	'/uploadvideoinfo/(\d+)','UploadVideoInfo',
	'/uploadvideoinfo','UploadVideoInfo',
	'/editvideo/(\d+)','EditVideo',
	'/deletevideo/(\d+)','DeleteVideo',
	'/comment','Comment',
	'/logout','Logout',
	'/search','Search',
	'/profile','Profile',
	'/updateprofile','UpdateProfile',
	'/myprofile', 'MyProfile',
	'/uploads', 'Uploads',
	'/statistics', 'Statistics',
	'/videos/(\d+)','Videos',
	'/subtitles/(\d+)','Subtitles',
	'/thumbnails/(\d+)','Thumbnails', 
	'/profilepic/(\d+)','ProfilePic',
	'/coverpic/(\d+)','CoverPic',
	'/like','Like',
	'/dislike','Dislike',
	'/nonelike','Nonelike',
	'/subscribe','Subscribe',
	'/unsubscribe','Unsubscribe',
	'/demo/(\d+)','Demo',
	'/updatevideo','UpdateVideo',
	'/subscription','Subscription',
	'/profile/(.+)','Profile',
	'/profileuploads/(.+)','ProfileUploads',
	'/history','History',
	'/profilepic/(.+)','ProfilePic',
	'/coverpic/(.+)','CoverPic',
	'/categories/(.+)','Categories',
	
)


### Templates
render = web.template.render('templates', base='base')

app = web.application(urls, globals())

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'user':'username'})
    web.config._session = session
else:
    session = web.config._session

class Categories:

	def GET(self,category):
			if session.user=='username':
				raise web.seeother('/')
			s=model.get_category_videoids(category,model.calculate_Age(model.get_dob(session.user)['dob']),model.get_country(session.user)['country'])
			t=s['id']
			videonames=[]
			for i in range(len(t)):
				videonames.append(model.get_videoname(t[i])['name'])
			uploaders=[]
			for i in range(len(t)):
				uploaders.append(model.get_uploader(t[i])['uploader'])
			descriptions=[]
			for i in range(len(t)):
				descriptions.append(model.get_description(t[i])['description'])
			views=[]
			for i in range(len(t)):
				views.append(model.get_views(t[i])['views'])
			likes=[]
			dislikes=[]
			for i in range(len(t)):
				x=model.get_likestatus_count(t[i])
				likes.append(x['likes'])
				dislikes.append(x['dislikes'])
			return render.category(session.user,model.get_firstname(session.user)['firstname'],t,videonames,uploaders,category,descriptions,views,likes,dislikes)

class Profile:

	def GET(self,profileusername):
		if session.user=='username':
			raise web.seeother('/')
		if session.user==profileusername:
			raise web.seeother('/myprofile')
		u=model.get_user_stats(profileusername)
		return render.profile(model.get_firstname(session.user)['firstname'],profileusername,model.get_firstname(profileusername)['firstname'],u['about'],u['joined'],u['likes'],u['dislikes'],u['subscribers'])

class ProfileUploads:

	def GET(self,profileusername):
		if session.user=='username':
			raise web.seeother('/')
		if session.user==profileusername:
			raise web.seeother('/uploads')
		s=model.get_uploads(profileusername)
		t=s['videouploads']
 		videonames=[]
		for i in range(len(t)):
			videonames.append(model.get_videoname(t[i])['name'])
		uploaders=[]
		for i in range(len(t)):
			uploaders.append(model.get_uploader(t[i])['uploader'])
		descriptions=[]
		for i in range(len(t)):
			descriptions.append(model.get_description(t[i])['description'])
		views=[]
		for i in range(len(t)):
			views.append(model.get_views(t[i])['views'])
		likes=[]
		dislikes=[]
		for i in range(len(t)):
			x=model.get_likestatus_count(t[i])
			likes.append(x['likes'])
			dislikes.append(x['dislikes'])
		return render.profileuploads(model.get_firstname(session.user)['firstname'],profileusername,t,videonames,uploaders,model.get_firstname(profileusername)['firstname'],descriptions,views,likes,dislikes)


class Subscribe:
	def POST(self):
		i = web.input()
		s=model.subscribe(i.username,i.uploader)
		if s['subscribestatus']=="Subscribed":
			t=model.get_subscribestatus_count(i.uploader)
			sbs=t['Subscribers']
			model.update_subscribestatus(i.uploader,sbs)			
			raise web.seeother('/play/'+i.videoid)


class Unsubscribe:
	def POST(self):
		i = web.input()
		s=model.unsubscribe(i.username,i.uploader)
		if s['subscribestatus']=="Unsubscribed":
			t=model.get_subscribestatus_count(i.uploader)
			sbs=t['Subscribers']
			model.update_subscribestatus(i.uploader,sbs)
			if int(i.videoid)==0:
				raise web.seeother('/subscription')
			else:
				raise web.seeother('/play/'+i.videoid)
				



class Comment:
	def POST(self):
		i = web.input()
		s = model.send_comment(i.videoid,i.username,i.commenttext)
		raise web.seeother('/play/'+i.videoid)

class Subscription:
	def GET(self):
		s=model.get_subscription(session.user)
		t=s['subscriptions']
		return render.subscription(session.user,model.get_firstname(session.user)['firstname'],t)
		

class ProfilePic:
    def GET(self,username):
		s=model.get_profilepic(username)		
		return s

class CoverPic:
    def GET(self,username):
		s=model.get_coverpic(username)		
		return s

class DeleteVideo:

	def GET(self,video_id):
		id=int(video_id)
		s=model.delete_video(id)
		if s['status']=="Deleted":
			raise web.seeother('/uploads')

class Like:

	def POST(self):
		i = web.input()
		s=model.update_like(i.username,i.videoid)
		if s['likestatus']=="Liked":
			t=model.get_likestatus_count(i.videoid)
			lks=t['likes']
			dlks=t['dislikes']
			model.update_likestatus(i.videoid,lks,dlks)
			model.update_channel_likes_count(i.uploader)
			raise web.seeother('/play/'+i.videoid)

class Dislike:
	def POST(self):
		i = web.input()
		s=model.update_dislike(i.username,i.videoid)
		if s['likestatus']=="Disliked":
			t=model.get_likestatus_count(i.videoid)
			lks=t['likes']
			dlks=t['dislikes']
			model.update_likestatus(i.videoid,lks,dlks)
			model.update_channel_likes_count(i.uploader)

			raise web.seeother('/play/'+i.videoid)

class Nonelike:
	def POST(self):
		i = web.input()
		s=model.update_nonelike(i.username,i.videoid)
		if s['likestatus']=="Noneliked":
			t=model.get_likestatus_count(i.videoid)
			lks=t['likes']
			dlks=t['dislikes']
			model.update_likestatus(i.videoid,lks,dlks)
			model.update_channel_likes_count(i.uploader)
			raise web.seeother('/play/'+i.videoid)


class UpdateVideo:
	def POST(self):

		i = web.input()
		th = web.input(mythumbnail={})
		st = web.input(mysubtitles={})
		countries=[]
		if hasattr(i, 'India'):
			countries.append(i.India)
		if hasattr(i, 'UnitedStates'):
			countries.append(i.UnitedStates)
		if hasattr(i, 'Australia'):
			countries.append(i.Australia)
		if hasattr(i, 'China'):
			countries.append(i.China)
		if hasattr(i, 'Germany'):
			countries.append(i.Germany)
		if hasattr(i, 'None1'):
			countries.append(i.None1)

		t=str(i.tags)
		tg=json.dumps(t.split(","))
		p=model.update_video(i.id,i.name,i.description,tg,countries,i.category,session.user,int(i.age),th,st)
		#raise web.seeother('/play/'+i.id)
		raise web.seeother('/uploads')

class EditVideo:

	def POST(self,video_id):
		id=int(video_id)
		s=model.get_videodesc(id)
		#if s['id']==session.user:
		id1=s['id']
		name=s['name']
		uploader=s['uploader']
		description=s['description']
		category=s['category']
		if s['countries']!='null':
			countries=ast.literal_eval(s['countries'])
		else:
			countries=[]
		age=s['age']
		if s['tags']!='null':
			tags=ast.literal_eval(s['tags'])
			tags=','.join(tags)
		else:
			tags=""
		return render.editvideo(session.user,model.get_firstname(session.user)['firstname'],int(id1),name,description,category,countries,int(age),tags)

class UpdateProfile:	
	def GET(self):
		if session.user=='username':
			raise web.seeother('/')
		s=model.get_profile(session.user)
		fn=s['firstname']
		ln=s['lastname']
		db=s['dob']
		abt=s['about']
		eml=s['email']
		ph=s['phone']
		cntry=s['country']
		return render.updateprofile(session.user,model.get_firstname(session.user)['firstname'],fn,ln,abt,db,eml,ph,cntry)


	def POST(self):
		i = web.input()
		x = web.input(myprofilepic={})
		y = web.input(mycoverpic={})
		s = model.update_profile(i.firstname,i.lastname,i.username,i.about,i.phone,i.email,i.country,i.dob,x,y)
		session.kill()
		raise web.seeother('/myprofile')

class Index:

	login = form.Form(
	form.Textbox('username',form.notnull),
	form.Password('password',form.notnull),
	form.Button('Login'),
	)

	def GET(self):

		if session.user!='username':
				raise web.seeother('/home')
		login = self.login()
		return render.index(login)
		
	def POST(self):
		login = self.login()
		if not login.validates():            
			return render.index(login)
		else:
			un=login.d.username
			pwd=login.d.password
			
			s= model.check_user(un,pwd)			
			if s['status']== "LoggedIn":
				session.loggedin = True
				session.user = s['username']
				raise web.seeother('/home')
			else:
				raise web.seeother('/')
        	
			

class Register:


	register = form.Form(
	form.Textbox('firstname',form.notnull),
	form.Textbox('lastname',form.notnull),
	form.Textbox('phone',form.notnull),
	form.Textbox('email',form.notnull),
	form.Textbox('username',form.notnull),
	form.Password('password',form.notnull),
	form.Button('Register'),
	)

	def GET(self):
		register = self.register()
		return render.register(register)

	def POST(self):
		register = self.register()
		if not register.validates():            
			raise web.seeother('/')

		fn=register.d.firstname
		ln=register.d.lastname
		ph=register.d.phone
		eml=register.d.email
		un=register.d.username
		pwd=register.d.password
		s=model.new_user(fn,ln,ph,eml,un,pwd,str(date.today()))
		if s['status']== "Registered":
			session.loggedin = True
			session.user = s['username']
			#return s
        	raise web.seeother('/updateprofile')
		#return s

class Search:


	def POST(self):
		i = web.input()
		s = model.send_search(i.searchtext,model.calculate_Age(model.get_dob(session.user)['dob']),model.get_country(session.user)['country'])
		t=s['id']
 		videonames=[]
		for i in range(len(t)):
			videonames.append(model.get_videoname(t[i])['name'])
		uploaders=[]
		for i in range(len(t)):
			uploaders.append(model.get_uploader(t[i])['uploader'])
		descriptions=[]
		for i in range(len(t)):
			descriptions.append(model.get_description(t[i])['description'])
		views=[]
		for i in range(len(t)):
			views.append(model.get_views(t[i])['views'])
		likes=[]
		dislikes=[]
		for i in range(len(t)):
			x=model.get_likestatus_count(t[i])
			likes.append(x['likes'])
			dislikes.append(x['dislikes'])
		return render.search(session.user,t,videonames,uploaders,descriptions,views,likes,dislikes)
		

class Homepage:
	def GET(self):
		
		if session.user=='username':
				raise web.seeother('/')
		else:
			x= model.get_trending(int(model.calculate_Age(model.get_dob(session.user)['dob'])),model.get_country(session.user)['country'])
			t= x['trend_video']
			
			videonames=[]
			for i in range(len(t)):
				videonames.append(model.get_videoname(t[i])['name'])
			
			uploaders=[]
			for i in range(len(t)):
				uploaders.append(model.get_uploader(t[i])['uploader'])
			descriptions=[]
			for i in range(len(t)):
				descriptions.append(model.get_description(t[i])['description'])
			views=[]
			for i in range(len(t)):
				views.append(model.get_views(t[i])['views'])
			likes=[]
			dislikes=[]
			for i in range(len(t)):
				x=model.get_likestatus_count(t[i])
				likes.append(x['likes'])
				dislikes.append(x['dislikes'])
			return render.homepage(model.get_firstname(session.user)['firstname'],t,videonames,uploaders,descriptions,views,likes,dislikes)

class Play:
	def GET(self,video_id):

		if session.user=='username':
			raise web.seeother('/')
		else:
			z=model.get_country(session.user)['country']
			y=model.get_countryrestriction(video_id)['CountryRestriction']
			y=ast.literal_eval(y)
			ag=model.calculate_Age(model.get_dob(session.user)['dob'])
			agres=model.get_agerestriction(video_id)['AgeRestriction']
			
			if (int(ag)>int(agres)):
				if (z not in y):
					
					model.add_history(session.user,video_id)
					model.update_views(video_id)

					ls=model.get_likestatus(session.user,video_id)
					ss=model.get_subscribestatus(session.user,model.get_uploader(video_id)['uploader'])
					cmts=model.get_commentlist(video_id)
					x=model.get_recommendation(int(video_id),int(model.calculate_Age(model.get_dob(session.user)['dob'])),model.get_country(session.user)['country'])
					t= x['recom_id']
					s=[]
					for i in range(len(t)):
						if t[i]==video_id:
							r=t.pop(i)
							break
					
					if t==None:
						t=[]
					if range(len(t))>7:
						t=t[0:7]
					videonames=[]
					for i in range(len(t)):
						videonames.append(model.get_videoname(t[i])['name'])
					uploaders=[]
					for i in range(len(t)):
						uploaders.append(model.get_uploader(t[i])['uploader'])
					descriptions=[]
					for i in range(len(t)):
						descriptions.append(model.get_description(t[i])['description'])
					views=[]
					for i in range(len(t)):
						views.append(model.get_views(t[i])['views'])
					likes=[]
					dislikes=[]
					for i in range(len(t)):
						x=model.get_likestatus_count(t[i])
						likes.append(x['likes'])
						dislikes.append(x['dislikes'])
					return render.play(session.user,model.get_firstname(session.user)['firstname'],video_id,model.get_videoname(video_id)['name'],model.get_uploader(video_id)['uploader'],model.get_description(video_id)['description'],model.get_views(video_id)['views'],model.get_likestatus_count(video_id)['likes'],model.get_likestatus_count(video_id)['dislikes'],ls['likestatus'],ss['subscribestatus'],cmts['commentid'],cmts['usernames'],cmts['commentlist'],t,videonames,uploaders,descriptions,views,likes,dislikes)
				else:
					return render.restrictions(model.get_firstname(session.user)['firstname'])
			else:
				return render.restrictions(model.get_firstname(session.user)['firstname'])


class Uploadvideo:
	def GET(self):
		if session.user=='username':
				raise web.seeother('/')
		else:	
			return render.uploadvideo(model.get_firstname(session.user)['firstname'])

	def POST(self):
		
		x = web.input(myfile={})
		th = web.input(mythumbnail={})
		r = model.upload_video(x,th,session.user)
		id=str(r['id'])
		raise web.seeother('/uploadvideoinfo/'+id)

class UploadVideoInfo:

	def GET(self,video_id):
		if session.user=='username':
			raise web.seeother('/')
		id=int(video_id)
		s=model.get_videodesc(id)
		#if s['id']==session.user:
		id1=s['id']
		name=s['name']
		uploader=s['uploader']
		description=s['description']
		category=s['category']
		countries=s['countries']
		age=s['age']
		return render.uploadvideoinfo(session.user,model.get_firstname(session.user)['firstname'],id1,name,description,category,countries,age)

	def POST(self):

		i = web.input()
		th = web.input(mythumbnail={})
		st = web.input(mysubtitles={})
			
		countries=[]
		if hasattr(i, 'India'):
			countries.append(i.India)
		if hasattr(i, 'UnitedStates'):
			countries.append(i.UnitedStates)
		if hasattr(i, 'Australia'):
			countries.append(i.Australia)
		if hasattr(i, 'China'):
			countries.append(i.China)
		if hasattr(i, 'Germany'):
			countries.append(i.Germany)
		if hasattr(i, 'None1'):
			countries.append(i.None1)
		
		if i.tags=="":
			tg='null'
		else:
			t=i.tags
			tg=json.dumps(t.split(","))
		model.upload_video_info(i.id,i.name,i.description,tg,countries,i.category,session.user,i.age,th,st)

		raise web.seeother('/uploads')


	
"""-----------------------------------------------------------------------------"""
class Videos:
    def GET(self,video_id):
		id=int(video_id)
		s=model.get_video(id)		
		return s

class Subtitles:
    def GET(self,video_id):
		id=int(video_id)
		s=model.get_subtitle(id)		
		return s

class Thumbnails:
    def GET(self,video_id):
		id=int(video_id)
		s=model.get_thumbnail(id)		
		return s


class Logout:
    def GET(self):
        session.kill()
        raise web.seeother('/')
"""------------------------------------------------------------------"""		


class MyProfile:
	def GET(self):
		if session.user=='username':
			raise web.seeother('/')
		u=model.get_user_stats(session.user)
		s=model.get_profile(session.user)
		return render.myprofile(session.user,model.get_firstname(session.user)['firstname'],s['firstname'],s['lastname'],s['dob'],s['about'],s['email'],s['phone'],s['country'],u['joined'],u['likes'],u['dislikes'],u['subscribers'])


class Uploads:

	def GET(self):
		if session.user=='username':
			raise web.seeother('/')
		s=model.get_uploads(session.user)
		t=s['videouploads']
 		videonames=[]
		for i in range(len(t)):
			videonames.append(model.get_videoname(t[i])['name'])
		uploaders=[]
		for i in range(len(t)):
			uploaders.append(model.get_uploader(t[i])['uploader'])
		descriptions=[]
		for i in range(len(t)):
			descriptions.append(model.get_description(t[i])['description'])
		views=[]
		for i in range(len(t)):
			views.append(model.get_views(t[i])['views'])
		likes=[]
		dislikes=[]
		for i in range(len(t)):
			x=model.get_likestatus_count(t[i])
			likes.append(x['likes'])
			dislikes.append(x['dislikes'])
		
		return render.uploads(session.user,model.get_firstname(session.user)['firstname'],t,videonames,uploaders,descriptions,views,likes,dislikes)

class Statistics:

	def GET(self):
		if session.user=='username':
			raise web.seeother('/')
		s=model.get_uploads(session.user)
		t=s['videouploads']
 		videonames=[]
		for i in range(len(t)):
			videonames.append(model.get_videoname(t[i])['name'])
		uploaders=[]
		for i in range(len(t)):
			uploaders.append(model.get_uploader(t[i])['uploader'])
		descriptions=[]
		for i in range(len(t)):
			descriptions.append(model.get_description(t[i])['description'])
		views=[]
		for i in range(len(t)):
			views.append(model.get_views(t[i])['views'])
		likes=[]
		dislikes=[]
		for i in range(len(t)):
			x=model.get_likestatus_count(t[i])
			likes.append(x['likes'])
			dislikes.append(x['dislikes'])
		return render.statistics(session.user,model.get_firstname(session.user)['firstname'],t,videonames,uploaders,descriptions,views,likes,dislikes)

"""-------------------------------------------------------------------------------------------------------"""



class History:
	def GET(self):
		if session.user=='username':
			raise web.seeother('/')
		t=model.get_history(session.user)['videoids']

		videonames=[]
		for i in range(len(t)):
			videonames.append(model.get_videoname(t[i])['name'])
		uploaders=[]
		for i in range(len(t)):
			uploaders.append(model.get_uploader(t[i])['uploader'])
		descriptions=[]
		for i in range(len(t)):
			descriptions.append(model.get_description(t[i])['description'])
		views=[]
		for i in range(len(t)):
			views.append(model.get_views(t[i])['views'])
		likes=[]
		dislikes=[]
		for i in range(len(t)):
			x=model.get_likestatus_count(t[i])
			likes.append(x['likes'])
			dislikes.append(x['dislikes'])
		return render.history(session.user,model.get_firstname(session.user)['firstname'],t,videonames,uploaders,descriptions,views,likes,dislikes)



"""----------------------------------------------------------------------------------------------------------------------------------------"""

if __name__ == "__main__":
   app.run()
