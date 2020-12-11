from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import QuerySet
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from occasions.models import Occasion
from occasions.serializers import OccasionSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class OccasionListView(APIView):
    @csrf_exempt
    @swagger_auto_schema(
        operation_description="Gets a list of Occasion objects.",
        responses={
            200: OccasionSerializer(many=True)
        },
        tags=['Occasion'],
    )
    def get(self, request, *args, **kwargs):
        objects: QuerySet[Occasion] = Occasion.objects.all()
        serializer = OccasionSerializer(objects, many=True)
        return JSONResponse(serializer.data)

    @csrf_exempt
    @swagger_auto_schema(
        operation_description="Creates a new Occasion entry with a given name",
        # query_serializer=OccasionSerializer,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(
                    description='The occasions unique name.',
                    type=openapi.TYPE_STRING
                )
            },
        ),
        responses={
            200: OccasionSerializer(many=False),
            400: """
                The required request parameters are not met.
                """
        },
        tags=['Occasion'],
    )
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = OccasionSerializer(data=data)
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


class OccasionDetailView(APIView):
    @csrf_exempt
    @swagger_auto_schema(
        operation_description="Gets an Occasion object for a given id.",
        responses={
            200: OccasionSerializer(many=False),
            404: """
               The object could not be retrieved, since it doesn't exist.
               """,
        },
        tags=['Occasion'],
    )
    def get(self, request, pk):
        try:
            data = Occasion.objects.get(pk=pk)
        except Occasion.DoesNotExist:
            return HttpResponse(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = OccasionSerializer(data)
        return JSONResponse(serializer.data)

    @csrf_exempt
    @swagger_auto_schema(
        operation_description="Updates an Occasion object with a given id.",
        # query_serializer=OccasionSerializer,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(
                    description='The occasions unique name.',
                    type=openapi.TYPE_STRING
                )
            },
        ),
        responses={
            200: OccasionSerializer(many=False),
            400: """
                The required request parameters are not met.
                """,
            404: """
               The object could not be updated, since it doesn't exist.
               """,
        },
        tags=['Occasion'],
    )
    def put(self, request, pk):
        try:
            data = Occasion.objects.get(pk=pk)
        except Occasion.DoesNotExist:
            return HttpResponse(
                status=status.HTTP_404_NOT_FOUND
            )

        parsed_data = JSONParser().parse(request)
        serializer = OccasionSerializer(
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
        operation_description="Updates an Occasion object with a given id.",
        # query_serializer=OccasionSerializer,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
                'name': openapi.Schema(
                    description='The occasions unique name.',
                    type=openapi.TYPE_STRING
                )
            },
        ),
        responses={
            200: OccasionSerializer(many=False),
            400: """
                The required request parameters are not met.
                """,
            404: """
               The object could not be updated, since it doesn't exist.
               """,
        },
        tags=['Occasion'],
    )
    def patch(self, request, pk):
        try:
            data = Occasion.objects.get(pk=pk)
        except Occasion.DoesNotExist:
            return HttpResponse(
                status=status.HTTP_404_NOT_FOUND
            )
        parsed_data = JSONParser().parse(request)
        serializer = OccasionSerializer(
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
        operation_description="Deletes an Occasion object with a given id.",
        responses={
            203: None,
            404: """
                The object could not be deleted, since it doesn't exist.
                """,
        },
        tags=['Occasion'],
    )
    def delete(self, request, pk):
        try:
            data = Occasion.objects.get(pk=pk)
        except Occasion.DoesNotExist:
            return HttpResponse(
                status=status.HTTP_404_NOT_FOUND
            )

        data.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
