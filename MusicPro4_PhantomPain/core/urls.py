from django.contrib import admin
from django.urls import path
from .views import home,producto,html_registro,html_login,tienda,vista_usuario,vista_admin,tienda_admin,agregar_productos,carrito, formProducto,modperfil,olvidar,resetear,completar_pago,cancelar_pago,historial \
    ,  eliminacion_prod,modificar_productos,funcion_login,registro_view,mostrar_producto,agregar_al_carrito,actualizar_cantidad, carritoVacio, guardar_cantidades,iniciar_pago \
    ,  eliminacion_prodCarrito,modificar_perfil



urlpatterns = [
    path('historial', historial, name='historial'),
    path('cancelar_pago', cancelar_pago, name='cancelar_pago'),
    path('completar_pago/', completar_pago, name='completar_pago'),
    path('', home, name='index'),
    path('registro', html_registro, name='registro'),
    path('login', html_login, name='login'),
    path('tienda', tienda, name='tienda'),
    path('usuario', vista_usuario, name='vista_usuario'),
    path('modperfil', modperfil, name='modperfil'),
    path('resetear', resetear, name='resetear'),
    path('olvidar', olvidar, name='olvidar'),
    path('vista_admin', vista_admin, name='vista_admin'),
    path('tienda_admin', tienda_admin, name='tienda_admin'),
    path('agregar_productos', agregar_productos, name='agregar_productos'),
    path('carrito', carrito, name='carrito'),
    path('formProducto', formProducto, name='formProducto'),
    path('eliminacion_prod/<nombreProducto>', eliminacion_prod, name='eliminacion_prod'),
    path('modificar_productos/<id>', modificar_productos, name='modificar_productos'),
    path('funcion_login',funcion_login,name='funcion_login'),
    path('registro_view',registro_view,name='registro_view'),
    path('producto/<id>/',mostrar_producto, name='mostrar_producto'),
    path('agregar-al-carrito/<id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('actualizar-cantidad/', actualizar_cantidad, name='actualizar_cantidad'),
    path('carrito/eliminacion_prodCarrito/<id>',eliminacion_prodCarrito,name='eliminacion_prodCarrito'),
    path('carritoVacio',carritoVacio,name='carritoVacio'),
    path('guardar_cantidades/', guardar_cantidades, name='guardar_cantidades'),
    path('iniciar-pago/', iniciar_pago, name='iniciar_pago'),
    # path('compraExitosa',compraExitosa,name='compraExitosa'),
    path('modificar_perfil/<int:id>/', modificar_perfil, name='modificar_perfil'),
]

