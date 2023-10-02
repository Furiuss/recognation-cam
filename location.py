# import socket
# import requests
# from ip2geotools.databases.noncommercial import DbIpCity
# from geopy.distance import distance
#
# def printDetails(ip):
#     res = DbIpCity.get(ip, api_key="free")
#     print(f"IP Address: {res.ip_address}")
#     print(f"Location: {res.city}, {res.region}, {res.country}")
#     print(f"Coordinates: (Lat: {res.latitude}, Lng: {res.longitude})")
#
# # ip_add = input("Enter IP: ")  # 198.35.26.96
# printDetails("189.63.6.231")

import geocoder

def obter_geolocalizacao():
    # Obtém a geolocalização atual
    localizacao = geocoder.ip('me')

    # Verifica se a geolocalização foi obtida com sucesso
    if localizacao.ok:
        latitude = localizacao.latlng[0]
        longitude = localizacao.latlng[1]
        print(f"Sua latitude: {latitude}")
        print(f"Sua longitude: {longitude}")
    else:
        print("Não foi possível obter a geolocalização.")

obter_geolocalizacao()