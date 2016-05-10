# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SiguaPlugin
                                 A QGIS plugin
 Utilidad para añadir edificios Sigua a Qgis
                             -------------------
        begin                : 2016-04-06
        copyright            : (C) 2016 by José Manuel Mira (Universidad de Alicante)
        email                : josema.mira@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load SiguaPlugin class from file SiguaPlugin.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .sigua_plugin import SiguaPlugin
    return SiguaPlugin(iface)
