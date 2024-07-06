from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def cargar_datos_por_defecto(sender, **kwargs):
    if sender.name == 'productos':
        Categoria = apps.get_model('productos', 'Categoria')  # Obtén el modelo Categoria
        CStateProducto = apps.get_model('productos', 'CStateProducto')

        # Datos por defecto a insertar
        categorias = [
            {'nombre': 'Alimentos y bebidas', 'descripcion': 'Incluye productos comestibles como alimentos enlatados, cereales, productos frescos, bebidas no alcohólicas, vinos, licores, etc.'},
            {'nombre': 'Hogar y jardín', 'descripcion': 'Incluye muebles, electrodomésticos, utensilios de cocina, decoración, herramientas, productos para el jardín, etc.'},
            {'nombre': 'Automoción', 'descripcion': 'Comprende productos para automóviles como piezas de repuesto, accesorios, herramientas, productos de limpieza, neumáticos, sistemas de audio y navegación, etc.'},
            {'nombre': 'Electrónica', 'descripcion': 'Incluye productos como teléfonos móviles, computadoras, televisores, cámaras digitales, auriculares, consolas de videojuegos, etc.'},
            {'nombre': 'Salud y belleza', 'descripcion': 'Engloba productos como cosméticos, productos para el cuidado de la piel, maquillaje, perfumes, productos para el cuidado del cabello, suplementos nutricionales, etc.'},
            {'nombre': 'Moda', 'descripcion': 'Abarca ropa, zapatos, accesorios, joyería, bolsos, gafas de sol, relojes, etc.'},
            {'nombre': 'Deportes y actividades al aire libre', 'descripcion': 'Comprende artículos como equipos deportivos, ropa deportiva, calzado deportivo, productos para fitness, camping, senderismo, ciclismo, etc.'},
            {'nombre': 'Juguetes y juegos', 'descripcion': 'Incluye juguetes para niños, juegos de mesa, rompecabezas, muñecas, peluches, juegos educativos, etc.'},
            {'nombre': 'Libros y medios de comunicación', 'descripcion': 'Abarca libros impresos, libros electrónicos, audiolibros, música, películas, series de televisión, videojuegos, etc.'},
            {'nombre': 'Mascotas', 'descripcion': 'Abarca productos para mascotas como alimentos, juguetes, camas, correas, collares, productos para el cuidado, etc.'},
            {'nombre': 'Limpieza', 'descripcion': 'Incluye productos para la limpieza del hogar y productos de cuidado personal, como detergentes, desinfectantes, productos para el cuidado del suelo, limpiadores de cocina y baño, productos para el lavado de ropa, entre otros.'},
        ]
        
        states = [
            {'nombre': 'Activo'},
            {'nombre': 'Inactivo'},
            {'nombre': 'Descontinuado'}
        ]

        # Insertar categorias por defecto si no existen
        for dato in categorias:
            Categoria.objects.get_or_create(nombre=dato['nombre'], defaults={'descripcion': dato['descripcion']})

        for state in states:
            CStateProducto.objects.get_or_create(nombre=state['nombre'])