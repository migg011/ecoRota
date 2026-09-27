from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    email = models.EmailField(
        db_column='tx_email',
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Email'
    )

    nome_completo = models.CharField(
        db_column='tx_nome_completo',
        max_length=1000,
        blank=False,
        null=False,
        unique=False,
        verbose_name='Nome Completo'
    )

    class Meta:
        managed = True
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.username

class Destino(models.Model):
    categoria = models.CharField(
        db_column='tx_categoria',
        max_length=100,
        blank=False,
        null=False,
        verbose_name='Categoria'
    )

    endereco = models.TextField(
        db_column='tx_endereco',
        blank=False,
        null=False,
        verbose_name='Endereco'
    )

    descricao = models.TextField(
        db_column='tx_descricao',
        blank=False,
        null=False,
        verbose_name='Descricao'
    )

    class Meta:
        managed = True
        db_table = 'destino'
        verbose_name = 'Destino'
        verbose_name_plural = 'Destino'

    def __str__(self):
        return self.endereco


class Descarte(models.Model):
    Usuario = models.ForeignKey(
        Usuario,
        db_column='usuario_id',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name='Usuario',
        related_name='descarte',
    )

    Destino = models.ForeignKey(
        Destino,
        db_column='destino_id',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name='Destino',
        related_name='descarte',
    )

    data_criacao = models.DateTimeField(
        db_column='dt_data_criacao',
        blank=False,
        null=False,
        unique=True,
        verbose_name='Data de criacao'
    )

    peso_estimado_kg = models.FloatField(
        db_column='vl_peso_estimado_kg',
        blank=False,
        null=False,
        unique=True,
        verbose_name='Peso Estimado'
    )

    categoria = models.CharField(
        db_column='tx_categoria',
        max_length=100,
        blank=False,
        null=False,
        verbose_name='Categoria'
    )

    input_do_usuario = models.TextField(
        db_column='tx_input_do_usuario',
        max_length=1000,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Input do Usuario'
    )

    class Meta:
        managed = True
        db_table = 'descarte'
        verbose_name = 'Descarte'
        verbose_name_plural = 'Descarte'

    def __str__(self):
        return self.Destino.endereco


