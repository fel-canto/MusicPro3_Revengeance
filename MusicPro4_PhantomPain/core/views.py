from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto,TipoProducto,Carrito,ItemCarrito, Usuario
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import F, Sum
from decimal import Decimal
from paypalrestsdk import Payment
from django.http import HttpResponse
from forex_python.converter import CurrencyRates
from decimal import Decimal
from datetime import datetime
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login

def home(request):
    productos = Producto.objects.all()
    instrumentos = Producto.objects.filter(tipoNombre='1')
    equipos = Producto.objects.filter(tipoNombre='2')
    accesorios = Producto.objects.filter(tipoNombre='3')
    oferta = Producto.objects.filter(tipoNombre='4')
    bajos = Producto.objects.filter(nombreProducto__icontains='Bajo')
    data = {
        'oferta': oferta,
        'instrumentos': instrumentos,
        'equipos': equipos,
        'accesorios': accesorios,
        'bajos': bajos
    }
    return render(request, 'core/index.html', data)
# Create your views here.
def historial(request):
    return render(request, 'core/historial.html')

def cancelar_pago(request):
    return render(request, 'core/cancelar_pago.html')


def modperfil(request):
    return render(request, 'core/modperfil.html')

def olvidar(request):
    return render(request, 'core/olvidar.html')

def resetear(request):
    return render(request, 'core/resetear.html')

def producto(request):
    return render(request, 'core/producto.html')

def html_registro(request):
    return render(request, 'core/formularioRegistro.html')

def html_login(request):
    return render(request, 'core/formularioLogin.html')

@login_required
def tienda(request):
    productos = Producto.objects.all()
    instrumentos = Producto.objects.filter(tipoNombre='1')
    equipos = Producto.objects.filter(tipoNombre='2')
    accesorios = Producto.objects.filter(tipoNombre='3')
    oferta = Producto.objects.filter(tipoNombre='4')

    data = {
        'oferta': oferta,
        'instrumentos': instrumentos,
        'equipos': equipos,
        'accesorios': accesorios
    }
    return render(request, 'core/tienda.html', data)

@login_required
def vista_usuario(request):
    productos = Producto.objects.all()
    instrumentos = Producto.objects.filter(tipoNombre='1')
    equipos = Producto.objects.filter(tipoNombre='2')
    accesorios = Producto.objects.filter(tipoNombre='3')
    oferta = Producto.objects.filter(tipoNombre='4')
    bajos = Producto.objects.filter(nombreProducto__icontains='Bajo')
    data = {
        'oferta': oferta,
        'instrumentos': instrumentos,
        'equipos': equipos,
        'accesorios': accesorios,
        'bajos': bajos
    }
    return render(request, 'core/vista_usuario.html',data)
@permission_required('core.add_producto')
def vista_admin(request):
    productos = Producto.objects.all()
    instrumentos = Producto.objects.filter(tipoNombre='1')
    equipos = Producto.objects.filter(tipoNombre='2')
    accesorios = Producto.objects.filter(tipoNombre='3')
    oferta = Producto.objects.filter(tipoNombre='4')
    bajos = Producto.objects.filter(nombreProducto__icontains='Bajo')
    data = {
        'oferta': oferta,
        'instrumentos': instrumentos,
        'equipos': equipos,
        'accesorios': accesorios,
        'bajos': bajos
    }
    return render(request, 'core/vista_admin.html',data)


@permission_required('core.add_producto')
def tienda_admin(request):
    productos = Producto.objects.all()
    instrumentos = Producto.objects.filter(tipoNombre='1')
    equipos = Producto.objects.filter(tipoNombre='2')
    accesorios = Producto.objects.filter(tipoNombre='3')
    oferta = Producto.objects.filter(tipoNombre='4')

    data = {
        'oferta': oferta,
        'instrumentos': instrumentos,
        'equipos': equipos,
        'accesorios': accesorios
    }
    return render(request, 'core/tienda_admin.html', data)

@permission_required('core.add_producto')
def agregar_productos(request):
    tipo_producto = TipoProducto.objects.all()
    variables ={
        'tipo_producto':tipo_producto
    }

    return render(request, 'core/formularioAgregarProductos.html', variables)

@login_required
def agregar_al_carrito(request, id):
    producto = get_object_or_404(Producto, id=id)

    if 'carrito_id' in request.session:
        carrito = get_object_or_404(Carrito, id=request.session['carrito_id'])
        carrito.estado = 'abierto'  # Cambia el estado del carrito a 'abierto'
    else:
        carrito = Carrito.objects.create(usuario=request.user)
        request.session['carrito_id'] = carrito.id

    cantidad = 1
    item_carrito = ItemCarrito(carrito=carrito, producto=producto, cantidad=cantidad)
    item_carrito.save()

    # Recalcular el total del carrito
    items = ItemCarrito.objects.filter(carrito=carrito)
    total = items.aggregate(total=Sum(F('producto__precioProducto') * F('cantidad')))['total']
    if total is not None:
        total = Decimal(total).quantize(Decimal('.00'))
    else:
        total = 0
    carrito.total = total
    carrito.save()

    return redirect('carrito')

#PARA CUANDO EL FELIPE QL SE DIGNE A HACER LA WEA DE CARRITO @login_required
@login_required
def carrito(request):
    carrito_id = request.session.get('carrito_id')
    if carrito_id:
        try:
            carrito_actual = Carrito.objects.get(id=carrito_id)
        except Carrito.DoesNotExist:
            carrito_actual = None
    else:
        carrito_actual = Carrito.objects.create(usuario=request.user)
        request.session['carrito_id'] = carrito_actual.id

    items = ItemCarrito.objects.filter(carrito=carrito_actual)

    if not items:
        return redirect('carritoVacio')

    total = items.aggregate(total=Sum(F('producto__precioProducto') * F('cantidad')))['total'] or 0
    total = Decimal(total).quantize(Decimal('.00'))

    context = {
        'items': items,
        'total': total
    }

    return render(request, 'core/carrito.html', context)
    
@permission_required('core.add_producto')
def formProducto(request):
    tipo_producto = TipoProducto.objects.all()
    variables ={
        'tipo_producto':tipo_producto
    }

    if request.POST:
        pro = Producto()
        pro.nombreProducto = request.POST.get('nomProd')
        pro.descripcionProducto = request.POST.get('descProd')
        pro.precioProducto = request.POST.get('precio')
        pro.stockProducto = request.POST.get('cantidad')
        ti_producto = TipoProducto()
        ti_producto.id = request.POST.get('tipo_producto')
        pro.tipoNombre = ti_producto
        pro.imagenUno = request.FILES.get('foto_1')
        pro.imagenDos = request.FILES.get('foto_2')
        pro.imagenTres = request.FILES.get('foto_3')
        pro.imagenCuatro = request.FILES.get('foto_4')

        try:
            pro.save()
            messages.success(request, 'Producto agregado correctamente')
            return redirect('agregar_productos')
        except:
            messages.error(request, 'No se pudo agregar el producto')

    return redirect(request, 'core/formularioAgregarProductos.html')

@permission_required('core.add_producto')
def eliminacion_prod(request, nombreProducto):
    producto = Producto.objects.get(nombreProducto = nombreProducto)
    producto.delete()
    messages.success(request, 'Producto eliminado con éxito')

    return redirect('tienda_admin')

@permission_required('core.add_producto')
def modificar_productos(request, id):
    producto = get_object_or_404(Producto, pk=id)
    tipo_producto = TipoProducto.objects.all()

    if request.method == 'POST':
        producto.nombreProducto = request.POST.get('nomProd')
        producto.descripcionProducto = request.POST.get('descripcionProducto')
        producto.precioProducto = request.POST.get('precioProducto')
        producto.stockProducto = request.POST.get('stockProducto')
        producto.tipoNombre_id = request.POST.get('tipo_producto')

        # Actualizar las imágenes solo si se proporcionan nuevos archivos
        if 'imagenUno' in request.FILES:
            producto.imagenUno = request.FILES['imagenUno']
        if 'imagenDos' in request.FILES:
            producto.imagenDos = request.FILES['imagenDos']
        if 'imagenTres' in request.FILES:
            producto.imagenTres = request.FILES['imagenTres']
        if 'imagenCuatro' in request.FILES:
            producto.imagenCuatro = request.FILES['imagenCuatro']

        producto.save()
        return redirect('tienda_admin')
    
    return render(request, 'core/modificarProductos.html', {'producto': producto, 'tipo_producto': tipo_producto})

def funcion_login(request):
    if request.method == 'POST':
        username = request.POST['nombre']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.has_perm('core.add_producto'):      
                 return redirect('vista_admin')
            else:
                 return redirect('vista_usuario') # Cambia 'vista_usuario' con el nombre de tu vista principal

        else:
            messages.error(request, 'El usuario y/o contraseña no coinciden o no existen.')
            return render(request, 'core/formularioLogin.html')
            
    return render(request, 'core/formularioLogin.html')

@csrf_protect
def registro_view(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        email = request.POST['email']
        celular = request.POST['celular']
        password = request.POST['password']
        repeat_password = request.POST['repeatPassword']

        if password == repeat_password:
            try:
                # Crea un nuevo usuario utilizando la tabla User de Django
                user = User.objects.create_user(username=email, password=password)
                # Agrega los campos personalizados al usuario
                user.first_name = nombre
                user.last_name = apellido
                user.email = email
                user.save()
                # Inicia sesión automáticamente después del registro
                user = authenticate(request, username=email, password=password)
                login(request, user)
                return redirect('login')  # Redirige a la página de inicio después del registro exitoso
            except Exception as e:
                messages.error(request, f'Error al registrar el usuario: {str(e)}')
        else:
            messages.error(request, 'Las contraseñas no coinciden')

    return render(request, 'core/formularioRegistro.html')


def mostrar_producto(request, id):
    producto = get_object_or_404(Producto, pk=id)
    return render(request, 'core/producto.html', {'producto': producto})



def actualizar_cantidad(request):
    if request.method == 'POST' and request.is_ajax():
        product_id = request.POST.get('productId')
        quantity = request.POST.get('quantity')
        item = ItemCarrito.objects.get(pk=product_id)
        item.cantidad_actualizada = quantity
        item.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})

@login_required
def carritoVacio(request):
    return render(request, 'core/carritoVacio.html')


@csrf_exempt
def guardar_cantidades(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        cantidad = request.POST.get('cantidad')
        item = ItemCarrito.objects.get(id=item_id)
        item.cantidad = cantidad
        item.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)

@login_required
def iniciar_pago(request):
    user = request.user

    try:
        # Obtener el carrito actual del usuario
        carrito = Carrito.objects.get(usuario=user, estado='abierto')

        # Obtener el precio total del carrito en CLP
        total_carrito_clp = carrito.total

        # Calcular el precio total del carrito en USD utilizando la tasa de cambio
        exchange_rate_clp_usd = 0.0012
        total_carrito_usd = round(float(total_carrito_clp) * exchange_rate_clp_usd, 2)

        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://localhost:8000/completar_pago/",
                "cancel_url": "http://localhost:8000/cancelar_pago/"
            },
            "transactions": [{
                "amount": {
                    "total": str(total_carrito_usd),  # Pasar el precio total del carrito en USD
                    "currency": "USD"
                },
                "description": "Compra en la tienda de instrumentos musicales"
            }]
        })

        if payment.create():
            # Asociar el ID del pago con el carrito actual
            carrito.payment_transaction = payment.id
            carrito.save()

            for link in payment.links:
                if link.method == "REDIRECT":
                    redirect_url = str(link.href)

                    return redirect(redirect_url)
        else:
            error_message = "Error al iniciar el pago: " + payment.error
            return render(request, "core/cancelar_pago.html", {"error_message": error_message})
    except Carrito.DoesNotExist:
        error_message = "Carrito no encontrado."
        return render(request, "core/cancelar_pago.html", {"error_message": error_message})

    error_message = "Error al iniciar el pago."
    return render(request, "core/cancelar_pago.html", {"error_message": error_message})


def completar_pago(request):
    payment_id = request.GET.get('paymentId')
    token = request.GET.get('token')
    payer_id = request.GET.get('PayerID')
    current_date = datetime.now()

    if payment_id:
        payment = Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            user = request.user
            carrito = Carrito.objects.get(usuario=user.id, estado='abierto')
            carrito.estado = 'cerrado'
            carrito.save()
            total = carrito.total
            idCompra = carrito.id
            contexto = {
                'usuario': user,
                'total_pagado': payment.transactions[0].amount.total,
                'moneda': payment.transactions[0].amount.currency,
                'hora': current_date,
                'total': total,
                'idCompra':idCompra
                # Agrega aquí cualquier otro dato que desees mostrar en el template
            }
            ItemCarrito.objects.all().delete()
            return render(request, 'core/completar_pago.html', contexto)
        else:
            return render(request, 'core/cancelar_pago.html')
    else:
        return render(request, 'core/cancelar_pago.html')

@csrf_exempt
def eliminacion_prodCarrito(request, id):
    productoCarrito = ItemCarrito.objects.get(id=id)
    productoCarrito.delete()
    messages.success(request, 'Producto eliminado con éxito')

    return redirect('carrito')

@login_required
def modificar_perfil(request, id):
    user = request.user

    if request.method == 'POST':
        # Obtener los datos enviados en el formulario
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        celular = request.POST.get('celular')
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        repeat_password = request.POST.get('repeat-new-password')
        print(user.first_name)
        print(user.last_name)
        print(user.email)

        # Verificar si la contraseña antigua es correcta
        if not user.check_password(password):
            messages.error(request, 'Contraseña incorrecta.')
            return redirect('modificar_perfil', id=id)

        # Actualizar los datos del usuario
        user.first_name = nombre
        user.last_name = apellido
        user.email = email
        user.username = email
        user.save()

        # Verificar si se proporcionó una nueva contraseña
        if new_password:
            # Verificar si las contraseñas nuevas coinciden
            if new_password != repeat_password:
                messages.error(request, 'Las contraseñas no coinciden.')
                return redirect('modificar_perfil', id=id)

            # Cambiar la contraseña del usuario
            user.set_password(new_password)
            user.save()

            # Iniciar sesión nuevamente para actualizar la sesión con la nueva contraseña
            auth_login(request, user)

        messages.success(request, 'Perfil actualizado exitosamente.')
        return redirect('vista_usuario')

    return render(request, 'core/modperfil.html', {'usuario': user})