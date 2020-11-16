from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import (
    Ingredient,
    Ingredients_in_recipe,
    Recipe,
    Purchases,
    Favorites,
)
from .forms import RecipeForm


def index(request):
    recipes_list = Recipe.objects.order_by(
        '-id').select_related('author').all()
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
    return render(request, 'index.html', {'page': page,
                                          'paginator': paginator,
                                          'tags': tags,
                                          })


@login_required
def new_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        ingredients = []
        tags = []
        if 'breakfast' in request.POST:
            tags.append(1)
        if 'lunch' in request.POST:
            tags.append(2)
        if 'dinner' in request.POST:
            tags.append(3)
        for item in request.POST:
            ingredient = []
            if item.startswith('nameIngredient_'):
                i = item[-1]
                ingredient.append(request.POST.get(
                        f'nameIngredient_{i}', ''))
                ingredient.append(request.POST.get(f'valueIngredient_{i}', 0))
                ingredient.append(request.POST.get(f'unitsIngredient_{i}', ''))
                ingredients.append(ingredient)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.tag = tuple(tags)
            recipe.save()
            for item in ingredients:
                ingredient = Ingredient.objects.get(title=item[0])
                Ingredients_in_recipe.objects.create(recipe=recipe,
                                                     ingredient=ingredient,
                                                     amount=item[1])
            return redirect('index')
        return render(request, 'new_recipe.html', {'form': form,
                                                   'ingredients': ingredients,
                                                   'tags': tags})
    form = RecipeForm()
    return render(request, 'new_recipe.html', {'form': form})


@login_required
def recipe_edit(request, recipe_id):
    edited_recipe = get_object_or_404(Recipe, id=recipe_id)
    tags = [int(i) for i in edited_recipe.tag]
    ingredients_in_recipe = Ingredients_in_recipe.objects.filter(
        recipe=edited_recipe).select_related('ingredient').all()
    ingredients = []
    for item in ingredients_in_recipe:
        ingredient = []
        ingredient.append(item.ingredient.title)
        ingredient.append(item.amount)
        ingredient.append(item.ingredient.dimension)
        ingredients.append(tuple(ingredient))
    if edited_recipe.author != request.user:
        return redirect('recipe', recipe_id=recipe_id)
    form = RecipeForm(request.POST or None, files=request.FILES or None,
                      instance=edited_recipe)
    if request.method == 'POST':
        tags = []
        if 'breakfast' in request.POST:
            tags.append(1)
        if 'lunch' in request.POST:
            tags.append(2)
        if 'dinner' in request.POST:
            tags.append(3)
        new_ingredients = []
        for item in request.POST:
            ingredient = []
            if item.startswith('nameIngredient_'):
                i = item[-1]
                ingredient.append(request.POST.get(
                        f'nameIngredient_{i}', ''))
                ingredient.append(request.POST.get(f'valueIngredient_{i}', 0))
                ingredient.append(request.POST.get(f'unitsIngredient_{i}', ''))
                new_ingredients.append(tuple(ingredient))
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.tag = tuple(tags)
            recipe.save()
            new_ingredients = set(new_ingredients)
            ingredients = set(ingredients)
            if new_ingredients != ingredients:
                adding = new_ingredients.difference(ingredients)
                deleting = ingredients.difference(new_ingredients)
                for item in deleting:
                    ingredient = Ingredient.objects.get(title=item[0])
                    del_item = Ingredients_in_recipe.objects.get(
                        recipe=recipe, ingredient=ingredient)
                    del_item.delete()
                for item in adding:
                    ingredient = Ingredient.objects.get(title=item[0])
                    Ingredients_in_recipe.objects.create(recipe=recipe,
                                                         ingredient=ingredient,
                                                         amount=item[1])
                return redirect('recipe', recipe_id=recipe_id)
        return render(request, 'new_recipe.html', {'form': form,
                                                   'ingredients': ingredients,
                                                   'tags': tags})
    return render(request, 'new_recipe.html', {'form': form,
                                               'ingredients': ingredients,
                                               'tags': tags})


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = Ingredients_in_recipe.objects.filter(
        recipe=recipe).select_related('ingredient').all()
    return render(request, 'singlePage.html', {'recipe': recipe,
                                               'ingredients': ingredients})


def shoplist_view(request):
    if request.user.is_authenticated:
        user = request.user
        purchases = Purchases.objects.filter(
            user=user).select_related('recipe').all()
        recipes = [i.recipe for i in purchases]
        return render(request, 'shopList.html', {'recipes': recipes})
    else:
        recipes_id = request.session.get('purchases', [])
        recipes = Recipe.objects.filter(id__in=recipes_id).all()
        return render(request, 'shopList.html', {'recipes': recipes})


@login_required
def favorites_view(request):
    favorites = Favorites.objects.filter(
        user=request.user).select_related('recipe').all()
    recipes_id_list = [i.recipe.id for i in favorites]
    recipe_list = Recipe.objects.filter(id__in=recipes_id_list).all()
    tags = [False, False, False]
    if request.GET.get('breakfast') == 'True':
        recipe_list = recipe_list.filter(tag__contains=1)
        tags[0] = True
    if request.GET.get('lunch') == 'True':
        recipe_list = recipe_list.filter(tag__contains=2)
        tags[1] = True
    if request.GET.get('dinner') == 'True':
        recipe_list = recipe_list.filter(tag__contains=3)
        tags[2] = True
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    return render(request, 'favorites.html', {'page': page,
                                              'paginator': paginator,
                                              'tags': tags,
                                              })
