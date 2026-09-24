from django.db import models

class Usuario(models.Model):
    username = models.CharField(
        db_column='tx_username',
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Username'
    )

    email = models.EmailField(
        db_column='tx_email',
        max_length=100,
        blank=False,
        null=False,
        verbose_name='Email'
    )

    senha = models.CharField(
        db_column='tx_senha',
        max_length=1000,
        blank=False,
        null=False,
        unique=True,
    )

    nome_completo = models.CharField(
        db_column='tx_nome_completo',
        max_length=1000,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Nome Completo'
    )

    ta_ativo = models.BooleanField(
        db_column='fl_ta_ativo',
        default=False,
        verbose_name='Ativo'
    )

    data_entrada = models.DateTimeField(
        db_column='dt_data_login',
        blank=False,
        null=False,
        unique=True,
        verbose_name='Data de entrada'
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.username

class Descarte(models.Model):
    pass

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

    class Meta:
        verbose_name = 'Destino'
        verbose_name_plural = 'Destino'

    def __str__(self):
        return self.endereco



