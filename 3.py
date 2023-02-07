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
map_data = {"lon": 58.977560, "lat": 53.404915, "spn": 0.001, "l": 'sat'}
map_file = False
request()
while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()

        elif i.type == pygame.KEYUP:
            # если была нажата стрелка влев# если была нажата стрелка вверхо
            if i.key == pygame.K_LEFT:
                map_data['lon'] -= map_data['spn'] * 1.25
            # если была нажата стрелка вправо
            if i.key == pygame.K_RIGHT:
                map_data['lon'] += map_data['spn'] * 1.25
            # если была нажата стрелка вниз
            if i.key == pygame.K_DOWN:
                map_data['lat'] -= map_data['spn']
            # если была нажата стрелка вверх
            if i.key == pygame.K_UP:
                map_data['lat'] += map_data['spn']
            request()
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_z:
                map_data['spn'] *= 2
                request()
            elif i.key == pygame.K_x:
                map_data['spn'] /= 2
                request()
    pygame.display.flip()
os.remove(map_file)
pygame.quit()
