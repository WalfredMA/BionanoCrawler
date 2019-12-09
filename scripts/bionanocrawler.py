#!/usr/bin/python2.7

#######################usage of this script#################################
#
#script by walfred ma, Kwok lab, please do not share out without permission                                                                       		
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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import Queue
import sys
import getopt

##type of download data##
want_type='Assembly'

##the column save as filename, can be jobname or assembly name##
savename='name'

##the path or chrome browser, default is the default install path##
chromepath=''

##the path of chromer driver folder##
driverpath='./chromedriver'

##the output file path##
outputfile='findbionanolinks.txt'

ifsamplename=0
opts,args=getopt.getopt(sys.argv[1:],"w:u:p:s:c:d:o:")
for op, value in opts:
	if op=='-w':
		want_type=value
	
	if op=='-u':
		user=value
	
	if op=='-p':
		password=value

	if op=='-s':
		savename=value
	
	if op=='-c':
		chromepath=value

	if op=='-d':
		driverpath=value

	if op=='-o':
		outputfile=value
		
loginlink='http://169.230.142.202:3005/index.html'

link='http://169.230.142.202:3005/ProjectBrowser/Objects.html?projectpk=12'

####filtering rule here, can change by your self####
def filterrules(errornode, columns, assembly_nodes, downloadnode,want_type,savename,outputfile):
	
	##check if any error reported##
	error_status=errornode.get_attribute('class')
	
	if 'hide' not in error_status:
		
		return 1	
	
	##check if any active download link##
	ifdownload=downloadnode.get_attribute('class')
	
	if ifdownload is not None and 'not' in ifdownload:
		
		return 1
	
	##find all information in the table##
	name0=columns[0].text
	sample0=columns[1].text
	tag0=columns[2].text
	type0=columns[3].text
	date0=columns[4].text
	
	##filter by table text##
	if want_type not in type0:
		
		return 1
	
	if want_type=='Container' and  len(assembly_nodes)!=3:
	
		return 1
	
	downloadlink=downloadnode.get_attribute('href')
	
	
	##determine the name for each link, name can be used to name download file##
	if savename != 'sample' or (sample0 is None or len(sample0)<1):
		
		downloadname=name0
	
	else:
		
		downloadname=sample0
	
	
	print downloadname, downloadlink
	
	##save found link to file##
	with open(outputfile,mode='a') as f:
		
		print >>f, downloadname, downloadlink
		
		f.close()
		
	return 0

class Bionanobrowser():
	
	###init of the crawler, can edit parameter here###
	def __init__(self, driverpath, chromepath=''):
		
		if chromepath != '':
			options = webdriver.ChromeOptions()
			prefs = {"profile.default_content_settings.popups": 0,
				 "download.default_directory": r"{:s}".format(chromepath), "directory_upgrade": True}
			options.add_experimental_option("prefs", prefs)
			
			self.browser  = webdriver.Chrome(executable_path=driverpath, chrome_options=options)
		
		else:
			
			self.browser  = webdriver.Chrome(executable_path=driverpath)
	
	##login to bionano site##
	def login(self, user, password):
		
		global loginlink
		
		self.browser.get(loginlink)
		
		time.sleep(3)
		
		self.browser.find_element_by_xpath('//input[@id="username"]').send_keys(user)

		self.browser.find_element_by_xpath('//input[@id="password"]').send_keys(password)

		self.browser.find_element_by_xpath('//input[@type="submit"]').submit()
		
		time.sleep(3)
	
	##save cookie from website, can used for download file##
	def savecookie(self, cookiename='cookies.txt'):
		
		cookies_dict = {'email':'Stephen.Chow@ucsf.edu','fullname':'Irys','username':'Irys', 'userrole':'1', 'userpk':'13', 'projectpk':'12', 'projectbrowserpage':'1', 'token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IklyeXMiLCJmdWxsX25hbWUiOiJJcnlzIiwiZW1haWwiOiJTdGVwaGVuLkNob3dAdWNzZi5lZHUiLCJ1c2VycGsiOjEzLCJyb2xlIjoxLCJpYXQiOjE1Mzg3NTcwNTcsImV4cCI6MTU0MTM0OTA1N30.Nh8V0hq0cjht-HSSC3MAgB_q0hg5Po9JXVbhgtzxjLA'}
		
		cookie_content=['email','fullname','username', 'userrole', 'userpk', 'projectpk', 'projectbrowserpage', 'token']
		
		for cookie in self.browser.get_cookies():
			cookies_dict[str(cookie['name'])] = str(cookie['value'])
	
			
		with open('cookies.txt', mode='w') as f:
			
			for cookie_content0 in cookie_content:
				
				if cookie_content0 not in cookies_dict.keys():
					
					cookies_dict[cookie_content0]=''
			
				print >> f, '169.230.142.202	FALSE	/	FALSE	0	{:s}	{:s}'.format(cookie_content0, cookies_dict[cookie_content0])
		
		f.close()
	
	##open bionano site, can change the project by editing the project##
	def openlink(self):
		
		global link

		self.browser.get(link)

		time.sleep(5)
		
		lastpage=self.browser.find_elements_by_xpath('//a [@title="Go to the last page"]')[0]

		self.pagenum=int(lastpage.get_attribute('data-page'))

		self.currentpage=1
	
	##read each page of the bionano site##
	def readpage(self,want_type,savename,outputfile):
		
		##browser all jobs in the page##
		ids=self.browser.find_elements_by_xpath('//tbody [@role="rowgroup"]/tr')
		
		i=0
		repeat=0
		while i<len(ids):
			
			ii=ids[i]
			
			ii.click()
			
			time.sleep(0.1)
			
			##find informative nodes##
			errornode=self.browser.find_element_by_xpath('//tr [@ng-show="obCtrl.jobHasError"]')
							
			columns=ii.find_elements_by_xpath('.//td')
			
			assembly_nodes=self.browser.find_elements_by_xpath('//tr [@ng-repeat="item in obCtrl.ContainerDetails"]')
			
			downloadnode=self.browser.find_elements_by_xpath('//div [@class="panel-heading" and contains(text(),"Options")]/../div [@class="panel-body"]/div/a [not(parent::span) and contains(text(),"Download")]')
			
			downloadnode=[x for x in downloadnode if x.is_enabled()]
			
			##sometimes error, repeat 3 times##
			if len(downloadnode)==0:
				
				repeat=repeat+1
				
				if repeat>3:
					
					print 'not found link for ', columns[0].text
					
					i=i+1
				
				continue
			
			downloadnode=downloadnode[-1]
								
			##fitler wanted files and output links##
			filterrules(errornode, columns, assembly_nodes, downloadnode,want_type,savename,outputfile)
			
			i=i+1
			repeat=0

			
			
	
	##scroll to next page if there is any##	
	def nextpage(self):	
			
			if self.currentpage<self.pagenum:
			
				self.currentpage=self.currentpage+1

				page=self.browser.find_element_by_xpath('//a [@title="Go to the next page"]')

				self.browser.execute_script("arguments[0].click();", page)
				
				time.sleep(0.1)
			
			else:
				
				self.currentpage=self.currentpage+1
				



def main():
	
	bionanobrowser=Bionanobrowser(driverpath,chromepath)	
	
	bionanobrowser.login(user,password)
	
	bionanobrowser.savecookie()
	
	bionanobrowser.openlink()
	
	while bionanobrowser.currentpage <= bionanobrowser.pagenum:
		
		bionanobrowser.readpage(want_type, savename, outputfile)
		
		bionanobrowser.nextpage()
		
		

if __name__=='__main__':
	main()


	






