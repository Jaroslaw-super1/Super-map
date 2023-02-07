import os
import sys

import pygame
import requests


def request():
    global map_file, map_data, screen
    if map_file:
        os.remove(map_file)
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={map_data['lon']},{map_data['lat']}&spn={map_data['spn']},{map_data['spn']}&l={map_data['l']}"
    print(map_request)
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    screen.blit(pygame.image.load(map_file), (0, 0))


pygame.init()
screen = pygame.display.set_mode((600, 450))
map_data = {"lon": 58.977560, "lat": 53.404915, "spn": 0.005, "l": 'map'}
map_file = False
request()
while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_z:
                map_data['spn'] -= 0.001
                request()
            elif i.key == pygame.K_x:
                map_data['spn'] += 0.001
                request()
    pygame.display.flip()
os.remove(map_file)
pygame.quit()
