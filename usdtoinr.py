#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
import argparse
import re

def _xoom():
	r = requests.get('https://www.xoom.com/india/send-money')
	data = r.text

	soup = BeautifulSoup(data)

	for rate in soup.find_all('em'):
		return rate.text

def _all():
	r = requests.get('http://www.compareremit.com')
	print "[+] Requested information!"
	data = r.text
	print "[+] Grabbed all exchange rates online!"
	soup = BeautifulSoup(data)
	for rate in soup.find_all('div',{"class":"c_logo_box"}):
    		print rate.a.img['alt'] 
    		print rate.span.text

def _rate_calc():
	ratetext = _xoom()
	print "[+] Requested exchange rate from Xoom!"
	found = re.search("(?<=\=)(.*?)(?=I)", ratetext)
	print "[+] Located today's exhange rate!" 
	rate = float(found.group())
	print "[+] Converting USD to INR now..."
	amount = args.convert * rate
	return amount

def _paypal():
	ratetext = _xoom()
	print "[+] Requested exchange rate from Xoom!"
	found = re.search("(?<=\=)(.*?)(?=I)", ratetext)
	print "[+] Located today's exchange rate!" 
	rate = float(found.group())
	print "[+] Converting USD to INR now..."
	print "[+] Calculating amount left after PayPal's 4 percent fee..."
	amount = 0.96*(args.paypal*rate)
	return amount
	

parser = argparse.ArgumentParser(description="Script for USD to INR calculations")
parser.add_argument('-x', '--xoom', help='exchange rate from xoom.com', action='store_true')
parser.add_argument('-a', '--all', help='exchange rate from all major remit websites', action='store_true')
parser.add_argument('-c', '--convert', help='USD to INR conversion using current exchange rate', type=float)
parser.add_argument('-p', '--paypal', help='amount after deducting PayPal\'s 4 percent fees', type=float)
args = parser.parse_args()

print """               _ _        _           
 _   _ ___  __| | |_ ___ (_)_ __  _ __ 
| | | / __|/ _` | __/ _ \| | '_ \| '__|
| |_| \__ \ (_| | || (_) | | | | | |   
 \__,_|___/\__,_|\__\___/|_|_| |_|_|   

                          --by Pranshu
"""


if args.xoom:
	rate = _xoom()
	print "[i] Exchange Rate: " + rate
elif args.all:
	_all()
elif args.convert:
	amount = _rate_calc()
	print "\n[i]Amount in Rupees according to the exchange rate today: %f" %amount
elif args.paypal:
	amount = _paypal()
	print "\n[i]Amount in Rupees after deduction of Paypal's fees: %f" %amount
else:
	rate = _xoom()
	print "[i] Exchange Rate: " + rate
	#parser.print_help()
