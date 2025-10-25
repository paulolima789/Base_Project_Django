from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Cria usuários padrão e associa aos grupos (Admin, User, Example)"

    def handle(self, *args, **options):
        User = get_user_model()
        USERNAME_FIELD = User.USERNAME_FIELD

        usuarios = [
            {"email": "admin@example.com", "password": "admin123", "grupo": "Admin", "superuser": True},
            {"email": "example@example.com", "password": "example123", "grupo": "Example", "superuser": False},
            {"email": "user@example.com", "password": "user123", "grupo": "User", "superuser": False},
        ]

        for u in usuarios:
            identifier = u["email"]
            password = u["password"]
            group_name = u["grupo"]
            is_super = u.get("superuser", False)

            exists = User.objects.filter(**{USERNAME_FIELD: identifier}).exists()
            if not exists:
                create_kwargs = {USERNAME_FIELD: identifier, "password": password}
                if hasattr(User, "name"):
                    create_kwargs["name"] = identifier.split("@")[0]

                if is_super:
                    user = User.objects.create_superuser(**create_kwargs)
                else:
                    user = User.objects.create_user(**create_kwargs)

                group, _ = Group.objects.get_or_create(name=group_name)
                user.groups.add(group)
                self.stdout.write(self.style.SUCCESS(f"Usuário {getattr(user, USERNAME_FIELD)} criado e adicionado ao grupo '{group.name}'."))
            else:
                self.stdout.write(self.style.WARNING(f"Usuário {identifier} já existe."))

        self.stdout.write(self.style.SUCCESS("Usuários populados com sucesso."))
