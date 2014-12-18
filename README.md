[![logo](imgs/bloggerlogo.jpg)](https://github.com/checkcheckzz/blogger-spider)  

> Grab, parse and save contents of articles from Blogger

##Installation

The fast way is to download the exe file:

[dropbox link](https://www.dropbox.com/s/ob37vsje5fsvz57/blogspider.exe)

Put the exe file in an empty folder, and run it.  


##Dependencies

[pywin32](http://sourceforge.net/projects/pywin32/files/pywin32/Build%20218/)
	
##Note

Input: bogspot.com/wordpress.com ID and format (txt or doc) you want to save.

Output (to a local folder the python program runs):

1.all articles in different formats (txt or doc)

2.a log file which records the processes and results

current version has some limitations:
 
1.It can't grap content such as hyperlink, images, special symbol, or resources hosted on other websites

2.It can only process the blogspot with certain blog archive structure: year as the top level, month year or month as the second level, article title as the third level

3.It only support English content now.

You can try blogspot ID such as yucoding (this is not my blog) and txt format at first.

**Saving the content to local folder as doc format takes some time and uses a lot of CPU, you have to wait for a while**.

##History

Check [Releases](https://github.com/checkcheckzz/blog-spider/releases) for detailed changelog.

##License

blog spider is licensed under the terms of the MIT License. See the [LICENSE file](https://github.com/checkcheckzz/blogger-spider/blob/master/LICENSE) for details.
