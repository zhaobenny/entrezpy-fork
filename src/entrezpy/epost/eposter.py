# Copyright 2018, 2019 The University of Sydney
# This file is part of entrezpy.
#
#  Entrezpy is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Lesser General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  Entrezpy is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
#  A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with entrezpy.  If not, see <https://www.gnu.org/licenses/>.
"""
.. module:: eposter
   :synopsis: This module is part of entrezpy. It exports the Eposter class
              implementing Epost queries. It inherits
              :class:`entrezpy.base.query.EutilsQuerys`
.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import json
import logging

import entrezpy.base.query
import entrezpy.epost.epost_analyzer
import entrezpy.epost.epost_parameter
import entrezpy.epost.epost_request


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class Eposter(entrezpy.base.query.EutilsQuery):
  """Eposter implements Epost queries to E-Utilities [0]
  It implements :meth:`entrezpy.base.query.inquire` and
  :meth:`entrezpy.base.query.inquire`.  EPost posts UIDs to the history server.
  Without passed WebEnv, a new WebEnv and correspndong QueryKey are returned.
  With a given WebEvn the posted UIDs will be added to this WebEnv and the
  corresponding QueryKey is returned. All parameters described in [0] are
  acccepted.
  [0]: https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EPost
  """

  def __init__(self, tool, email, apikey=None, apikey_var=None, threads=None, qid=None):
    """Inits Eposter instance with given attributes.

      :param str tool: tool name
      :param str email: user email
      :param str apikey: NCBI apikey
      :param str apikey_var: enviroment variable storing NCBI apikey
      :param int threads: set threads for multithreading
      :param str qid: unique query id
    """
    super().__init__('epost.fcgi', tool, email, apikey, apikey_var, threads, qid)

  def inquire(self, parameter, analyzer=entrezpy.epost.epost_analyzer.EpostAnalyzer()):
    """Implements :meth:`entrezpy.base.query.inquire` and posts UIDs to Entrez.
       Epost is only one request.

    :param dict parameter: Epost parameter
    :param analyzer analyzer: analyzer for Epost results, default is
        :class:`entrezpy.epost.epost_analyzer.EpostAnalyzer`
    :return: analyzer or None if request errors have been encountered
    :rtype: :class:`entrezpy.base.analyzer.EntrezpyAnalyzer` instance or None
    """
    p = entrezpy.epost.epost_parameter.EpostParameter(parameter)
    self.monitor_start(p)
    self.add_request(entrezpy.epost.epost_request.EpostRequest(self.eutil, p), analyzer)
    self.request_pool.drain()
    self.monitor_stop()
    if self.check_requests() != 0:
      return None
    return analyzer

  def check_requests(self):
    """Test for request errors

    :return: 1 if request errors else 0
    :rtype: int
    """
    if not self.hasFailedRequests():
      logger.info(json.dumps({__name__ : {'Query status' : {self.id : 'OK'}}}))
      return 0
    logger.info(json.dumps({__name__ : {'Query status' : {self.id : 'failed'}}}))
    logger.debug(json.dumps({__name__ : {'Query status' :
                                         {self.id : 'failed',
                                          'request-dumps' : [x.dump_internals()
                                                             for x in self.failed_requests]}}}))
    return 1
