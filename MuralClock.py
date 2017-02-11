#!/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import sys
import time

	

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

blanco = (255, 255, 255)
naranja = ()
negro = (0, 0, 0)

class weather():
	pyowm = 1

def getTime():
	return time.strftime("%H:%M:%S")

def getDate():
	dias = ["Domingo","Lunes","Martes","Miércoles","Jueves","Viernes","Sábado"]
	meses = ["Diciembre","Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre"]
	hoy = time.strftime("%w,%d,%m,%Y")
	hoy = hoy.split(',')

	dia = dias[int(hoy[0])]
	diaNum = str(hoy[1])
	mes = meses[int(hoy[2])]
	anio = str(hoy[-1])

	return (dia,diaNum,mes,anio)


def main():
	## Inicializo la ventana (dimensiones y titulo)
	screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.RESIZABLE)
	pygame.display.set_caption("MuralClock")
	fps = pygame.time.Clock()
	fondo = pygame.image.load("wallpapers/fondoGris.jpg").convert()
	fuenteReloj = pygame.font.Font("fonts/Roboto.ttf", 210)
	fuenteFecha = pygame.font.Font("fonts/Roboto.ttf",45)
	## Main loop
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		
		fps.tick(10)
		
		date = getDate()
		d = str(date[0])
		num = str(date[1])
		m = str(date[2])
		a = str(date[3])
		date = str(d+", "+num+" de "+m+", "+a)
		
		reloj = fuenteReloj.render(getTime(), 1, blanco)
		fecha = fuenteFecha.render(str(date) ,1, blanco)
		screen.blit(reloj, (300,200))
		screen.blit(fecha, (400,15))
		pygame.display.flip()
		screen.blit(fondo, (0, 0))

if __name__ == "__main__":
	## Inicializo pygame
	pygame.init()
	main()