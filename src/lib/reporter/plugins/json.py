# -*- coding: utf-8 -*-

"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Development Team: Stanislav WEB
"""

from .provider import PluginProvider
from src.core import filesystem, FileSystemError
from src.core import helper


class JsonReportPlugin(PluginProvider):
    """ JsonReportPlugin class"""

    PLUGIN_NAME = 'JsonReport'
    EXTENSION_SET = '.json'

    def __init__(self, taget, data):
        """
        PluginProvider constructor
        :param str taget: target host
        :param dict data: result set
        """

        PluginProvider.__init__(self, taget, data)

        try:
            config = filesystem.readcfg(self.CONFIG_FILE)
            directory = config.get('opendoor', 'reports')
            self.__target_dir = "".join((directory, self._target))
            filesystem.makedir(self.__target_dir)
        except FileSystemError as e:
            raise Exception(e)

    def process(self):
        """
        Process data
        :return: str
        """

        resultset = helper.to_json(self._data)

        try:
            filesystem.clear(self.__target_dir, extension=self.EXTENSION_SET)
            self.record(self.__target_dir, self._target, resultset)
        except (Exception, FileSystemError) as e:
            raise Exception(e)
