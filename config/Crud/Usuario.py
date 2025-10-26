from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Usuario
from ..serializers import UsuarioSerializer

@api_view(['GET'])
def obtener_usuarios(request):
    usuarios = Usuario.objects.all()
    serializer = UsuarioSerializer(usuarios, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def obtener_usuario(request):
    usuario_id = request.GET.get('id')
    usuario = Usuario.objects.filter(id=usuario_id).first()
    if not usuario:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)

@api_view(['POST'])
def crear_usuario(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje": "Usuario creado", "usuario": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def editar_usuario(request):
    usuario_id = request.data.get('id')
    usuario = Usuario.objects.filter(id=usuario_id).first()
    if not usuario:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje": "Usuario actualizado", "usuario": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_usuario(request):
    usuario_id = request.GET.get('id')
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        usuario.delete()
        return Response({"mensaje": "Usuario eliminado"})
    except Usuario.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
