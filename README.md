[![logo](imgs/bloggerlogo.jpg)](https://github.com/checkcheckzz/blogger-spider)  
[![logo](imgs/wordpresslogo.jpg)](https://github.com/checkcheckzz/blogger-spider)

> Grab and save articles from Blogger, Wordpress

##Example

This Python program grabs the content of articles from a blogspot.com, wordpress.com account.

Input: bogspot.com/wordpress.com ID and format you want to save.

Output (to a local folder the python program runs):

1.all articles in different formats (txt or doc)

2.a log which records the processes and results

This first version has some limitations:
 
1.It can't load content such as hyperlink, images, special symbol, or resources hosted on other websites

2.It can only process the blogspot or wordpress with certain blog archive structure: year as the top level, month year or month as the second level, article title as the third level

3.It only support English content now.

You can try blogspot ID such as yucoding (this is not my blog) and txt format at first.

##Note

1.Save the content to local as doc format takes some time and uses a lot of CPU, you have to wait.

##How to run

The fast way is to download the exe file:

[dropbox link](<https://www.dropbox.com/sh/lfhgu02asw1ebqp/f6zJuZDTJJ>)

Put the exe file in an empty folder, and run it.  

If you want to run the python file, you need first install the package pywin32 for python 2.7:


[pywin32](<http://sourceforge.net/projects/pywin32/files/pywin32/Build%20218/>)

then

    git clone https://github.com/checkcheckzz/blogger-spider.git
    cd blogger-spider
    python blogv1.py
    
##Possible improvement in next version

1.Add GUI and let user to choose which article they want to download 

2.Improve the regex part to handle more complex archive structure 

3.Grab pictures from article and save them in the proper position

4.Use multiprocess to speed the saving process (GIL in python prevents multithread from working here)

5.Build a http pool to replace urllib2 

6.Write the test code


##License

blog spider is licensed under the terms of the MIT License. See the [LICENSE file](https://github.com/checkcheckzz/blogger-spider/blob/master/LICENSE) for details.
