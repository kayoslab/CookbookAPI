from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import QuerySet
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from cuisines.models import Cuisine
from cuisines.serializers import CuisineSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class CuisineListView(APIView):
    @csrf_exempt
    @swagger_auto_schema(
        operation_description="Gets a list of Cuisine objects.",
        responses={
            200: CuisineSerializer(many=True)
        },
        tags=['Cuisine'],
    )
    def get(self, request, *args, **kwargs):
        objects: QuerySet[Cuisine] = Cuisine.objects.all()
        serializer = CuisineSerializer(objects, many=True)
        return JSONResponse(serializer.data)

    @csrf_exempt
    @swagger_auto_schema(
        operation_description="Creates a new Cuisine entry with a given name",
        # query_serializer=CuisineSerializer,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(
                    description='The cuisines unique name.',
                    type=openapi.TYPE_STRING
                )
            },
        ),
        responses={
            200: CuisineSerializer(many=False),
            400: """
                The required request parameters are not met.
                """,
        },
        tags=['Cuisine'],
    )
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = CuisineSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return JSONResponse(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CuisineDetailView(APIView):
    @csrf_exempt
    @swagger_auto_schema(
        operation_description="Gets a Cuisine object for a given id.",
        responses={
            200: CuisineSerializer(many=False),
            404: """
               The object could not be retrieved, since it doesn't exist.
               """,
        },
        tags=['Cuisine'],
    )
    def get(self, request, pk):
        try:
            data = Cuisine.objects.get(pk=pk)
        except Cuisine.DoesNotExist:
            return HttpResponse(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CuisineSerializer(data)
        return JSONResponse(serializer.data)

    @csrf_exempt
    @swagger_auto_schema(
        operation_description="Updates a Cuisine object with a given id.",
        # query_serializer=CuisineSerializer,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(
                    description='The cuisines unique name.',
                    type=openapi.TYPE_STRING
                )
            },
        ),
        responses={
            200: CuisineSerializer(many=False),
            400: """
                The required request parameters are not met.
                """,
            404: """
               The object could not be updated, since it doesn't exist.
               """,
        },
        tags=['Cuisine'],
    )
    def put(self, request, pk):
        try:
            data = Cuisine.objects.get(pk=pk)
        except Cuisine.DoesNotExist:
            return HttpResponse(
                status=status.HTTP_404_NOT_FOUND
            )

        parsed_data = JSONParser().parse(request)
        serializer = CuisineSerializer(
            data,
            data=parsed_data
        )
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @csrf_exempt
    @swagger_auto_schema(
        operation_description="Updates a Cuisine object with a given id.",
        # query_serializer=CuisineSerializer,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
                'name': openapi.Schema(
                    description='The cuisines unique name.',
                    type=openapi.TYPE_STRING
                )
            },
        ),
        responses={
            200: CuisineSerializer(many=False),
            400: """
                The required request parameters are not met.
                """,
            404: """
               The object could not be updated, since it doesn't exist.
               """,
        },
        tags=['Cuisine'],
    )
    def patch(self, request, pk):
        try:
            data = Cuisine.objects.get(pk=pk)
        except Cuisine.DoesNotExist:
            return HttpResponse(
                status=status.HTTP_404_NOT_FOUND
            )
        parsed_data = JSONParser().parse(request)
        serializer = CuisineSerializer(
            data,
            data=parsed_data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @csrf_exempt
    @swagger_auto_schema(
        operation_description="Deletes a Cuisine object with a given id.",
        responses={
            203: None,
            404: """
                The object could not be deleted, since it doesn't exist.
                """,
        },
        tags=['Cuisine'],
    )
    def delete(self, request, pk):
        try:
            data = Cuisine.objects.get(pk=pk)
        except Cuisine.DoesNotExist:
            return HttpResponse(
                status=status.HTTP_404_NOT_FOUND
            )

        data.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
