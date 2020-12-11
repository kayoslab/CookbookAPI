from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import QuerySet
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class RecipeListView(APIView):
    @csrf_exempt
    @swagger_auto_schema(
        operation_description="Gets a list of Recipe objects.",
        responses={
            200: RecipeSerializer(many=True)
        },
        tags=['Recipe'],
    )
    def get(self, request, *args, **kwargs):
        objects: QuerySet[Recipe] = Recipe.objects.all()
        serializer = RecipeSerializer(objects, many=True)
        return JSONResponse(serializer.data)

    @csrf_exempt
    @swagger_auto_schema(
        operation_description="Creates a new Recipe entry.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(
                    description='The recipes unique name.',
                    type=openapi.TYPE_STRING
                ),
                'url': openapi.Schema(
                    description="""
                                The URL from which the recipe comes originally. 
                                This URL will be used to download a pdf export of the recipe
                                to allow traceability and long term storage.
                                """,
                    type=openapi.TYPE_STRING
                ),
                'note': openapi.Schema(
                    description="""
                                A descriptive text which might be helpful finding the recipe
                                again when using the search functionality. You might want to
                                write what was good and bad, but also additional information
                                and significant facts are usefull for indexing.
                                """,
                    type=openapi.TYPE_STRING
                ),
                'cuisine_ids': openapi.Schema(
                    description="""
                                A list of cuisines unique ids in order to link an existing 
                                cuisine to the recipe.
                                """,
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                ),
                'diet_ids': openapi.Schema(
                    description="""
                                A list of diets unique ids in order to link an existing 
                                diet to the recipe.
                                """,
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                ),
                'ingredient_ids': openapi.Schema(
                    description="""
                                A list of ingredients unique ids in order to link an existing 
                                ingredient to the recipe.
                                """,
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                ),
                'occasion_ids': openapi.Schema(
                    description="""
                                A list of occasions unique ids in order to link an existing 
                                occasion to the recipe.
                                """,
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                ),
            },
        ),
        responses={
            200: RecipeSerializer(many=False),
            400: """
                The required request parameters are not met or an expected 
                object could not be retrieved from the data store.
                """,
        },
        tags=['Recipe'],
    )
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = RecipeSerializer(data=data)
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


class RecipeDetailView(APIView):
    @csrf_exempt
    @swagger_auto_schema(
        operation_description="Gets a Recipe object for a given id.",
        responses={
            200: RecipeSerializer(many=False),
            404: """
                The object could not be retrieved, since it doesn't exist.
                """,
        },
        tags=['Recipe'],
    )
    def get(self, request, pk):
        try:
            data = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return HttpResponse(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = RecipeSerializer(data)
        return JSONResponse(serializer.data)

    @csrf_exempt
    @swagger_auto_schema(
        operation_description="Updates a Recipe object with a given id.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(
                    description='The recipes unique name.',
                    type=openapi.TYPE_STRING
                ),
                'url': openapi.Schema(
                    description="""
                                The URL from which the recipe comes originally. 
                                This URL will be used to download a pdf export of the recipe
                                to allow traceability and long term storage.
                                """,
                    type=openapi.TYPE_STRING
                ),
                'note': openapi.Schema(
                    description="""
                                A descriptive text which might be helpful finding the recipe
                                again when using the search functionality. You might want to
                                write what was good and bad, but also additional information
                                and significant facts are usefull for indexing.
                                """,
                    type=openapi.TYPE_STRING
                ),
                'cuisine_ids': openapi.Schema(
                    description="""
                                A list of cuisines unique ids in order to link an existing 
                                cuisine to the recipe.
                                """,
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                ),
                'diet_ids': openapi.Schema(
                    description="""
                                A list of diets unique ids in order to link an existing 
                                diet to the recipe.
                                """,
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                ),
                'ingredient_ids': openapi.Schema(
                    description="""
                                A list of ingredients unique ids in order to link an existing 
                                ingredient to the recipe.
                                """,
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                ),
                'occasion_ids': openapi.Schema(
                    description="""
                                A list of occasions unique ids in order to link an existing 
                                occasion to the recipe.
                                """,
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                ),
            },
        ),
        responses={
            200: RecipeSerializer(many=False),
            400: """
                The required request parameters are not met or an expected 
                object could not be retrieved from the data store.
                """,
            404: """
                The object could not be updated, since it doesn't exist.
                """,
        },
        tags=['Recipe'],
    )
    def put(self, request, pk):
        try:
            data = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return HttpResponse(
                status=status.HTTP_404_NOT_FOUND
            )

        parsed_data = JSONParser().parse(request)
        serializer = RecipeSerializer(
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
        operation_description="Updates a Recipe object with a given id.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
                'name': openapi.Schema(
                    description='The recipes unique name.',
                    type=openapi.TYPE_STRING
                ),
                'url': openapi.Schema(
                    description="""
                        The URL from which the recipe comes originally. 
                        This URL will be used to download a pdf export of the recipe
                        to allow traceability and long term storage.
                        """,
                    type=openapi.TYPE_STRING
                ),
                'note': openapi.Schema(
                    description="""
                        A descriptive text which might be helpful finding the recipe
                        again when using the search functionality. You might want to
                        write what was good and bad, but also additional information
                        and significant facts are usefull for indexing.
                        """,
                    type=openapi.TYPE_STRING
                ),
                'cuisine_ids': openapi.Schema(
                    description="""
                        A list of cuisines unique ids in order to link an existing 
                        cuisine to the recipe.
                        """,
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                ),
                'diet_ids': openapi.Schema(
                    description="""
                        A list of diets unique ids in order to link an existing 
                        diet to the recipe.
                        """,
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                ),
                'ingredient_ids': openapi.Schema(
                    description="""
                        A list of ingredients unique ids in order to link an existing 
                        ingredient to the recipe.
                        """,
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                ),
                'occasion_ids': openapi.Schema(
                    description="""
                        A list of occasions unique ids in order to link an existing 
                        occasion to the recipe.
                        """,
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                ),
            },
        ),
        responses={
            200: RecipeSerializer(many=False),
            400: """
                The required request parameters are not met or an expected 
                object could not be retrieved from the data store.
                """,
            404: """
                The object could not be updated, since it doesn't exist.
                """,
        },
        tags=['Recipe'],
    )
    def patch(self, request, pk):
        try:
            data = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return HttpResponse(
                status=status.HTTP_404_NOT_FOUND
            )
        parsed_data = JSONParser().parse(request)
        serializer = RecipeSerializer(
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
        operation_description="Deletes a Recipe object with a given id.",
        responses={
            203: None,
            404: """
                The object could not be deleted, since it doesn't exist.
                """,
        },
        tags=['Recipe'],
    )
    def delete(self, request, pk):
        try:
            data = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return HttpResponse(
                status=status.HTTP_404_NOT_FOUND
            )

        data.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
