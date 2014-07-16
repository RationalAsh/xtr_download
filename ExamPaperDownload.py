import mechanize
import urllib2
from bs4 import BeautifulSoup
import webbrowser
from urllib2 import urlopen, URLError, HTTPError
import os

#Funtion that finds the url to the
#first pdf in the reversed string
def find_first_pdf(html, url):
    #find first occurence of .pdf extension
    pdf_st = html.find('"fdp.')

    #If no more pdfs are found let the program know
    if(pdf_st == -1):
        return "END", 0

    #Find the ending index of pdf
    pdf_en = html.find('=', pdf_st)

    #unflip the string
    pdf_str = html[pdf_st+1:pdf_en-1]

	#In the xtremepapers website the pdf links
    #are only filenames. So I need to append the 
    #Filenames with the url of the page to get the
    #URL of the actual pdf
    pdf = pdf_str[::-1]
    download_url = url + pdf
    return download_url, pdf_en+1


#Funciton to find all the pdfs in
#the html of the page
def find_all_pdfs(html_rev, url):
    #list of download urls
    papers = []

    curr_url = ''
    break_point = 0

    #Loop through the html to find all download links
    while(True):
        curr_url, break_point = find_first_pdf(html_rev, url)
        if(curr_url == "END"):
            break
        papers.append(curr_url)
        html_rev = html_rev[break_point:]
    return papers

#Function that downloads a file
#given by the url
def dlfile(url):
    # Open the url
    try:
        f = urlopen(url)
        print "downloading " + url

        # Open our local file for writing
        with open(os.path.basename(url), "wb") as local_file:
            local_file.write(f.read())
        return 1

    #handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
        return -1
    except URLError, e:
        print "URL Error:", e.reason, url
        return -1

#Function that downloads all the files in a list
def download_all_files(papers):
    counter=1
    for url in papers:
        dlflag = dlfile(url)
        if(dl_flag == 1):
            print "\n Yay! File #%d downloaded!\n" %(counter)
        else:
            print "\n Download of file #%d failed. :(" %(counter)
        counter = counter+1

url = raw_input("Enter the Xtremepapers web address: ")
#Set up the browser emulation
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6')]
br.set_handle_robots(False) # ignore robots

#Connect and retrrieve data from url and 
#store html in a string
br.open(url)
html = br.response().read()

#Reverse the string
html_rev = html[::-1]
#Declare list that will contain the list
#of download links
papers = []
#Fill the list with download links
papers = find_all_pdfs(html_rev, url)
#For testing purposes
tes_papers = papers[0:3]
#function that downloads all the files in the list
download_all_files(tes_papers)
