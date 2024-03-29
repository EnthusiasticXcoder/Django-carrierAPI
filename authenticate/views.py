from django.contrib.auth.models import User

from rest_framework import status, response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import authenticate
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from scrapper.AppConstants import AppConstants      

from .serializers import UserSerialiser

class LoginView(APIView) :
    def get(self, request):
        ''' No Get Method Allowed in This Rout'''
        data = {
            AppConstants.USERNAME: AppConstants.MESSAGES.ENTER_USERNAME, 
            AppConstants.PASSWORD: AppConstants.MESSAGES.ENTER_PASSWORD
        }
        return response.Response(data= data, status=status.HTTP_200_OK)
    
    def post(self, request) :
        data : dict = request.data
        username = data.get(AppConstants.USERNAME)
        password = data.get(AppConstants.PASSWORD)
        return self.__Login_User(username = username, password = password)

    def __Login_User(self, username, password) :
        ''' Methord to cheack user credentials and login user with credentials'''
        try :
            user = authenticate(username = username, password = password)
            if user is not None :
                token, _ = Token.objects.get_or_create(user = user)
                serialiser = UserSerialiser(instance=user)
                payload = serialiser.data
                payload.pop(AppConstants.PASSWORD)
                return response.Response(data= {AppConstants.TOKEN: str(token.key), AppConstants.PAYLOAD: payload}, status= status.HTTP_200_OK)
            else :
                return response.Response({AppConstants.MESSAGE : AppConstants.MESSAGES.USER_NOT_FOUND,}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e :    
            return response.Response(data= str(e), status=status.HTTP_400_BAD_REQUEST)    

class RegesterView(APIView):
    def get(self ,request):
        ''' No Get Method Allowed in This Rout'''
        data = {
            AppConstants.FIRST_NAME: AppConstants.MESSAGES.ENTER_FIRST_NAME,
            AppConstants.LAST_NAME: AppConstants.MESSAGES.ENTER_LAST_NAME,
            AppConstants.EMAIL: AppConstants.MESSAGES.ENTER_EMAIL,
            AppConstants.USERNAME: AppConstants.MESSAGES.ENTER_USERNAME,
            AppConstants.PASSWORD: AppConstants.MESSAGES.ENTER_PASSWORD
        }
        return response.Response(data= data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        return self.__RegesterUser(data)
    
    def __RegesterUser(self, data : dict) :
        ''' Method to regester a user in database with data'''
        try :
            serializer = UserSerialiser(data= data)
            if serializer.is_valid() :
                serializer.save()
                user = User.objects.get(username = data.get(AppConstants.USERNAME))
                user.set_password(data.get(AppConstants.PASSWORD))
                user.save()
                token, _ = Token.objects.get_or_create(user = user)
                payload = serializer.data
                payload.pop(AppConstants.PASSWORD)
                return response.Response(data= {AppConstants.TOKEN: str(token.key), AppConstants.PAYLOAD: payload}, status= status.HTTP_200_OK)
            else : 
                return response.Response(data= serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return response.Response(data= str(e), status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try :
            user = request.user
            serializer = UserSerialiser(instance=user)
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(data= str(e), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try :
            user : User = request.user
            user.set_password(request.data[AppConstants.PASSWORD])
            user.save()
            return response.Response(data= {AppConstants.MESSAGE : AppConstants.MESSAGES.USER_DATA_UPDATED},status=status.HTTP_200_OK)
        except Exception as e :
            return response.Response(data= str(e), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try :
            user : User = request.user
            user.delete()
            user.save()
            return response.Response(data= {AppConstants.MESSAGE : AppConstants.MESSAGES.USER_DELETED},status=status.HTTP_200_OK)
        except Exception as e :
            return response.Response(data= str(e), status=status.HTTP_400_BAD_REQUEST)
