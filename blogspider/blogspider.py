# coding: utf-8 

import urllib2
from urllib2 import URLError, HTTPError  
import time
import copy
import re
import os
import sys
import logging
import threading
import Queue
import win32com
from win32com.client import Dispatch, constants
import socket
#set the response time of request to 10 seconds
timeout = 10
socket.setdefaulttimeout(10)

#number of threads to get the content
#do not increase it too much because the website thinks this program is attacking it
parsethreadnum = 15
#thread pools
parse_queue = Queue.Queue()
save_queue = Queue.Queue()

class ParseThread(threading.Thread):
    """Threads to parse the content
	
    """
    def __init__(self, parse_queue, save_queue):
        threading.Thread.__init__(self)
        self.parse_queue = parse_queue
        self.save_queue = save_queue

    def run(self):
        while True:
	    #this statement can make sure thread work properly
            if self.parse_queue.empty():		
                break
            pair = {}	
            article = self.parse_queue.get()
			
            final_content = self.deal_data(article.values()[0])
            #sleep for a while otherwise the website thinks this program is attacking it. 
            time.sleep(1.5)
            pair[article.keys()[0]] = final_content
            temppair = copy.deepcopy(pair)
            self.save_queue.put(temppair)
            pair.clear()
            #signals to queue job is done
            self.parse_queue.task_done()
        return
		
    def deal_data(self, article_url):
        """get the content of article
		
        """
        try:
            headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
            req = urllib2.Request(article_url, headers=headers)
            resp = urllib2.urlopen(req)
        except URLError, e:    
            if hasattr(e, 'reason'):    
                logging.warning('Your internet connection has issues or We got nothing from a server in '+str(timeout)+' seconds')  
        else:		
            org_content = resp.read()
            real_content = re.findall(r'class=\'post-body.*?>(.*?)\n<div class=\'post-footer\'>', org_content, re.S)
        
            data = article_url+'\n\n\n'
            #process the content of each article 
            if real_content:
                data = data + HTML_Process().replace_char(real_content[0])
            else:
                data='no content in this article' 			
            return data	    		


class HTML_Process(object):
    """handle the tags in content
	
    """
    # match \t or href or image
    beg_new_none = re.compile('(\t|<a.*?>|<img.*?>)')
    
    # match <.?> tag
    end_new_none = re.compile('<.*?>')

    # match <p> tag
    new_par = re.compile('<p.*?>')
    # match <br/>, <p/>, <tr>, <div>, </div> tag
    new_line = re.compile('(<br/>|</p>|<tr>|<div>|</div>)')
    # match <td> tag
    next_tab = re.compile('<td>')

    # replace html symbol with original symbol
    replace_symbol = [("&lt;","<"),('&#8804', "<="), ('&#8722', "-"),('&#8800', "!="), ('&#8805', ">="), ("&gt;",">"),("&amp;","&"),("&amp;","\""),("&nbsp;"," ")]
    
    #substitute the symbols  
    def replace_char(self,x):
        x = self.beg_new_none.sub('',x)
        x = self.new_par.sub('\n    ',x)
        x = self.new_line.sub('\n',x)
        x = self.next_tab.sub('\t',x)
        x = self.end_new_none.sub('',x)

        for t in self.replace_symbol:  
            x = x.replace(t[0],t[1])  
        return x
		
		
class Doc_Process(object):
    """save the content in correct 
	Doc format
	
    """
    def __init__(self, title, data):  
        self.title = title
        self.datas = data
    
    def save_Doc(self):
        """set the doc format 
        and save the context as doc
	
        """	
        dirname = os.getcwd()+'\\'
        w = win32com.client.Dispatch('Word.Application')
        w.Visible = 0
        w.DisplayAlerts = 0
        doc = w.Documents.Add()
        #set the margins
        doc.PageSetup.TopMargin = 1.27*28.35           
        doc.PageSetup.BottomMargin = 1.27*28.35         
        doc.PageSetup.LeftMargin = 1.27*28.35         
        doc.PageSetup.RightMargin = 1.27*28.35        
        wrange = doc.Range(0,0)
        wrange.InsertBefore(self.datas)
        doc.SaveAs(dirname+self.title+'.doc')
        doc.Close()
        w.Quit()

class Log_Process(object):
    """Set the log configuration
	
    """
    FILE = os.getcwd()
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(filename)s %(levelname)s %(message)s',
                    datefmt='%a, %b %d %Y %H:%M:%S',
                    filename = os.path.join(FILE,'log.txt')) 
    console = logging.StreamHandler()
    #set the console level with at least WARNING, all debug, info will go to logo file
    console.setLevel(logging.WARNING)
    logging.getLogger('').addHandler(console)					
		
    
class BlogSpider(object):
    """Main class to crawl
	the blog.
	
    """
    def __init__(self, url, artformat): 
        #url of the blog site	
        self.my_url = url
        #document format
        self.my_format = artformat
        #content of raw article 		
        self.datas = []
        #total number of articles		
        self.total_article = 0
        #archieve urls		
        self.archieve_urls = [] 
        #article urls		
        self.article_urls = []  
        #article titles		
        self.article_titles = []
       
        print 'spider begins to work...'
  
   
    def blog_collection(self):
        """Main process to crawl the blog
		  
        """        
        try:
            headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
            req = urllib2.Request(self.my_url, headers=headers)
            response = urllib2.urlopen(req)
        except URLError, e:
            #url error		
            if hasattr(e, 'reason'):    
                logging.warning('Your internet connection has issues or We got nothing from a server in '+str(timeout)+' seconds')       
            #http error     
            elif hasattr(e, 'code'):    
                logging.warning('Blog does not exist!')    
       				
        else:
            print 'Blog is found sucessfully!'
            logging.info('Blog is found sucessfully!')
            my_blog = response.read()
            					
            self.total_article = self.article_counter(my_blog)
            if self.total_article != 0:
                self.archive_urls = self.archive_url(my_blog)
                self.article_urls, self.article_titles = self.article_url()
                self.save_data()
            else:
                #current version only works for certain blog archive structure			
                logging.warning( 'This spider version can not process the content correctly. Sorry!')
        
   
    
    def article_counter(self, my_blog):
        """calculate the total number of articles
        in this blog 		
		
        """
        #this format only works when the year archive has a number in the ().
        my_match = re.findall(r'class=\'post-count\' dir=\'ltr\'>\((\d+?)\)</span>\n<ul class=\'hierarchy\'>', my_blog)
        
        int_match = [int(i) for i in my_match]
        if my_match:  
            temp_total_article = sum(int_match)
            print 'Number of %d Articles is found in this blog' % temp_total_article
            logging.info('Number of %d Articles is found in this blog ' % temp_total_article)
        else:
            temp_total_article = 0
            			
        return temp_total_article
		
    	
    def archive_url(self, my_blog):
        """get the urls of all archives 
        in this blog
		
        """
        
        #match format with month and year such as Oct 2013		
        my_match = re.findall(r'class=\'post-count-link\' href=\'(.*?)\'>\D{3}\s\d{4}</a>', my_blog)
        if my_match:  
            print "Archive Found"
        #match format with only months (short or long)			
        else:
            my_match = re.findall(r'class=\'post-count-link\' href=\'(.*?)\'>\D{3,10}</a>', my_blog) 
            if my_match:			
                print "Archive Found"
            else:
                print "Archive Not Found"
                my_match=''
                
        return my_match
		
    	
    def article_url(self):
        """get the urls of all archives
        in the blog
		
        """
        temp_article_urls = []
        temp_article_titles = []
        for i, url in enumerate(self.archive_urls):
            try:
                headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
                req = urllib2.Request(url, headers=headers)
                resp = urllib2.urlopen(req)
                
            except URLError, e:    
                if hasattr(e, 'reason'):    
                    logging.warning('Your internet connection has problem or We got nothing from a server in '+str(timeout)+' seconds')  
            else:
                my_archive = resp.read()
                #get article url and title
                my_match = re.findall(r'<li><a href=\'(.*?)\'>(.*?)</a></li>', my_archive)
                
                for article in my_match: 
                    if article[1]!='Home':
                        temp_article_urls.append(article[0].replace('(',''))
                        #note the title may include ')', but it can not include: \ / ： * ? " < > |  
                        temp_article_titles.append(article[1].replace(')','').replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('>','').replace('<','').replace('|',''))
                    
        
        return temp_article_urls, temp_article_titles
		
    def save_data(self):
        """save the content of articles 
        to each file
		
        """
        
        #put parse tasks into Parse Queue
        pair = {}	

        for i in range(0,self.total_article):
            pair[self.article_titles[i]] = self.article_urls[i]
            temp_pair = copy.deepcopy(pair)
            parse_queue.put(temp_pair)
            pair.clear()
            
        #create threads to get and parse the content 
        for i in range(parsethreadnum):
            dp = ParseThread(parse_queue, save_queue)
            dp.setDaemon(False)
            dp.start()
       #block the queue to wait all tasks done	
        parse_queue.join() 

        print 'downloading article......'
        i = 0		
        while save_queue.empty() == False:
            i = i+1
            pair = save_queue.get()
            
            if self.my_format=='txt':
                f = open(pair.keys()[0]+'.txt','w+')
                f.writelines(pair.values()[0])
                f.close()
            else:
                doc = Doc_Process(pair.keys()[0], pair.values()[0])
                doc.save_Doc()
            if (i % 5)==0:	
                print 'number '+str(i)+' article is downloaded' 	
     	
        print 'all articles are downloaded and saved in folder: '+os.getcwd()
        logging.info('all articles are downloaded and saved in folder: '+os.getcwd())
		
	
if __name__=='__main__':

    mylog=Log_Process()
    logging.info('Begin A New Task')
    print 'Enter the blogspot ID'
    blogID=str(raw_input())
    blogurl = 'http://'+blogID+'.blogspot.com'
    print 'Enter the saved article format: txt or doc'
    format=str(raw_input())
    #check format
    while (format!='txt' and  format!='doc'):
        print 'The format you input is not correct, please input the correct format (txt or doc)'
        format=str(raw_input())

    logging.info('save files in blog with ID: '+blogID+' in '+ format+' format')
    start=time.time() 
    mySpider = BlogSpider(blogurl, format)
    mySpider.blog_collection()
    end=time.time()
    print 'total time is %f seconds' %(end-start)
    logging.info('total time is %f seconds' %(end-start))
