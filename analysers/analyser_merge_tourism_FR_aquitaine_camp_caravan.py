#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014-2016                                 ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from .Analyser_Merge import Analyser_Merge, Source, JSON, Load, Mapping, Select, Generate


class Analyser_Merge_Tourism_FR_Aquitaine_Caravan(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8140", "class": 1, "level": 3, "tag": ["merge", "tourism"], "desc": T_(u"Aquitaine caravan site not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            "http://catalogue.datalocale.fr/dataset/liste-aires-campingcars-aquitaine",
            u"Liste des aires de camping-cars en Aquitaine",
            JSON(Source(attribution = u"Réseau SIRTAQUI - Comité Régional de Tourisme d'Aquitaine - www.sirtaqui-aquitaine.com", millesime = "08/2018",
                    fileUrl = "http://wcf.tourinsoft.com/Syndication/aquitaine/eda0e9ba-cec4-48f5-bd24-985d1d614c23/Objects?$format=json"),
                extractor = lambda json: json['d']),
            Load("LON", "LAT",
                xFunction = self.degree,
                yFunction = self.degree),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"tourism": "caravan_site"}),
                conflationDistance = 500,
                generate = Generate(
                    static1 = {"tourism": "caravan_site"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "name": "NOMOFFRE",
                        "ref:FR:CRTA": "SyndicObjectID",
                        "website": lambda fields: None if not fields["URL"] else fields["URL"] if fields["URL"].startswith('http') else 'http://' + fields["URL"]},
                    text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x and x != 'None', [fields["NOMOFFRE"], fields["AD1"], fields["AD1SUITE"], fields["AD2"], fields["AD3"], fields["CP"], fields["COMMUNE"]]))} )))

class Analyser_Merge_Tourism_FR_Aquitaine_Camp(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8140", "class": 11, "level": 3, "tag": ["merge", "tourism"], "desc": T_(u"Aquitaine camp site not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            "http://catalogue.datalocale.fr/dataset/liste-campings-aquitaine",
            u"Liste des campings en Aquitaine",
            JSON(Source(attribution = u"Réseau SIRTAQUI - Comité Régional de Tourisme d'Aquitaine - www.sirtaqui-aquitaine.com", millesime = "08/2018",
                    fileUrl = "http://wcf.tourinsoft.com/Syndication/aquitaine/13d7f8ab-bd69-4815-b02c-d8134663b849/Objects?$format=json"),
                extractor = lambda json: json['d']),
            Load("LON", "LAT",
                xFunction = self.degree,
                yFunction = self.degree),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"tourism": "camp_site"}),
                conflationDistance = 300,
                generate = Generate(
                    static1 = {"tourism": "camp_site"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "name": "NOMOFFRE",
                        "stars": lambda fields: fields["RECHERCHECLAS"][0] if fields["RECHERCHECLAS"] and fields["RECHERCHECLAS"][0].isdigit() else None,
                        "ref:FR:CRTA": "SyndicObjectID",
                        "website": lambda fields: None if not fields["URL"] else fields["URL"] if fields["URL"].startswith('http') else 'http://' + fields["URL"]},
                    text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x and x != 'None', [fields["NOMOFFRE"], fields["AD1"], fields["AD1SUITE"], fields["AD2"], fields["AD3"], fields["CP"], fields["COMMUNE"]]))} )))
