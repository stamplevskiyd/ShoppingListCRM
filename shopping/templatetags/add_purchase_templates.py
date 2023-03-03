from django import template

register = template.Library()


@register.simple_tag
def get_purchase_name_input():
    """Input tag для ввода названия покупки"""
    return '<input type="text" ' \
           'id="product_name" ' \
           'name="product_name"' \
           'required="required" ' \
           'placeholder="Название покупки"/>'


@register.simple_tag
def get_purchase_price_input():
    """Input tag для ввода цены покупки"""
    return '<input type="number" ' \
           'id="product_price" ' \
           'required="required" ' \
           'pattern="[0-9]+([\.,][0-9]+)?" ' \
           'step="0.01" ' \
           'min="0" ' \
           'name="product_prices[]" ' \
           'placeholder="100.0"/>'


@register.simple_tag
def get_purchase_count_input():
    """Input tag для ввода числа предметов"""
    return '<input type="number" ' \
           'id="product_count" ' \
           'required="required" ' \
           'pattern="^[ 0-9]+$" ' \
           'step="1" ' \
           'min="0" ' \
           'name="product_counts[]" ' \
           'placeholder="1" ' \
           'value="1"/>'


@register.simple_tag
def get_remove_button():
    """Тег для кнопки удаления"""
    return '<button class="remove_product btn btn-danger btn-sm">Удалить</button>'

# @register.simple_tag
# def get_person_selector():
#     """Селектор людей"""
#     return '{% autoescape off %}' \
#            '<select class="selectpicker" name="person_list[]" id="person_list[]" multiple data-live-search="true">' \
#            '   <option value="all">Все</option>' \
#            '       {% for person in persons %}' \
#            '            <option value="{{ person.id }}">{{ person.name }}</option>' \
#            '    {% endfor %}' \
#            '</select>' \
#            '{% endautoescape %}'

