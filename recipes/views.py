from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Ingredient, Ingredients_in_recipe, Recipe, Purchases
from .forms import RecipeForm
import json


def index(request):
    recipes_list = Recipe.objects.select_related('author').all()
    tags = [False, False, False]
    if request.GET.get('breakfast') == 'True':
        recipes_list = recipes_list.filter(tag__contains=1)
        tags[0] = True
    if request.GET.get('lunch') == 'True':
        recipes_list = recipes_list.filter(tag__contains=2)
        tags[1] = True
    if request.GET.get('dinner') == 'True':
        recipes_list = recipes_list.filter(tag__contains=3)
        tags[2] = True
    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    """
    with open('ingredients.json', 'r') as ingredients:
        ingredients_json = json.load(ingredients)
        for ingredient in ingredients_json:
            Ingredient.objects.create(title=ingredient['title'], dimension=ingredient['dimension'])
    """
    return render(request, 'index.html', {'page': page,
                                          'paginator': paginator,
                                          'tags': tags,
                                          })


@login_required
def new_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        print(request.POST)
        if form.is_valid():
            tags = []
            if 'breakfast' in request.POST:
                tags.append(1)
            if 'lunch' in request.POST:
                tags.append(2)
            if 'dinner' in request.POST:
                tags.append(3)
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.tag = tuple(tags)
            recipe.save()
            i = 1
            while True:
                ingredient_name = request.POST.get(f'nameIngredient_{i}', '')
                if ingredient_name == '':
                    break
                amount = request.POST.get(f'valueIngredient_{i}', 0)
                ingredient = Ingredient.objects.get(title=ingredient_name)
                Ingredients_in_recipe.objects.create(recipe=recipe,
                                                     ingredient=ingredient,
                                                     amount=amount)
                i += 1
            return redirect('index')
        return render(request, 'new_recipe.html', {'form': form})
    form = RecipeForm()
    return render(request, 'new_recipe.html', {'form': form})


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = Ingredients_in_recipe.objects.filter(
        recipe=recipe).select_related('ingredient').all()
    return render(request, 'singlePage.html', {'recipe': recipe,
                                               'ingredients': ingredients})


def shoplist_view(request):
    user = request.user
    purchases = Purchases.objects.filter(
        user=user).select_related('recipe').all()
    recipes = [i.recipe for i in purchases]
    return render(request, 'shopList.html', {'recipes': recipes})
