#!/usr/bin/python
"""A parser of /var/log/puppet.log.


"""


import argparse 
from datetime import datetime
import dateutil.parser
import re
import collections
import os


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		help="parse the given filename", type=str, 
		dest="filename", action="store")
	parser.add_argument(
		"-y","--year", help="parse file by setting start year", 
		type=int, dest="year", action="store")
	args = parser.parse_args()
	if args.year:
		print("year to use: {0:d}".format(args.year))
		year = args.year

	else: #build year for date parsing
		year = datetime.utcfromtimestamp(
			os.stat(args.filename).st_birthtime).year
		# print("creation of file: {0:d}".format(year))

	puppet_parser(args.filename,year)


def puppet_parser(filepath, year):
	"""Accepts the puppet file path and parses it out by calling other functions.

	"""

	# pattern to match from log file and group each finding for referencing
	# pattern looks for a time foormat (x:x:x)any text after which is
	# followed by the process and so on 
	pattern = re.compile(
		r'(^.+:..:..)\s(\S+)\s(\S+)(\[\d+\]):\s(.+$)')
	#group 1 = date
	#group 2 = hostname
	#group 3 = proccess
	#group 4 = PID
	#group 5 = message
	
	# add to list for counter purposes 
	message_list = []
	proccess_list =[]
	hostname_list= []
	processID_list = []
	
	looped = 0
	with open(filepath, "rU") as f:
		for line in f:
			if not pattern.match(line):
				continue
 
			current_date = pattern.match(line).group(1)
			if looped >= 1:
				if (dateutil.parser.parse(prv_date).month <
					dateutil.parser.parse(current_date).month):
					year+=1
			
			set_date = (current_date + " " + str(year))
			hostname_list.append(pattern.match(line).group(2))
			proccess_list.append(pattern.match(line).group(3))
			processID_list.append(pattern.match(line).group(4))
			message_list.append(pattern.match(line).group(5))
			
			prv_date = current_date
			looped+=1
				

	uniq_process(proccess_list)
	host_names(hostname_list)
	top_messages(message_list)
	
	
def uniq_process(proccessList):
	"""Unique processes.

	"""

	uniq_list = collections.Counter(proccessList).most_common()
	print("Unique Proccess: ")
	for each in uniq_list:
		print("[{0:d}] {1:s}").format(each[1],each[0])


def top_messages(messageList):
	"""List top 10 messages in the file.

	"""

	messages = collections.Counter(messageList).most_common(10)
	print("Top 10 Messages: ")
	for each in messages:
		print(each[0])


def host_names(hostnameList):
	"""Prints hostnames from list.

	"""
	
	hosts = collections.Counter(hostnameList)
	print("Hostsnames in file: ")
	for each in hosts:
		print(each)


if __name__ == '__main__':
	main()