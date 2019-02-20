#!/usr/bin/python
""" A parser of /var/log/puppet.log."""


import argparse 
import datetime
import dateutil.parser
import re
import collections
import os


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		help="path to the puppet log", type=str, 
		dest="filename", action="store")
	parser.add_argument(
		"-y","--year", help="year format:XXXX", 
		type=int, dest="year", action="store")
	args = parser.parse_args()
	# Puppet logs use syslog format therefor have no year we have to base
	# ourselves on the creation of the file as a base unless a year is given 

	file_stat = os.stat(args.filename)
	file_birth = file_stat.st_birthtime
	file_year = datetime.datetime.utcfromtimestamp(file_birth).year
	if args.year:
		year = args.year
		print("Year to use: {0:d}".format(args.year))
	else: 
		year = file_year
		print("Creation of file: {0:d}".format(year))


	if(year < file_year):
		print("Year: {0:d} is below file creation date: {1:d}").format(year,file_year)
	else:
		puppet_parser(args.filename,year,file_birth)


def puppet_parser(filepath, year, file_birth):
	""" Accepts the puppet file path and parses it out by calling other functions."""

	# Pattern to match from log file and group each finding for referencing
	# pattern looks for a time foormat (x:x:x)any text after which is
	# followed by the process and so on. 
	pattern = re.compile(
		r'(^.+:..:..)\s(\S+)\s(\S+)(\[\d+\]):\s(.+$)')
	#group 1 = date
	#group 2 = hostname
	#group 3 = proccess
	#group 4 = PID
	#group 5 = message
	
	#collection for results
	hostname_col = collections.Counter()
	process_col = collections.Counter()
	message_col = collections.Counter()
	processID_col = collections.Counter()
	
	looped = 0
	newyear = False
	with open(filepath, "rU") as f:
		for line in f:
			if not pattern.match(line):
				continue
 
			current_month = dateutil.parser.parse(pattern.match(line).group(1)).month
			if looped == True:
				if (previous_month < current_month):
					newyear = True
			# Increments the year when the month has decreased signaling start of a new year
			if newyear==True:
				year+=1
			if newyear==False:

				hostname_col[(pattern.match(line).group(2))] +=1
				process_col[(pattern.match(line).group(3))] +=1
				processID_col[(pattern.match(line).group(4))] +=1
				message_col[(pattern.match(line).group(5))] +=1
			
			previous_month = current_month
			looped = True
				

	uniq_process(process_col)
	host_names(hostname_col)
	top_messages(message_col)
	
	
	
def uniq_process(proccessCol):
	"""Unique processes."""

	uniq_list = proccessCol.most_common()
	print("Unique Proccess: ")
	for each in uniq_list:
		print("[{0:d}] {1:s}").format(each[1],each[0])


def top_messages(messageCol):
	"""List top 10 messages in the file."""

	messages = messageCol.most_common(10)
	print("Top 10 Messages: ")
	for each in messages:
		print(each[0])


def host_names(hostnameCol):
	"""Prints hostnames from list."""
	
	print("Hostsnames in file: ")
	for each in hostnameCol:
		print(each)


if __name__ == '__main__':
	main()