from django.contrib.auth.models import Group
from api.models import CustomUser  # ajuste o import se o CustomUser estiver em outro lugar

def run():
    usuarios = [
        {
            "username": "admin",
            "email": "admin@example.com",
            "password": "admin123",
            "grupo": "Admin",
            "superuser": True
        },
        {
            "username": "example",
            "email": "example@example.com",
            "password": "example123",
            "grupo": "Example",
            "superuser": False
        },
        {
            "username": "user",
            "email": "user@example.com",
            "password": "user123",
            "grupo": "User",
            "superuser": False
        },
    ]

    for user_info in usuarios:
        if not CustomUser.objects.filter(username=user_info["username"]).exists():
            user = CustomUser.objects.create_superuser(
                username=user_info["username"],
                email=user_info["email"],
                password=user_info["password"],
            ) if user_info["superuser"] else CustomUser.objects.create_user(
                username=user_info["username"],
                email=user_info["email"],
                password=user_info["password"],
            )

            group, _ = Group.objects.get_or_create(name=user_info["grupo"])
            user.groups.add(group)

            print(f"Usuário {user.username} criado e adicionado ao grupo '{group.name}'.")
        else:
            print(f"Usuário {user_info['username']} já existe.")

    print("Usuários e grupos populados com sucesso.")
