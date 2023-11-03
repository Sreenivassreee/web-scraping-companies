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
print("Total Main Catorory Links : "+str(len(main_catorogies_links)))

def write_to_excel(catorogy_link,company_url):
    each_company_response = requests.get(company_url)
    soup = BeautifulSoup(each_company_response.text, 'html.parser')
    company_div=soup.select_one('#main')
    company_name=company_div.find('h1').text
    data_table=soup.select_one('#company-detail')
    data_table=data_table.findAll('div')[1].findAll('dl')[1].find('dd').find('table')
    # [2].find('dd').find('table').find('tbody')
    # print(data_table)
    # #company-detail > div > dl:nth-child(2) > d
    
    business_type=''
    address=''
    for tr in data_table:
        col_name=tr.find('td').text
        if col_name=='Businss Type:':
            business_type=tr.findAll('td')[1].text
        elif col_name=='Address:':
            address==tr.findAll('td')[1].text
    catorogy_link=final_catogary_link
    company_link=company_url
    print(catorogy_link)
    print(company_link)
    print(company_name)
    print(business_type)
    print(address)

    # df = pd.DataFrame({'catorogy_link': catorogy_link,"company_link":company_link,"company_name":company_name,"business_type":business_type,"address":address})
    # excel_file='Data.csv'
    # df.to_csv(excel_file, index=False)
    # print(f"Data saved to {excel_file}")

for catorogy_link in main_catorogies_links:
    company_links=[]
    for page in range(1,100):
        print("Currectly Working on : "+str(page))
        final_catogary_link=base_url+catorogy_link+"/page-"+str(page)
        catorogy_response = requests.get(final_catogary_link)
        if catorogy_response.status_code == 200:
            soup = BeautifulSoup(catorogy_response.text, 'html.parser')
            list_of_companies=soup.select_one('#List-of-companies')
            if list_of_companies:
                for company in list_of_companies:
                    if company.find('dt').find('a').get('href'):
                        company_link=company.find('dt').find('a').get('href')
                        write_to_excel(final_catogary_link,company_link)
                        break
                    else:
                        break
            else:
                break
            
        else:
            break
    

print(catorogy_link)
print("------------------Hitting next -----------")
# print(len(company_links))


# /html/body/div/div[2]/div[3]/div[1]/div/dl[2]/dd/table/tbody
# /html/body/div/div[2]/h1



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
