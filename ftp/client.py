from ftplib import FTP
import os

# 连接
def ftp_connect(host, post, username, password):
	ftp_client = FTP()
	ftp_client.connect(host, post)
	ftp_client.login(username, password)
	return ftp_client


# 从FTP下载文件
def download_file(ftp, remotepath, localpath):
	ftp.sendcmd("TYPE I")
	remote_filesize=ftp.size(remotepath)  #用户可见，肯定是存在的
	if os.path.exists(localpath):
		local_filesize=os.path.getsize(localpath)
		if local_filesize==remote_filesize:
			print(f"remote_filesize是{remote_filesize / 1024}K，local_filesize是{local_filesize / 1024}K，请确保你需要的文件和服务器上文件一致，无需下载")
			return
		else:
			#断点续传,设置下载的起始位置
			ftp.sendcmd(f"REST {local_filesize}")
			print(f"remote_filesize是{remote_filesize / 1024}K，local_filesize是{local_filesize / 1024}K，请确保你需要的文件和服务器上文件一致，需要下载{(remote_filesize-local_filesize)/1024}K")
			with open(localpath,"ab") as f:
				ftp.retrbinary(f"RETR {remotepath}",f.write,blocksize=1024*1024,rest=local_filesize)
			print("下载完毕了~~~")
	else:
		with open(localpath,"wb") as f:
			ftp.retrbinary(f"RETR {remotepath}",f.write,blocksize=1024*1024)
	ftp.set_debuglevel(0)


# 从FTP上传文件
def upload_file(ftp, remotepath, localpath):
	ftp.sendcmd("TYPE I")
	#获取本地文件大小和远程文件大小
	local_filesize=os.path.getsize(localpath)
	try:
		remote_filesize=ftp.size(remotepath)
	except:
		remote_filesize=-1
	print(f"remote_filesize是{remote_filesize/1024}K\nlocal_filesize是{local_filesize/1024}K")
	if remote_filesize==local_filesize:
		return
	#需要断点重传
	if remote_filesize<local_filesize and remote_filesize!=-1:
		#设置传输起始位置
		start=remote_filesize
		with open(localpath,"rb") as f:
			f.seek(start)   	#跳过传输的起始位置
			blocksize=1024*1024  #设置传输块大小
			print(f"断点续传中~~~~将从{start/1024}K处开始传输文件,文件总大小是{local_filesize/1024}K,需要传输{local_filesize-start}K")
			ftp.storbinary(f"APPE {remotepath}",f,blocksize)
			print("断点续传完毕~~~~")
	else:
		with open(localpath,"rb") as f:
			blocksize = 1024 * 1024
			print(f"重新传输文件中~~~~文件总大小是{local_filesize/1024}K,需要传输{local_filesize}K")
			ftp.storbinary(f"STOR {remotepath}",f,blocksize)
			print("传输文件完毕~~~~")
	ftp.set_debuglevel(0)


if True:
	host = "127.0.0.1"
	port = 21
	username = "user"
	password = "123456"
	ftp_client = ftp_connect(host, port, username, password)
	ftp_client.retrlines('LIST')
	upload_file(ftp_client, "sb.doc", "D:\learn\sb.doc")
	download_file(ftp_client,"sb.doc","D:\learn\sb2.doc")
	ftp_client.quit()