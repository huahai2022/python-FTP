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
		authorizer.add_user("user","123456","D:\project",perm="elradfmw")
		authorizer.add_anonymous("D:\project")
		handler=FTPHandler
		handler.authorizer=authorizer
		handler.passive_ports=range(2000,8333)
		sever=FTPServer(("127.0.0.1",21),handler)
		sever.serve_forever()
ftpServer=FtpServer()
ftpServer.ftpStart()
