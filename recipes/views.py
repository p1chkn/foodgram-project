from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import ttfonts
from users.models import User
from .models import (
    Ingredient,
    Ingredients_in_recipe,
    Recipe,
    Purchases,
    Favorites,
    Follow,
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
    editing = recipe_id
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
                                                   'tags': tags,
                                                   'editing': editing})
    return render(request, 'new_recipe.html', {'form': form,
                                               'ingredients': ingredients,
                                               'tags': tags,
                                               'editing': editing})


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = Ingredients_in_recipe.objects.filter(
        recipe=recipe).select_related('ingredient').all()
    return render(request, 'singlePage.html', {'recipe': recipe,
                                               'ingredients': ingredients})


def shoplist_view(request):
    empty = False
    if request.user.is_authenticated:
        user = request.user
        purchases = Purchases.objects.filter(
            user=user).select_related('recipe').all()
        recipes = [i.recipe for i in purchases]
        if recipes == []:
            empty = True
    else:
        recipes_id = request.session.get('purchases', [])
        recipes = Recipe.objects.filter(id__in=recipes_id).all()
        if not recipes.count():
            empty = True
    return render(request, 'shopList.html', {'recipes': recipes,
                                             'empty': empty})


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
    empty = False
    if not recipe_list.count():
        empty = True
    return render(request, 'index.html', {'page': page,
                                          'paginator': paginator,
                                          'tags': tags,
                                          'empty': empty, })


@login_required
def user_view(request, user_id):
    author = get_object_or_404(User, id=user_id)
    recipes_list = Recipe.objects.order_by(
        '-id').filter(author=author).all()
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
    empty = False
    if not recipes_list.count():
        empty = True
    return render(request, 'authorRecipe.html', {'page': page,
                                                 'paginator': paginator,
                                                 'tags': tags,
                                                 'author': author,
                                                 'empty': empty})


@login_required
def follow_view(request):
    follows = Follow.objects.filter(
        user=request.user).select_related('author').all()
    author_list = []
    for item in follows:
        author = []
        recipes = Recipe.objects.filter(
            author=item.author).order_by("-id")[:3].all()
        count = Recipe.objects.filter(author=item.author).count()
        count -= 3
        author.append(item.author)
        author.append(recipes)
        author.append(count)
        author_list.append(author)
    paginator = Paginator(author_list, 3)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    empty = False
    if author_list == []:
        empty = True
    return render(request, 'myFollow.html', {'page': page,
                                             'paginator': paginator,
                                             'empty': empty, })


@login_required
def remove_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe', recipe_id=recipe_id)
    recipe.delete()
    return redirect('index')


def download_shoplist(request):
    ingredients = {}
    if request.user.is_authenticated:
        purchases = Purchases.objects.filter(
            user=request.user).select_related().all()
        recipes = [i.recipe for i in purchases]
    else:
        purchases_id = request.session.get('purchases', [])
        purchases = Recipe.objects.filter(
            id__in=purchases_id).select_related().all()
        recipes = [i for i in purchases]
    for recipe in recipes:
        ingredients_in_recipe = Ingredients_in_recipe.objects.filter(
            recipe=recipe).select_related().all()
        for item in ingredients_in_recipe:
            if item.ingredient.title not in ingredients:
                ingredients[item.ingredient.title] = [item.amount,
                                                      item.ingredient.dimension]
            else:
                ingredients[item.ingredient.title][0] += item.amount
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="shoplist.pdf"'
    buffer = BytesIO()
    MyFontObject = ttfonts.TTFont('Arial', 'arial.ttf')
    pdfmetrics.registerFont(MyFontObject)
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Arial", 7)
    p.drawString(20, 830, 'Автор проекта: Чуйкин Павел')
    p.drawString(400, 830, 'Ссылка на github:  https://github.com/p1chkn/')
    p.drawString(20, 800, 'Ссылка на резюме:  https://hh.ru/resume/fcc0665cff0808b5fe0039ed1f6f65794c5650')
    p.line(0, 780, 1000, 780)
    p.line(0, 778, 1000, 778)
    p.setFont("Arial", 9)
    p.drawString(260, 750, 'Список покупок:')
    x1 = 20
    y1 = 720
    for key in ingredients:
        p.drawString(x1, y1-12, f"{key} - {ingredients[key][0]} {ingredients[key][1]}")
        y1 -= 20
        p.setTitle("Список покупок")
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def clear_shoplist(request):
    if request.user.is_authenticated:
        purchases = Purchases.objects.filter(
            user=request.user).select_related().all()
        for item in purchases:
            purchases.delete()
    else:
        request.session['purchases'] = []
    return redirect('index')
