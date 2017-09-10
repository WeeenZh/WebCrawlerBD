# WebCrawlerBD
Web crawler for BD in python

Project Development Summary (Design) Manual (Documentation Requirements)

Ⅰ project background
Baidu Post Bar is a broad information platform, where you can find the same interest through a simple search of the collective, to provide a wealth of information, some need to save a lot, especially some posts may soon be invalid, so I designed a " Text crawler "to meet this demand, will specify the contents of the post were saved as txt and jpg file, convenient and concise.

Ⅱ projects of the initial concept
1. Project Name:
"Multi-functional post it text crawler"
2. Main contents of the project:
Save the bar picture and the text to the local, and realize the preservation of the function of the form of diversification
3. Project implementation of several major modules:
Noise removal tools:
Text crawler implementation class:
Image reptile implementation class:
Start interface visualization class:
4. Target and implementation of the preset project:
Users can enter the interface through the GUI interface to download the information, according to the interface back to the information to achieve accurate reptile function.

Ⅲ project implementation plan
Development schedule
11/01 days ago to think about how to determine the theme of large operations
11/01 to complete the "project development process document"
Find the basics of reading the crawler
11/21 to write the first picture of the crawler program
11/28 will be the image reptiles into a class
11/29 Write the graphical user interface class incoming parameters
12/07 days ago to find regular expressions such as text reptiles required knowledge
12/08 days of text crawler pseudo code is complete
12/19 Japanese word crawler program written
12/20 Japanese word reptile package associated with graphical user interface
12/23 debugging increase "only look at the landlord" "floor display" and other options
12/24 days of the code of the rules
12/26 to complete the "project development summary"
2. Personnel division of project development:
Tao Wen Zheng: find information, view the page source code, to achieve the preparation of the program

3. List the key technologies in the project and how to acquire this knowledge:
1) graphical user interface: python textbook
2) Web page HTML code view and meaning: network data
3) regular expression matching: network data
4) text noise removal: network data
5) file write: network data
6) exception capture processing: python textbook

Ⅳ project support conditions
1. What computer system environment:
"Multi-function post bar graphic crawler" in the win10 64bit computer environment development completed;
2. Development of the software used by the system:
Used to develop part of Python 3.4, Python 3.5
And then all converted to Python 2.7.11, using SublimeText 3 prepared;
3. Development of auxiliary software tools used:
Sublime Text 3;
Five detailed development narration and implementation function
1. Program structure description:
1) the top of a graphical user interface to guide the user input the required parameters of the crawler: post code, whether to see the landlord / display floor number, folder and picture name, together with the text reptiles;
2) text crawler will download the HTML code, the use of regular expressions to filter the required text, call the removal of noise tools to organize, save the text file;
3) and then send the parameters to the picture reptile, download the HTML code, use the policy expression filter image URL, downloaded by the urlretrieve remote image, rename.
