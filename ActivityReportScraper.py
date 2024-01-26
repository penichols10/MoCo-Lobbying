import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import os


def parseSection(fieldset, lobbyist, period):
    sectionNum = fieldset.legend.text
    sectionTotal = fieldset.find_all('span')[-1].text
    
    tables = fieldset.find_all('table')
    if len(tables):
        table = tables[0]
        df = pd.read_html(str(table))[0]
        df.to_csv(f'{lobbyist}/subtables/{period}/{lobbyist}_{sectionNum}.csv', index=False)
        
    return sectionNum, sectionTotal
    
    
def parseReport(url, lobbyist='testDir'):
    resp = requests.get(url)
    soup = bs(resp.content)
    reportingPeriod = soup.find('span', {'id':'ctl00_MainContent_LblHalf'}).replace(' ','')
    expenses = {'Period':reportingPeriod, 'Section': [], 'Total':[]}

    # Each section is a fieldset in a div - I do not love finding the div with hardcoded ID
    content = soup.find('div', {'id':'ctl00_MainContent_Detail'})
    sections = content.find_all('fieldset')

    for section in sections:
        num, total = parseSection(section, lobbyist, reportingPeriod)
        expenses['Section'].append(num)
        expenses['Total'].append(total)
        
    df = pd.read_csv(expenses)
    df.to_csv(f'{lobbyist}/subtable/{reportingPeriod}')
    
    
def parseLobbyist(lobbyist):
    # Build out folders, parse reports
    if lobbyist not in os.listdir():
        os.mkdir(f'{os.getcwd()}/{lobbyist}')
        os.mkdir(f'{os.getcwd()}/{lobbyist}/subtables')
        os.mkdir(f'{os.getcwd()}/{lobbyist}/subtables/Jan1-June30')
        os.mkdir(f'{os.getcwd()}/{lobbyist}/subtables/July1-Dec31')
    pass
    # Should not parse 1) periods that have not completed, 2) periods that have been processed    
parseLobbyist('testDir')
        
base_url = 'https://www2.montgomerycountymd.gov/Lobbyist/ViewReportingPublic.aspx?qtr=1&id=622'
