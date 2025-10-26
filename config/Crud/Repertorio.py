from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Repertorio
from ..serializers import RepertorioSerializer

# -----------------------------
# Crear un nuevo repertorio
# -----------------------------
@api_view(['POST'])
def crear_repertorio(request):
    nombre = request.data.get('nombre')
    coro = request.data.get('coro')
    if not nombre or not coro:
        return Response(
            {"error": "Debe proporcionar nombre y coro"},
            status=status.HTTP_400_BAD_REQUEST
        )
    serializer = RepertorioSerializer(data={"nombre": nombre, "coro": coro})
    if serializer.is_valid():
        serializer.save()
        return Response({"repertorio": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------
# Obtener todos los repertorios
# -----------------------------
@api_view(['GET'])
def obtener_repertorios(request):
    repertorios = Repertorio.objects.all()
    serializer = RepertorioSerializer(repertorios, many=True)
    return Response(serializer.data)

# -----------------------------
# Obtener un repertorio por ID
# -----------------------------
@api_view(['GET'])
def obtener_repertorio(request):
    id_repertorio = request.GET.get('id')
    if not id_repertorio:
        return Response({"error": "Debe proporcionar un id"}, status=status.HTTP_400_BAD_REQUEST)
    
    repertorio = Repertorio.objects.filter(id=id_repertorio).first()
    if not repertorio:
        return Response({"error": "Repertorio no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = RepertorioSerializer(repertorio)
    return Response(serializer.data)

# -----------------------------
# Editar un repertorio existente
# -----------------------------
@api_view(['PUT'])
def editar_repertorio(request):
    id_repertorio = request.data.get('id')
    if not id_repertorio:
        return Response({"error": "Debe proporcionar un id"}, status=status.HTTP_400_BAD_REQUEST)

    repertorio = Repertorio.objects.filter(id=id_repertorio).first()
    if not repertorio:
        return Response({"error": "Repertorio no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    nombre = request.data.get('nombre', repertorio.nombre)
    coro = request.data.get('coro', repertorio.coro)

    serializer = RepertorioSerializer(repertorio, data={"nombre": nombre, "coro": coro}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje": "Repertorio actualizado exitosamente", "repertorio": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------
# Eliminar un repertorio
# -----------------------------
@api_view(['DELETE'])
def eliminar_repertorio(request):
    id_repertorio = request.GET.get('id')
    if not id_repertorio:
        return Response({"error": "Debe proporcionar un id"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        repertorio = Repertorio.objects.get(id=id_repertorio)
        repertorio.delete()
        return Response({"mensaje": "Repertorio eliminado exitosamente"})
    except Repertorio.DoesNotExist:
        return Response({"error": "Repertorio no encontrado"}, status=status.HTTP_404_NOT_FOUND)
