# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser

class Clients(models.Model):
    nif = models.CharField(unique=True, max_length=15)
    nom = models.CharField(max_length=150)
    cognoms = models.CharField(max_length=255)
    telefon = models.CharField(max_length=15)
    email = models.CharField(max_length=100)
    direccio = models.CharField(max_length=255)
    ciutat = models.CharField(max_length=100)
    codi_postal = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'clients'


class Comptadors(models.Model):
    concepte = models.CharField(primary_key=True, max_length=1)
    comptador = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'comptadors'


class DefinicioTipusLinia(models.Model):
    nom = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'definicio_tipus_linia'


class EstatReparacio(models.Model):
    nom = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'estat_reparacio'


class Factura(models.Model):
    num_fact = models.CharField(max_length=18)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    preu_ma_obra = models.DecimalField(max_digits=10, decimal_places=2)
    id_reparacio = models.ForeignKey('Reparacio', models.DO_NOTHING, db_column='id_reparacio')
    data_factura = models.DateField()
    pagada = models.IntegerField()
    base_imposable = models.DecimalField(max_digits=10, decimal_places=2)
    quota_iva = models.DecimalField(max_digits=10, decimal_places=2)
    total_factura = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'factura'


class LiniesReparacio(models.Model):
    id_def = models.ForeignKey(DefinicioTipusLinia, models.DO_NOTHING, db_column='id_def')
    descripcio = models.CharField(max_length=255, blank=True, null=True)
    preu = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    codi_fabricant = models.CharField(max_length=255, blank=True, null=True)
    descompte = models.IntegerField()
    id_factura = models.ForeignKey(Factura, models.DO_NOTHING, db_column='id_factura', blank=True, null=True)
    preu_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantitat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    id_pack = models.ForeignKey('PacksDef', models.DO_NOTHING, db_column='id_pack', blank=True, null=True)
    id_reparacio = models.ForeignKey('Reparacio', models.DO_NOTHING, db_column='id_reparacio')

    class Meta:
        managed = False
        db_table = 'linies_reparacio'


class MarcaModel(models.Model):
    nom = models.CharField(max_length=2000)

    class Meta:
        managed = False
        db_table = 'marca_model'


class PacksDef(models.Model):
    nom = models.CharField(max_length=255)
    preu = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'packs_def'


class Reparacio(models.Model):
    data_alta = models.DateField()
    id_estat_reparacio = models.ForeignKey(EstatReparacio, models.DO_NOTHING, db_column='id_estat_reparacio')
    id_usuari = models.ForeignKey('Usuari', models.DO_NOTHING, db_column='id_usuari')
    id_vehicle = models.ForeignKey('Vehicle', models.DO_NOTHING, db_column='id_vehicle')

    class Meta:
        managed = False
        db_table = 'reparacio'


class TipusUsuari(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tipus_usuari'

    def to_json(self):
        return {
            'id': self.id,
            'nom': self.nom
        }


class Usuari(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.CharField(unique=True, max_length=20)
    contrasenya = models.CharField(max_length=255)
    nom = models.CharField(max_length=100)
    id_tipus_usuari = models.ForeignKey(TipusUsuari, models.DO_NOTHING, db_column='id_tipus_usuari')
    

    class Meta:
        managed = False
        db_table = 'usuari'

    def to_json(self):
        return {
            'id': self.id,
            'login': self.login,
            'contrasenya': self.contrasenya,
            'nom': self.nom,
            'id_tipus_usuari': self.id_tipus_usuari.id
            
        }


class Vehicle(models.Model):
    matricula = models.CharField(unique=True, max_length=15)
    kms = models.DecimalField(max_digits=10, decimal_places=2)
    id_client = models.ForeignKey(Clients, models.DO_NOTHING, db_column='id_client')
    id_marca_model = models.ForeignKey(MarcaModel, models.DO_NOTHING, db_column='id_marca_model')

    class Meta:
        managed = False
        db_table = 'vehicle'
