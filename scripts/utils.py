import re
from strawberry.types import Info

def get_selected_fields(info:Info):
    selected_fields = [field.name for field in info.selected_fields[0].selections]
    return selected_fields

