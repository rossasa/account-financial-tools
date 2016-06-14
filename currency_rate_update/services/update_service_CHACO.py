# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2009 CamptoCamp. All rights reserved.
#    @author Nicolas Bessi
#
#    Abstract class to fetch rates from Yahoo Financial
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from .currency_getter_interface import Currency_getter_interface

from lxml import html
import requests
import logging
_logger = logging.getLogger(__name__)

class CHACO_getter(Currency_getter_interface):
    """Implementation of Currency_getter_factory interface
    for Cambios Chaco website
    """

    def get_updated_currency(self, currency_array, main_currency,
                             max_delta_days):
        """implementation of abstract method of curreny_getter_interface"""
        self.validate_cur(main_currency)
        page = requests.get('http://www.cambioschaco.com.py')
        tree = html.fromstring(page.content)
        if main_currency == "USD":
            val = {
            'BRL': tree.xpath('//*[@id="arb-exchange-brl"]/td[3]/span/text()')[0].replace('.','').replace(',','.'),
            'ARS': tree.xpath('//*[@id="arb-exchange-ars"]/td[3]/span/text()')[0].replace('.','').replace(',','.'),
            'EUR': tree.xpath('//*[@id="arb-exchange-eur"]/td[3]/span/text()')[0].replace('.','').replace(',','.'),
            'PYG': tree.xpath('//*[@id="exchange-usd"]/td[3]/span/text()')[0].replace('.','').replace(',','.')
            }
        else:
            val = {
            'BRL': tree.xpath('//*[@id="exchange-brl"]/td[3]/span/text()')[0].replace('.','').replace(',','.'),
            'ARS': tree.xpath('//*[@id="exchange-ars"]/td[3]/span/text()')[0].replace('.','').replace(',','.'),
            'EUR': tree.xpath('//*[@id="exchange-eur"]/td[3]/span/text()')[0].replace('.','').replace(',','.'),
            'USD': tree.xpath('//*[@id="exchange-usd"]/td[3]/span/text()')[0].replace('.','').replace(',','.')
            }
        if main_currency in currency_array:
            currency_array.remove(main_currency)
        _logger.info('maincurrency: %s', main_currency)
        for curr in currency_array:
            self.validate_cur(curr)
            _logger.info('valor %s (moneda: %s)', val[curr], curr)
            if val[curr]:
                self.updated_currency[curr] = val[curr]
            else:
                raise Exception('Could not update the %s' % (curr))

        return self.updated_currency, self.log_info
