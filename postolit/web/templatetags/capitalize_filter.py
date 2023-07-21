from django import template
register = template.Library()
@register.filter # Регитрация фильтра


def capitalize(value): # Название самого фильтра(в шаблоне)
    new_value = value.capitalize() # Начинает строку с заглавной буквы
    return new_value