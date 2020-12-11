import os
from rest_framework import serializers
from CookbookAPI import settings
from django.core.files import File
from recipes.models import Recipe
from cuisines.serializers import CuisineSerializer
from cuisines.models import Cuisine
from diets.serializers import DietSerializer
from diets.models import Diet
from ingredients.serializers import IngredientSerializer
from ingredients.models import Ingredient
from occasions.serializers import OccasionSerializer
from occasions.models import Occasion
import subprocess
import threading
import asyncio


class RecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()
    file_url = serializers.ReadOnlyField()

    cuisines = CuisineSerializer(many=True, default=[])
    diets = DietSerializer(many=True, default=[])
    ingredients = IngredientSerializer(many=True, default=[])
    occasions = OccasionSerializer(many=True, default=[])

    cuisine_ids = serializers.ListField(write_only=True, required=False)
    diet_ids = serializers.ListField(write_only=True, required=False)
    ingredient_ids = serializers.ListField(write_only=True, required=False)
    occasion_ids = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'created',
            'name',
            'url',
            'note',
            'cuisines',
            'diets',
            'ingredients',
            'occasions',
            'file_url',
            'cuisine_ids',
            'diet_ids',
            'ingredient_ids',
            'occasion_ids'
        )
        extra_kwargs = {
            'file_url': {
                'required': False
            },
            'cuisine_ids': {
                'required': False
            },
            'diet_ids': {
                'required': False
            },
            'ingredient_ids': {
                'required': False
            },
            'occasion_ids': {
                'required': False
            },
        }

    def create(self, validated_data):
        instance = Recipe.objects.create(
            name=validated_data.get('name')
        )
        try:
            self.update(instance=instance, validated_data=validated_data)
        except Cuisine.DoesNotExist:
            instance.delete()
        except Diet.DoesNotExist:
            instance.delete()
        except Ingredient.DoesNotExist:
            instance.delete()
        except Occasion.DoesNotExist:
            instance.delete()
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.note = validated_data.get('note', instance.note)

        # Update URL related data
        if validated_data.get('url', None):
            # Check if there's already a file object present that needs deletion from disk
            # delete()
            if instance.get_file_url is not None and validated_data.get('url', None) is not instance.get_file_url:
                # Create a path for deletion
                file_path = '{}{}'.format(settings.MEDIA_ROOT, instance.file_name)
                # Delete if still exists
                if os.path.exists(file_path):
                    print('Deleting {}.'.format(file_path))
                    os.remove(file_path)
                else:
                    print('File not found at {}.'.format(file_path))
                # Delete file reference from database
                instance.file.delete()

        # Update Cuisines
        if validated_data.get('cuisine_ids', None):
            cuisines = []
            for cuisine_id in validated_data.get('cuisine_ids', None):
                cuisines.append(Cuisine.objects.get(pk=cuisine_id))
            instance.cuisines.set(cuisines)

        # Update Diets
        if validated_data.get('diet_ids', None):
            diets = []
            for diet_id in validated_data.get('diet_ids', None):
                diets.append(Diet.objects.get(pk=diet_id))
            instance.diets.set(diets)

        # Update Ingredients
        if validated_data.get('ingredient_ids', None):
            ingredients = []
            for ingredient_id in validated_data.get('ingredient_ids', None):
                ingredients.append(Ingredient.objects.get(pk=ingredient_id))
            instance.ingredients.set(ingredients)

        # Update Occasions
        if validated_data.get('occasion_ids', None):
            occasions = []
            for occasion_id in validated_data.get('occasion_ids', None):
                occasions.append(Occasion.objects.get(pk=occasion_id))
            instance.occasions.set(occasions)

        instance.save()

        # Initialise the thread
        t = threading.Thread(
            target=self.threaded_loading,
            args=(instance.id,)
        )
        t.start()

        return instance

    def threaded_loading(self, recipe_id):
        instance = Recipe.objects.get(pk=recipe_id)
        if instance.url is not None and instance.url != "":
            # The file path for the output file
            media_root = settings.MEDIA_ROOT
            if media_root.endswith('/'):
                media_root = media_root[:-1]
            local_file_path = "{}/recipe-{}.pdf".format(
                media_root,
                instance.id
            )

            # Get a run loop and wait for it's execution
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            print('Spawned run loop')
            loop.run_until_complete(
                self.download_file(
                    url=str(instance.url),
                    local_file_path=local_file_path
                )
            )
            loop.close()

            # Set the loaded file to the instance.
            try:
                with open(local_file_path, 'rb') as file:
                    print('Did open file at {}'.format(local_file_path))
                    pdf_export = File(file, name=os.path.basename(file.name))
                    instance.file = pdf_export

                    pdf_export.closed
                    file.closed

                    instance.save()
                    print('Did save instance with file {}'.format(instance.file))

            except FileNotFoundError:
                print('Could not find file '.format(local_file_path))

    async def download_file(self, url, local_file_path):
        # Load a file for the new URL
        cmd = "{} {} {} {}".format(
            'xvfb-run -a -s "-screen 0 640x480x16"',
            'wkhtmltopdf --zoom 1.0 --load-error-handling ignore',
            url,
            local_file_path
        )

        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).wait()
