from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from Scrapper.scrapper import Scrapper
from Scrapper.AppConstants import AppConstants

class BlogListView(APIView):
    def post(self, request):
        ''' Get List of Blogs available in the Particular career Path URL '''
        try :    
            URL = request.data[AppConstants.URL_FIELD]
            scrapper = Scrapper(URL=URL)
            return scrapper.get_json_data()
        except Exception as e :
            return Response(data= str(e), status=status.HTTP_400_BAD_REQUEST) 
        
    def get(self, request):
        ''' Get List Of Blogs in The Home Page Of the App '''
        try :
            scrapper = Scrapper()
            return scrapper.get_home_json()
        except Exception as e :
            return Response(data= str(e), status=status.HTTP_400_BAD_REQUEST) 
    
    
class BlogContantView(APIView):
    def post(self, request):
        ''' Get Content of the Blog For The Perticular URL '''
        try :
            URL = request.data[AppConstants.URL_FIELD]
            scrapper = Scrapper(URL=URL)
            return scrapper.get_content_json()
        except Exception as e :
            return Response(data= str(e), status=status.HTTP_400_BAD_REQUEST) 
    
        
    
class MenuListView(APIView):
    def get(self, request):
        ''' Function to Extract the career path and list them '''
        try :
            scrapper = Scrapper()
            return scrapper.get_menu_list_json()
        except Exception as e :
            return Response(data= str(e), status=status.HTTP_400_BAD_REQUEST) 
