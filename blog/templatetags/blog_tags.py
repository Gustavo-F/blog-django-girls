from unicodedata import category
from django import template

register = template.Library()

@register.filter(name='post_categories')
def post_categories(categories):
    if not categories:
        return ''
    elif len(categories) == 1:
        return categories[0].name
    else:
        result = ''
        for index, category in enumerate(categories):
            if index < (len(categories) - 1):
                result += (f'{category.name}, ')
            else:
                result += (category.name)

        return result
