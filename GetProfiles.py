import requests
from bs4 import BeautifulSoup
import sys
import os

DOWNLOADLOC = ".\downloads"
# TODO: Crete Override for download location

def usage():
	print("Define names and steam profiles in profiles.cfg")
	print(".\GetProfiles.py [-h] [--help]  prints this message")
	print("Use Format: [Name][\\t][Stean Profile Link]")
	print("# are comments")
	print("[\\t] means tab")

def main():
	if(not os.path.exists(DOWNLOADLOC)):
		os.mkdir(DOWNLOADLOC)
	if(not os.path.exists(".\\profiles.cfg")):
		print("profiles.cfg missing")
		exit()
	friends = readProfileConfig()
	downloadProfiles(friends)

def downloadProfiles(friends):
	for friend in friends:
		http = requests.get(friends[friend])

		soup = BeautifulSoup(http.text, 'html5lib')
		AvatarDiv = soup.find_all("div", {"class": "playerAvatarAutoSizeInner"})
		image = AvatarDiv[0].find_all("img")
		image = str(image[-1]["src"])

		imagedata = requests.get(image)

		if(imagedata.status_code != 200):
			print(f"Couldn't download {friend}")
			continue

		print(f"Saving {friend} ")
		with open(f".\\downloads\\{friend}.jpg","wb") as f:
			f.write(imagedata.content)


def readProfileConfig():
	friends = {}
	with open("profiles.cfg","r") as f:
		forline in f:
			name,link = lineParser(line.strip())
			if name == None:
				continue
			friends[name] = link
	return friends

def lineParser(line):
	if(len(line) == 0):
		return (None,None)
	if line[0] == "#":
		return (None,None)

	temp = line.split("\t")
	return (temp[0],temp[-1])


if __name__ == '__main__':
	if(len(sys.argv) > 1):
		usage()
	else:
		main()
