from django.core.management.base import BaseCommand

from EcoRota.models import Usuario


EMAIL_DEMO = "teste@ecorota.com"
SENHA_DEMO = "TESTE123"
NOME_DEMO = "UsuariorTeste"


class Command(BaseCommand):
    help = "Cria (ou reforça a senha do) usuário de demonstração do projeto"

    def handle(self, *args, **options):
        usuario = Usuario.objects.filter(username=EMAIL_DEMO).first()

        if usuario is None:
            usuario = Usuario.objects.create_user(
                username=EMAIL_DEMO,
                email=EMAIL_DEMO,
                nome_completo=NOME_DEMO,
                password=SENHA_DEMO,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Usuário demo criado: {EMAIL_DEMO}")
            )
        else:
            # garante que a senha de demonstração funcione mesmo se alguém mudou
            usuario.set_password(SENHA_DEMO)
            usuario.save()
            self.stdout.write(
                self.style.SUCCESS(f"Usuário demo já existia, senha redefinida: {EMAIL_DEMO}")
            )

        self.stdout.write(f"Email: {EMAIL_DEMO}")
        self.stdout.write(f"Senha: {SENHA_DEMO}")
