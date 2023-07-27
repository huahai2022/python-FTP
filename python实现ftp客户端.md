##### 1.ftp服务端，启动！

```
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
class FtpServer:
	def ftpStart(self):
		authorizer = DummyAuthorizer()
		#TODO:e:更改目录(cmd,cdup命令)
		#l:列表文件(LIST,NLST,STAT，MLSD,MLST)
		#r:从服务器上检索文件(RETR)
		#a:将文件上传到服务器
		#d:删除文件或者目录
		#f:重命名文件或目录
		#m:创建目录
		#w:更改文件权限
		authorizer.add_user("user","123456","D:/project",perm="elradfmw")
		authorizer.add_anonymous("D:/project")
		handler=FTPHandler
		handler.authorizer=authorizer
		handler.passive_ports=range(2000,8333)
		sever=FTPServer(("127.0.0.1",21),handler)
		sever.serve_forever()
ftpServer=FtpServer()
ftpServer.ftpStart()
```

###### DummyAuthorizer类介绍

```
`DummyAuthorizer` 是 `pyftpdlib` 库中提供的一个虚拟的用户授权管理类，它允许您在 Python 代码中轻松地定义和管理 FTP 用户及其权限。

该类的主要作用是充当一个用户数据库，您可以使用它来添加、删除和修改 FTP 用户。每个用户都可以被授予不同的权限，例如读取、写入、删除、重命名等等。

由于 `DummyAuthorizer` 是一个虚拟的授权管理类，因此它不会实际地创建或管理任何系统用户。相反，它只是在内存中维护一份用户列表和其对应的权限，这些信息将被传递给 FTP 服务器以进行身份验证和授权。

在实际应用中，您可以使用 `DummyAuthorizer` 或其他一些类似的授权管理类来创建自己的 FTP 服务器，并在其中定义您自己的用户和权限规则。
```

###### FTPHandler介绍

```
在 `pyftpdlib` 中，`FTPHandler` 是一个用于处理 FTP 请求的类。具体来说，当客户端连接到 FTP 服务器并发送 FTP 命令时，`FTPHandler` 类将根据命令类型执行相应的操作，例如列出目录、上传文件、下载文件等。

您可以通过继承 `FTPHandler` 类并重写其方法来自定义 FTP 服务器的行为。例如，您可以重写 `FTPHandler` 类的 `on_file_received()` 方法来在文件上传完成时执行一些额外的操作。

在您的示例代码中，`FTPHandler` 类被用来创建一个自定义的 FTP 请求处理器。该处理器定义了在客户端请求连接时和文件上传时执行的操作。具体来说：

- `on_connect()` 方法被重写以输出有关新连接的信息。
- `on_file_received()` 方法被重写以在文件上传完成时输出有关上传文件的信息。

通过继承和重写 `FTPHandler` 类的方法，您可以对 FTP 服务器的行为进行更细粒度的控制，并添加您自己的逻辑来处理 FTP 请求。
```

##### FTP客户端

ftplib模块是python中默认安装的，通过它定义FTP类中的各个函数，可以完成对FTP服务器的操作，既能实现FTP客户端，也可以连接或者操作FTP服务器。

###### 函数介绍

```
ftp=FTP()          		      #设置变量 ，实例化
ftp.set_debuglevel(2)         #打开调试级别2，显示详细信息 
ftp.connect("IP","port")      #连接的ftp sever和端口 
ftp.login("user","password")  #连接的用户名，密码 
print ftp.getwelcome()        #打印出欢迎信息 
ftp.cmd("xxx/xxx")     		  #更改远程目录 
bufsize=1024                  #设置的缓冲区大小 
filename="filename.txt"       #需要下载的文件 
file_handle=open(filename,"wb").write
#以写模式在本地打开文件 
ftp.retrbinaly("RETR filename.txt",file_handle,bufsize)
#接收服务器上文件并写入本地文件 
ftp.set_debuglevel(0)        #关闭调试模式 
ftp.quit                     #退出ftp 
ftp.dir()                    #显示目录下文件信息 
ftp.pwd()          	         #返回当前所在位置 
ftp.cwd(pathname) 	         #设置FTP当前操作的路径
ftp.mkd(pathname)            #新建远程目录
ftp.rmd(dirname)             #删除远程目录 
ftp.delete(filename)         #删除远程文件 
ftp.rename(oldname, newname) #将oldname修改名称为newname。 
ftp.storbinaly("STOR filename.txt",file_handel,bufsize) #上传目标文件
ftp.retrbinary("RETR filename.txt",file_handel,bufsize) #下载FTP目标文件
```

###### python实现上传文件、下载文件

```
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
```

###### ftp.sendcmd("TYPE I")解析

```
`ftp.sendcmd("TYPE I")` 是一个 FTP 命令，用于设置传输模式为二进制模式。

在 FTP 协议中，`TYPE` 命令用于设置传输模式，常用的传输模式有 ASCII 模式和二进制模式。ASCII 模式适用于文本文件的传输，它会将文本文件中的换行符和回车符转换为网络标准的换行符 `\r\n`，并在文件末尾添加一个结束符。而二进制模式适用于非文本文件（例如图像、音频和视频等）的传输，它不会对文件内容进行任何转换，直接传输文件的二进制数据。

在 Python 的 ftplib 库中，可以使用 `ftp.sendcmd` 方法发送 FTP 命令。在下载和上传文件时，我们通常需要将传输模式设置为二进制模式，以确保文件的内容正确传输。因此，我们可以在下载和上传文件之前，先使用 `ftp.sendcmd("TYPE I")` 命令将传输模式设置为二进制模式。

需要注意的是，在使用 ASCII 模式传输文件时，如果文件中包含二进制数据（例如图片），可能会导致文件损坏。因此，如果不确定文件的内容类型，最好使用二进制模式传输文件。
```

