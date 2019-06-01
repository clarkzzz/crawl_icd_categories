#%%
from bs4 import BeautifulSoup
import pandas as pd
import requests

#%%
# the initial page that contains the major groups of ICD categories
url = 'https://www.icd10data.com/ICD10CM/Codes'
response = requests.get(url)
content = response.content
parser = BeautifulSoup(content, 'html.parser')

#%%
# retrive the 1st level ICD categories from the initial page (ex: 'A00-B99', 'C00-D49')
level1_data = parser.select('a')[58:79]
level1_categories = []
for item in level1_data:
    temp = str(item)[-11:-4]
    level1_categories.append(temp)

#%%
# define a function that takes in an 1st level ICD category and retrive its corresponding 2nd level ICD categories
def map1_2(icd):
    list = []
    url2 = url + '/' + icd
    response = requests.get(url2)
    content = response.content
    parser = BeautifulSoup(content, 'html.parser')
    div = parser.find_all('ul', class_='i51')
    for each in div:
        links = each.find_all('a', class_='identifier')
    for link in links:
        temp = str(link)[-11:-4]
        list.append(temp)
    return list

#%%
# for each 1st level ICD categories, retrive its corresponding subcategories and build them into a dictionary
map12 = {}
for each in level1_categories:
    map12[each] = list()
    map12[each].extend(map1_2(each))

#%%
# construct the final list of URLs for each individual ICD Category
list_url = []
for k,v in map12.items():
    for each in v:
        list_url.append(url + '/' + k + '/' + each)

#%%
%%timeit
map = {}
for each_url in list_url:
    response = requests.get(each_url)
    content = response.content
    parser = BeautifulSoup(content, 'html.parser')
    div = parser.find_all('ul', class_='i51')
    for each in div:
        descriptions = each.find_all('li')
        for description in descriptions:
            category = str(description)[70:73]
            text = str(description.text)[6:-10]
            map[category] = text

#%%
df_map = pd.DataFrame.from_dict(map, orient='index')
df_map = df_map.reset_index()
df_map.columns = ['Category Code', 'Category Description']

#%%
df_map.to_csv('D:\Clark\Downloads\icd_categories.csv')
