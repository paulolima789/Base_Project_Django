from django.core.management.base import BaseCommand
from api.seeds import run

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais.'

    def handle(self, *args, **kwargs):
        try:
            run()
            self.stdout.write(self.style.SUCCESS('Dados carregados com sucesso!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao carregar dados: {e}'))