
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
base_url="http://www.business-yellowpages.com"

excel_file='Data.csv'
catorogy_links=[]
company_links=[]
company_names=[]
business_types=[]
addresses= []

def write_to_csv(catorogy_link,company_url,company_name,business_type,address):
    catorogy_links.append(catorogy_link)
    company_links.append(company_url)
    company_names.append(company_name)
    business_types.append(business_type)
    addresses.append(address)
    print(f"Added {catorogy_link}--   {company_name}--   {business_type}")



def read_company_details(catorogy_link,company_url):
    
    each_company_response = requests.get(company_url)
    time.sleep(1)
    soup = BeautifulSoup(each_company_response.text, 'html.parser')
    company_div=soup.select_one('#main')
    company_name=company_div.find('h1').text if company_div.find('h1') else "None"
    data_table=soup.select_one('#company-detail')
    data_table=data_table.findAll('div')[1].findAll('dl')[1].find('dd').find('table')
    business_type=''
    address=''
    for tr in data_table:
        col_name=tr.findAll('td')[0].text

        if col_name=='Businss Type:':
            business_type=tr.findAll('td')[1].text
        if col_name=='Address:':
            address=tr.findAll('td')[1].text

    write_to_csv(catorogy_link,company_url,company_name,business_type,address)


def getMainCatorogiesLinks():
    response = requests.get(base_url+"/italy/")
    time.sleep(1)

    soup = BeautifulSoup(response.text, 'html.parser')
    links =soup.select_one('#list_top_product_country > ul > ul')
    for li in links.findAll('li'):
        if li.find('a'):
            catorogy_link=li.find('a').get('href')
            company_links=[]
            for page in range(1,100):
                final_catogary_link=base_url+catorogy_link+"/page-"+str(page)
                print("Currectly Working on Page : "+str(catorogy_link+"/page-"+str(page)))

                catorogy_response = requests.get(final_catogary_link)
                time.sleep(1)
                soup = BeautifulSoup(catorogy_response.text, 'html.parser')
                list_of_companies=soup.select_one('#List-of-companies')
                # print(list_of_companies)
                try:
                    for company in list_of_companies:
                        if company.find('dt')!=None:
                            if company.find('dt').find('a').get('href'):
                                company_link=company.find('dt').find('a').get('href')
                                read_company_details(final_catogary_link,company_link)
                            else:
                                break
                        else:
                            break
                    else:
                        break
                except:
                    print("Error")
            continue



getMainCatorogiesLinks()

data={
    "catorogy_link":catorogy_links,
    "company_link":company_links,
    "company_name":company_names,
    "business_type":business_types,
    "address":addresses
}
df = pd.DataFrame(data)
df.to_csv(excel_file, index=False)
print(f"Data saved to {excel_file}")

