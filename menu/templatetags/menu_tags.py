from django import template
from django.template.loader import render_to_string

from menu.models import MenuItem

register = template.Library()


def get_menu_items(menu_name, current_url):
    menu_items = MenuItem.objects.filter(menu_name=menu_name).prefetch_related('children')

    def build_tree(items, parent=None):
        tree = []
        for item in items:
            if item.parent == parent:
                children = build_tree(items, item)
                tree.append({
                    'item': item,
                    'children': children,
                    'is_active': current_url == item.url,
                    'is_open': current_url.startswith(item.url) or any(
                        child['is_active'] for child in children),
                })
        return tree

    return build_tree(menu_items)


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    current_url = context['request'].path
    menu_tree = get_menu_items(menu_name, current_url)
    return render_to_string('menu.html', {'menu_tree': menu_tree})


# menu/templatetags/menu_tags.py

# from django import template
# from django.template.loader import render_to_string
# from menu.models import MenuItem
#
# register = template.Library()
#
#
# def get_menu_items(menu_name, current_url):
#     menu_items = MenuItem.objects.filter(menu_name=menu_name).prefetch_related('children')
#
#     def build_tree(items, parent=None):
#         tree = []
#         for item in items:
#             if item.parent == parent:
#                 children = build_tree(items, item)
#                 tree.append({
#                     'item': item,
#                     'children': children,
#                     'is_active': current_url == item.url,
#                     'is_open': current_url.startswith(item.url) or any(
#                         child['is_active'] for child in children),
#                 })
#         return tree
#
#     return build_tree(menu_items)



# @register.simple_tag(takes_context=True)
# def draw_all_menus(context):
#     print(context)
#     current_url = context['request'].path
#     # Извлекаем все корневые элементы меню (где parent=None)
#     root_menus = MenuItem.objects.filter(parent=None).prefetch_related('children')
#
#     menu_trees = []
#     for menu in root_menus:
#         menu_tree = get_menu_items(menu.menu_name, current_url)
#         menu_trees.append({
#             'menu': menu,
#             'tree': menu_tree,
#         })
#
#     # Используем render_to_string для генерации HTML
#     return render_to_string('menu.html', {'menu_trees': menu_trees})
