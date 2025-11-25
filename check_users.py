import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_matriculas.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print('=' * 60)
print('CREDENCIALES DE ACCESO AL SISTEMA')
print('=' * 60)

print('\n=== ADMINISTRADOR ===')
admin = User.objects.filter(rol='administrador').first()
if admin:
    print(f'Nombre: {admin.get_full_name()}')
    print(f'Codigo: {admin.codigo}')
    print(f'USERNAME (para login): {admin.username}')
    print(f'PASSWORD: Pedro1415@')

print('\n=== PROFESORES ===')
for p in User.objects.filter(rol='profesor').order_by('codigo'):
    print(f'\nNombre: {p.get_full_name()}')
    print(f'Codigo: {p.codigo}')
    print(f'USERNAME (para login): {p.username}')
    print(f'PASSWORD: Pedro1415@')

print('\n=== ALUMNOS ===')
for a in User.objects.filter(rol='alumno').order_by('codigo'):
    print(f'\nNombre: {a.get_full_name()}')
    print(f'Codigo: {a.codigo}')
    print(f'USERNAME (para login): {a.username}')
    print(f'PASSWORD: Pedro1415@')

print('\n' + '=' * 60)
