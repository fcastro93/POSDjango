from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group
from django.forms import inlineformset_factory

from menu.models import Inventario, UnidadMedida, Producto, Orden, TipoOrden, Moneda, TipoPago, \
    Descuento, CantidadesProductos, CantidadesInventario, CantidadesSelf, CustomUser
from django import forms
from django.utils.translation import ugettext_lazy as _


class UnidadMedidaForm(forms.ModelForm):
    class Meta:
        model = UnidadMedida
        fields = ['nombre', 'sigla']
        widgets = {
            'nombre': forms.TextInput(attrs={'style': 'background: #c2c0c0', 'class': 'form-control'}),
            'sigla': forms.TextInput(attrs={'style': 'background: #c2c0c0', 'class': 'form-control'})

        }


class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['nombre', 'cantidad', 'unidadMedida', 'valorCompra', 'valorVenta']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'style': 'background: #c2c0c0'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control', 'style': 'background: #c2c0c0'}),
            'valorCompra': forms.NumberInput(attrs={'class': 'form-control', 'style': 'background: #c2c0c0'}),
            'valorVenta': forms.NumberInput(attrs={'class': 'form-control', 'style': 'background: #c2c0c0'})

        }
        unidadMedida = forms.ModelChoiceField(queryset=UnidadMedida.objects.all(),
                                              widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(InventarioForm, self).__init__(*args, **kwargs)
        self.fields['unidadMedida'].empty_label = _("UNIT")
        self.fields['unidadMedida'].widget.choices = self.fields['unidadMedida'].choices


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'valor']
        widgets = {
            'nombre': forms.TextInput(attrs={'style': 'background: #c2c0c0', 'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'style': 'background: #c2c0c0', 'class': 'form-control'})
        }


class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['cliente', 'tipoOrden', 'pagadores', 'tipoPago', 'notas',
                  'precioFinal', 'descuento', 'facturado']
        widgets = {
            'cliente': forms.TextInput(attrs={'style': 'background: #c2c0c0', 'class': 'form-control'}),
            'pagadores': forms.NumberInput(
                attrs={'style': 'background: #c2c0c0', 'class': 'form-control'}),
            'notas': forms.TextInput(attrs={'style': 'background: #c2c0c0', 'class': 'form-control'}),
            'precioFinal': forms.NumberInput(attrs={'style': 'background: #c2c0c0', 'class': 'form-control'}),
            'facturado': forms.CheckboxInput()
        }
        tipoOrden = forms.ModelChoiceField(queryset=TipoOrden.objects.all(),
                                           widget=forms.Select(attrs={'class': 'wrap-input100'}))
        descuento = forms.ModelChoiceField(queryset=Descuento.objects.all(),
                                           widget=forms.Select(attrs={'class': 'wrap-input100'}))
        tipoPago = forms.ModelChoiceField(queryset=TipoPago.objects.all())

    def __init__(self, *args, **kwargs):
        super(OrdenForm, self).__init__(*args, **kwargs)
        self.fields['descuento'].empty_label = "0"
        self.fields['descuento'].widget.choices = self.fields['descuento'].choices
        self.fields['tipoPago'].empty_label = _("PAYMENT")
        self.fields['tipoPago'].widget.choices = self.fields['tipoPago'].choices
        self.fields['tipoOrden'].empty_label = _("TYPE")
        self.fields['tipoOrden'].widget.choices = self.fields['tipoOrden'].choices


class CantidadesProductosForm(forms.ModelForm):
    class Meta:
        model = CantidadesProductos
        exclude = ()


CantidadesProductosFormSet = inlineformset_factory(Orden, CantidadesProductos, form=CantidadesProductosForm, extra=1)


class CantidadesInventarioForm(forms.ModelForm):
    class Meta:
        model = CantidadesInventario
        exclude = ()


CantidadesInventarioFormSet = inlineformset_factory(Producto, CantidadesInventario, form=CantidadesInventarioForm,
                                                    extra=1)


class CantidadesSelfForm(forms.ModelForm):
    class Meta:
        model = CantidadesSelf
        exclude = ()


CantidadesSelfFormSet = inlineformset_factory(Producto, CantidadesSelf, form=CantidadesSelfForm, fk_name="producto",
                                              extra=1)


class DescuentoForm(forms.ModelForm):
    class Meta:
        model = Descuento
        fields = ['valor']


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'direct_boss', 'indirect_boss', 'creator_boss')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'direct_boss', 'indirect_boss', 'creator_boss')


class UserGroupForm(forms.Form):
    CHOICES = [(group.name, group.name) for group in Group.objects.all()]
    name = forms.ChoiceField(choices=CHOICES, widget=forms.widgets.RadioSelect())
