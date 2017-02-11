#!/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import sys
import time
#import pyowm
from pyql.weather.forecast import Forecast

	

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

blanco = (255, 255, 255)
naranja = ()
negro = (0, 0, 0)

## Seteo para Fcio. Varela
forecast_id = 466961

class Clima():
	textos = {"Breezy":"Viento Suave", "Scattered Showers":"Llovizna", "Showers":"Lluvia", "Scattered Thunderstorms":"Tormentas Dispersas","Sunny":"Soleado","Partly Cloudy":"Parcialmente Nublado", "Mostly Cloudy":"Mayormente Nublado", "Cloudy":"Nublado","Thunderstorms":"Tormentas"}
	dia = {'Mon':'Lun','Tue':'Mar','Wed':'Mie','Thu':'Jue','Fri':'Vie','Sat':'Sab','Sun':'Dom'}
	climaHoy = Forecast.get(woeid=forecast_id, u='c')
	climaExtendido = climaHoy.item.forecast

	clima0 = climaExtendido[0]
	clima1 = climaExtendido[1]
	clima2 = climaExtendido[2]
	clima3 = climaExtendido[3]

	def traducirClima(self,texto):
		traducido = self.textos[texto]
		return traducido


	def climaActual(self):
		## USANDO PYQL (YAHOO WEATHER)
		temp = self.climaHoy.item.condition.temp
		tempMax = self.clima0['high']
		tempMin = self.clima0['low']
		texto = self.climaHoy.item.condition.text
		texto = self.traducirClima(texto)
		return (temp, tempMax, tempMin,texto)

	def climaManiana(self):
		## Obtener clima del dia siguiente
		tempMax = self.clima1['high']
		tempMin = self.clima1['low']
		texto = self.clima1['text']
		texto = self.traducirClima(texto)
		dia = self.dia[self.clima1['day']]
		return (tempMax,tempMin,texto,dia)
	
	def climaPasado(self):
		## Obtener clima a dos dias del actual
		tempMax = self.clima2['high']
		tempMin = self.clima2['low']
		texto = self.clima2['text']
		texto = self.traducirClima(texto)
		dia = self.dia[self.clima2['day']]
		return (tempMax,tempMin,texto,dia)

	def climaPasadoPlus(self):
		## Obtener clima a dos dias del actual
		tempMax = self.clima3['high']
		tempMin = self.clima3['low']
		texto = self.clima3['text']
		texto = self.traducirClima(texto)
		dia = self.dia[self.clima3['day']]
		return (tempMax,tempMin,texto,dia)



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
	iconTemp = pygame.image.load("icons/weather/temp-blanco.png").convert()
	fuenteReloj = pygame.font.Font("fonts/Roboto.ttf", 220)
	fuenteFecha = pygame.font.Font("fonts/Roboto.ttf",50)
	fuenteClima = pygame.font.Font("fonts/Roboto.ttf",130)
	fuenteMinMax = pygame.font.Font("fonts/Roboto.ttf",47)
	
	date = getDate()
	hoy = date

	c = Clima()
	print('Clima actual:')
	print(c.climaActual())

	print('\nClima Mañana:')
	print(c.climaManiana())

	print('\nClima Pasado:')
	print(c.climaPasado())

	print('\nClima pasado pasado:')
	print(c.climaPasadoPlus())


	## Main loop
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		
		fps.tick(10)
		
		date = getDate()
		
		#if (date != hoy):
		#	print('Hoy NO es hoy')
		
		d = str(date[0])
		num = str(date[1])
		m = str(date[2])
		a = str(date[3])
		date = str(d+", "+num+" de "+m+", "+a)

		
		reloj = fuenteReloj.render(getTime(), 1, blanco)
		fecha = fuenteFecha.render(str(date) ,1, blanco)
		tempActual = fuenteClima.render(c.climaActual()[0]+"°C",1,blanco)
		tempMinMaxHoy = fuenteMinMax.render("Min: "+c.climaActual()[2]+"°C / Max: "+c.climaActual()[1]+"°C",1,blanco)
		#tempMinHoy = fuenteClima.render("Min: "+c.climaActual()[2]+"°C",1,blanco)
		estadoHoy = fuenteMinMax.render(c.climaActual()[3],1,blanco)
		
		## Sector superior
		screen.blit(reloj, (320,110))
		screen.blit(fecha, (420,15))

		## Clima de hoy
		screen.blit(tempActual, (70,450))
		screen.blit(tempMinMaxHoy, (70,600))
		screen.blit(estadoHoy, (340,500))

		screen.blit(iconTemp,(70, 550))

		## Pronostico extendido



		pygame.display.flip()
		screen.blit(fondo, (0, 0))

if __name__ == "__main__":
	## Inicializo pygame
	pygame.init()
	main()