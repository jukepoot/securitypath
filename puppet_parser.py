#!/usr/bin/python -tt

#write a simple parser of /var/log/puppet.log
#import argparse for parsing arguments
#script should accept as an optional argument the year the
#file was created. 
#then the required file name as an arg


#import argparse from standard lib
import argparse 
import datetime
import dateutil.parser
import re
import collections




def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("filename",help="parse the given filename")
	parser.add_argument("-y","--year",help="parse file with given year",type=int)
	args = parser.parse_args()
	print("filename is: "+ args.filename)
	if args.year:
		print("year to use: " + str(args.year))
		#can call a function to check validity of this ?
	puppet_parser(args.filename)
	
	
def puppet_parser(file):
	#no year was given 
	#assume current year
	print(file)
	year = datetime.datetime.utcnow().year
	print("default year: "+ str(year))
	f = open(file,"rU")
	dump = f.readlines()
	f.close()
	 
 
	logDict = {}
	dumpline_list = []
	message_atrib = []
	proccess_atrib =[]
	hostname_atrib= []
	timedate_atrib= []
	processID_atrib = []
	#list containing all attributes 
	
	#pattern to match and group each finding if need call 
	pattern = re.compile(r'(^.+:..:..)\s(\S+)\s(\S+)(\[\d+\]):\s(.+$)')
	#group 1 = date
	#group 2 = hostname
	#group 3 = proccess
	#group 4 = PID
	#group 5 = message

	for each in dump:
		#print each
		dumpline_list.append(each)
	for each in dumpline_list:
		if pattern.match(each):
			#print(dateutil.parser.parse(pattern.match(each).group(1)))
			#create a list of each attribute 
			#then add each list to a dictionary with the time formatted 
			attrib_list = []




			hostnm = pattern.match(each).group(2)
			proccnm = pattern.match(each).group(3)
			pidnm = pattern.match(each).group(4)
			messnm = pattern.match(each).group(5)


			message_atrib.append(messnm)
			proccess_atrib.append(proccnm)
			time_date = dateutil.parser.parse(pattern.match(each).group(1))
			timedate_atrib.append(time_date)
			hostname_atrib.append(hostnm)
			processID_atrib.append(pidnm)
			#d = dateutil.parser.parse("2018-04-29T17:45:25Z")
			attrib_list.append(hostnm)
			attrib_list.append(proccnm)
			attrib_list.append(pidnm)
			attrib_list.append(messnm)
			#print(attrib_list)
			logDict[time_date] = attrib_list


		#print(k," value of",v) 
	print_log(logDict)
	uniq_process(proccess_atrib,logDict)
	hostnames(hostname_atrib)
	top_messages(message_atrib)
	
	
	
def parse_log(logDictionary):
	#get dictionary and paste it in order 
	for x in logDictionary:
		print x

def print_log(dic):
		#I didn't know how to use print functions as easily as with python 2 so ...
	#print entire log 
	for k, v in sorted(dic.items()):
		print "%s %s %s %s %s" % (k,v[0],v[1],v[2],v[3])


def uniq_process(proccessList):
	#unique processes sorted by appearance 

	proces = collections.Counter(proccessList).most_common()
	#testprocess = collections.Counter(dict.values(),key=process_sort)
	print("Unique Proccess(sorted): ")
	for each in proces:
		print("["+str(each[1])+"]" +" " + each[0])


def top_messages(messageList):
	#list top 10 messages in the file 
	messages = collections.Counter(messageList).most_common(10)
	print("Top 10 Messages: ")
	for each in messages:
		print(each[0])
def hostnames(hostnameList):
	hosts = collections.Counter(hostnameList)
	print("Hostsnames in file: ")
	for each in hosts:
		print(each)
if __name__ == '__main__':
	main()