#!/usr/bin/python3
import urllib.request, sys, http.client

if(len(sys.argv) >= 2):
    addr = sys.argv[1]
    if(len(sys.argv) >= 3):
        if(sys.argv[2] == "w"):
            ifwrite = "y"
            if(len(sys.argv) >= 4):
                fname = sys.argv[3]
            else:
                fname = "crawl.txt"
        else:
            ifwrite = "n"
else:
    addr = input("url: ")
    ifwrite = input("Write results to text file?(y/n): ")
    if(ifwrite == "y"):
        fname = input("filename: ")
source = ""
links = []
to_crawl = []
external_links = []

def openurl(url):
    try:
        u = urllib.request.urlopen("http://"+url)
        global source
        source = u.read()
        u.close()
        return True
    except (urllib.request.URLError, http.client.InvalidURL, UnicodeError):
        return False

def findlinks():
    src_len = len(source)
    i = 0
    while(i<src_len):
        if(source[i: i+6] == b"href=\""):
            increment = 6
            link = ""
            while(chr(source[i+increment]) != "\"" and chr(source[i+increment]) != "'"):
                link = link + chr(source[i+increment])
                increment+=1
            if(("://" in link) or ("www." in link) or ("mailto:" in link)):
                if(link not in external_links):
                    external_links.append(link)
            else:
                if(link not in links):
                    directory = ""
                    z  = link.split()
                    if(len(z)!=0 and z[-1]==""):
                        for inc in range(len(z)-2):
                            directory = directory + z[inc]+"/"
                    else:
                        for inc in range(len(z)-1):
                            directory = directory + z[inc]+"/"
                    if((link+directory) not in links):
                        links.append(link+directory)
                        to_crawl.append(link+directory)
            i+= increment-1

        elif(source[i:i+5] == b"src=\""):
            increment=6
            link = ""
            while(chr(source[i+increment]) != "\"" and chr(source[i+increment]) != "'"):
                link = link + chr(source[i+increment])
                increment+=1
            if(("://" in link) or ("www." in link) or ("mailto:" in link)):
                if(link not in external_links):
                    external_links.append(link)
            else:
                if(link not in links):
                    directory = ""
                    z  = link.split()
                    if(len(z)!=0 and z[-1]==""):
                        for inc in range(len(z)-2):
                            directory = directory + z[inc]+"/"
                    else:
                        for inc in range(len(z)-1):
                            directory = directory + z[inc]+"/"
                    if((link+directory) not in links):
                        links.append(link+directory)
                        to_crawl.append(link+directory)
            i+= increment-1

        elif(source[i:i+8] == b"action=\""):
            increment=8
            link = ""
            while(chr(source[i+increment]) != "\"" and chr(source[i+increment]) != "'"):
                link = link + chr(source[i+increment])
                increment+=1
            if(("://" in link) or ("www." in link) or ("mailto:" in link)):
                if(link not in external_links):
                    external_links.append(link)
            else:
                if(link not in links):
                    directory = ""
                    z  = link.split()
                    if(len(z)!=0 and z[-1]==""):
                        for inc in range(len(z)-2):
                            directory = directory + z[inc]+"/"
                    else:
                        for inc in range(len(z)-1):
                            directory = directory + z[inc]+"/"
                    if((link+directory) not in links):
                        links.append(link+directory)
                        to_crawl.append(link+directory)
                i+= increment-1
        i+=1

def filterto_crawl():
    cnt = 0
    while(cnt < len(to_crawl)):
        s = to_crawl[cnt]
        if((s[-1:] != "/") and (s[-5:] != ".html") and (s[-4:] != ".htm") and (s[-4:] != ".php") and (s[-4:] != ".asp")):
            del to_crawl[cnt]
        else:
            cnt+=1
def writefile(fname):
    file = open(fname, 'w')
    file.write(addr+":\n\n")
    for l in links:
        file.write(l+"\n")
    file.close()
def main():
    openurl(addr)
    findlinks()
    filterto_crawl()

    while(len(to_crawl) > 0):
        print(to_crawl[0])
        if(openurl(addr+to_crawl[0])):
            
            findlinks()
            filterto_crawl()
        del to_crawl[0]

    if(ifwrite == "y"):
        writefile(fname)
    
    links.sort()
    for l in links:
        print(l)
main()

