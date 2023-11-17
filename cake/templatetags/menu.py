from django import template
from cake.models import Category

register = template.Library()


@register.inclusion_tag('cake/menu_tpl.html')
def show_menu(menu_class='menu'):  # темплэйтэг получения меню
    categories = Category.objects.all()
    return {"categories": categories, "menu_class": menu_class}
