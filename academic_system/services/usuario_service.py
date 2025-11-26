from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.exceptions import ValidationError

Usuario = get_user_model()


class UsuarioService:

    @staticmethod
    @transaction.atomic
    def crear_usuario(datos_usuario):
        rol = datos_usuario.get('rol')

        if rol not in ['administrador', 'profesor', 'alumno']:
            raise ValidationError('Rol inválido')

        username = datos_usuario.get('username')
        if username and Usuario.objects.filter(username=username).exists():
            raise ValidationError(f'El username {username} ya está en uso')

        numero_documento = datos_usuario.get('numero_documento')
        if Usuario.objects.filter(numero_documento=numero_documento).exists():
            raise ValidationError(f'Ya existe un usuario con el documento {numero_documento}')

        usuario = Usuario(
            username=username or None,
            first_name=datos_usuario.get('nombre'),
            apellido_paterno=datos_usuario.get('apellido_paterno'),
            apellido_materno=datos_usuario.get('apellido_materno'),
            tipo_documento=datos_usuario.get('tipo_documento', 'DNI'),
            numero_documento=numero_documento,
            email=datos_usuario.get('email', ''),
            telefono=datos_usuario.get('telefono', ''),
            direccion=datos_usuario.get('direccion', ''),
            fecha_nacimiento=datos_usuario.get('fecha_nacimiento'),
            sexo=datos_usuario.get('sexo'),
            rol=rol,
        )

        password = datos_usuario.get('password', numero_documento)
        usuario.set_password(password)
        usuario.save()

        return usuario

    @staticmethod
    def actualizar_usuario(usuario_id, datos):
        usuario = Usuario.objects.get(pk=usuario_id)

        campos_permitidos = [
            'first_name', 'apellido_paterno', 'apellido_materno',
            'email', 'telefono', 'direccion', 'fecha_nacimiento', 'sexo', 'rol', 'username'
        ]

        if 'username' in datos and datos['username']:
            if Usuario.objects.filter(username=datos['username']).exclude(pk=usuario_id).exists():
                raise ValidationError(f'El username {datos["username"]} ya está en uso')

        for campo in campos_permitidos:
            if campo in datos:
                setattr(usuario, campo, datos[campo])

        usuario.save()
        return usuario

    @staticmethod
    def inactivar_usuario(usuario_id):
        usuario = Usuario.objects.get(pk=usuario_id)
        usuario.is_active = False
        usuario.save()
        return usuario

    @staticmethod
    def activar_usuario(usuario_id):
        usuario = Usuario.objects.get(pk=usuario_id)
        usuario.is_active = True
        usuario.save()
        return usuario

    @staticmethod
    def cambiar_contraseña(usuario_id, nueva_contraseña):
        usuario = Usuario.objects.get(pk=usuario_id)
        usuario.set_password(nueva_contraseña)
        usuario.save()
        return usuario

    @staticmethod
    def obtener_por_rol(rol):
        return Usuario.objects.filter(rol=rol, is_active=True)

    @staticmethod
    def buscar_usuarios(criterio):
        return Usuario.objects.filter(
            is_active=True
        ).filter(
            models.Q(codigo__icontains=criterio) |
            models.Q(first_name__icontains=criterio) |
            models.Q(apellido_paterno__icontains=criterio) |
            models.Q(apellido_materno__icontains=criterio) |
            models.Q(numero_documento__icontains=criterio)
        )
