from django.http import Http404
from django.shortcuts import render
from drf_yasg import openapi
from drf_spectacular import openapi
from drf_yasg.utils import swagger_auto_schema, logger
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Wallpaper
from .serializers import CategorySerializer, WallpaperSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import permission_classes

#2
# Create your views here.
class CategoryList(APIView):

    @swagger_auto_schema(
        tags=['Categories'],
        operation_description="Endpoint for retrieving a list of categories or creating a new category.",
        responses={
            200: "Successful retrieval. Returns a list of categories.",
            201: "Successful creation. Returns the created category.",
            400: "Bad request. Invalid input.",
            500: "Internal server error. Failed to process the request."
        }
    )
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#3
class CategoryDetail(APIView):

    @swagger_auto_schema(
        tags=['Wallpapers'],
        operation_description="Endpoint for retrieving detailed information about a specific wallpaper.",
        responses={
            200: WallpaperSerializer,
            404: "Not found. The specified wallpaper does not exist.",
            500: "Internal server error. Failed to process the request."
        }
    )
    def get(self, request, pk, *args, **kwargs):
        try:
            wallpaper = Wallpaper.objects.get(pk=pk)
            # Сериализация объекта обоев
            serializer = WallpaperSerializer(wallpaper)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Wallpaper.DoesNotExist:
            return Response({"detail": "Wallpaper not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": "An error occurred. Please try again later."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# 1
class WallpaperByCategory(APIView):

    @swagger_auto_schema(
        tags=['Wallpapers'],
        operation_description="Получаешь лист объектов по конкретным категориям, например 1 у нас это аниме",
        responses={
            200: WallpaperSerializer(many=True),
            400: "Bad request. Invalid input.",
            404: "Not found. The specified category does not exist.",
            500: "Internal server error. Failed to process the request."
        }
    )
    def get(self, request, pk):
        try:
            logger.info(f"Retrieving category with ID {pk}")
            category = Category.objects.get(id=pk)
            logger.info(f"Category retrieved: {category}")

            wallpapers = category.wallpapers.all()
            logger.info(f"Retrieved {wallpapers.count()} wallpapers for category ID {pk}")

            serializer = WallpaperSerializer(wallpapers, many=True)
            logger.info("Serialization complete")

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            logger.error(f"Category with ID {pk} does not exist.")
            return Response({"detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception(f"An error occurred while retrieving wallpapers for category {pk}: {e}")
            return Response({"detail": "An error occurred. Please try again later."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)











