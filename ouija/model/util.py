

def normalize_column_type(column):
    name = unicode(column.type).lower()
    if name.startswith('varchar') or name.startswith('char'):
        return 'text'
    if name.startswith('numeric'):
        return 'float'
    return name
