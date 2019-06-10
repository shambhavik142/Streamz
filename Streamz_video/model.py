import web
import json 
import sqlite3

db = web.database(dbn='sqlite', db='videos.db')

def get_videodesc(id):
	data = db.select('video', order='id')
	authdb = sqlite3.connect('videos.db')
	c= authdb.execute('select * from video where id=?',[id])
	row = c.fetchone()
	nm=row[1]
	upl=row[4]
	des=row[5]
	cat=row[6]
	count=row[7]
	age=row[8]
	tags=row[9]
	params={'id':id, 'name':nm, 'uploader':upl, 'description':des, 'category':cat, 'countries':count, 'age':age, 'tags':tags}
	return json.dumps(params)

def get_video(id):
	data = db.select('video', order='id')
	authdb = sqlite3.connect('videos.db')
	c= authdb.execute('select * from video where id=?',[id])
	row = c.fetchone()
	url=row[2]
	return open(url,"rb").read()

def get_subtitle(id):
	data = db.select('video', order='id')
	authdb = sqlite3.connect('videos.db')
	c= authdb.execute('select * from video where id=?',[id])
	row = c.fetchone()
	url=row[12]
	return open(url,"rb").read()

def get_thumbnail(id):
	data = db.select('video', order='id')
	authdb = sqlite3.connect('videos.db')
	c= authdb.execute('select * from video where id=?',[id])
	row = c.fetchone()
	url=row[3]
	return open(url,"rb").read()

def get_videoname(id):
	data = db.select('video', order='id')
	authdb = sqlite3.connect('videos.db')
	c= authdb.execute('select * from video where id=?',[id])
	row = c.fetchone()
	nm=row[1]
	params={'name':nm}
	return json.dumps(params)

def get_description(id):
	data = db.select('video', order='id')
	authdb = sqlite3.connect('videos.db')
	c= authdb.execute('select * from video where id=?',[id])
	row = c.fetchone()
	desc=row[5]
	params={'description':desc}
	return json.dumps(params)

def get_uploader(id):
	data = db.select('video', order='id')
	authdb = sqlite3.connect('videos.db')
	c= authdb.execute('select * from video where id=?',[id])
	row = c.fetchone()
	ul=row[4]
	params={'uploader':ul}
	return json.dumps(params)

def get_views(id):
	data = db.select('video', order='id')
	authdb = sqlite3.connect('videos.db')
	c= authdb.execute('select * from video where id=?',[id])
	row = c.fetchone()
	vw=row[13]
	params={'views':vw}
	return json.dumps(params)

def upload_video(name,videopath,thumbnail,uploader):
	id=db.insert('video', name=name, urlpath=videopath,thumbnail=thumbnail, uploader=uploader,likes=0,dislikes=0,views=0)
	params={'id':id}
	return json.dumps(params)

def upload_thumbnail(name,thumbnailpath):
	id=db.insert('video', thumbnail=thumbnailpath)
	params={'id':id}
	return json.dumps(params)
		

def update_video_desc(id,name,description,category,country,age,tags):
	age=int(age)
	db.update('video', where='id= $id',vars=locals(), name=name,description=description,category=category,country=country,age=age,tags=tags)
	params={'status':"updated"}
	return json.dumps(params)

def update_video_thumbnail(id,thumbnail):
	db.update('video', where='id= $id',vars=locals(), thumbnail=thumbnail)
	return "success"

def update_video_subtitles(id,subtitles):
	db.update('video', where='id= $id',vars=locals(), subtitles=subtitles)
	return "success"

def get_uploads(username):
	data = db.select('video', order='id')
	authdb = sqlite3.connect('videos.db')
	c= authdb.execute('select id from video where uploader=?',[username])
	row = c.fetchall()
	l=[]
	for i in range(len(row)):
		l.append(row[i][0])
	params={'videouploads':l}
	return json.dumps(params)


def delete_video(id):
	db.delete('video', where="id=$id", vars=locals())
	params={'status':"Deleted"}
	return json.dumps(params)

def update_likestatus(id,likes,dislikes):
	db.update('video', where='id= $id',vars=locals(), likes=likes,dislikes=dislikes)
	params={'status':"updated"}
	return json.dumps(params)

def get_channel_likes_count(uploader):
	data = db.select('video', order='id')
	authdb = sqlite3.connect('videos.db')
	c= authdb.execute('select likes,dislikes from video where uploader=?',[uploader])
	row = c.fetchall()
	print row
	likes=0
	for i in range(len(row)):
		likes+=int(row[i][0])
	dislikes=0
	for i in range(len(row)):
		dislikes+=int(row[i][1])
	params={'uploader':uploader,'likescount':likes,'dislikescount':dislikes}
	return json.dumps(params)

def get_agerestriction(videoid):
	data = db.select('video', order='id')
	authdb = sqlite3.connect('videos.db')
	c= authdb.execute('select age from video where id=?',[videoid])
	row = c.fetchall()
	params={'AgeRestriction':int(row[0][0])}
	return json.dumps(params)

def get_countryrestriction(videoid):
	data = db.select('video', order='id')
	authdb = sqlite3.connect('videos.db')
	c= authdb.execute('select country from video where id=?',[videoid])
	row = c.fetchall()
	params={'CountryRestriction':row[0][0]}
	return json.dumps(params)

def update_views(videoid):
	authdb = sqlite3.connect('videos.db')
	c= authdb.execute('select views from video where id=?',[videoid])
	row = c.fetchall()
	db.update('video', where='id= $videoid',vars=locals(), views=int(row[0][0])+1)
	params={'status':"updated"}
	return json.dumps(params)