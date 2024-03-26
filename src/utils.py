import re
from strawberry.types import Info

def get_selected_fields(info:Info):
    selected_fields = [field.name for field in info.selected_fields[0].selections]
    return selected_fields

def clean_field_name(name):
    if name[0].isdigit():
        return f"_{name}"
    name = re.sub(r'\([^)]*\)', '', name)
    name = name.replace('/', '_')
    name = name.replace('-', '_')
    name = name.replace('+', '')
    
    return name

