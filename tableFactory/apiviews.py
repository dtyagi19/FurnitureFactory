from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Feet, Leg, Table
from .serializers import FeetSerializer, LegSerializer, \
    LegRetrieveSerializer, TableRetrieveSerializer, TableSerializer


@api_view(['GET', 'POST'])
def feet_view(request):
    if request.method == 'GET':
        feets = Feet.objects.all()
        serializer = FeetSerializer(feets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FeetSerializer(data=request.data)
        if serializer.is_valid():
            feet = serializer.save()
            return Response(FeetSerializer(feet).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def feet_detail_view(request, feet_id):
    feet = get_object_or_404(Feet, pk=feet_id)
    if request.method == 'GET':
        serializer = FeetSerializer(feet)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = FeetSerializer(feet, data=request.data,
                                    partial=True)
        if serializer.is_valid():
            feet = serializer.save()
            return Response(FeetSerializer(feet).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        feet.delete()
        return Response("Feet deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def leg_view(request):
    if request.method == 'GET':
        legs = Leg.objects.all()
        serializer = LegRetrieveSerializer(legs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        feet = get_object_or_404(Feet, pk=request.data['feet_id'])
        serializer = LegSerializer(data=request.data)
        if serializer.is_valid():
            leg = serializer.save(feet=feet)
            return Response(LegRetrieveSerializer(leg).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def leg_detail_view(request, leg_id):
    leg = get_object_or_404(Leg, pk=leg_id)
    if request.method == 'GET':
        serializer = LegRetrieveSerializer(leg)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = LegSerializer(leg, data=request.data,
                                   partial=True)
        if serializer.is_valid():
            if 'feet_id' in request.data:
                feet = get_object_or_404(Feet, pk=request.data['feet_id'])
                leg = serializer.save(feet=feet)
                return Response(LegRetrieveSerializer(leg).data)
            else:
                leg = serializer.save()
                return Response(LegRetrieveSerializer(leg).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        leg.delete()
        return Response("Leg deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def table_view(request):
    if request.method == 'GET':
        tables = Table.objects.all()
        # serializer = LegSerializer(legs, many=True)
        serializer = TableRetrieveSerializer(tables, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        leg = get_object_or_404(Leg, pk=request.data['leg_id'])
        serializer = TableSerializer(data=request.data)
        if serializer.is_valid():
            table = serializer.save(leg=leg)
            return Response(TableRetrieveSerializer(table).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def table_detail_view(request, table_id):
    table = get_object_or_404(Table, pk=table_id)
    if request.method == 'GET':
        serializer = TableRetrieveSerializer(table)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = TableSerializer(table, data=request.data,
                                     partial=True)
        if serializer.is_valid():
            if 'leg_id' in request.data:
                leg = get_object_or_404(Leg, pk=request.data['leg_id'])
                table = serializer.save(leg=leg)
                return Response(TableRetrieveSerializer(table).data)
            else:
                table = serializer.save()
                return Response(TableRetrieveSerializer(table).data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        table.delete()
        return Response("Table deleted", status=status.HTTP_204_NO_CONTENT)
