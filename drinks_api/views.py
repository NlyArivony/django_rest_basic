from django.http import JsonResponse
from .models import Drink
from .serializers import DrinkSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# swagger ui
from drf_spectacular.utils import extend_schema


@extend_schema(
    description="- Get all the drinks\n" "- Serialize them\n" "- Return JSON",
    responses={200: DrinkSerializer(many=True)},
)
@api_view(["GET", "POST"])
def drink_list(request):
    """
    - get all the drinks
    - serialize them
    - return json
    """
    if request.method == "GET":
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many=True)
        # return JsonResponse({"drinks": serializer.data}, safe=False)
        return Response({"drinks": serializer.data})

    elif request.method == "POST":
        serializer = DrinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    description="Get a drink\n" "Update a drink\n" "Delete a drink",
    responses={200: DrinkSerializer()},
)
@api_view(["GET", "PUT", "DELETE"])
def drink_detail(request, id):
    """
    GET a drink
    UPDATE a drink
    DELETE a drink
    """
    try:
        drink = Drink.objects.get(pk=id)
    except Drink.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = DrinkSerializer(drink)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = DrinkSerializer(drink, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        drink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
