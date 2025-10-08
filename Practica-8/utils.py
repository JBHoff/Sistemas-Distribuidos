from geopy.distance import geodesic 
 
def distancia_geo(coord1, coord2): 
    """Calcula la distancia en kilómetros entre dos coordenadas GPS""" 
    return geodesic(coord1, coord2).kilometers 
 
def validar_coordenadas(lat, lon): 
    """Verifica que la latitud y longitud estén dentro de rangos válidos""" 
    if not (-90 <= lat <= 90): 
        raise ValueError("Latitud fuera de rango (-90, 90)") 
    if not (-180 <= lon <= 180): 
        raise ValueError("Longitud fuera de rango (-180, 180)") 
    return True