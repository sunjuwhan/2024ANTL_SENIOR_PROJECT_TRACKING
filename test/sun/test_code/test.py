import urllib.request

from bs4 import BeautifulSoup
with open("/Users/seonjuhwan/Documents/GitHub/2024ANTL_SENIOR_PROJECT_TRACKING/test/sun/test_code/US08621662-20140107.XML","r",encoding="utf8") as patent_xml:
    xml=patent_xml.read()

soup=BeautifulSoup(xml,"lxml")

inventiont_title_tag=soup.find("invention-title")
print(inventiont_title_tag.get_text())