"""
..
  Copyright 2018, 2019 The University of Sydney
  This file is part of entrezpy.

  Entrezpy is free software: you can redistribute it and/or modify it under the
  terms of the GNU Lesser General Public License as published by the Free
  Software Foundation, either version 3 of the License, or (at your option) any
  later version.

  Entrezpy is distributed in the hope that it will be useful, but WITHOUT ANY
  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
  A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with entrezpy.  If not, see <https://www.gnu.org/licenses/>.

.. module:: entrezpy.elink.linkset.unit.linklist
   :synopsis:
    Exports class LinkList impelementing Elink results for acheck command.

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import entrezpy.elink.linkset.unit.linksetunit

class LinkList(entrezpy.elink.linkset.unit.linksetunit.LinksetUnit):
  """
  Inits new link result unit for the ncheck command.

  :param str dbto: target database
  :param str linkname: Elink linkname
  :param str menutag: Elink menutag
  :param str htmltag: Elink htmltag
  :param int priority: Elink priority
  :rtype: New class instance
  """

  @classmethod
  def new(cls, dbto, linkname, menutag, htmltag, priority):
    """
    Returns new instance.

    :rtype: :class:`entrezpy.elink.linkset.unit.linklist.LinksetUnit`
    """
    return cls(dbto, linkname, menutag, htmltag, priority)

  def __init__(self, dbto, linkname, menutag, htmltag, priority):
    super().__init__(dbto, linkname)
    self.menutag = menutag
    self.htmltag = htmltag
    self.priority = priority

  def dump(self):
    return dict({'htmltag' : self.htmltag, 'priority' : self.priority}, **self.basic_dump())
