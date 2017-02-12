#!/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import sys
import time
from pyql.weather.forecast import Forecast
import time
import schedule

	

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600

blanco = (255, 255, 255)
naranja = ()
negro = (0, 0, 0)

tipografia = "fonts/Roboto.ttf"
color_icono = "blanco"

## Seteo para Fcio. Varela
forecast_id = 466961


class Clima():
	textos = {"Breezy":"Hay vientito", "Scattered Showers":"Chaparrones", "Showers":"Llovizna, prepará mate!","Rain":"Lluvia, torta frita!", "Scattered Thunderstorms":"Puede haber tormentas","Sunny":"Solcito afuera","Partly Cloudy":"Un poco nublado", "Mostly Cloudy":"Bastante nublado", "Cloudy":"Nublado","Thunderstorms":"Tormenta, no salgas"}
	dia = {'Mon':'Lunes','Tue':'Martes','Wed':'Miércoles','Thu':'Jueves','Fri':'Viernes','Sat':'Sábado','Sun':'Domingo'}
	climaHoy = Forecast.get(woeid=forecast_id, u='c')
	climaExtendido = climaHoy.item.forecast

	clima0 = climaExtendido[0]
	clima1 = climaExtendido[1]
	clima2 = climaExtendido[2]
	clima3 = climaExtendido[3]

#	def actualizarClima(self):
#		self.climaHoy = Forecast.get(woeid=forecast_id, u='c')
#		climaExtendido = climaHoy.item.forecast		

	## Actualizar clima cada 30 min
#	schedule.every(30).minutes.do(actualizarClima())
#	while 1:
#		schedule.run_pending()
#		time.sleep(1)

	def climasDisponibles(self):
		return list(self.textos.values())

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

	
	
	date = getDate()
	hoy = date


	## Main loop
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		
		fps.tick(10)

		## Instancio el clima	
		c = Clima()
		iconos = c.climasDisponibles()
		iconos = {iconos[0]:"viento", iconos[1]:"chaparrones",iconos[2]:"llovizna",iconos[3]:"lluvia",iconos[4]:"tormenta",iconos[5]:"soleado", iconos[6]:"parcialmente_nublado",iconos[7]:"muy_nublado",iconos[8]:"nublado",iconos[9]:"tormenta_fuerte"}

		## Cargando icono temperaturas
		iconTemp = pygame.image.load("icons/weather/temp.png").convert()
		transparente = iconTemp.get_at((0,0))
		iconTemp.set_colorkey(transparente,RLEACCEL)


		## Cargando icono clima actual
		iconActual = pygame.image.load("icons/weather/"+iconos[c.climaActual()[-1]]+".png").convert()
		transparente = iconActual.get_at((0,0))
		iconActual.set_colorkey(transparente,RLEACCEL)

		## Cargando iconos predicciones
		iconoPrediccion1 = pygame.image.load('icons/weather/'+iconos[c.climaManiana()[-2]]+'.png').convert()
		transparente = iconoPrediccion1.get_at((0,0))
		iconoPrediccion1.set_colorkey(transparente,RLEACCEL)

		iconoPrediccion2 = pygame.image.load('icons/weather/'+iconos[c.climaPasado()[-2]]+'.png').convert()
		transparente = iconoPrediccion2.get_at((0,0))
		iconoPrediccion2.set_colorkey(transparente,RLEACCEL)

		iconoPrediccion3 = pygame.image.load('icons/weather/'+iconos[c.climaPasadoPlus()[-2]]+'.png').convert()
		transparente = iconoPrediccion3.get_at((0,0))
		iconoPrediccion3.set_colorkey(transparente,RLEACCEL)

		## Cargando fuentes
		fuenteReloj = pygame.font.Font(tipografia, 200)
		fuenteFecha = pygame.font.Font(tipografia,40)
		fuenteClima = pygame.font.Font(tipografia,110)
		fuenteMinMax = pygame.font.Font(tipografia,37)
		fuentePrediccion = pygame.font.Font(tipografia,27)
			
		date = getDate()		
		
		d = str(date[0])
		num = str(date[1])
		m = str(date[2])
		a = str(date[3])
		date = str(d+", "+num+" de "+m+", "+a)

		
		reloj = fuenteReloj.render(getTime(), 1, blanco)
		fecha = fuenteFecha.render(str(date) ,1, blanco)
		tempActual = fuenteClima.render(c.climaActual()[0]+"°",1,blanco)
		tempMinMaxHoy = fuenteMinMax.render(c.climaActual()[2]+"°C / "+c.climaActual()[1]+"°C",1,blanco)
		estadoHoy = fuenteMinMax.render(c.climaActual()[3],1,blanco)

		tempPrediccion1 = fuentePrediccion.render(c.climaManiana()[1]+"°C / "+c.climaManiana()[0]+"°C",1,blanco)
		diaPrediccion1 = fuentePrediccion.render(c.climaManiana()[-1],1,blanco)

		tempPrediccion2 = fuentePrediccion.render(c.climaPasado()[1]+"°C / "+c.climaPasado()[0]+"°C",1,blanco)
		diaPrediccion2 = fuentePrediccion.render(c.climaPasado()[-1],1,blanco)

		tempPrediccion3 = fuentePrediccion.render(c.climaPasadoPlus()[1]+"°C / "+c.climaPasadoPlus()[0]+"°C",1,blanco)
		diaPrediccion3 = fuentePrediccion.render(c.climaPasadoPlus()[-1],1,blanco)
		
		## Sector superior
		screen.blit(reloj, (180,80))
		screen.blit(fecha, (280,10))

		## Clima de hoy
		screen.blit(tempActual, (70,330))
		screen.blit(tempMinMaxHoy, (130,510))
		screen.blit(estadoHoy, (70,460))

		screen.blit(iconTemp,(95, 515))
		screen.blit(iconActual,(250,350))

		## Pronostico extendido

		screen.blit(diaPrediccion1,(490,370))
		screen.blit(iconoPrediccion1,(475,415))
		screen.blit(tempPrediccion1,(460,515))

		screen.blit(diaPrediccion2,(675,370))
		screen.blit(iconoPrediccion2,(665,415))
		screen.blit(tempPrediccion2,(655,515))

		screen.blit(diaPrediccion3,(865,370))
		screen.blit(iconoPrediccion3,(865,415))
		screen.blit(tempPrediccion3,(855,515))



		pygame.display.flip()
		screen.blit(fondo, (0, 0))

if __name__ == "__main__":
	## Inicializo pygame
	pygame.init()
	main()