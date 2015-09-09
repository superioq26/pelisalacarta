# -*- coding: utf-8 -*-
#-----------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Repelis - Por Kampanita-2015 
# ( con ayuda de neno1978, DrZ3r0, y robalo )
# 4/9/2015
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#-----------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "repelis"
__category__ = "F,L"
__type__ = "generic"
__title__ = "Repelis"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

# Main list manual
def mainlist(item):

    logger.info("[repelis] mainlist")
    itemlist = []
   
    item.url = "http://www.repelis.tv/page/1"
    
    itemlist.append( Item(channel=__channel__, action="menupelis", title="Peliculas",  url="http://www.repelis.tv/page/1" , thumbnail="http://t0.gstatic.com/images?q=tbn:ANd9GcSJ4ByP8F0kxW4rjaP14k0E1BXNdUOvRDf-Rc-qNGwJ2-qMO7a0", fanart="http://t0.gstatic.com/images?q=tbn:ANd9GcSJ4ByP8F0kxW4rjaP14k0E1BXNdUOvRDf-Rc-qNGwJ2-qMO7a0") )
    itemlist.append( Item(channel=__channel__, action="menuestre", title="Estrenos",  url="http://www.repelis.tv/archivos/estrenos/page/1" , thumbnail="http://t0.gstatic.com/images?q=tbn:ANd9GcSEPlR5CWoa6nSwOvCrnTGbLJSMXmpcF1EzeQaHeFN5D83CrJWmhg", fanart="http://t0.gstatic.com/images?q=tbn:ANd9GcSEPlR5CWoa6nSwOvCrnTGbLJSMXmpcF1EzeQaHeFN5D83CrJWmhg") )  
    itemlist.append( Item(channel=__channel__, action="menudesta", title="Destacadas",  url="http://www.repelis.tv/page/1" , thumbnail="https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcTXL1q8_tKHnM36lA8VgsqoJ5Wy_D4DC0IdhR2Pwk0OtBVlEXkr", fanart="https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcTXL1q8_tKHnM36lA8VgsqoJ5Wy_D4DC0IdhR2Pwk0OtBVlEXkr") )  
    itemlist.append( Item(channel=__channel__, action="todaspelis", title="Proximos estrenos", url="http://www.repelis.tv/archivos/proximos-estrenos/page/1", thumbnail="http://www.multicinesplazajesusmaria.com/images/backs/titulo-proximos-estrenos.jpg", fanart="http://www.multicinesplazajesusmaria.com/images/backs/titulo-proximos-estrenos.jpg"))
    itemlist.append( Item(channel=__channel__, action="todaspelis", title="Todas las Peliculas",  url="http://www.repelis.tv/page/1" , thumbnail="http://images.akamai.steamusercontent.com/ugc/713033622832846513/B34FDD11E93838A3BE172858A56758E23AA43A34/", fanart="http://images.akamai.steamusercontent.com/ugc/713033622832846513/B34FDD11E93838A3BE172858A56758E23AA43A34/") )
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item(channel=__channel__, action="todaspelis", title="Eroticas +18",  url="http://www.repelis.tv/genero/eroticas/page/1" , thumbnail="http://www.topkamisetas.com/catalogo/images/TB0005.gif", fanart="http://www.topkamisetas.com/catalogo/images/TB0005.gif") )
    #Quito la busqueda por año si no esta enabled el adultmode, porque no hay manera de filtrar los enlaces eroticos
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item(channel=__channel__, action="poranyo", title="Por Año", url="http://www.repelis.tv/fecha/2015/page/1", thumbnail="https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcRBLbjjOzoOrPLvEl-0ryt0BD_Hb4zKNunwS-dG1HBZc-_GWp2M3w", fanart="https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcRBLbjjOzoOrPLvEl-0ryt0BD_Hb4zKNunwS-dG1HBZc-_GWp2M3w"))
    #Por categoria si que filtra la categoria de eroticos
    itemlist.append( Item(channel=__channel__, action="porcateg", title="Por Categoria", url="http://www.repelis.tv/genero/accion/page/1", thumbnail="http://www.logopro.it/blog/wp-content/uploads/2013/07/categoria-sigaretta-elettronica.png", fanart="http://www.logopro.it/blog/wp-content/uploads/2013/07/categoria-sigaretta-elettronica.png"))
    itemlist.append( Item(channel=__channel__, action="search", title="Buscar...", url="http://www.repelis.tv/search/?s=", thumbnail="http://thumbs.dreamstime.com/x/buscar-pistas-13159747.jpg", fanart="http://thumbs.dreamstime.com/x/buscar-pistas-13159747.jpg"))

    return itemlist
 		

#Peliculas recien agregadas ( quitamos las de estreno del slide-bar en el top
def menupelis(item):
   
    logger.info("[repelis] menupelis")
    logger.info("[repelis] "+item.url)
    
    itemlist = []
       
    data = scrapertools.cache_page(item.url).decode('iso-8859-1').encode('utf-8')
        
    patronenlaces= '<h3>Películas Recién Agregadas</h3>.*?>(.*?)</section>'
    matchesenlaces = re.compile(patronenlaces,re.DOTALL).findall(data)
     
    for bloque_enlaces in matchesenlaces:
    
        patron = '<a href="([^"]+)" title="([^"]+)"> <div class="poster".*?<img src="([^"]+)"'
        matches = re.compile(patron,re.DOTALL).findall(bloque_enlaces)
        scrapertools.printMatches(matches)
        for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
            title = scrapertools.remove_show_from_title(scrapedtitle,"Ver Película")  
            title = title.replace("Online","");
            url = urlparse.urljoin(item.url,scrapedurl)
            thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
            itemlist.append( Item(channel=__channel__, action="verpeli", title=title, fulltitle=title , url=url , thumbnail=thumbnail, fanart=thumbnail) )
    
    ## Paginación
    #<span class="current">2</span><a href="http://www.repelis.tv/page/3"
    
    # Si falla no muestra ">> Página siguiente"
    try:
        next_page = scrapertools.get_match(data,'<span class="current">\d+</span><a href="([^"]+)"')
        title= "[COLOR red][B]Pagina siguiente »[/B][/COLOR]"
        itemlist.append( Item(channel=__channel__, title=title, url=next_page, action="menupelis",  folder=True) )
    except: pass
    return itemlist


#Todas las peliculas   
def todaspelis(item):
   
    logger.info("[repelis] menupelis")
    logger.info("[repelis] "+item.url)
    
    itemlist = []
       
    data = scrapertools.cache_page(item.url).decode('iso-8859-1').encode('utf-8')
   
    patronenlaces= '<h1>.*?</h1>.*?>(.*?)</section>'
    matchesenlaces = re.compile(patronenlaces,re.DOTALL).findall(data)
     
    for bloque_enlaces in matchesenlaces:
    
        patron = '<a href="([^"]+)" title="([^"]+)"> <div class="poster".*?<img src="([^"]+)"'
        matches = re.compile(patron,re.DOTALL).findall(bloque_enlaces)
        scrapertools.printMatches(matches)
        for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
            title = scrapertools.remove_show_from_title(scrapedtitle,"Ver Película")  
            title = title.replace("Online","");
            url = urlparse.urljoin(item.url,scrapedurl)
            thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
            itemlist.append( Item(channel=__channel__, action="verpeli", title=title, fulltitle=title , url=url , thumbnail=thumbnail, fanart=thumbnail) )
    
    ## Paginación
    #<span class="current">2</span><a href="http://www.repelis.tv/page/3"
    
    # Si falla no muestra ">> Página siguiente"
    try:
        next_page = scrapertools.get_match(data,'<span class="current">\d+</span><a href="([^"]+)"')
        title= "[COLOR red][B]Pagina siguiente »[/B][/COLOR]"
        itemlist.append( Item(channel=__channel__, title=title, url=next_page, action="todaspelis",  folder=True) )
    except: pass
    return itemlist

#Peliculas Destacadas
def menudesta(item):
   
    logger.info("[repelis] menupelis")
    logger.info("[repelis] "+item.url)
    
    itemlist = []
       
    data = scrapertools.cache_page(item.url).decode('iso-8859-1').encode('utf-8')  
   
    patronenlaces= '<h3>.*?Destacadas.*?>(.*?)<h3>'
    matchesenlaces = re.compile(patronenlaces,re.DOTALL).findall(data)
     
    for bloque_enlaces in matchesenlaces:
    
        patron = '<a href="([^"]+)" title="([^"]+)"> <div class="poster".*?<img src="([^"]+)"'
        matches = re.compile(patron,re.DOTALL).findall(bloque_enlaces)
        scrapertools.printMatches(matches)
        for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
            title = scrapertools.remove_show_from_title(scrapedtitle,"Ver Película")  
            title = title.replace("Online","");
            url = urlparse.urljoin(item.url,scrapedurl)
            thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
            itemlist.append( Item(channel=__channel__, action="verpeli", title=title, fulltitle=title , url=url , thumbnail=thumbnail, fanart=thumbnail) )
    
    return itemlist

#Peliculas de Estreno
def menuestre(item):
   
    logger.info("[repelis] menupelis")
    logger.info("[repelis] "+item.url)
    
    itemlist = []
       
    data = scrapertools.cache_page(item.url).decode('iso-8859-1').encode('utf-8')
    patronenlaces= '<h1>Estrenos</h1>(.*?)</section>'
    matchesenlaces = re.compile(patronenlaces,re.DOTALL).findall(data)
     
    for bloque_enlaces in matchesenlaces:
    
        patron = '<a href="([^"]+)" title="([^"]+)"> <div class="poster".*?<img src="([^"]+)"'
        matches = re.compile(patron,re.DOTALL).findall(bloque_enlaces)
        scrapertools.printMatches(matches)
        for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
            title = scrapertools.remove_show_from_title(scrapedtitle,"Ver Película")  
            title = title.replace("Online","");
            url = urlparse.urljoin(item.url,scrapedurl)
            thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
            itemlist.append( Item(channel=__channel__, action="verpeli", title=title, fulltitle=title , url=url , thumbnail=thumbnail, fanart=thumbnail) )
    
    ## Paginación
    #<span class="current">2</span><a href="http://www.repelis.tv/page/3"
    
    # Si falla no muestra ">> Página siguiente"
    try:
        next_page = scrapertools.get_match(data,'<span class="current">\d+</span><a href="([^"]+)"')
        title= "[COLOR red][B]Pagina siguiente »[/B][/COLOR]"
        itemlist.append( Item(channel=__channel__, title=title, url=next_page, action="menuestre",  folder=True) )
    except: pass
    return itemlist


def verpeli(item):   
   
   logger.info("[repelis] menupelis")
   logger.info("[repelis] "+item.url)
    
   itemlist = []
            
   data = scrapertools.cache_page(item.url).decode('iso-8859-1').encode('utf-8')
  
   '''<h2>Sinopsis</2><p>(.*?)</p>
   <div id="informacion" class="tab-pane">
   <h2>Titulo en Español</h2>
   <p>Abzurdah</p>
   <h2>Titulo Original</h2>
   <p>Abzurdah</p>
   <h2>Año de Lanzamiento</h2>
   <p>2015</p>
   <h2>Generos</h2>
   <p>Romance</p>
   <h2>Idioma</h2>
   <p>Latino</p>
   <h2>Calidad</h2>
   <p>DVD-Rip</p>
   '''
   
   #estos son los datos para plot 
   patron = '<h2>Sinopsis</h2>.*?<p>(.*?)</p>.*?<div id="informacion".*?</h2>.*?<p>(.*?)</p>' #titulo
   matches = re.compile(patron,re.DOTALL).findall(data)    
   scrapertools.printMatches(matches)
   for sinopsis,title in matches:
       title = "[COLOR white][B]" + title + "[/B][/COLOR]"
   
   patron = '<div id="informacion".*?>(.*?)</div>'
   matches = re.compile(patron,re.DOTALL).findall(data)    
   scrapertools.printMatches(matches)
   for scrapedplot in matches:
       splot = title + "\n\n"
       plot = scrapedplot
       plot = re.sub('<h2>',"[COLOR red][B]",plot)
       plot = re.sub('</h2>',"[/B][/COLOR] : ",plot)
       plot = re.sub('<p>',"[COLOR green]",plot)
       plot = re.sub('</p>',"[/COLOR]\n",plot)
       plot = re.sub('<[^>]+>',"",plot)
       splot += plot + "\n[COLOR red][B] Sinopsis[/B][/COLOR]\n " + sinopsis
        
    
   #datos de los enlaces
   patron = '<a rel="nofollow".*?</a>.*?</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?src="http://www.google.com/s2/favicons\?domain=(.*?)"'
   matches = re.compile(patron,re.DOTALL).findall(data)    
   scrapertools.printMatches(matches)
         
   for scrapedlang, scrapedquality, scrapedurl in matches:
      url = urlparse.urljoin(item.url,scrapedurl)
      logger.info("[repelis] Lang:["+scrapedlang+"] Quality["+scrapedquality+"] URL["+url+"]")
      patronenlaces= '.*?://(.*?)/'
      matchesenlaces = re.compile(patronenlaces,re.DOTALL).findall(scrapedurl)      
      scrapertools.printMatches(matchesenlaces)
      scrapedtitle = ""
      for scrapedenlace in matchesenlaces:
          scrapedtitle = title + "  [COLOR white][ [/COLOR]" +"[COLOR green]" +scrapedquality+"[/COLOR]" +"[COLOR white] ][/COLOR]" + " [COLOR red]" + scrapedlang +"[/COLOR]  » " + scrapedenlace 
      itemlist.append( Item(channel=__channel__, action="play" ,  title=scrapedtitle  , extra=title, url=url, fanart=item.thumbnail, thumbnail=item.thumbnail, plot=splot, folder=False))
      
   return itemlist
   

def play(item):
   logger.info("[repelis] play url="+item.url)
   
   itemlist = servertools.find_video_items(data=item.url)
    
   return itemlist
   

def search(item, texto):

   logger.info("[repelis] "+item.url)
   item.url = 'http://www.repelis.tv/search/?s=%s' % (texto)
   logger.info("[repelis] "+item.url)
   
   data = scrapertools.cache_page(item.url).decode('iso-8859-1').encode('utf-8')
 
   patron = '<p class="num-resultados">.*?<a href="([^"]+)" title="([^"]+)">.*?<img src="([^"]+)".*?<p class="text-list">(.*?)</p>'
   matches = re.compile(patron,re.DOTALL).findall(data)    
   scrapertools.printMatches(matches)
   itemlist = []
   
   for scrapedurl,scrapedtitle,scrapedthumbnail,scrapedinfo in matches:      
      title = scrapertools.remove_show_from_title(scrapedtitle,"Ver Película")  
      title = title.replace("Online","")
      url = urlparse.urljoin(item.url,scrapedurl)
      thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
      logger.info("[repelis] "+url)
      itemlist.append( Item(channel=__channel__, action="verpeli", title=title, fulltitle=title , url=url , thumbnail=thumbnail, fanart=thumbnail) )
    
   return itemlist  
   

#Por año, aquí está difícil filtrar las "eroticas" así que quito la opcion si no esta el adultmode enabled
def poranyo(item):
   
    logger.info("[repelis] poranyo")
    logger.info("[repelis] "+item.url)
    
    itemlist = []
       
    data = scrapertools.cache_page(item.url).decode('iso-8859-1').encode('utf-8')
       
    patron = '<option value="([^"]+)">(.*?)</option>'    
    matches = re.compile(patron,re.DOTALL).findall(data)    
    scrapertools.printMatches(matches)
    for scrapedurl,scrapedtitle in matches:
       title = scrapertools.remove_show_from_title(scrapedtitle,"Ver Película")  
       title = title.replace("Online","")
       url = urlparse.urljoin(item.url,scrapedurl)       
       itemlist.append( Item(channel=__channel__, action="todaspelis", title=title, fulltitle=title , url=url ) )
            
    return itemlist
   

#Aqui si que se filtran las eroticas    
def porcateg(item):
 		
    logger.info("[repelis] poranyo")
    logger.info("[repelis] " + item.url )
    itemlist = []
       
    data = scrapertools.cache_page(item.url).decode('iso-8859-1').encode('utf-8')   
    patron = '<li class="cat-item cat-item-3">.*?<a href="([^"]+)" title="([^"]+)">'
    matches = re.compile(patron,re.DOTALL).findall(data)    
    scrapertools.printMatches(matches)
    itemlist = []
   
    for scrapedurl,scrapedtitle in matches:      
        title = scrapertools.remove_show_from_title(scrapedtitle,"Ver Película")  
        title = title.replace("Online","")
        url = urlparse.urljoin(item.url,scrapedurl)        
        logger.info("[repelis] "+url)
        #si no esta permitidas categoria adultos, la filtramos
        erotica = ""
        if config.get_setting("enableadultmode") == "false":
            patron = '.*?/erotic.*?'
            try:
                erotica = scrapertools.get_match(scrapedurl,patron)
            except:            
               itemlist.append( Item(channel=__channel__, action="todaspelis", title=title, fulltitle=title , url=url ) )
        else: 
            itemlist.append( Item(channel=__channel__, action="todaspelis", title=title, fulltitle=title , url=url ) )
    
    return itemlist  