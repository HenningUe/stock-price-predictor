

def get_modul_name_pure(module):
    mod_name = module.__name__.split('.')[-1]
    return mod_name
