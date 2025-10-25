from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Orquestra seeds: chama seed_groups (accounts) e seed_users (accounts).'

    def handle(self, *args, **kwargs):
        try:
            # cria grupos via accounts
            call_command('seed_groups')
            # cria usuários via accounts
            call_command('seed_users')
            self.stdout.write(self.style.SUCCESS('Dados carregados com sucesso!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao carregar dados: {e}'))