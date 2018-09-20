from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from menu.forms import UnidadMedidaForm, ProductoForm, OrdenForm, InventarioForm, \
    CantidadesProductosFormSet, CantidadesInventarioFormSet, CantidadesSelfForm, CantidadesSelfFormSet, \
    CantidadesProductosForm, DescuentoForm, CustomUserCreationForm
from .models import UnidadMedida, Producto, Inventario, Orden, TipoCambio, CantidadesProductos, Descuento, \
    CustomUser, CantidadesInventario, Moneda
from django.urls import reverse_lazy, reverse


# MENU PRINCIPAL
def index(request):
    return render(request, 'menu/index.html')


# MENU INGREDIENTES

# -> Elementos

class detalleElemento(ListView):
    template_name = 'menu/modInventario.html'
    form_class = InventarioForm

    def get_queryset(self):
        return Inventario.objects.all()


class listaElementos(ListView):
    template_name = 'menu/listaInventario.html'

    def get_queryset(self):
        return Inventario.objects.all()


class ElementoCreate(CreateView):
    form_class = InventarioForm
    model = Inventario


class DescuentoCreate(CreateView):
    form_class = DescuentoForm
    model = Descuento


class DescuentoUpdate(UpdateView):
    form_class = DescuentoForm
    model = Descuento
    template_name = 'menu/modDescuento_form.html'


class listaDescuento(ListView):
    template_name = 'menu/listaDescuento.html'

    def get_queryset(self):
        return Descuento.objects.all()


class DescuentoDelete(DeleteView):
    model = Descuento
    success_url = reverse_lazy('home')


class ElementoUpdate(UpdateView):
    template_name = 'menu/modificarInventario_form.html'
    model = Inventario
    form_class = InventarioForm


class ElementoDelete(DeleteView):
    model = Inventario
    success_url = reverse_lazy('home')


# -> Unidades de medida
class UnidadMedidaCreate(CreateView):
    form_class = UnidadMedidaForm
    model = UnidadMedida


class UnidadMedidaUpdate(UpdateView):
    form_class = UnidadMedidaForm
    model = UnidadMedida
    template_name = 'menu/modificarUnidadMedida_form.html'


class detalleUnidadMedida(ListView):
    template_name = 'menu/modUnidadMedida.html'

    def get_queryset(self):
        return UnidadMedida.objects.all()


class UnidadMedidaDelete(DeleteView):
    model = UnidadMedida
    success_url = reverse_lazy('home')


# MENU Producto


class ProductoCreate(CreateView):
    form_class = ProductoForm
    model = Producto


class ProductoUpdate(UpdateView):
    form_class = ProductoForm
    model = Producto


class ProductoDelete(DeleteView):
    model = Producto
    success_url = reverse_lazy('home')


class listaProductos(ListView):
    template_name = 'menu/listaProducto.html'

    def get_queryset(self):
        return Producto.objects.all()


class detalleProducto(ListView):
    template_name = 'menu/modProducto.html'

    def get_queryset(self):
        return Producto.objects.all()


class OrdenUpdateF(UpdateView):
    model = Orden
    template_name = 'menu/listaOrden.html'
    context_object_name = 'factura'
    form_class = OrdenForm

    def get_context_data(self, **kwargs):
        data = super(OrdenUpdateF, self).get_context_data(**kwargs)
        if self.request.POST:
            data['lista_items'] = CantidadesProductos.objects.all()
            data['lista_productosFactura'] = Producto.objects.all()
        else:
            data['lista_items'] = CantidadesProductos.objects.all()
            data['lista_productosFactura'] = Producto.objects.all()
        return data


class detalleOrden(ListView):
    template_name = 'menu/modOrden.html'

    def get_queryset(self):
        return Orden.objects.filter(facturado=False)


class OrdenProductoCreate(CreateView):
    model = Orden
    form_class = OrdenForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        data = super(OrdenProductoCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['lista_prodOrden'] = CantidadesProductosFormSet(self.request.POST)
            data['lista_productosOrden'] = Producto.objects.all()
            data['lista_moneda'] = Moneda.objects.all()
            data['lista_tipoCambio'] = TipoCambio.objects.all()
        else:
            data['lista_prodOrden'] = CantidadesProductosFormSet()
            data['lista_productosOrden'] = Producto.objects.all()
            data['lista_moneda'] = Moneda.objects.all()
            data['lista_tipoCambio'] = TipoCambio.objects.all()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        lista_prodOrden = context['lista_prodOrden']
        with transaction.atomic():
            self.object = form.save()

            if lista_prodOrden.is_valid():
                lista_prodOrden.instance = self.object
                lista_prodOrden.save()
        return super(OrdenProductoCreate, self).form_valid(form)


class OrdenProductoUpdate(UpdateView):
    model = Orden
    form_class = OrdenForm
    template_name = "menu/modificarOrden_form.html"
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        data = super(OrdenProductoUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['lista_prodOrden'] = CantidadesProductosFormSet(self.request.POST, instance=self.object)
            data['lista_productosOrden'] = Producto.objects.all()
            data['lista_moneda'] = Moneda.objects.all()
            data['lista_tipoCambio'] = TipoCambio.objects.all()
        else:
            data['lista_prodOrden'] = CantidadesProductosFormSet(instance=self.object)
            data['lista_productosOrden'] = Producto.objects.all()
            data['lista_moneda'] = Moneda.objects.all()
            data['lista_tipoCambio'] = TipoCambio.objects.all()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        lista_prodOrden = context['lista_prodOrden']
        with transaction.atomic():
            self.object = form.save()

            if lista_prodOrden.is_valid():
                lista_prodOrden.instance = self.object
                lista_prodOrden.save()
        return super(OrdenProductoUpdate, self).form_valid(form)


class ProductoInventarioCreate(CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        data = super(ProductoInventarioCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['lista_inv'] = CantidadesInventarioFormSet(self.request.POST)
            data['lista_prod'] = CantidadesSelfFormSet(self.request.POST)
            data['lista_elementos'] = Inventario.objects.all()
            data['lista_productos'] = Producto.objects.all()
        else:
            data['lista_inv'] = CantidadesInventarioFormSet()
            data['lista_prod'] = CantidadesSelfFormSet()
            data['lista_elementos'] = Inventario.objects.all()
            data['lista_productos'] = Producto.objects.all()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        lista_inv = context['lista_inv']
        lista_prod = context['lista_prod']

        with transaction.atomic():
            self.object = form.save()

            if lista_inv.is_valid():
                lista_inv.instance = self.object
                lista_inv.save()

            if lista_prod.is_valid():
                lista_prod.instance = self.object
                lista_prod.save()

        return super(ProductoInventarioCreate, self).form_valid(form)


class ProductoInventarioUpdate(UpdateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        data = super(ProductoInventarioUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['lista_inv'] = CantidadesInventarioFormSet(self.request.POST, instance=self.object)
            data['lista_prod'] = CantidadesSelfFormSet(self.request.POST, instance=self.object)
            data['lista_elementos'] = Inventario.objects.all()
            data['lista_productos'] = Producto.objects.all()
        else:
            data['lista_inv'] = CantidadesInventarioFormSet(instance=self.object)
            data['lista_prod'] = CantidadesSelfFormSet(instance=self.object)
            data['lista_elementos'] = Inventario.objects.all()
            data['lista_productos'] = Producto.objects.all()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        lista_inv = context['lista_inv']
        lista_prod = context['lista_prod']
        with transaction.atomic():
            self.object = form.save()

            if lista_inv.is_valid():
                lista_inv.instance = self.object
                lista_inv.save()

            if lista_prod.is_valid():
                lista_prod.instance = self.object
                lista_prod.save()

        return super(ProductoInventarioUpdate, self).form_valid(form)


class modFactura(ListView):
    template_name = 'menu/modOrden.html'

    def get_queryset(self):
        return Orden.objects.filter(facturado=True)


class OrdenDelete(DeleteView):
    model = Orden
    success_url = reverse_lazy('home')


class detalleFactura(ListView):
    template_name = 'menu/modOrden.html'

    def get_queryset(self):
        return Orden.objects.filter(facturado=True)


class TipoCambioCreate(UpdateView):
    template_name = 'menu/tipoCambio_form.html'
    model = TipoCambio
    fields = fields = ['valor']


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'menu/usuario_form.html'

    def get_context_data(self, **kwargs):
        data = super(SignUp, self).get_context_data(**kwargs)
        if self.request.POST:
            data['lista_grupos'] = Group.objects.all()
        else:
            data['lista_grupos'] = Group.objects.all()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        with transaction.atomic():
            answer = self.request.POST['selectGrupos']
            print(answer)
            self.object = form.save()
            my_group = Group.objects.get(name=answer)
            my_group.user_set.add(self.object)
            reverse_lazy('home')

        return super(SignUp, self).form_valid(form)


class ModificarUsuario(UpdateView):
    form_class = UserChangeForm
    success_url = reverse_lazy('home')
    template_name = 'menu/actualizarUsuario.html'

    def get_queryset(self):
        return CustomUser.objects.all()


class ActualizarUsuario(ListView):
    form_class = UserChangeForm
    success_url = reverse_lazy('home')
    template_name = 'menu/modUsuario.html'

    def get_queryset(self):
        return CustomUser.objects.all()


class UsuarioDelete(DeleteView):
    form_class = UserChangeForm
    success_url = reverse_lazy('home')
