from datetime import datetime
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

from Inventario import settings


class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=500)
    sigla = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre


class Inventario(models.Model):
    nombre = models.CharField(max_length=500)
    cantidad = models.IntegerField()
    unidadMedida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE, default=None)
    valorCompra = models.BigIntegerField(default=None, blank=True, null=True)
    valorVenta = models.BigIntegerField(default=None, blank=True, null=True)

    def __str__(self):
        return self.nombre


class TipoPago(models.Model):
    nombre = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre


class TipoOrden(models.Model):
    nombre = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre


class Moneda(models.Model):
    nombre = models.CharField(max_length=500)
    siglas = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    class Meta:
        ordering = ['nombre']

    nombre = models.CharField(max_length=500)
    valor = models.BigIntegerField(default=None, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Descuento(models.Model):
    class Meta:
        ordering = ['valor']

    valor = models.IntegerField()

    def __str__(self):
        return str(self.valor)


class Orden(models.Model):
    fecha = models.DateField(default=timezone.now)
    pagadores = models.IntegerField()
    tipoOrden = models.ForeignKey(TipoOrden, on_delete=models.CASCADE)
    tipoPago = models.ForeignKey(TipoPago, on_delete=models.CASCADE)
    cliente = models.CharField(max_length=500)
    productosExtra = models.ManyToManyField(Producto, through='CantidadesProductos', blank=True)
    notas = models.CharField(max_length=1000, default=None, blank=True, null=True)
    precioFinal = models.BigIntegerField()
    facturado = models.BooleanField(default=False)
    numero = models.BigIntegerField(default=0)
    descuento = models.ForeignKey(Descuento, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.pk)


class CantidadesProductos(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.BigIntegerField(default=0)


class CantidadesInventario(models.Model):
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.BigIntegerField(default=0)


class CantidadesSelf(models.Model):
    productoSelf = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="elemento")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="lista")
    cantidad = models.BigIntegerField(default=0)


class TipoCambio(models.Model):
    valor = models.IntegerField()

    def __str__(self):
        return self.valor


class CustomUser(AbstractUser):
    class Meta:
        permissions = (
            ("can_inventory", "Puede Ver Inventario"),
            ("can_products", "Puede Ver Productos"),
            ("can_orders", "Puede Ver Ordenes"),
            ("can_reports", "Puede Ver Reportes"),
            ("can_discounts", "Puede Ver Descuentos"),

            #Funciones especificas

                # User
            ("is_agent", "Puede Crear cajeros"),
                # Inventario
            ("can_create_element", "Puede Crear Elemento"),
            ("can_mod_element", "Puede Modificar Elemento"),
            ("can_create_unit", "Puede Crear Unidad de Medida"),
            ("can_mod_unit", "Puede Modificar Unidad de Medida"),
                # Productos
            ("can_create_product", "Puede Crear Producto"),
            ("can_mod_product", "Puede Modificar Producto"),
                # Orden
            ("can_create_order", "Puede Crear Orden"),
            ("can_invoices", "Puede Entrar a facturas"),
            ("can_frozen_order", "Puede Entrar a Ordenes Abiertas"),
            ("can_mod_exchange", "Puede Modificar Tipo de Cambio"),
                # Descuento
            ("can_create_discount", "Puede Crear Descuento"),
            ("can_mod_discount", "Puede Modificar Descuento"),
        )

    direct_boss = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="rdirect_boss", unique=False, blank=True,
                                    null=True, db_index=True)
    indirect_boss = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="rindirect_boss", unique=False, blank=True,
                                      null=True,
                                      db_index=True)
    creator_boss = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="rcreator_boss", unique=False, blank=True,
                                     null=True,
                                     db_index=True)
