#list_top_product_country > ul > ul

import urllib3
from bs4 import BeautifulSoup
http = urllib3.PoolManager()
import requests

base_url="http://www.business-yellowpages.com"

def getMainCatorogiesLinks():
    response = requests.get(base_url+"/italy/")
    soup = BeautifulSoup(response.text, 'html.parser')  
    lis=[]
    links =soup.select_one('#list_top_product_country > ul > ul')
    for li in links.findAll('li'):
        if li.find('a'):
            lis.append(li.find('a').get('href'))
    return lis


main_catorogies_links=getMainCatorogiesLinks()
print("TOTal Main Catorory Links : "+str(len(main_catorogies_links)))
company_links=[]
for catorogy_link in main_catorogies_links:
    for page in range(1,100):
        print("Currectly Working on : "+str(page))
        catorogy_response = requests.get(base_url+catorogy_link+"/page-"+str(page))
        if catorogy_response.status_code == 200:
            soup = BeautifulSoup(catorogy_response.text, 'html.parser')
            list_of_companies=soup.select_one('#List-of-companies')
            print(page)
            print(list_of_companies)
            for company in list_of_companies:
                company_link=company.find('dt').find('a').get('href')
                company_links.append(company_link)
        else:
            break
    break
# print(len(company_links))






# List-of-companies












# //*[@id="list_top_product_country"]/ul/ul/li[1]/text()
#list_top_product_country > ul > ul
# if response.status_code == 200:
#     soup = BeautifulSoup(response.text, 'html.parser')

#     links = [link.get('href') for link in soup.find_all('a')]

#     df = pd.DataFrame({'Links': links})

#     excel_file = 'C:\\Users\\kesimi.r.reddy\\OneDrive - Accenture\\U4b\\ItalyClawler.xlsx'
#     df.to_excel(excel_file, index=False)
#     print(f"Data saved to {excel_file}")

