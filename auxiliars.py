import re

def convert_to_valid_folder_name(name):
    # Reemplazar caracteres no permitidos con un guion bajo
    valid_name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    # Reemplazar espacios con guion bajo
    valid_name = valid_name.replace(' ', '_')
    # Limitar la longitud del nombre a 255 caracteres
    valid_name = valid_name[:255]
    return valid_name

# Example usage
#folder_name = "Mi carpeta inválida?*"
#valid_folder_name = convert_to_valid_folder_name(folder_name)
#print("Nombre de carpeta válido:", valid_folder_name)
