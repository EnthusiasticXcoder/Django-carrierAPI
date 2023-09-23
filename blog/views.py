import bs4
import requests

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

BLOG_PATH_URL = 'https://leverageedu.com/blog/'


class BlogListView(APIView):
    def post(self, request):
        try :    
            URL = request.data['url']
            request = requests.get(URL)
            soup = bs4.BeautifulSoup(request.content, 'html.parser')
            return self.get_json_data(soup)
        except Exception as e :
            return Response(data= str(e), status=status.HTTP_400_BAD_REQUEST) 
        
    def get(self, request):
        try :
            request = requests.get(BLOG_PATH_URL)
            soup = bs4.BeautifulSoup(request.content, 'html.parser')
            return self.get_home_json(soup)
        except Exception as e :
            return Response(data= str(e), status=status.HTTP_400_BAD_REQUEST) 
    
    def get_home_json(self, soup : bs4.BeautifulSoup) :
        data = []
        alldiv = soup.find('main', id='main').find_all('div', class_ = 'article_category')

        for div in alldiv :
            sectiondata = {
            'title' : div.find('h3').text,
            'contant' : []
            }
            data.append(sectiondata)

            for div in div.find_all('div', class_ ='articlesView') :
                sectiondata['contant'].append(self.get_Home_details(div))

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
        
    def get_json_data(self, soup : bs4.BeautifulSoup):
        data = {
            'title' : soup.find('h1', class_ = 'page-title').text,
            'contant' : []
        }

        for article in soup.find('div', class_ = 'archive-wrap').find_all('article') :
            data['contant'].append(self.get_details(article))
        
        return Response(data = data , status= status.HTTP_200_OK)

    def get_details(self, article : bs4.Tag):
        return {
            'img' : article.find('img').get('src'),
            'catagory' : article.find('div', class_ = 'meta-category').find('span', class_ = 'label').text,
            'title' : article.find('h2', class_ = 'entry-title').find('a').text,
            'link' : article.find('h2', class_ = 'entry-title').find('a').get('href'),
            'text' : article.find('div', class_ = 'entry-excerpt').get_text(strip=True).split('\u2026')[0],
            }

class BlogContantView(APIView):
    def post(self, request) :
        URL = request.data['url']
        request = requests.get(URL)
        soup = bs4.BeautifulSoup(request.text, 'html.parser')
        data = []
        article = soup.find('article')

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

    def extract_table(self, soup : bs4.Tag) :
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
    
    def extract_list(self, list_tag : bs4.Tag) :
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
    
    def extract_div(self, contant : bs4.Tag) :
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

class MenuListView(APIView):
    def get(self, request):
        ''' Function to Extract the cureer path and list them '''
        request = requests.get(BLOG_PATH_URL)
        soup = bs4.BeautifulSoup(request.text, 'html.parser')

        careers = soup.find('ul').find('li', id = 'menu-item-1917')
        exam = soup.find('ul').find('li', id = 'menu-item-2812')
        degree = soup.find('ul').find('li', id = 'menu-item-9601')

        data = []

        data.append(self.list_to_json(careers))
        data.append(self.list_to_json(exam))
        data.append(self.list_to_json(degree))
        data.append({
            'text' : 'Career Options After 12th',
            'blog' : 'https://leverageedu.com/blog/career-options-after-12th/'
        })


        return Response(data = data , status= status.HTTP_200_OK)



    def list_to_json(self, element : bs4.Tag) :
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

    def list_data(self, element : bs4.Tag) :
        tag = element.find('a')
        return {
            'text' : tag.string,
            'blog' : tag.get('href')
        }

