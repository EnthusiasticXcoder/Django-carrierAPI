import bs4
import requests
from typing import Union

from rest_framework import status
from rest_framework.response import Response

class Scrapper :
    def __init__(self, URL : Union[str, None] = None):
            
        BLOG_PATH_URL = 'https://leverageedu.com/blog/'

        HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
            "X-Amzn-Trace-Id": "Root=1-62d8036d-2b173c1f2e4e7a416cc9e554", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-GB"
            }

        URL = URL if URL is not None else BLOG_PATH_URL
        
        request = requests.get(URL, headers=HEADERS)
        self.soup = bs4.BeautifulSoup(request.content, 'html.parser')
    
    def get_menu_list_json(self) -> Response:
        careers = self.soup.find('ul').find('li', id = 'menu-item-1917')
        exam = self.soup.find('ul').find('li', id = 'menu-item-2812')
        degree = self.soup.find('ul').find('li', id = 'menu-item-9601')

        data = []

        data.append({
            'text' : 'Career Options After 10th',
            'blog' : 'https://leverageedu.com/blog/list-of-courses-after-10th-standard/'
        })

        data.append({
            'text' : 'Career Options After 12th',
            'blog' : 'https://leverageedu.com/blog/career-options-after-12th/'
        })

        data.append(self.list_to_json(careers))
        data.append(self.list_to_json(exam))
        data.append(self.list_to_json(degree))
    
        return Response(data = data , status= status.HTTP_200_OK)

    def get_content_json(self) -> Response:
        data = []
        article = self.soup.find('article')

        heading = article.find('h1')
        data.append({
                "tag": heading.name,
                "content": heading.text
            })
        data.append({
            "tag" : "img",
            "content" : article.find('div', class_='post-media').find('img').get('src'),
        })
        
        contant = article.find('div', class_ = 'show-content')
        data.extend(self.extract_div(contant))
        
        return Response(data = data , status= status.HTTP_200_OK)

    def get_home_json(self) -> Response:
        data = []
        alldiv = self.soup.find('main', id='main').find_all('div', class_ = 'article_category')

        for div in alldiv :
            sectiondata = {
            'title' : div.find('h3').text,
            'contant' : []
            }
            data.append(sectiondata)

            for div in div.find_all('div', class_ ='articlesView') :
                sectiondata['contant'].append(self.get_Home_details(div))

        return Response(data = data , status= status.HTTP_200_OK)

    def get_json_data(self) -> Response:
        data = {
            'title' : self.soup.find('h1', class_ = 'page-title').text,
            'contant' : []
        }

        for article in self.soup.find('div', class_ = 'archive-wrap').find_all('article') :
            data['contant'].append(self.get_details(article))
        
        return Response(data = data , status= status.HTTP_200_OK)

    def get_Home_details(self, divtag : bs4.Tag):
        atag = divtag.find('a', class_ ='category-style')
        aimgtag = divtag.find('a', class_ = 'more-link')
        
        return {
            'img' : divtag.find('div', class_ = 'articleImg').find('img').get('src'),
            'catagory' : atag.find('span', class_ = 'label').text,
            'catagorylink' : atag.get('href'),
            'title' : divtag.find('h4').text,
            'link' : aimgtag.get('href'),
            'text' : divtag.find_all('p')[-1].get_text(strip=True).split('\u2026')[0],    
        }       

    def get_details(self, article : bs4.Tag):
        return {
            'img' : article.find('img').get('src'),
            'catagory' : article.find('div', class_ = 'meta-category').find('span', class_ = 'label').text,
            'title' : article.find('h2', class_ = 'entry-title').find('a').text,
            'link' : article.find('h2', class_ = 'entry-title').find('a').get('href'),
            'text' : article.find('div', class_ = 'entry-excerpt').get_text(strip=True).split('\u2026')[0],
            }

    def extract_table(self, soup : bs4.Tag):
        ''' Function To Extract Table Data'''
        # Extract and append table data (table tags)
        table = soup.find('table')
        rows = table.find_all('tr')
        table_data = []
        for row in rows:
            cells = row.find_all(['th', 'td'])
            row_data = []
            for cell in cells:
                row_data.append(cell.text)
            table_data.append(row_data)

        data = {
            "tag": "table",
            "content": table_data
            }
        return data
    
    def extract_list(self, list_tag : bs4.Tag):
        ''' Function To Get List Data '''
        data = {
            'tag' : 'list',
            'content' : []
        }
        for i in list_tag.find_all('li') :
            data['content'].append(
                {
                    'text' : i.text,
                    'link' : i.find('a').get('href') if i.find('a') else None
                }
            )
        return data
    
    def extract_div(self, contant : bs4.Tag):
        ''' Extract data from div '''
        data = []
        for i in contant.children :
            match i.name :
                case 'div' :
                    data.extend(self.extract_div(i))
                case 'ul' :
                    data.append(self.extract_list(i))
                case 'ol' :
                    data.append(self.extract_list(i))
                case 'figure' :
                    if i.find('table') :
                        data.append(self.extract_table(i))
                case 'a' :
                    if i.text.strip() != '' :
                        data.append({
                            "tag": i.name,
                            "content": i.text,
                            "link" : i.get('href')
                        })
                case _ :
                    if i.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6' ] and i.text.strip() != '':
                        data.append({
                            "tag": i.name,
                            "content": i.text
                        })
        return data
    
    def list_to_json(self, element : bs4.Tag):
        data = {
            "text": element.find('a').text,
            "attlist": []
                }
        # Find only the direct <li> children of the current <ul> element
        list_elements = element.find('ul', recursive= False).find_all('li', recursive=False)

        for li_tag in list_elements:
            # Recursively process nested <ul> elements
            nested_list = li_tag.find('ul')
            if nested_list:
                data["attlist"].append(self.list_to_json(li_tag))
            else:
                data["attlist"].append(self.list_data(li_tag))
        return data

    def list_data(self, element : bs4.Tag):
        tag = element.find('a')
        return {
            'text' : tag.string,
            'blog' : tag.get('href')
        }
