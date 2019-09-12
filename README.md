# BionanoCrawler
Web Crawler for Bionano server
#######################usage of this script#################################
#
#script by walfred ma, Puilab, please do not share out without permission                                                                       		
#this is a script recommand run on local computer instead of server 
#please make sure you have 500Mb memory and efficient internet connection to ucsf inner network when running this
#
#----usage: 
#		1. run in python2.7 
#		2. can in IDE or by bash command: python2.7 bionanocrawler.py [-options ]
#(after this script finished):
#		3.copy text of cookie.txt and findbionanolinks.txt to the server you want to download
# 		4.download by running this command on bash: 
#.                  fileItemString=($(cat  bionanodownloadlink.txt |tr "\ " "," |tr "\n" "\ "));for line in ${fileItemString[@]}; do row=($(echo $line | tr "," "\ ")); wget --load-cookies cookie.txt -O "${row[0]}".tar.gz "${row[1]}"; done
#		5.all files then can be sequencially downloaded to the current folder.
#
#-----requirements: 
#			   1. python selenium package, can be installed by "sudo pip install selenium" ,https://selenium-python.readthedocs.io/installation.html
#			   2. google chrome browser, if not installed on default folder, please indicate in the input					   
#			   3. google chrome diver, http://chromedriver.chromium.org/getting-started
#			
#-----what is does:
#              1. access the page of bionano server and obtain cookies, save to cookie.txt
#	       2. find all download link of target files, and save them to default findbionanolinks.txt, has option to redirect to other file
#
#-----all optional parameters: 
#               -w, the type if data want to download, default is the Container
#		-u, username for login, default setted
#		-p, password for login, default setted
#		-s, how the save file is named, by assembly or jobnames (default)
# 		-c, chromepath, default is the default insteal folder	
#		-d, driver path, default is ./chromedriver
#		-o, output path, where the links save, 	default is ./findbionanolinks.txt					                                                                      
#######################usage of this script#################################
