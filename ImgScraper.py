import sys
import os
import selenium
import json
import urllib
import urllib.request
import argparse
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import InvalidSessionIdException
import http.client
from socket import timeout

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("Directory", help = "Specifies the directory to create the image class folders. Note: This will create a directory if it doesn't exist.")
    parser.add_argument("File", help = "Location of the txt file containing a list of search terms.")
    parse.args = parser.parse_args()

#Opens new Chromedriver browser window
def new_browser():
    new_browser.browser = webdriver.Chrome(#CHROMEDRIVER PATH GOES HERE)

#Creates file directory where images folders will be created
def new_dir():
        new_dir.directory = parse.args.Directory
        try:
            if not os.path.exists(new_dir.directory):
                os.makedirs(new_dir.directory)
                print(f" {new_dir.directory} directory successfully created.")
        except OSError as e:
            print(f"Creation of {new_dir.directory} failed.")
            print(e.errno)
            print(e.filename)
            print(e.strerror)

#Creates image class folders
def open_list():
        open_list.searchListLocation = parse.args.File
        open_list.searchList = open(open_list.searchListLocation, "r+")

        for query in open_list.searchList:
            pathTest = os.path.join(new_dir.directory, query)
            path = pathTest.replace('\n','')

            try:
                if not os.path.exists(f"{path}"):
                    os.makedirs(f"{path}")
                    print(f"{query} directory successfully created.")
            except OSError as e:
                print(f"Creation of {query} directory failed.")
                print(e.errno)
                print(e.filename)
                print(e.strerror)
        open_list.searchList.close()

#Checks to see if an element exists by trying to find it's xpath on a page
def check_exists_by_xpath(xpath):
    try:
        new_browser.browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

#Scrapes the images off Google
def scrape():
    scrape.totalImgs = 0
    for query in open(open_list.searchListLocation, "r+"):
        url = "https://www.google.com/search?q="+query+"&source=lnms&tbm=isch"
        new_browser.browser.get(url)
        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        scrape.counter = 0
        scrape.succounter = 0
        i = 0

        while i <= 2:
            for _ in range(400):
                new_browser.browser.execute_script("window.scrollBy(0,10000)")

            if(check_exists_by_xpath('//*[@id="smb"]') is True):
                try:
                    new_browser.browser.find_element_by_xpath('//*[@id="smb"]').click()
                except ElementNotVisibleException:
                    break

            i += 1

        for x in new_browser.browser.find_elements_by_xpath('//div[contains(@class,"rg_meta")]'):
            scrape.counter = scrape.counter + 1
            print(f"\n{scrape.succounter} of {scrape.counter} possible images successfully downloaded")
            print ("URL:",json.loads(x.get_attribute('innerHTML'))["ou"])

            img = json.loads(x.get_attribute('innerHTML'))["ou"]
            imgtype = json.loads(x.get_attribute('innerHTML'))["ity"]

            try:
                req = urllib.request.Request(img, headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})##img swapped for url
                raw_img = urllib.request.urlopen(req, timeout = 10).read()##.decode('utf-8')
                cleanQuery = query.replace('\n','')
                File = open(os.path.join(new_dir.directory, cleanQuery , cleanQuery + "_" + str(scrape.counter) + "." + imgtype), "wb")
                File.write(raw_img)
                File.close()
                scrape.succounter = scrape.succounter + 1
            except urllib.error.URLError as u:
                 print ("Image download failed", u.reason)
            except(InvalidSessionIdException,http.client.IncompleteRead, ConnectionError, timeout, http.client.HTTPException, http.client.BadStatusLine):
                continue
        scrape.totalImgs += scrape.succounter

#Returns number of images downloaded and closes the browser
def success():
    print (f"\n{scrape.totalImgs} pictures succesfully downloaded")
    new_browser.browser.close()
    print("\a")

def main():

    parse()
    new_browser()
    new_dir()
    open_list()
    scrape()
    success()
    exit()


if __name__ == "__main__":
    main()
