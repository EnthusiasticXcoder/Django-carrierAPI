from django.contrib.auth.models import User

from rest_framework import status, response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import authenticate
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated      

from .serializers import UserSerialiser

class LoginView(APIView) :
    def post(self, request) :
        data : dict = request.data
        username = data.get('username')
        password = data.get('password')
        return self.__Login_User(username = username, password = password)

    def __Login_User(self, username, password) :
        ''' Methord to cheack user credentials and login user with credentials'''
        try :
            user = authenticate(username = username, password = password)
            if user is not None :
                token, _ = Token.objects.get_or_create(user = user)
                serialiser = UserSerialiser(instance=user)
                payload = serialiser.data
                payload.pop('password')
                return response.Response(data= {'token': str(token.key), 'payload': payload}, status= status.HTTP_200_OK)
            else :
                return response.Response({'message' : 'user not found',}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e :    
            return response.Response(data= str(e), status=status.HTTP_400_BAD_REQUEST)    

class RegesterView(APIView):
    def post(self, request):
        data = request.data
        return self.__RegesterUser(data)
    
    def __RegesterUser(self, data : dict) :
        ''' Method to regester a user in database with data'''
        try :
            serializer = UserSerialiser(data= data)
            if serializer.is_valid() :
                serializer.save()
                user = User.objects.get(username = data.get('username'))
                user.set_password(data.get('password'))
                user.save()
                token, _ = Token.objects.get_or_create(user = user)
                payload = serializer.data
                payload.pop('password')
                return response.Response(data= {'token': str(token.key), 'payload': payload}, status= status.HTTP_200_OK)
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
            user.set_password(request.data['password'])
            user.save()
            return response.Response(data= {'message' : 'user data updated'},status=status.HTTP_200_OK)
        except Exception as e :
            return response.Response(data= str(e), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try :
            user : User = request.user
            user.delete()
            user.save()
            return response.Response(data= {'message' : 'user deleted'},status=status.HTTP_200_OK)
        except Exception as e :
            return response.Response(data= str(e), status=status.HTTP_400_BAD_REQUEST)
