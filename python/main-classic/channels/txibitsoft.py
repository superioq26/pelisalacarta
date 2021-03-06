# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para txibitsoft
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys


from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

import xbmcgui

__category__ = "A"
__type__ = "generic"
__title__ = "Txibitsoft"
__channel__ = "txibitsoft"
__language__ = "ES"

host = "http://www.txibitsoft.com/"

DEBUG = config.get_setting("debug")



def isGeneric():
    return True



def mainlist(item):
    logger.info("pelisalacarta.txibitsoft mainlist")
    
    itemlist = []
    
    
    
    title="[COLOR white][B]Peliculas[/B][/COLOR]"
    itemlist.append( Item(channel=__channel__, title=title , action="peliculas"           , url="http://www.txibitsoft.com/torrents.php?procesar=1&categorias='Peliculas'&pagina=1", thumbnail="http://s27.postimg.org/nbbeles4j/tbpelithu.jpg", fanart="http://s14.postimg.org/743jqty35/tbpelifan.jpg"))
    title="[COLOR white][B]1080[/B][/COLOR]"
    itemlist.append( Item(channel=__channel__, title=title , action="peliculas"           , url="http://www.txibitsoft.com/torrents.php?procesar=1&categorias='Cine%20Alta%20Definicion%20HD'&subcategoria=1080p&pagina=1", thumbnail="http://s4.postimg.org/t4i9vgjgd/tb1080th.jpg", fanart="http://s17.postimg.org/7z5pnf5tb/tb1080fan.jpg"))
    title="[COLOR white][B]Series[/B][/COLOR]"
    itemlist.append( Item(channel=__channel__, title=title , action="peliculas"           , url="http://www.txibitsoft.com/torrents.php?procesar=1&categorias='Series'&pagina=1", thumbnail="http://s12.postimg.org/4ao5ekygd/tbseriethu.jpg", fanart="http://s12.postimg.org/oymstbjot/tbseriefan.jpg"))
    title="[COLOR white][B]Buscar...[/B][/COLOR]"
    itemlist.append( Item(channel=__channel__, title=title      , action="search", url="", fanart="http://s1.postimg.org/f5mnv2pcf/tbbusfan.jpg", thumbnail="http://s28.postimg.org/r2911z0rx/tbbusthu.png"))
    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.txibitsoft search")
    texto = texto.replace(" ","+")
    
    item.url = "http://www.txibitsoft.com/torrents.php?procesar=1&texto=%s" % (texto)
    try:
        return buscador(item)
    # Se captura la excepciÛn, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def buscador(item):
    logger.info("pelisalacarta.txibitsoft buscador")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|&amp;","",data)
    item.url = re.sub(r"&amp;","",item.url)
    # corrige la falta de imagen
    data = re.sub(r'<img src="<!doctype html><html xmlns="','</div><img src="http://s30.postimg.org/8n4ej5j0x/noimage.jpg" texto ><p>',data)
    
    #<div class="torrent-container-2 clearfix"><img class="torrent-image" src="uploads/torrents/images/thumbnails2/4441_step--up--all--in----blurayrip.jpg" alt="Imagen de Presentaci&oacute;n" /><div class="torrent-info"><h4><a href ="/descargar_torrent_27233-id_step_up_all_in_microhd_1080p_ac3_5.1--castellano--ac3_5.1_ingles_subs.html">Step Up All In MicroHD 1080p AC3 5.1-Castellano-AC3 5.1 Ingles Subs</a> </h4><p>19-12-2014</p><p>Subido por: <strong>TorrentEstrenos</strong> en <a href="/ver_torrents_41-id_en_peliculas_microhd.html" title="Peliculas MICROHD">Peliculas MICROHD</a><br />Descargas <strong><a href="#" style="cursor:default">46</a></strong></p><a class="btn-download" href ="/descargar_torrent_27233-id_step_up_all_in_microhd_1080p_ac3_5.1--castellano--ac3_5.1_ingles_subs.html">Descargar</a></div></div>
    
    patron =  '<dl class=".*?dosColumnasDobles"><dt>'
    patron += '<a href="([^"]+)" '
    patron += 'title.*?:([^<]+)".*?'
    patron += '<img src="([^"]+)".*?'
    patron += 'Idioma: <span class="categoria">([^<]+).*?'
    patron += 'Tama&ntilde;o: <span class="categoria">([^<]+)'
    
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)==0 :
       itemlist.append( Item(channel=__channel__, title="[COLOR gold][B]No se ha encontrado nada en la busqueda...[/B][/COLOR]", thumbnail ="http://s6.postimg.org/vhczf38ep/oops.png", fanart ="http://s12.postimg.org/59o1c792l/oopstxibi.jpg",folder=False) )


    
    for scrapedurl, scrapedtitle, scrapedthumbnail, scrapedlenguage, scrapedsize in matches:
        scrapedurl = "http://www.txibitsoft.com" + scrapedurl
        scrapedlenguage = scrapedlenguage.replace(scrapedlenguage,"[COLOR blue]"+scrapedlenguage+"[/COLOR]")
        scrapedsize = scrapedsize.replace(scrapedsize,"[COLOR gold]"+scrapedsize+"[/COLOR]")
        scrapedtitle = scrapedtitle.replace(scrapedtitle,"[COLOR white]"+scrapedtitle+"[/COLOR]")
        scrapedtitle = scrapedtitle + "-(Idioma:" + scrapedlenguage + ")" + "-(Tamaño: " + scrapedsize +")"
        
        
        itemlist.append( Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="fanart", thumbnail=scrapedthumbnail, fanart ="http://s21.postimg.org/w0lgvyud3/tbfanartgeneral2.jpg",fulltitle=scrapedtitle, folder=True) )
    return itemlist

def peliculas(item):
    logger.info("pelisalacarta.txibitsoft peliculas")
    itemlist = []
    
    # Descar<div id="catalogheader">ga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|&amp;","",data)
    item.url = re.sub(r"&amp;","",item.url)
    # corrige la falta de imagen
    data = re.sub(r'<img src="<!doctype html><html xmlns="','</div><img src="http://s30.postimg.org/8n4ej5j0x/noimage.jpg" texto ><p>',data)
    
    #<div class="torrent-container-2 clearfix"><img class="torrent-image" src="uploads/torrents/images/thumbnails2/4441_step--up--all--in----blurayrip.jpg" alt="Imagen de Presentaci&oacute;n" /><div class="torrent-info"><h4><a href ="/descargar_torrent_27233-id_step_up_all_in_microhd_1080p_ac3_5.1--castellano--ac3_5.1_ingles_subs.html">Step Up All In MicroHD 1080p AC3 5.1-Castellano-AC3 5.1 Ingles Subs</a> </h4><p>19-12-2014</p><p>Subido por: <strong>TorrentEstrenos</strong> en <a href="/ver_torrents_41-id_en_peliculas_microhd.html" title="Peliculas MICROHD">Peliculas MICROHD</a><br />Descargas <strong><a href="#" style="cursor:default">46</a></strong></p><a class="btn-download" href ="/descargar_torrent_27233-id_step_up_all_in_microhd_1080p_ac3_5.1--castellano--ac3_5.1_ingles_subs.html">Descargar</a></div></div>
    
    patron =  '<dl class=".*?dosColumnasDobles"><dt>'
    patron += '<a href="([^"]+)" '
    patron += 'title.*?:([^<]+)".*?'
    patron += '<img src="([^"]+)".*?'
    patron += 'Idioma: <span class="categoria">([^<]+).*?'
    patron += 'Tama&ntilde;o: <span class="categoria">([^<]+)'
    
    
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)==0 :
       itemlist.append( Item(channel=__channel__, title="[COLOR gold][B]El video ya no se encuentra en la web, prueba a encontrala por busqueda...[/B][/COLOR]", thumbnail ="http://s6.postimg.org/vhczf38ep/oops.png", fanart ="http://s12.postimg.org/59o1c792l/oopstxibi.jpg",folder=False) )
    
    for scrapedurl, scrapedtitle, scrapedthumbnail, scrapedlenguage, scrapedsize in matches:
        scrapedurl = "http://www.txibitsoft.com" + scrapedurl
        scrapedlenguage = scrapedlenguage.replace(scrapedlenguage,"[COLOR blue]"+scrapedlenguage+"[/COLOR]")
        scrapedsize = scrapedsize.replace(scrapedsize,"[COLOR gold]"+scrapedsize+"[/COLOR]")
        scrapedtitle = scrapedtitle.replace(scrapedtitle,"[COLOR white]"+scrapedtitle+"[/COLOR]")
        scrapedtitle = scrapedtitle + "-(Idioma:" + scrapedlenguage + ")" + "-(Tamaño: " + scrapedsize +")"
        
        
        itemlist.append( Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="fanart", thumbnail=scrapedthumbnail, fanart= "http://s21.postimg.org/w0lgvyud3/tbfanartgeneral2.jpg", fulltitle=scrapedtitle, folder=True) )
    
    # Extrae el paginador
    ## Paginación
    
    if "pagina=" in item.url:
       current_page_number = int(scrapertools.get_match(item.url,'pagina=(\d+)'))
       item.url = re.sub(r"pagina=\d+","pagina={0}",item.url)
    else:
        current_page_number = 1

    

    next_page_number = current_page_number + 1
    next_page = item.url.format(next_page_number)
    
    
        
        

    title ="siguiente>>"
    title = title.replace(title,"[COLOR orange]"+title+"[/COLOR]")
    itemlist.append( Item(channel=__channel__, action="peliculas", title=title , url=next_page , thumbnail="http://s18.postimg.org/4l9172cqx/tbsiguiente.png", fanart="http://s21.postimg.org/w0lgvyud3/tbfanartgeneral2.jpg" , folder=True) )
    
    
    
    
    
    
    return itemlist

def fanart(item):
    logger.info("pelisalacarta.txibitsoft fanart")
    itemlist = []
    url = item.url
    data = scrapertools.cachePage(url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    if "peliculas" in item.url :
        title= scrapertools.get_match(data,'<form name="frm" id="frm" method="get" action="torrent.php">.*?alt="([^<]+)"')
        title= re.sub(r"3D|SBS|\[.*?\]|\(.*?\)|-|Montaje del Director|V.Extendida|Quadrilogia","",title)
        title= title.replace('Reparado','')
        title= title.replace('V.Extendida','')
        title= title.replace('á','a')
        title= title.replace('Á','A')
        title= title.replace('é','e')
        title= title.replace('í','i')
        title= title.replace('ó','o')
        title= title.replace('ú','u')
        title= title.replace('ñ','n')
        title= title.replace(' ','%20')
        url="http://api.themoviedb.org/3/search/movie?api_key=57983e31fb435df4df77afb854740ea9&query=" + title + "&language=es&include_adult=false"
        data = scrapertools.cachePage(url)
        data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
        patron = '"page":1.*?"backdrop_path":"(.*?)".*?,"id":(.*?),'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if len(matches)==0:
            extra=item.thumbnail
            show= item.thumbnail
            category= item.thumbnail
            itemlist.append( Item(channel=__channel__, title=item.title, url=item.url, action="findvideos", thumbnail=item.thumbnail, fanart=item.thumbnail ,extra=extra, show=show, category= category, folder=True) )
        else:
            for fan, id in matches:
                fanart="https://image.tmdb.org/t/p/original" + fan
                item.extra= fanart
      #clearart, fanart_2 y logo
                url ="http://assets.fanart.tv/v3/movies/"+id+"?api_key=dffe90fba4d02c199ae7a9e71330c987"
                data = scrapertools.cachePage(url)
                data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
                patron = '"hdmovielogo":.*?"url": "([^"]+)"'
                matches = re.compile(patron,re.DOTALL).findall(data)
                if '"moviedisc"' in data:
                    disc = scrapertools.get_match(data,'"moviedisc":.*?"url": "([^"]+)"')
                if '"movieposter"' in data:
                    poster = scrapertools.get_match(data,'"movieposter":.*?"url": "([^"]+)"')
                if '"moviethumb"' in data:
                    thumb = scrapertools.get_match(data,'"moviethumb":.*?"url": "([^"]+)"')
                if '"moviebanner"' in data:
                    banner= scrapertools.get_match(data,'"moviebanner":.*?"url": "([^"]+)"')
                
                if len(matches)==0:
                    extra=  item.thumbnail
                    show = item.extra
                    category = item.extra
                    itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=item.thumbnail, fanart=item.extra, extra=extra,category= category, show=show, folder=True) )
            for logo in matches:
                if '"hdmovieclearart"' in data:
                    clear=scrapertools.get_match(data,'"hdmovieclearart":.*?"url": "([^"]+)"')
                    if '"moviebackground"' in data:
                        fanart_2=scrapertools.get_match(data,'"moviebackground":.*?"url": "([^"]+)"')
                        extra=clear
                        show= fanart_2
                        if '"moviebanner"' in data:
                            category= banner
                        else:
                            category= clear
                        itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show,  category= category,folder=True) )
                    else:
                        extra= clear
                        show=item.extra
                        if '"moviebanner"' in data:
                             category= banner
                        else:
                            category= clear
                        itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show,  category= category, folder=True) )
                
                if '"moviebackground"' in data:
                    fanart_2=scrapertools.get_match(data,'"moviebackground":.*?"url": "([^"]+)"')
                    if '"hdmovieclearart"' in data:
                        clear=scrapertools.get_match(data,'"hdmovieclearart":.*?"url": "([^"]+)"')
                        extra=clear
                        show= fanart_2
                        if '"moviebanner"' in data:
                            category= banner
                        else:
                            category= clear
                    else:
                        extra=logo
                        show= fanart_2
                        if '"moviebanner"' in data:
                             category= banner
                        else:
                            category= logo  
                        itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show,  category= category, folder=True) )






                if not '"hdmovieclearart"' in data and not '"moviebackground"' in data:
                        extra= logo
                        show=  item.extra
                        if '"moviebanner"' in data:
                             category= banner
                        else:
                            category= item.extra
                        itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show ,  category= category, folder=True) )



    elif "cine" in item.url:
          title= scrapertools.get_match(data,'alt="([^<]+) \[')
          title= re.sub(r"3D|SBS|\[.*?\]|\(.*?\)|-|Montaje del Director|V.Extendida|Quadrilogia","",title)
          title= title.replace('á','a')
          title= title.replace('Á','A')
          title= title.replace('é','e')
          title= title.replace('í','i')
          title= title.replace('ó','o')
          title= title.replace('ú','u')
          title= title.replace('ñ','n')
          title= title.replace(' ','%20')
          url="http://api.themoviedb.org/3/search/movie?api_key=57983e31fb435df4df77afb854740ea9&query=" + title + "&language=es&include_adult=false"
          data = scrapertools.cachePage(url)
          data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
          patron = '"page":1.*?"backdrop_path":"(.*?)".*?,"id":(.*?),'
          matches = re.compile(patron,re.DOTALL).findall(data)
          if len(matches)==0:
              extra=item.thumbnail
              show= item.thumbnail
              category= item.thumbnail
              itemlist.append( Item(channel=__channel__, title=item.title, url=item.url, action="findvideos", thumbnail=item.thumbnail, fanart=item.thumbnail,extra = extra, show= show, category= category,folder=True) )
          else:
              for fan,id in matches:
                  fanart="https://image.tmdb.org/t/p/original" + fan
                  item.extra= fanart
        #clearart, fanart_2 y logo
                  url ="http://assets.fanart.tv/v3/movies/"+id+"?api_key=dffe90fba4d02c199ae7a9e71330c987"
                  data = scrapertools.cachePage(url)
                  data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
                  patron = '"hdmovielogo":.*?"url": "([^"]+)"'
                  matches = re.compile(patron,re.DOTALL).findall(data)
                  if '"moviedisc"' in data:
                       disc = scrapertools.get_match(data,'"moviedisc":.*?"url": "([^"]+)"')
                  if '"movieposter"' in data:
                       poster = scrapertools.get_match(data,'"movieposter":.*?"url": "([^"]+)"')
                  if '"moviethumb"' in data:
                       thumb = scrapertools.get_match(data,'"moviethumb":.*?"url": "([^"]+)"')
                  if '"moviebanner"' in data:
                       banner= scrapertools.get_match(data,'"moviebanner":.*?"url": "([^"]+)"')
                
                  if len(matches)==0:
                      extra=  item.thumbnail
                      show = item.extra
                      category = item.extra
                      itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=item.thumbnail, fanart=item.extra, extra=extra, show=show, category= category, folder=True) )
              for logo in matches:
                  if '"hdmovieclearart"' in data:
                      clear=scrapertools.get_match(data,'"hdmovieclearart":.*?"url": "([^"]+)"')
                      if '"moviebackground"' in data:
                          fanart_2=scrapertools.get_match(data,'"moviebackground":.*?"url": "([^"]+)"')
                          extra=clear
                          show= fanart_2
                          if '"moviebanner"' in data:
                               category= banner
                          else:
                               category= clear
                          itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show,  category= category,folder=True) )
                      else:
                            extra= clear
                            show=item.extra
                            if '"moviebanner"' in data:
                                 category= banner
                            else:
                                 category= clear
                            itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show,  category= category, folder=True) )
                                                                                                                                                                          
                  if '"moviebackground"' in data:
                       fanart_2=scrapertools.get_match(data,'"moviebackground":.*?"url": "([^"]+)"')
                       if '"hdmovieclearart"' in data:
                            clear=scrapertools.get_match(data,'"hdmovieclearart":.*?"url": "([^"]+)"')
                            extra=clear
                            show= fanart_2
                            if '"moviebanner"' in data:
                                 category= banner
                            else:
                                 category= clear
                       else:
                             extra=logo
                             show= fanart_2
                             if '"moviebanner"' in data:
                                  category= banner
                             else:
                                  category= clear
                             itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show,  category= category, folder=True) )
                            
                            
                                                                                                                                                                                                                                                  
                                                                                                                                                                                                                                                  
                  if not '"hdmovieclearart"' in data and not '"moviebackground"' in data:
                           extra= logo
                           show=  item.extra
                           if '"moviebanner"' in data:
                                category= banner
                           else:
                                category= item.extra
                           itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show ,  category= category, folder=True) )
                 

    elif "series" in item.url:
          title= title= scrapertools.get_match(data,'</script><title>([^<]+)')
          title= re.sub(r"3D|Temporada.*?\d+|\[.*?\]|\(.*?\)|SBS|-|Txibit|Soft|\d+x\d+","",title)
          
          title= title.replace('Fin','')
          title= title.replace('á','a')
          title= title.replace('Á','A')
          title= title.replace('é','e')
          title= title.replace('í','i')
          title= title.replace('ó','o')
          title= title.replace('ú','u')
          title= title.replace('ñ','n')
          title= title.replace(' ','%20')
          title= title.replace('Temporada','')
          url="http://thetvdb.com/api/GetSeries.php?seriesname=" + title + "&language=es"
          if "Érase%20una%20vez" in url:
              url ="http://thetvdb.com/api/GetSeries.php?seriesname=Erase%20una%20vez%20(2011)&language=es"
          if "Hawaii%20Five%200%20" in url:
              url ="http://thetvdb.com/api/GetSeries.php?seriesname=hawaii%205.0&language=es"
          if "The%20Big%20Bang%20Theory" in url:
              url = "http://thetvdb.com/api/GetSeries.php?seriesname=The%20Big%20Bang%20Theory%20%20&language=es"
          data = scrapertools.cachePage(url)
          data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
          patron = '<Data><Series><seriesid>([^<]+)</seriesid>'
          matches = re.compile(patron,re.DOTALL).findall(data)
          if len(matches)==0:
             extra= item.thumbnail
             show=  item.thumbnail
             category= ""
             itemlist.append( Item(channel=__channel__, title=item.title, url=item.url, action="findvideos", thumbnail=item.thumbnail, fanart=item.thumbnail ,extra=extra, category= category, show=show , folder=True) )
          else:
             #fanart
              for id in matches:
                  category = id
                  id_serie = id
                  url ="http://thetvdb.com/api/1D62F2F90030C444/series/"+id_serie+"/banners.xml"
                  if "Castle" in title:
                      url ="http://thetvdb.com/api/1D62F2F90030C444/series/83462/banners.xml"
                  data = scrapertools.cachePage(url)
                  data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
                  patron = '<Banners><Banner>.*?<VignettePath>(.*?)</VignettePath>'
                  matches = re.compile(patron,re.DOTALL).findall(data)
                  if len(matches)==0:
                     extra=item.thumbnail
                     show= item.thumbnail
                     itemlist.append( Item(channel=__channel__, title=item.title, url=item.url, action="findvideos", thumbnail=item.thumbnail, fanart=item.thumbnail ,category = category, extra=extra, show=show, folder=True) )
        
                  for fan in matches:
                      fanart="http://thetvdb.com/banners/" + fan
                      item.extra= fanart
                #clearart, fanart_2 y logo
                  for id in matches:
                      url ="http://assets.fanart.tv/v3/tv/"+id_serie+"?api_key=dffe90fba4d02c199ae7a9e71330c987"
                      if "Castle" in title:
                          url ="http://assets.fanart.tv/v3/tv/83462?api_key=dffe90fba4d02c199ae7a9e71330c987"
                      data = scrapertools.cachePage(url)
                      data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
                      patron = '"clearlogo":.*?"url": "([^"]+)"'
                      matches = re.compile(patron,re.DOTALL).findall(data)
                      if '"tvposter"' in data:
                           tvposter = scrapertools.get_match(data,'"tvposter":.*?"url": "([^"]+)"')
                      if '"tvbanner"' in data:
                         tvbanner = scrapertools.get_match(data,'"tvbanner":.*?"url": "([^"]+)"')
                      if '"tvthumb"' in data:
                         tvthumb = scrapertools.get_match(data,'"tvthumb":.*?"url": "([^"]+)"')
                      if '"hdtvlogo"' in data:
                           hdtvlogo = scrapertools.get_match(data,'"hdtvlogo":.*?"url": "([^"]+)"')
                      if '"hdclearart"' in data:
                           hdtvclear = scrapertools.get_match(data,'"hdclearart":.*?"url": "([^"]+)"')
                      if len(matches)==0:
                          if '"hdtvlogo"' in data:
                               if "showbackground" in data:
                                   fanart_2=scrapertools.get_match(data,'"showbackground":.*?"url": "([^"]+)"')
                                   if '"hdclearart"' in data:
                                        thumbnail = hdtvlogo
                                        extra=  hdtvclear
                                        show = fanart_2
                                   
                                   else:
                                       thumbnail = hdtvlogo
                                       extra= thumbnail
                                       show = fanart_2
                                   
                                   itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=thumbnail, fanart=item.extra, category=category, extra=extra, show=show,  folder=True) )
                
                
                               else:
                                   if '"hdclearart"' in data:
                                        thumbnail= hdtvlogo
                                        extra= hdtvclear
                                        show= item.extra
                                   
                                   else:
                                        thumbnail= hdtvlogo
                                        extra= thumbnail
                                        show= item.extra
                                   
                    
                                   itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=thumbnail, fanart=item.extra, extra=extra, show=show, category= category, folder=True) )
                          else:
                               extra=  item.thumbnail
                               show = item.extra
                               
                               itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=item.thumbnail, fanart=item.extra, extra=extra, show=show, category = category, folder=True) )

                  for logo in matches:
                      if '"hdtvlogo"' in data:
                           thumbnail = hdtvlogo
                      elif not '"hdtvlogo"' in data :
                              if '"clearlogo"' in data:
                                 thumbnail= logo
                      else:
                          thumbnail= item.thumbnail
                      if '"clearart"' in data:
                           clear=scrapertools.get_match(data,'"clearart":.*?"url": "([^"]+)"')
                           if "showbackground" in data:
                               fanart_2=scrapertools.get_match(data,'"showbackground":.*?"url": "([^"]+)"')
                               extra=clear
                               show= fanart_2
                               
                               itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=thumbnail,  fanart=item.extra, extra=extra,show=show, category= category,  folder=True) )
                           else:
                                extra= clear
                                show=item.extra
                                
                                itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=thumbnail, fanart=item.extra, extra=extra,show=show,  category= category, folder=True) )

                      if "showbackground" in data:
                          fanart_2=scrapertools.get_match(data,'"showbackground":.*?"url": "([^"]+)"')
                          if '"clearart"' in data:
                               clear=scrapertools.get_match(data,'"clearart":.*?"url": "([^"]+)"')
                               extra=clear
                               show= fanart_2
                          
                          else:
                               extra=logo
                               show= fanart_2
                               
                               itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=thumbnail, fanart=item.extra, extra=extra,show=show, category = category, folder=True) )
        
                      if not '"clearart"' in data and not '"showbackground"' in data:
                               if '"hdclearart"' in data:
                                   extra= hdtvclear
                                   show= item.extra
                               
                               else:
                                   extra= thumbnail
                                   show=  item.extra

                               itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=thumbnail, fanart=item.extra, extra=extra,show=show , category = category, folder=True) )

    title ="Info"
    title = title.replace(title,"[COLOR turquoise]"+title+"[/COLOR]")
    if len(item.extra)==0:
        fanart=item.thumbnail
    else:
        fanart = item.extra

    if '"movieposter"' in data:
        thumbnail= poster
    elif '"tvposter"' in data:
         thumbnail= tvposter
    else:
        thumbnail = item.thumbnail
    if "serie" in item.url:
        if "tvbanner" in data:
            category = tvbanner
        else:
            category = show


    itemlist.append( Item(channel=__channel__, action="info" , title=title , url=item.url, thumbnail=thumbnail, fanart=fanart, extra= extra, category = category, show= show, folder=False ))


    ###trailer

    title= "[COLOR darkmagenta]Trailer[/COLOR]"
    if len(item.extra)==0:
        fanart=item.thumbnail
    else:
        fanart = item.extra
    
    if '"moviethumb"' in data:
        thumbnail = thumb
    elif '"tvthumb"' in data:
         thumbnail = tvthumb
    else:
        thumbnail = item.thumbnail
    if '"moviedisc"' in data:
        extra= disc
    elif '"tvbanner"' in data:
        extra= tvbanner
    else:
        if '"moviethumb"' in data:
             extra = thumb
        elif '"tvthumb"' in data:
              extra = tvthumb
        else:
            extra = item.thumbnail
    url = item.url
    data = scrapertools.cachePage(url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    title2= scrapertools.get_match(data,'</script><title>(.*?)</title>')
    title2= re.sub(r"3D|Temporada.*?\d+|\[.*?\]|\(.*?\)|SBS|-|Txibit|Soft|\d+x\d+","",title2)
    title2 = scrapertools.decodeHtmlentities( title2 )
    title2= title2.replace('Temporada','')
    if "año:" in data:
        year = scrapertools.get_match(data,'style="height:12em;">.*?A.*?o(.*?)Dura')
        year = re.sub(r":|\(|\)","",year)
    else:
        year= ""
    trailer = title2 + " " + year + " trailer"
    trailer = urllib.quote(trailer)


    itemlist.append( Item(channel=__channel__, action="trailer", title=title , url=item.url , thumbnail=thumbnail , plot=trailer , fanart=fanart, extra=extra, folder=True) )
    return itemlist

def trailer(item):
    logger.info("pelisalacarta.bityouth trailer")
    itemlist = []
    api_google_for_trailer = "https://www.google.com/uds/GvideoSearch?callback=google.search.VideoSearch.RawCompletion&rsz=small&hl=es&source=gsc&gss=.com&sig=cb6ef4de1f03dde8c26c6d526f8a1f35&q=site%3Ahttp%3A%2F%2Fyoutube.com%20" + item.plot + "&qid=14e3123d9b6320389&context=0&key=notsupplied&v=1.0"
    
    data = scrapertools.cache_page(api_google_for_trailer).replace('\\u003d','=').replace('\\u0026','&')
    
    patron = '"title":"([^"]+)".*?'
    patron+= '"tbUrl":"([^"]+)".*?'
    patron+= '"url":"([^"]+)"'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)==0 :
        itemlist.append( Item(channel=__channel__, title="[COLOR gold][B]No hay Trailer[/B][/COLOR]", thumbnail ="http://s6.postimg.org/vhczf38ep/oops.png", fanart ="http://s12.postimg.org/59o1c792l/oopstxibi.jpg",folder=False) )
    
    for scrapedtitle, scrapedthumbnail, scrapedurl in matches:
        scrapedtitle=re.sub(r"\n|\r|\t|\s{2}|&.*?;","",scrapedtitle)
        scrapedtitle=scrapedtitle.replace(scrapedtitle,"[COLOR darkgoldenrod][B]"+scrapedtitle+"[/B][/COLOR]")
        itemlist.append( Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, server="youtube", fanart="http://s6.postimg.org/htq12yor5/tbtrailers.png", thumbnail=item.extra, action="play", folder=False) )
    
    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.txibitsoft findvideos")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    
    patron = '<form name="frm" id="frm" method="get" action="torrent.php">.*?'
    patron += 'alt="([^<]+)".*?'
    patron += '<p class="limpiar centro"><a class="torrent" href="([^"]+)"'
    
    
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)==0 :
       itemlist.append( Item(channel=__channel__, title="[COLOR gold][B]El video ya no se encuentra en la web, prueba a encontrala por busqueda...[/B][/COLOR]", thumbnail ="http://s6.postimg.org/vhczf38ep/oops.png", fanart ="http://s12.postimg.org/59o1c792l/oopstxibi.jpg",folder=False) )
    
    for scrapedtitle, scrapedurl in matches:
        
        if "x" in scrapedtitle :
            patron='<form name="frm" id="frm" method="get" action="torrent.php">.*?alt=".*?(\d+)x(\d+)'
            matches = re.compile(patron,re.DOTALL).findall(data)
            for temp, epi in matches:
                plot= temp+"|"+epi
        
        if "Temporada" in scrapedtitle:
            patron='<form name="frm" id="frm" method="get" action="torrent.php">.*?alt=".*?Temporada (\d+).*?\[Cap.\d(\d+)'
            matches = re.compile(patron,re.DOTALL).findall(data)
            for temp, epi in matches:
                epi=re.sub(r"101|201|301|401|501|601|701|801|901","01",epi)
                epi=re.sub(r"102|202|302|402|502|602|702|802|902","02",epi)
                epi=re.sub(r"103|203|303|403|503|603|703|803|903","03",epi)
                epi=re.sub(r"104|204|304|404|504|604|704|804|904","04",epi)
                epi=re.sub(r"105|205|305|405|505|605|705|805|905","05",epi)
                epi=re.sub(r"106|206|306|406|506|606|706|806|906","06",epi)
                epi=re.sub(r"107|207|307|407|507|607|707|807|907","07",epi)
                epi=re.sub(r"108|208|308|408|508|608|708|808|908","08",epi)
                epi=re.sub(r"109|209|309|409|509|609|709|809|909","09",epi)
                epi=re.sub(r"110|210|310|410|510|610|710|810|910","10",epi)
                epi=re.sub(r"111|211|311|411|511|611|711|811|911","11",epi)
                epi=re.sub(r"112|212|312|412|512|612|712|812|912","12",epi)
                epi=re.sub(r"113|213|313|413|513|613|713|813|913","13",epi)
                epi=re.sub(r"114|214|314|414|514|614|714|814|914","14",epi)
                epi=re.sub(r"115|215|315|415|515|615|715|815|915","15",epi)
                epi=re.sub(r"116|216|316|416|516|616|716|816|916","16",epi)
                epi=re.sub(r"117|217|317|417|517|617|717|817|917","17",epi)
                epi=re.sub(r"118|218|318|418|518|618|718|818|918","18",epi)
                epi=re.sub(r"119|219|319|419|519|619|719|819|919","19",epi)
                epi=re.sub(r"120|220|320|420|520|620|720|820|920","20",epi)
                epi=re.sub(r"121|221|321|421|521|621|721|821|921","21",epi)
                epi=re.sub(r"122|222|322|422|522|622|722|822|922","22",epi)
                epi=re.sub(r"123|223|323|423|523|623|723|823|923","23",epi)
                epi=re.sub(r"124|224|324|424|524|624|724|824|924","24",epi)
                epi=re.sub(r"125|225|325|425|525|625|725|825|925","25",epi)
                epi=re.sub(r"126|226|326|426|526|626|726|826|926","26",epi)
                epi=re.sub(r"127|227|327|427|527|627|727|827|927","27",epi)
                epi=re.sub(r"128|228|328|428|528|628|728|828|928","28",epi)
                epi=re.sub(r"129|229|329|429|529|629|729|829|929","29",epi)
                epi=re.sub(r"130|230|330|430|530|630|730|830|930","30",epi)
                plot= temp+"|"+epi

        if "series" in item.url:
            title = scrapedtitle
            title= re.sub(r"\[.*?\]|-|Temporada.*?\d+|\d+x\d+|Fin","",title)
            title= title.replace(' ','%20')
            title= title.replace('Temporada','')
            url="http://api.themoviedb.org/3/search/tv?api_key=57983e31fb435df4df77afb854740ea9&query="+title+"&language=es&include_adult=false"
            if "%2090210%20Sensacion%20de%20vivir" in url:
                url="http://api.themoviedb.org/3/search/tv?api_key=57983e31fb435df4df77afb854740ea9&query=90210&language=es&include_adult=false"
            if "%20De%20vuelta%20al%20nido%20" in url:
                url ="http://api.themoviedb.org/3/search/tv?api_key=57983e31fb435df4df77afb854740ea9&query=packed%20to%20the%20rafter&language=es&include_adult=false"
            if "%20Asuntos%20de%20estado%20" in url:
                url="http://api.themoviedb.org/3/search/tv?api_key=57983e31fb435df4df77afb854740ea9&query=state%20of%20affair&language=es&include_adult=false"
            if "%20Como%20defender%20a%20un%20asesino%20" in url:
                url="http://api.themoviedb.org/3/search/tv?api_key=57983e31fb435df4df77afb854740ea9&query=how%20to%20get%20away%20with%20murder&language=es&include_adult=false"
            if "Rizzoli%20and%20Isles%20%20%20" in url:
                url="http://api.themoviedb.org/3/search/tv?api_key=57983e31fb435df4df77afb854740ea9&query=Rizzoli%20&%20Isles%20%20%20&language=es&include_adult=false"
            data = scrapertools.cachePage(url)
            data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
            patron = '{"page".*?"backdrop_path":.*?,"id":(.*?),"'
            matches = re.compile(patron,re.DOTALL).findall(data)
            if len(matches)==0:
                thumbnail= item.thumbnail
                fanart = item.fanart
                id = ""
                temp=""
                epi=""
                scrapedurl = "http://www.txibitsoft.com" + scrapedurl
                title_tag="[COLOR orange]Ver--[/COLOR]"
                scrapedtitle = scrapedtitle.replace(scrapedtitle,"[COLOR magenta][B]"+scrapedtitle+"[/B][/COLOR]")
                scrapedtitle = title_tag + scrapedtitle
                itemlist.append( Item(channel=__channel__, title = scrapedtitle , action="play", url=scrapedurl, server="torrent", thumbnail=thumbnail, fanart=fanart,  folder=False) )

            for id in matches:
                if not '{"page":1,"results":[{"backdrop_path":null' in data:
                         backdrop=scrapertools.get_match(data,'{"page".*?"backdrop_path":"(.*?)",.*?"id"')
                         fanart_3 = "https://image.tmdb.org/t/p/original" + backdrop
                         fanart = fanart_3
                else:
                    fanart= item.fanart
                url ="https://api.themoviedb.org/3/tv/"+id+"/season/"+temp+"/episode/"+epi+"/images?api_key=57983e31fb435df4df77afb854740ea9"
                data = scrapertools.cachePage(url)
                data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
                patron = '{"id".*?"file_path":"(.*?)","height"'
                matches = re.compile(patron,re.DOTALL).findall(data)
                if len(matches)==0:
                    thumbnail = item.thumbnail
                    scrapedurl = "http://www.txibitsoft.com" + scrapedurl
                    title_tag="[COLOR orange]Ver--[/COLOR]"
                    scrapedtitle = scrapedtitle.replace(scrapedtitle,"[COLOR magenta][B]"+scrapedtitle+"[/B][/COLOR]")
                    scrapedtitle = title_tag + scrapedtitle
                    itemlist.append( Item(channel=__channel__, title = scrapedtitle , action="play", url=scrapedurl, server="torrent", thumbnail=thumbnail, fanart=fanart,  folder=False) )
                for foto in matches:
                    thumbnail = "https://image.tmdb.org/t/p/original" + foto


                    scrapedurl = "http://www.txibitsoft.com" + scrapedurl
                    title_tag="[COLOR orange]Ver--[/COLOR]"
                    scrapedtitle = scrapedtitle.replace(scrapedtitle,"[COLOR magenta][B]"+scrapedtitle+"[/B][/COLOR]")
                    scrapedtitle = title_tag + scrapedtitle
                    itemlist.append( Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="play", server="torrent", thumbnail=thumbnail, category = item.category, fanart=fanart, folder=False) )
            extra= item.category+"|"+item.thumbnail+"|"+id+"|"+temp+"|"+epi+"|"+title
    
            title ="Info"
            title = title.replace(title,"[COLOR skyblue]"+title+"[/COLOR]")
            itemlist.append( Item(channel=__channel__, action="info_capitulos" , title=title , url=item.url, thumbnail=thumbnail, fanart=fanart, extra = extra, folder=False ))
        
        else:
            scrapedurl = "http://www.txibitsoft.com" + scrapedurl
            title_tag="[COLOR orange]Ver--[/COLOR]"
            scrapedtitle = scrapedtitle.replace(scrapedtitle,"[COLOR magenta][B]"+scrapedtitle+"[/B][/COLOR]")
            scrapedtitle = title_tag + scrapedtitle
            itemlist.append( Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="play", server="torrent", thumbnail=item.extra, fanart=item.show, folder=False) )
            
    
      
    return itemlist
def info(item):
    logger.info("pelisalacarta.zentorrents info")
    
    url=item.url
    data = scrapertools.cachePage(url)
    data = re.sub(r'\n|\r|\t|\s{2}|&nbsp;|</strong>|&quot;|<label for="|\(.*?\)|\[.*?\]|- Txibit Soft',' ',data)
    
    title= title= scrapertools.get_match(data,'</script><title>([^<]+)</title>')
    title = title.replace(title,"[COLOR aqua][B]"+title+"[/B][/COLOR]")
    scrapedplot = scrapertools.get_match(data,'<textarea.*?">(.*?)</textarea></li>')
    if "Sinopsis" in scrapedplot:
        scrapedplot= scrapertools.get_match(data,'<textarea.*Sinopsis(.*?)</textarea></li>')
    if "SINOPSIS" in scrapedplot:
        scrapedplot= scrapertools.get_match(data,'<textarea.*SINOPSIS(.*?)</textarea></li>')
    if "Sinópsis" in scrapedplot:
        scrapedplot= scrapertools.get_match(data,'<textarea.*Sinópsis(.*?)</textarea></li>')
    if "REPARTO" in scrapedplot:
        scrapedplot= scrapertools.get_match(data,'<textarea.*REPARTO(.*?)</textarea></li>')
    plot_title = "Sinopsis" + "[CR]"
    plot_title = plot_title.replace(plot_title,"[COLOR blue][B]"+plot_title+"[/B][/COLOR]")
    scrapedplot = plot_title + scrapedplot
    scrapedplot = scrapedplot.replace(scrapedplot,"[COLOR magenta]"+scrapedplot+"[/COLOR]")
    scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
    scrapedplot = scrapedplot.replace(":","")
    
    plot = scrapedplot
    if "series" in item.url:
        scrapedinfo= scrapertools.get_match(data,'<li><strong>(.*?)descripcion')
    else:
        scrapedinfo = scrapertools.get_match(data,'style="height:12em;">(.*?)Sinopsis')
    infotitle = "[COLOR blue][B]Más info...[/B][/COLOR]"
    scrapedinfo = scrapedinfo.replace(scrapedinfo,"[COLOR yellow]"+scrapedinfo+"[/COLOR]")
    scrapedinfo = scrapertools.decodeHtmlentities(scrapedinfo)
    scrapedinfo = scrapedinfo.replace ("&gt;","--")
    scrapedinfo= scrapedinfo.replace ("</li><li><strong>",". ")
    scrapedinfo= scrapedinfo.replace ("<li><strong>","")
    scrapedinfo= scrapedinfo.replace ("</li>",".")
    scrapedinfo= scrapedinfo.replace (">","--")
    info = infotitle+scrapedinfo
    if "series" in item.url:
        foto= item.category
        photo= item.extra
    else:

        foto = item.show
        photo= item.extra
    ventana2 = TextBox1(title=title, plot=plot, info=info, thumbnail=photo, fanart=foto)
    ventana2.doModal()


class TextBox1( xbmcgui.WindowDialog ):
        """ Create a skinned textbox window """
        def __init__( self, *args, **kwargs):
            
            self.getTitle = kwargs.get('title')
            self.getPlot = kwargs.get('plot')
            self.getInfo = kwargs.get('info')
            self.getThumbnail = kwargs.get('thumbnail')
            self.getFanart = kwargs.get('fanart')
            
            self.background = xbmcgui.ControlImage( 70, 20, 1150, 630, 'http://s6.postimg.org/58jknrvtd/backgroundventana5.png')
            self.title = xbmcgui.ControlTextBox(140, 60, 1130, 50)
            self.plot = xbmcgui.ControlTextBox( 120, 150, 1056, 140 )
            self.info = xbmcgui.ControlFadeLabel(120, 310, 1056, 100)
            self.thumbnail = xbmcgui.ControlImage( 813, 43, 390, 100, self.getThumbnail )
            self.fanart = xbmcgui.ControlImage( 120, 365, 1060, 250, self.getFanart )
            
            self.addControl(self.background)
            self.addControl(self.title)
            self.addControl(self.plot)
            self.addControl(self.thumbnail)
            self.addControl(self.fanart)
            self.addControl(self.info)
            
            self.title.setText( self.getTitle )
            self.plot.autoScroll(7000,6000,30000)
            self.plot.setText(  self.getPlot )
            self.info.addLabel(self.getInfo)
        
        def get(self):
            self.show()
        
        def onAction(self, action):
            self.close()

def test():
    return True

def info_capitulos(item):
    logger.info("pelisalacarta.bricocine trailer")
    url= item.url
    data = scrapertools.cachePage(url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    item.category = item.extra.split("|")[0]
    item.thumbnail = item.extra.split("|")[1]
    id = item.extra.split("|")[2]
    temp = item.extra.split("|")[3]
    epi = item.extra.split("|")[4]
    title = item.extra.split("|")[5]
    url="https://www.themoviedb.org/tv/"+item.extra.split("|")[2]+item.extra.split("|")[5]+"/season/"+item.extra.split("|")[3]+"/episode/"+item.extra.split("|")[4]+"?language=en"
    data = scrapertools.cachePage(url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    patron = '<p><strong>Air Date:</strong>.*?content="(.*?)">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)==0 :
        title = "[COLOR red][B]LO SENTIMOS...[/B][/COLOR]"
        plot = "Este capitulo no tiene informacion..."
        plot = plot.replace(plot,"[COLOR yellow][B]"+plot+"[/B][/COLOR]")
        foto = "http://s6.postimg.org/nm3gk1xox/noinfosup2.png"
        image="http://s6.postimg.org/ub7pb76c1/noinfo.png"

    for day in matches:
        url="http://thetvdb.com/api/GetEpisodeByAirDate.php?apikey=1D62F2F90030C444&seriesid="+item.extra.split("|")[0]+"&airdate="+day+"&language=es"
        if "Castle%20%20%20" in item.extra.split("|")[5]:
            url="http://thetvdb.com/api/GetEpisodeByAirDate.php?apikey=1D62F2F90030C444&seriesid=83462"+"&airdate="+day+"&language=es"
        
        data = scrapertools.cachePage(url)
        data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
        patron = '<Data>.*?<EpisodeName>([^<]+)</EpisodeName>.*?'
        patron += '<Overview>(.*?)</Overview>.*?'
        
        matches = re.compile(patron,re.DOTALL).findall(data)
        if len(matches)==0 :
            title = "[COLOR red][B]LO SENTIMOS...[/B][/COLOR]"
            plot = "Este capitulo no tiene informacion..."
            plot = plot.replace(plot,"[COLOR yellow][B]"+plot+"[/B][/COLOR]")
            image="http://s6.postimg.org/ub7pb76c1/noinfo.png"
            foto="http://s6.postimg.org/nm3gk1xox/noinfosup2.png"
    
        else :
            
            
            for name_epi, info in matches:
                if "<filename>episodes" in data:
                    foto = scrapertools.get_match(data,'<Data>.*?<filename>(.*?)</filename>')
                    fanart = "http://thetvdb.com/banners/" + foto
                else:
                    fanart=item.extra.split("|")[1]
                plot = info
                plot = plot.replace(plot,"[COLOR darkgoldenrod][B]"+plot+"[/B][/COLOR]")
                title = name_epi.upper()
                title = title.replace(title,"[COLOR orchid][B]"+title+"[/B][/COLOR]")
                image=fanart
                foto= item.extra.split("|")[1]
    ventana = TextBox2(title=title, plot=plot, thumbnail=image, fanart=foto)
    ventana.doModal()


class TextBox2( xbmcgui.WindowDialog ):
        """ Create a skinned textbox window """
        def __init__( self, *args, **kwargs):
            self.getTitle = kwargs.get('title')
            self.getPlot = kwargs.get('plot')
            self.getThumbnail = kwargs.get('thumbnail')
            self.getFanart = kwargs.get('fanart')
            
            self.background = xbmcgui.ControlImage( 70, 20, 1150, 630, 'http://s6.postimg.org/n3ph1uxn5/ventana.png')
            self.title = xbmcgui.ControlTextBox(120, 60, 430, 50)
            self.plot = xbmcgui.ControlTextBox( 120, 150, 1056, 100 )
            self.thumbnail = xbmcgui.ControlImage( 120, 300, 1056, 300, self.getThumbnail )
            self.fanart = xbmcgui.ControlImage( 780, 43, 390, 100, self.getFanart )
            
            self.addControl(self.background)
            self.addControl(self.title)
            self.addControl(self.plot)
            self.addControl(self.thumbnail)
            self.addControl(self.fanart)
            
            self.title.setText( self.getTitle )
            self.plot.setText(  self.getPlot )
        
        def get(self):
            self.show()
        
        def onAction(self, action):
            self.close()
def test():
    return True
















