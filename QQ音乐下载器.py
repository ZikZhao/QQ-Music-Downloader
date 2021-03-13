import requests
import tkinter as tk
import os
import subprocess
import time
import subprocess
from PIL import ImageTk,Image
from bs4 import BeautifulSoup
from io import BytesIO
from tkinter import messagebox
from pygame import mixer
import re

headers = {
	'Origin': 'https://y.qq.com',
	'Referer': 'https://y.qq.com/portal/search.html',
	'Sec-Fetch-Mode': 'cors',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

def user_help():
	#用户使用说明窗口
	help_window
	help_window=tk.Tk()
	help_window.title('使用说明')
	help_window.resizable(False,False)
	help_window.geometry('500x300')
	help_window.update()
	title=tk.Label(help_window,text='使用说明',font=(font,30))

def search():
	#查询界面
	def get_information():
		search_text=enterbox.get().encode('UTF-8')
		response=requests.get(f'https://c.y.qq.com/soso/fcgi-bin/client_search_cp',params={'p':1,'n':10,'w':search_text})
		data=eval(response.text[9:-1])
		#获取歌曲信息组
		global music_list
		try:
			music_list=data['data']['song']['list']
			if not len(music_list):messagebox.showwarning('警告','未查询到相关信息')
			else:show_information()
		except:
			messagebox.showwarning('警告','未查询到相关信息')
	def show_information():
		global music_list
		frame_list=[]
		for index in range(len(music_list)):
			element=music_list[index]
			music_name=element['songname']
			singer_name=''
			for singer in element['singer']:
				singer_name+=singer['name']
				singer_name+='/'
			singer_name=singer_name[:-1]
			album_name=element['albumname']
			songmid=element['songmid']
			#子框架
			sub_frame=tk.Frame(frame,width=1000,height=41,bg='white',bd=0)
			sub_frame.place(x=0,y=92+index*41)
			frame_list.append(sub_frame)
			#歌曲名，歌手以及专辑
			text_music_name=tk.Label(sub_frame,text=music_name,font=('Microsoft YaHei',16),bg='white')
			text_music_name.place(x=0,y=0)
			text_singer_name=tk.Label(sub_frame,text=singer_name,font=('Microsoft YaHei',16),bg='white')
			text_singer_name.place(x=500,y=0)
			text_album_name=tk.Label(sub_frame,text=album_name,font=('Microsoft YaHei',16),bg='white')
			text_album_name.place(x=700,y=0)
		#添加按钮
		try:
			frame_list[0]=(frame_list[0],tk.Button(frame_list[0],text='跳转',bd=2,command=lambda:details(0),font=('Microsoft YaHei',15)))
			frame_list[1]=(frame_list[1],tk.Button(frame_list[1],text='跳转',bd=2,command=lambda:details(1),font=('Microsoft YaHei',15)))
			frame_list[2]=(frame_list[2],tk.Button(frame_list[2],text='跳转',bd=2,command=lambda:details(2),font=('Microsoft YaHei',15)))
			frame_list[3]=(frame_list[3],tk.Button(frame_list[3],text='跳转',bd=2,command=lambda:details(3),font=('Microsoft YaHei',15)))
			frame_list[4]=(frame_list[4],tk.Button(frame_list[4],text='跳转',bd=2,command=lambda:details(4),font=('Microsoft YaHei',15)))
			frame_list[5]=(frame_list[5],tk.Button(frame_list[5],text='跳转',bd=2,command=lambda:details(5),font=('Microsoft YaHei',15)))
			frame_list[6]=(frame_list[6],tk.Button(frame_list[6],text='跳转',bd=2,command=lambda:details(6),font=('Microsoft YaHei',15)))
			frame_list[7]=(frame_list[7],tk.Button(frame_list[7],text='跳转',bd=2,command=lambda:details(7),font=('Microsoft YaHei',15)))
			frame_list[8]=(frame_list[8],tk.Button(frame_list[8],text='跳转',bd=2,command=lambda:details(8),font=('Microsoft YaHei',15)))
			frame_list[9]=(frame_list[9],tk.Button(frame_list[9],text='跳转',bd=2,command=lambda:details(9),font=('Microsoft YaHei',15)))  
		except:pass
		for element in frame_list:
			element[1].place(relx=1,rely=0.5,anchor='e')
		window.update()
	window.title('QQ音乐下载器')
	window.resizable(False,False)
	window.geometry('1000x500')
	window.update()
	global frame
	frame=tk.Frame(window,bg='white',width=1000,height=500,bd=0)
	frame.pack()
	music_column=tk.Label(frame,text='歌曲',font=('Microsoft YaHei',15),bg='white',fg='#555652')
	music_column.place(x=0,y=51)
	singer_column=tk.Label(frame,text='歌手',font=('Microsoft YaHei',15),bg='white',fg='#555652')
	singer_column.place(x=500,y=51)
	album_column=tk.Label(frame,text='专辑',font=('Microsoft YaHei',15),bg='white',fg='#555652')
	album_column.place(x=700,y=51)
	operation_column=tk.Label(frame,text='操作',font=('Microsoft YaHei',15),bg='white',fg='#555652')
	operation_column.place(x=945,y=51)
	text=tk.Label(frame,text='在输入框中输入音乐或者歌手名:',font=('Microsoft YaHei',20),bg='white')
	text.place(x=1,y=0)
	global enterbox
	enterbox=tk.Entry(frame,width=34,font=('Microsoft YaHei',20))
	enterbox.place(x=400,y=2)
	if last:
		enterbox.insert(0,last)
		get_information()
	OK_button=tk.Button(frame,text='查询',command=get_information,font=('Microsoft YaHei',15),bd=0)
	OK_button.place(x=950,y=0)
	line=tk.Frame(window,width=996,height=4,bg='#555652')
	line.place(x=2,y=88)
	window.mainloop()

def details(index):
	global detail_state,state
	detail_state=True
	state=[None,0]
	def return_to_search():
		global frame
		mixer.music.stop()
		frame.destroy()
		detail_state=False
		search()
	global window,frame,music_list,last,enterbox
	last=enterbox.get()
	window.destroy()
	window=tk.Tk()
	window.geometry('1000x700')
	window.resizable(False,False)

	frame=tk.Frame(window,bg='white',width=1000,height=700,bd=0)
	frame.pack()
	window.update()
	#整理信息
	element=music_list[index]
	global singer_name,music_name,songid
	music_name=element['songname']
	window.title('详情：'+music_name)
	singer_name=''
	for singer in element['singer']:
		singer_name+=singer['name']
		singer_name+=' / '
	singer_name=singer_name[:-3]
	album_name=element['albumname']
	songid=element['songid']
	#获取音乐图片
	response=requests.get('https://y.qq.com/n/yqq/song/%s.html'%music_list[index]['songmid'])
	print(response)
	soup=BeautifulSoup(response.content,'html.parser')
	image_url=soup.select('div.mod_data>span>img')[0].get('src')
	response_image=requests.get('http:'+image_url)
	print(response_image)
	#搭建界面
	photo=ImageTk.PhotoImage(Image.open(BytesIO(response_image.content)))
	photo_label=tk.Label(frame,image=photo)
	photo_label.place(x=100,y=100)
	image=ImageTk.PhotoImage(file='返回.png')
	return_button=tk.Button(frame,image=image,command=return_to_search,bd=0)
	return_button.image=image
	return_button.place(x=5,y=5)
	title=tk.Label(frame,text=music_name,font=('Microsoft YaHei Light',50),bg='white')
	title.place(x=420,y=95)
	singer_text=tk.Label(frame,text='歌手：'+singer_name,font=('Microsoft YaHei Light',20),bg='white')
	singer_text.place(x=420,y=300)
	album_text=tk.Label(frame,text='专辑：'+album_name,font=('Microsoft YaHei Light',20),bg='white')
	album_text.place(x=420,y=350)
	#搭建子框架
	global player_frame
	player_frame=tk.Frame(frame,width=800,height=200,bg='white')
	player_frame.place(x=100,y=500)
	image=ImageTk.PhotoImage(file='加载音乐.png')
	global preparation_button
	preparation_button=tk.Button(player_frame,image=image,command=lambda:preparation(index),bd=0)
	preparation_button.place(x=0,y=0)
	preparation_button.image=image
	while True:
		try:window.update()
		except:
			mixer.quit()
			try:os.remove('cache.mp3')
			except:pass
			exit()

def preparation(index):
	mixer.quit()
	#准备音乐以及插件
	global window,frame,player_frame,music_list,preparation_button
	#提示信息框
	info_box=tk.Text(frame,font=('Microsoft YaHei',10),bg='White',height=1,bd=1,highlightbackground='#e1e1e1')
	info_box.place(relx=0,rely=1,anchor='sw',x=-1,y=1)
	info_box.insert('insert','正在获取vkey: https://u.y.qq.com/cgi-bin/musicu.fcg')
	info_box.config(width=50)
	frame.update()
	songmid=music_list[index]['songmid']
	response=requests.get('https://u.y.qq.com/cgi-bin/musicu.fcg?data={"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"8846039534","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"8846039534","songmid":["%s"],"songtype":[0],"uin":"1152921504784213523","loginflag":1,"platform":"20"}},"comm":{"uin":"1152921504784213523","format":"json","ct":24,"cv":0}}'%songmid,headers=headers)
	url=response.json()['req_0']['data']['midurlinfo'][0]['purl']
	info_box.delete(1.0,tk.END)
	info_box.insert('insert','正在检查音乐类型')
	frame.update()
	global music_length
	if not url:
		info_box.delete(1.0,tk.END)
		info_box.insert('insert','该音乐为付费音乐，没有下载权限')
		frame.update()
		tk.messagebox.showwarning('警告','该音乐为付费音乐，没有下载权限')
		info_box.destroy()
		#更改设置以避免报错
		mixer.init()
		music_length=0
	else:
		info_box.delete(1.0,tk.END)
		info_box.insert('insert','正在建立连接: http://dl.stream.qqmusic.qq.com/'+url)
		frame.update()
		response=requests.get('http://dl.stream.qqmusic.qq.com/'+url,headers=headers)
		print(response)
		#保存m4a格式音频
		info_box.delete(1.0,tk.END)
		info_box.insert('insert','写入缓存文件')
		frame.update()
		with open('cache.m4a',mode='wb') as file:file.write(response.content)
		info_box.delete(1.0,tk.END)
		info_box.insert('insert','转换音频文件格式中')
		frame.update()
		mixer.quit()
		try:os.remove('cache.mp3')
		except:pass
		os.system('ffmpeg -i cache.m4a -y cache.mp3')
		del response
		os.remove('cache.m4a')
		mixer.init()
		mixer.music.load('cache.mp3')
		music_length=get_length('cache.mp3')
		info_box.delete(1.0,tk.END)
		info_box.insert('insert','加载音乐插件')
		frame.update()
		preparation_button.destroy()
		global play_image,pause_image,player_button
		play_image=ImageTk.PhotoImage(file='播放.png')
		pause_image=ImageTk.PhotoImage(file='暂停.png')
		player_button=tk.Button(player_frame,image=play_image,command=change_state,bd=0)
		player_button.place(x=0,y=0)
		player_button.image=play_image
		scale_button=tk.Scale(player_frame,from_=0,to=music_length,bd=0,label='等待播放',
			resolution=0.1,orient=tk.HORIZONTAL,length=665,showvalue=False)
		scale_button.place(x=135,y=0)
		image=ImageTk.PhotoImage(file='快进.png')
		fast_forward=tk.Button(player_frame,command=lambda:progress_config(True),image=image,bd=0)
		fast_forward.place(x=135,y=50)
		fast_forward.image=image
		image=ImageTk.PhotoImage(file='回退.png')
		fast_backward=tk.Button(player_frame,command=lambda:progress_config(False),image=image,bd=0)
		fast_backward.place(x=0,y=50)
		fast_backward.image=image
		image=ImageTk.PhotoImage(file='下载.png')
		download_button=tk.Button(player_frame,command=download,image=image,bd=0)
		download_button.place(x=270,y=50)
		download_button.image=image
		image=ImageTk.PhotoImage(file='直接打开.png')
		open_button=tk.Button(player_frame,command=lambda:download(True),image=image,bd=0)
		open_button.place(x=405,y=50)
		open_button.image=image
		text_box=tk.Label(player_frame,text='下载路径：',font=('Microsoft YaHei',15),bg='white')
		text_box.place(x=0,y=100)
		global volume_scale
		volume_scale=tk.Scale(player_frame,from_=0,to=1,bd=0,command=change_volume,
			resolution=0.01,orient=tk.HORIZONTAL,length=255,showvalue=False,label='当前音量：50%')
		volume_scale.set(0.5)
		volume_scale.place(x=545,y=50)
		global enterbox
		enterbox=tk.Entry(player_frame,font=('Microsoft YaHei',15))
		enterbox.place(x=100,y=100)
		enterbox.insert('insert',path)
		info_box.destroy()
		global state,current_progress
	while detail_state:
		try:player_frame.update()
		except:
			try:
				mixer.quit()
				os.remove('cache.mp3')
				exit()
			except:pass
		#更新按钮位置
		try:current_progress=(mixer.music.get_pos())/1000+state[1]
		except:return None
		if current_progress<0:current_progress=0
		if current_progress>music_length:
			state=[None,0]
			player_button.config(image=play_image)
		if state[0]==None:
			try:
				scale_button.config(label='等待播放')
				scale_button.set(0)
			except:pass
			continue
		try:
			current_format=time.localtime(current_progress)[4:6]
			total_format=time.localtime(music_length)[4:6]
			string='{0:02d}:{1:02d}/{2:02d}:{3:02d}'.format(
				current_format[0],current_format[1],total_format[0],total_format[1])
			scale_button.config(label='正在播放: '+string)
			scale_button.set(current_progress)
		except:pass
		
def get_length(filename):
	command=['ffprobe.exe','-loglevel','quiet','-print_format','json','-show_format','-show_streams','-i',filename]
	result=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	output=result.stdout.read()
	data=eval(str(output.decode('utf-8')))['format']['duration']
	return int(float(data))

def change_state():
	#播放状态改变
	global state,player_button
	if state[0]:state=[False,state[1]]
	else:state=[True,state[1]]
	if state[0]:
		mixer.music.play(start=state[1])
		player_button.config(image=pause_image)
	else:
		state[1]=state[1]+mixer.music.get_pos()/1000
		mixer.music.stop()
		player_button.config(image=play_image)

def progress_config(positive=True):
	global music_length,state,scale_button
	#进度改变
	state[1]=current_progress
	mixer.music.stop()
	if positive:
		state[1]+=5
		if state[1]>music_length:
			state=[False,0]
			scale_button.config(label='等待播放')
	else:
		state[1]-=5
		if state[1]<0:state[1]=0
	if state[0]:mixer.music.play(start=state[1])

def download(open_after=False):
	global enterbox,path
	path=enterbox.get()
	response=requests.get('https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric.fcg?nobase64=1&musicid=%d&callback=jsonp1&g_tk=5381&jsonpCallback=jsonp1&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'%songid
	,headers={'referer':'https://y.qq.com/n/yqq/song/003icETK3ej4cC.html'
	,'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3775.400 QQBrowser/10.6.4208.400'})
	lyrics=eval(response.text[7:-1])['lyric'].replace('apos&#59',"'")
	result=re.finditer(r'#\d+',lyrics)
	for element in result:
		lyrics=lyrics.replace(element.group(),chr(int(element.group()[1:])),1)
	lyrics=lyrics.replace(';','').replace('&','').replace('[offset:0]','[offset:0.5]')
	target_path=os.path.join(path,singer_name.replace('/','_')+' - '+music_name.replace('/','_'))
	with open('cache.mp3',mode='rb') as file:
		content=file.read()
		try:
			with open(target_path+'.mp3',mode='wb') as file1:
				file1.write(content)
			with open(target_path+'.lrc',mode='w') as file2:
				file2.write(lyrics)
		except:
			messagebox.showwarning('警告','未查询到相关信息')
		else:
			if open_after:os.popen('''"%ProgramFiles(x86)%/Windows Media Player/wmplayer.exe" "{0}.mp3"'''.format(target_path))

def change_volume(value):
	volume_scale.config(label='当前音量：{0:.0f}%'.format(float(value)*100))
	mixer.music.set_volume(float(value))

#准备
mixer.init()
last=None
global window
window=tk.Tk()
detail_state=False
path='F:/'
#启动器
user_help()
search()