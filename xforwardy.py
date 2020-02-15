#!/usr/bin/env python3

import requests
import sys
import validators
import os

usage = "Usage : \n\nxfowardy.py <options> <arguements>\n \nOptions : \n -u \t:\t URL of the Website \n -i \t:\t Input file of the URLS\n"
keyword = "xforwardy.com"
result_list = list()
header1 = {"Host": "xforwardy.com"}
header2 = {"X-Forwarded-Host": "xforwardy.com"}

print("""
        
       _  __    ____                                         __      
      | |/ /   / __/____   _____ _      __ ____ _ _____ ____/ /__  __
      |   /   / /_ / __ \ / ___/| | /| / // __ `// ___// __  // / / /
     /   |   / __// /_/ // /    | |/ |/ // /_/ // /   / /_/ // /_/ / 
    /_/|_|  /_/   \____//_/     |__/|__/ \__,_//_/    \__,_/ \__, /  
                                                            /____/   
 """)
													  

def is_redirect(status_code) :
	if status_code == 301 :
		return True
	elif status_code == 302 :
		return True
	else :
		return False


def process_file(url_file) :
	f = open(url_file,"r")
	for line in f :
		line = line.strip()
		custom_req(line)
		print("\r"+"Scanning : "+line)
	f.close()
	if len(result_list) == 0 :
		print("\nNo Vulnerable URL(s)")
	else :
		print("\nPotential Host Header Injection at :\n")
		for url in result_list :
			print(url)
	return
	
def custom_req(target_url) :
	target_url=target_url+"/"
	if validators.url(target_url) :
			response1=requests.get(target_url, headers=header1, allow_redirects=False)
			response2=requests.get(target_url, headers=header2, allow_redirects=False)
			response1_location=""
			response2_location=""
			
			if is_redirect(response1.status_code) :
				if len(response1.headers["Location"]) != 0 :	
					response1_location=response1.headers["Location"]
					
			response1_body=response1.content
			

			if is_redirect(response2.status_code) :
				if len(response2.headers["Location"]) != 0 :	
					response2_location=response2.headers["Location"]
					
			response2_body=response2.content
			
			
			if(response1_body.find(keyword) > -1  or response1_location.find(keyword) > -1 or response1.status_code==200 or response2_body.find(keyword) > -1 or response2_location.find(keyword) > -1) :
				result_list.append(target_url)
	else :
		print("\r"+"Malformed URL : "+target_url+"\r")
	return
	
if len(sys.argv) > 1 :
	if sys.argv[1] == '-u' :
		target_url=sys.argv[2]
		print("\nTarget : "+target_url)
		custom_req(target_url)
		
		if len(result_list) == 0 :
			print("\nNo Reflection of Custom Host at all !")
		else :
			print("\nPotential Host Header Injection at :")
			for url in result_list :
				print(url)
				
	elif sys.argv[1] == '-i' :
		print("\nReading from "+sys.argv[2])
		url_file = sys.argv[2];
		if os.path.isfile(url_file) :
			process_file(url_file)
		else:
			print("\nNot a Valid File")
	else :
		print(sys.argv)
		print(usage)
else :
	print("Too few arguements \n")
	print(usage)