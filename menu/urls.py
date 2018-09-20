from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [

    # MENU PRINCIPAL

    # index
    url(r'^$', login_required(views.index), name='home'),

    # login
    url(r'^login/$', LoginView.as_view(), name='login'),

    # login
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),

    # ELEMENTOS

    # Agregar un elemento

    url(r'^agregarElemento/$', login_required(views.ElementoCreate.as_view(success_url="/menu/")),
        name='agregarElemento'),

    # Lista para modificar elementos

    url(r'^modElemento/$', login_required(views.detalleElemento.as_view(
    )), name='modElemento'),

    # Actualizar elemento

    url(r'^actualizarElemento/(?P<pk>[0-9]+)/$', login_required(views.ElementoUpdate.as_view(
        success_url="/menu/modElemento/")), name='actualizarElemento'),

    # Borrar elemento

    url(r'^actualizarElemento/(?P<pk>[0-9]+)/borrar$', login_required(views.ElementoDelete.as_view(
    )), name='borrarElemento'),

    # Lista sola de elementos

    url(r'^listaElemento/$', login_required(views.listaElementos.as_view()), name='listaElementos'),

    # UNIDADES DE MEDIDA

    # Agregar unidad

    url(r'^agregarUnidadMedida/$', login_required(views.UnidadMedidaCreate.as_view(success_url="/menu/")),
        name='agregarUnidadMedida'),

    # Actualizar unidad

    url(r'^actualizarUnidadMedida/(?P<pk>[0-9]+)/$', login_required(views.UnidadMedidaUpdate.as_view(
        success_url="/menu/modUnidadMedida/")), name='actualizarUnidadMedida'),

    # Lista de unidades para modificar

    url(r'^modUnidadMedida/$', login_required(views.detalleUnidadMedida.as_view(
    )), name='modUnidadMedida'),

    # Borrar una unidad

    url(r'^borrarUnidadMedida/(?P<pk>[0-9]+)/borrar$', login_required(views.UnidadMedidaDelete.as_view(
    )), name='borrarUnidadMedida'),

    # PRODUCTOS

    # Agregar un producto

    url(r'^agregarProducto/$', login_required(views.ProductoInventarioCreate.as_view(success_url="/menu/")),
        name='agregarProducto'),

    # Lista de productos para modificar

    url(r'^modProducto/$', login_required(views.detalleProducto.as_view(
    )), name='modProducto'),

    # Actualizar un producto

    url(r'^actualizarProducto/(?P<pk>[0-9]+)/$', login_required(views.ProductoInventarioUpdate.as_view(
        success_url="/menu/modProducto/")), name='actualizarProducto'),

    # Borrar un producto

    url(r'^actualizarProducto/(?P<pk>[0-9]+)/borrar$', login_required(views.ProductoDelete.as_view(
    )), name='borrarProducto'),

    # ORDENES

    # Agregar una orden

    url(r'^agregarOrden/$', login_required(views.OrdenProductoCreate.as_view()),
        name='agregarElemento'),

    # Actualizar Orden

    url(r'^actualizarOrden/(?P<pk>[0-9]+)/$', login_required(views.OrdenProductoUpdate.as_view(
        success_url="/menu/modOrden/")), name='actualizarOrden'),

    # Borrar Orden

    url(r'^actualizarOrden/(?P<pk>[0-9]+)/borrar$', login_required(views.OrdenDelete.as_view(
        success_url="/menu/modOrden/")), name='borrarOrden'),

    # Facturacion

    url(r'^facturar/(?P<pk>[0-9]+)/$', login_required(views.OrdenUpdateF.as_view()), name='facturar'),

    # Lista de ordenes para modificar

    url(r'^modOrden/$', login_required(views.detalleOrden.as_view(
    )), name='modOrden'),

    # Lista de facturas a modificar

    url(r'^modFactura/$', login_required(views.modFactura.as_view(
    )), name='modFactura'),

    # TIPO DE CAMBIO

    # Modificar tipo de cambio

    url(r'^tipoCambio/(?P<pk>[0-9]+)/$', login_required(views.TipoCambioCreate.as_view(success_url="/menu/")),
        name='modFactura'),

    # USUARIOS

    # Crear usuario
    url(r'^crearUsuario/$', login_required(views.SignUp.as_view(success_url="/menu/")),
        name='crearUsuario'),

    # Editar usuario actual
    url(r'^actualizarUsuario/(?P<pk>[0-9]+)/$', login_required(views.ModificarUsuario.as_view(success_url="/menu/")),
        name='actualizarUsuario'),

    # Lista de usuarios a modificar

    url(r'^actualizarUsuario/$', login_required(views.ActualizarUsuario.as_view(
    )), name='modUsuario'),

    # Borrar usuario

    url(r'^borrarUsuario/(?P<pk>[0-9]+)/borrar$', login_required(views.UsuarioDelete.as_view(
    )), name='borrarUsuario'),

    # Descuentos

    # Agregar un Descuento

    url(r'^agregarDescuento/$', login_required(views.DescuentoCreate.as_view(success_url="/menu/")),
        name='agregarDescuento'),

    # Modificar un Descuento

    url(r'^actualizarDescuento/(?P<pk>[0-9]+)/$', login_required(views.DescuentoUpdate.as_view(success_url="/menu/")),
        name='actualizarDescuento'),

    # Lista de Descuento
    url(r'^listaDescuento/$', login_required(views.listaDescuento.as_view(
    )), name='listaDescuento'),

    # Borrar Descuento

    url(r'^actualizarDescuento/(?P<pk>[0-9]+)/borrar$', login_required(views.DescuentoDelete.as_view(
        success_url="/menu/")), name='borrarDescuento'),

]
