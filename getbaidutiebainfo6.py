# -*- coding:utf-8 -*-
import urllib,os,urllib2,re
from Tkinter import *

#测试帖子代码：3650478639；3770689406

#噪声去除类
class remNoise:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #将前后空白符删除
        return x.strip()

#百度贴吧文字爬虫类
class BDTB:

    #初始化，传入基地址，是否只看楼主的参数，是否显示楼层
    def __init__(self,baseUrl,seeLZ,floorTag,filename):
        #base链接地址
        self.baseURL = baseUrl
        #是否只看楼主
        self.seeLZ = '?see_lz='+str(seeLZ)
        #HTML标签剔除工具类对象
        self.remNoise = remNoise()
        #全局file变量，文件写入操作对象
        self.file = None
        #楼层标号，初始为1
        self.floor = 1
        #默认的标题，如果没有成功获取到标题的话则会用这个标题
        self.defaultTitle = filename
        #是否写入楼分隔符的标记
        self.floorTag = floorTag

    #获取帖子页数
    def getPageNum(self,page):
        #传递图片爬虫页数参数
        global pnum 
        #获取帖子页数的正则表达式
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        result = re.search(pattern,page)
        if result:
            #strip 消去标题前后的空格
            pnum =  result.group(1).strip()
            return result.group(1).strip()
        else:
            return None


    #传入页码，获取该页帖子的代码
    def getPage(self,pageNum):
        try:
            #构建URL
            url = self.baseURL+ self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            #返回UTF-8格式编码内容
            return response.read().decode('utf-8')
        #无法连接，报错
        except urllib2.URLError, e:
            #判断对象Obiect的属性是否存在
            if hasattr(e,"reason"):
                print u"fail to link to BDTB ,reason:",e.reason
                return None

    #获取帖子标题
    def getTitle(self,page):
        #全部分析匹配标题的正则表达式编译对象
        pattern = re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>',re.S)
        result = re.search(pattern,page)
        if result:
            #如果存在，则返回标题
            return result.group(1).strip()
        else:
            return None

    #获取每一层楼的内容,传入页面内容
    def getContent(self,page):
        #匹配所有楼层的内容
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            #将文本除燥，同时在前后加入换行符
            content = "\n"+self.remNoise.replace(item)+"\n"
            contents.append(content.encode('utf-8'))
        return contents

    #如果标题不是为None，即成功获取到标题
    def setFileTitle(self,title):
        #如果文件夹不存在，新建命名
        if (os.path.exists('%s'%self.defaultTitle)== False):
            os.mkdir('%s'%self.defaultTitle)  
        if title is not None:
            self.file = open("%s/%s.txt"%(self.defaultTitle ,title ) ,"w+")
        else:
            self.file = open(self.defaultTitle + ".txt","w+")

    def writeData(self,contents):
        #向文件写入每一楼的信息
        for item in contents:
            if self.floorTag == '1':
                #楼之间的分隔符
                floorLine = "\n" + str(self.floor) + u"-----------------------------------------------------------------------------------------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    def go_txt(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print "URL is invalid，please try again."
            return
        try:
            print "There are " + str(pageNum) + " pages"
            for i in range(1,int(pageNum)+1):
                print "Page " + str(i) + " saved successfully!"
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        #出现写入异常
        except IOError,e:
            print "in error，reason:" + e.message
        finally:
            print "Whole txt saved successfully!"

#百度贴吧图片爬虫类
class BDTBpic:
    def __init__(self,baseURL,fName,seeLZ):
        self.baseURL = baseURL
        self.fName = fName
        self.seeLZ = '?see_lz='+str(seeLZ)

    def getHtml(self,url):
        try:
            page = urllib.urlopen(str(url))
            html = page.read()
            html = html.decode('utf-8')
            return html
        except urllib2.URLError, e:
            #判断对象Obiect的属性是否存在
            if hasattr(e,"reason"):
                print u"fail to link to BDTB ,reason:",e.reason
                return None

    def getImg(self,html,picNum,pageNum):
        if (os.path.exists('%s'%self.fName)== False):
            os.mkdir('%s'%self.fName)  
        #原生字符串
        reg = r'src="(.+?\.jpg)" pic_ext'
        imgre = re.compile(reg)
        #print html 
        #如果出错导致HTML为空，结束爬虫
        if html == "":
            print "the end"
            exit()
        imglist = re.findall(imgre,html)
        try:
            for imgurl in imglist:
                urllib.urlretrieve(imgurl,'%s/%s.jpg' %(self.fName, "%s%s"%(self.fName,picNum)))
                print "Picture%s saved successfully!"%(picNum)
                if type(picNum) == NoneType:
                    print "the end"
                    exit()
                picNum+=1
            return picNum
        #出现写入异常
        except UnicodeError,e:
            print "in error，reason:" + e.message
        finally:
            print "Page %s pictures saved!"%pageNum

    def go_pic(self):
        #由文字爬虫传入帖子页数
        global pnum
        x = 1
        #遍历每一页
        for i in range(1,int(pnum)+1):
            self.html = self.getHtml( self.baseURL+ "%s"%self.seeLZ + '&pn=' + str(i))
            x = self.getImg("%s"%self.html,x,i)



#图形界面输入得到参数
class getatr:
    def __init__(self):
        self.groot = Tk()
        #输入框得到帖子代号
        self.nLabel = Label(self.groot,text = "请输入帖子代号：").pack()
        self.var = StringVar()
        #self.var.set("请输入帖子代号")
        self.entry = Entry(self.groot,textvariable = self.var)
        self.entry.pack()
        #个性选项只看楼主
        self.varlz = IntVar()
        #显示楼层
        self.varlc = IntVar()
        Checkbutton(self.groot,text = "是否只获取楼主发言",variable = self.varlz).pack()
        Checkbutton(self.groot,text = "是否写入楼层信息",variable = self.varlc).pack()
        #文件夹命名
        self.aLabel = Label(self.groot,text = "请为图片文件夹命名:").pack()
        self.fName = StringVar()
        self.entFN = Entry(self.groot,textvariable = self.fName)
        self.entFN.pack()
        #确认按钮
        self.sureButton = Button(self.groot,text = '确认',command = self.gofunc)
        self.sureButton.pack()
        self.groot.mainloop()



    def gofunc(self):
        #贴吧文字下载参数传递
        self.bdtb = BDTB('http://tieba.baidu.com/p/' +self.var.get(),str(self.varlz.get()),str(self.varlc.get()),self.fName.get())  
        self.bdtb.go_txt()
        self.groot.destroy()
        #贴吧图片下载参数传递
        self.bdtbpic = BDTBpic('http://tieba.baidu.com/p/' + self.var.get(),self.fName.get(),str(self.varlz.get()))
        self.bdtbpic.go_pic()


bdtb = getatr()

