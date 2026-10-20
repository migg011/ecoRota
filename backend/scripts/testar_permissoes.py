import sys
from pathlib import Path

from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
load_dotenv(RAIZ / '.env')

import django

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.test import Client

from EcoRota.models import Destino, Usuario

sys.stdout.reconfigure(encoding="utf-8")

EMAIL_DEMO = "teste@ecorota.com"
EMAIL_ADMIN = "AdminTeste"

aprovados = 0
reprovados = 0


def verificar(nome_do_teste, condicao, detalhe):
    global aprovados, reprovados
    if condicao:
        aprovados += 1
        print(f"  [OK] {nome_do_teste} -> {detalhe}")
    else:
        reprovados += 1
        print(f"  [ERRO] {nome_do_teste} -> {detalhe}")


def main():
    print("Testando as permissoes de acesso aos destinos")
    print("=" * 70)

    demo = Usuario.objects.filter(username=EMAIL_DEMO).first()
    admin = Usuario.objects.filter(username=EMAIL_ADMIN).first()

    verificar(
        "Usuario demo existe",
        demo is not None,
        EMAIL_DEMO if demo else "rode: python manage.py criar_usuario_demo",
    )
    verificar(
        "Usuario admin existe",
        admin is not None,
        EMAIL_ADMIN if admin else "crie o superusuario pelo /admin/",
    )
    if demo is None or admin is None:
        print("=" * 70)
        print("Sem os usuarios nao da pra continuar")
        sys.exit(1)

    verificar(
        "Admin tem a flag is_staff",
        admin.is_staff,
        "is_staff=True" if admin.is_staff else "o admin precisa de is_staff=True",
    )

    destino_qualquer = Destino.objects.first()
    verificar(
        "Existe pelo menos 1 destino no banco",
        destino_qualquer is not None,
        "rode: python manage.py seed_destinos" if destino_qualquer is None else destino_qualquer.nome,
    )

    destino_teste = {
        'nome': 'Ecoponto Teste Script',
        'categoria': 'Madeira',
        'endereco': 'Rua do Script, 99',
        'descricao': 'Destino criado pelo script de teste de permissoes',
        'horario': 'Seg a Sex, 8h as 17h',
    }

    anonimo = Client(HTTP_HOST='localhost')
    como_demo = Client(HTTP_HOST='localhost')
    como_demo.force_login(demo)
    como_admin = Client(HTTP_HOST='localhost')
    como_admin.force_login(admin)

    # 1) GET sem login -> 401
    r = anonimo.get('/api/destinos/')
    verificar(
        "GET sem login -> 401",
        r.status_code == 401,
        f"recebido {r.status_code}",
    )

    # 2) GET com usuario comum -> 200
    r = como_demo.get('/api/destinos/')
    verificar(
        f"GET com usuario comum ({EMAIL_DEMO}) -> 200",
        r.status_code == 200,
        f"recebido {r.status_code}",
    )

    # 3) GET com admin -> 200
    r = como_admin.get('/api/destinos/')
    verificar(
        f"GET com admin ({EMAIL_ADMIN}) -> 200",
        r.status_code == 200,
        f"recebido {r.status_code}",
    )

    # 4) POST sem login -> 401
    r = anonimo.post('/api/destinos/', destino_teste, content_type='application/json')
    verificar(
        "POST sem login -> 401",
        r.status_code == 401,
        f"recebido {r.status_code}",
    )

    # 5) POST como usuario comum -> 403
    r = como_demo.post('/api/destinos/', destino_teste, content_type='application/json')
    verificar(
        "POST como usuario comum -> 403",
        r.status_code == 403,
        f"recebido {r.status_code}",
    )

    # 6) PUT como usuario comum -> 403
    if destino_qualquer:
        r = como_demo.put(
            f'/api/destinos/{destino_qualquer.id}/',
            destino_teste,
            content_type='application/json',
        )
        verificar(
            "PUT como usuario comum -> 403",
            r.status_code == 403,
            f"recebido {r.status_code}",
        )

        # 7) DELETE como usuario comum -> 403
        r = como_demo.delete(f'/api/destinos/{destino_qualquer.id}/')
        verificar(
            "DELETE como usuario comum -> 403",
            r.status_code == 403,
            f"recebido {r.status_code}",
        )

    # 8) POST como admin -> 201 (e depois apaga o registro de teste)
    r = como_admin.post('/api/destinos/', destino_teste, content_type='application/json')
    criado_ok = r.status_code == 201
    verificar(
        "POST como admin -> 201",
        criado_ok,
        f"recebido {r.status_code}",
    )

    registro_de_teste = Destino.objects.filter(nome='Ecoponto Teste Script').first()
    if registro_de_teste:
        registro_de_teste.delete()
        print("  [INFO] registro de teste apagado do banco")

    print("=" * 70)
    print(f"Resultado: {aprovados} ok, {reprovados} erro(s)")

    if reprovados > 0:
        print("Algo mudou nas permissoes - confira o get_permissions do DestinoViewSet")
        sys.exit(1)
    else:
        print("Permissoes de destinos funcionando como esperado!")


if __name__ == "__main__":
    main()
