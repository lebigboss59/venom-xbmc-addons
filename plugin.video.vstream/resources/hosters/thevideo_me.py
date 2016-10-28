#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
import re,urllib2,urllib,time
import xbmcgui,xbmc,re

from resources.lib.packer import cPacker

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'thevideo.me'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR] [COLOR khaki]'+self.__sHD+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'thevideo_me'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';
        
    def __getIdFromUrl(self,sUrl):
        sPattern = 'http://www.thevideo.me/embed-([^\.]+)'
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return
        
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        
        id = self.__getIdFromUrl(self.__sUrl)

        api_call = False

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        oParser = cParser()
        
        sPattern = "var mpri_Key='([^']+)';(.+?)<\/script>"
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if not (aResult[0]):
            return False , False
            
        key = aResult[1][0][0]
        code = cPacker().unpack(aResult[1][0][1])
        
        xbmc.log(str(code))
        
        #ca deconne ici
        #sPattern = "\=\"\\'\+\\'\/(.+?)\\\'\.concat"
        #r = re.search(sPattern,code)
        #xbmc.log(str(r))
        #if not (r):
        #    return False , False
            
        url2 = 'http://thevideo.me/jwv/' + key       

        oRequest = cRequestHandler(url2)
        sHtmlContent2 = oRequest.request()
        
        xbmc.log(sHtmlContent2)
        
        code = cPacker().unpack(sHtmlContent2)
        
        xbmc.log(code)
        
        #*************************************************
        
        sPattern = '{"file":"([^"]+)","label":"(\d+p)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
        
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))
                
            #Si au moins 1 url
            if (url):
            #Afichage du tableau
                dialog2 = xbmcgui.Dialog()
                ret = dialog2.select('Select Quality',qua)
                if (ret > -1):
                    api_call = url[ret]
        
                api_call = api_call + '?direct=false&ua=1&vt=' + vt
        
        xbmc.log(api_call)
        
        if (api_call):
            return True, api_call
            
        return False, False
