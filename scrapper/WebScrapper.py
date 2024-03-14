import bs4
import requests
from typing import Union

from rest_framework import status
from rest_framework.response import Response

from scrapper.AppConstants import AppConstants 

class WebScrapper :
    def __init__(self, URL : Union[str, None] = None):
        ''' Initialise Scrapper class for scrapping Data from Website '''
        URL = URL if URL is not None else AppConstants.BLOG_PATH_URL
        
        request = requests.get(URL, headers=AppConstants.HEADERS)
        self.soup = bs4.BeautifulSoup(request.content, AppConstants.PARSER)
    
    def get_menu_list_json(self) -> Response:
        ''' Get List Of Menu Items For Side Drawer '''
        careers = self.soup.find(AppConstants.Tags.ul).find(AppConstants.Tags.li, id = 'menu-item-1917')
        exam = self.soup.find(AppConstants.Tags.ul).find(AppConstants.Tags.li, id = 'menu-item-2812')
        degree = self.soup.find(AppConstants.Tags.ul).find(AppConstants.Tags.li, id = 'menu-item-9601')

        data = []

        data.append({
            AppConstants.TEXT : 'Career Options After 10th',
            AppConstants.BLOG : 'https://leverageedu.com/blog/list-of-courses-after-10th-standard/'
        })

        data.append({
            AppConstants.TEXT : 'Career Options After 12th',
            AppConstants.BLOG : 'https://leverageedu.com/blog/career-options-after-12th/'
        })

        data.append(self.list_to_json(careers))
        data.append(self.list_to_json(exam))
        data.append(self.list_to_json(degree))
    
        return Response(data = data , status= status.HTTP_200_OK)

    def get_content_json(self) -> Response:
        ''' Get Content Of a Blog or Article form The Url '''
        data = []
        article = self.soup.find(AppConstants.Tags.article)

        heading = article.find(AppConstants.Tags.h1)
        data.append({
                AppConstants.TAG: heading.name,
                AppConstants.CONTENT: heading.text
            })
        data.append({
            AppConstants.TAG : AppConstants.Tags.img,
            AppConstants.CONTENT : article.find(AppConstants.Tags.div, class_='post-media').find(AppConstants.Tags.img).get(AppConstants.src),
        })
        
        content = article.find(AppConstants.Tags.div, class_ = 'show-content')
        data.extend(self.extract_div(content))
        
        return Response(data = data , status= status.HTTP_200_OK)

    def get_home_json(self) -> Response:
        ''' Get Data Of Home Page Of the Website '''
        data = []
        alldiv = self.soup.find(AppConstants.Tags.main, id='main').find_all(AppConstants.Tags.div, class_ = 'article_category')

        for div in alldiv :
            sectiondata = {
            AppConstants.TITLE : div.find(AppConstants.Tags.h3).text,
            AppConstants.CONTENT: []
            }
            data.append(sectiondata)

            for div in div.find_all(AppConstants.Tags.div, class_ ='articlesView') :
                sectiondata[AppConstants.CONTENT].append(self.get_Home_details(div))

        return Response(data = data , status= status.HTTP_200_OK)

    def get_json_data(self) -> Response:
        ''' Get List of Blogs available for The Particular Career Option '''
        data = {
            AppConstants.TITLE : self.soup.find(AppConstants.Tags.h1, class_ = 'page-title').text,
            AppConstants.CONTENT : []
        }

        for article in self.soup.find(AppConstants.Tags.div, class_ = 'archive-wrap').find_all(AppConstants.Tags.article) :
            data[AppConstants.CONTENT].append(self.get_details(article))
        
        return Response(data = data , status= status.HTTP_200_OK)

    def get_Home_details(self, divtag : bs4.Tag) -> map:
        ''' Get Details of each catagory article of Home Page Of Website '''
        atag = divtag.find(AppConstants.Tags.a, class_ ='category-style')
        aimgtag = divtag.find(AppConstants.Tags.a, class_ = 'more-link')
        
        return {
            AppConstants.IMAGE : divtag.find(AppConstants.Tags.div, class_ = 'articleImg').find(AppConstants.Tags.img).get(AppConstants.src),
            AppConstants.CATAGORY : atag.find(AppConstants.Tags.span, class_ = 'label').text,
            AppConstants.CATAGORY_LINK : atag.get(AppConstants.href),
            AppConstants.TITLE : divtag.find(AppConstants.Tags.h4).text,
            AppConstants.LINK : aimgtag.get(AppConstants.href),
            AppConstants.TEXT : divtag.find_all(AppConstants.Tags.p)[-1].get_text(strip=True).split('\u2026')[0],    
        }       

    def get_details(self, article : bs4.Tag) -> map:
        ''' Get Details of each Blog of a Particular career Path '''
        return {
            AppConstants.IMAGE : article.find(AppConstants.Tags.img).get(AppConstants.src),
            AppConstants.CATAGORY : article.find(AppConstants.Tags.div, class_ = 'meta-category').find(AppConstants.Tags.span, class_ = 'label').text,
            AppConstants.TITLE : article.find(AppConstants.Tags.h2, class_ = 'entry-title').find(AppConstants.Tags.a).text,
            AppConstants.LINK : article.find(AppConstants.Tags.h2, class_ = 'entry-title').find(AppConstants.Tags.a).get(AppConstants.href),
            AppConstants.TEXT : article.find(AppConstants.Tags.div, class_ = 'entry-excerpt').get_text(strip=True).split('\u2026')[0],
            }

    def extract_table(self, soup : bs4.Tag) -> map:
        ''' Function To Extract Table Data'''
        # Extract and append table data (table tags)
        table = soup.find(AppConstants.Tags.table)
        rows = table.find_all(AppConstants.Tags.tr)
        table_data = []
        for row in rows:
            cells = row.find_all([AppConstants.Tags.th, AppConstants.Tags.td])
            row_data = []
            for cell in cells:
                row_data.append(cell.text)
            table_data.append(row_data)

        data = {
            AppConstants.TAG: AppConstants.Tags.table,
            AppConstants.CONTENT: table_data
            }
        return data
    
    def extract_list(self, list_tag : bs4.Tag) -> map:
        ''' Function To Get List Data '''
        data = {
            AppConstants.TAG : AppConstants.Tags.list,
            AppConstants.CONTENT : []
        }
        for i in list_tag.find_all(AppConstants.Tags.li) :
            data[AppConstants.CONTENT].append(
                {
                    AppConstants.TEXT : i.text,
                    AppConstants.LINK : i.find(AppConstants.Tags.a).get(AppConstants.href) if i.find(AppConstants.Tags.a) else None
                }
            )
        return data
    
    def extract_div(self, contant : bs4.Tag) -> list[map]:
        ''' Extract data from div '''
        data = []
        for i in list(contant.children) :
            name = i.name
            if name == AppConstants.Tags.div :
                data.extend(self.extract_div(i))
            elif name == AppConstants.Tags.ul :
                data.append(self.extract_list(i))
            elif name == AppConstants.Tags.ol :
                data.append(self.extract_list(i))
            elif name == AppConstants.Tags.figure and i.find(AppConstants.Tags.table) :
                data.append(self.extract_table(i))
            elif name == AppConstants.Tags.a and i.text.strip() != '':
                data.append({
                    AppConstants.TAG: i.name,
                    AppConstants.CONTENT: i.text,
                    AppConstants.LINK: i.get(AppConstants.href)
                })
            elif name in AppConstants.Tags.HEADERS_AND_PARAGRAPH and i.text.strip() != '':
                data.append({
                    AppConstants.TAG: i.name,
                    AppConstants.CONTENT: i.text
                })
        return data
    
    def list_to_json(self, element : bs4.Tag) -> map:
        ''' Function to convert HTML List to Json List '''
        data = {
            AppConstants.TEXT: element.find(AppConstants.Tags.a).text,
            AppConstants.ATTRIBUTE_LIST: []
                }
        # Find only the direct <li> children of the current <ul> element
        list_elements: list[bs4.Tag] = element.find(AppConstants.Tags.ul, recursive= False).find_all(AppConstants.Tags.li, recursive=False)

        for li_tag in list_elements:
            # Recursively process nested <ul> elements
            nested_list = li_tag.find(AppConstants.Tags.ul)
            if nested_list:
                data[AppConstants.ATTRIBUTE_LIST].append(self.list_to_json(li_tag))
            else:
                data[AppConstants.ATTRIBUTE_LIST].append(self.list_data(li_tag))
        return data

    def list_data(self, element : bs4.Tag) -> map:
        ''' Function to get Data From each Element of a list '''
        tag = element.find(AppConstants.Tags.a)
        return {
            AppConstants.TEXT : tag.string,
            AppConstants.BLOG : tag.get(AppConstants.href)
        }
