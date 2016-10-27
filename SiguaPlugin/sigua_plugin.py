# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SiguaPlugin
                                 A QGIS plugin
 Utilidad para anyadir edificios Sigua a Qgis
                              -------------------
        begin                : 2016-04-06
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Jose Manuel Mira (Universidad de Alicante)
        email                : josema.mira@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
#from qgis.core import *

from qgis.core import *
from qgis.utils import iface
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from PyQt4.QtXml import QDomDocument
import colorbrewer
import dbsettings
#import time
#from ui import Ui_ui
#from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
#from PyQt4.QtGui import QAction, QIcon
from PyQt4.QtSql import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from sigua_plugin_dialog import SiguaPluginDialog
import os.path


class SiguaPlugin:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'SiguaPlugin_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = SiguaPluginDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Sigua Plugin')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'SiguaPlugin')
        self.toolbar.setObjectName(u'SiguaPlugin')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SiguaPlugin', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToDatabaseMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/SiguaPlugin/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Anyadir edificios UA'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginDatabaseMenu(
                self.tr(u'&Sigua Plugin'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # Cargar formulario desde consulta pg para combo de edificios


        db = QSqlDatabase('QPSQL')
        db.setHostName(dbsettings.params[0])
        db.setDatabaseName(dbsettings.params[2])
        db.setUserName(dbsettings.params[3])
        db.setPassword(dbsettings.params[4])
        db.setPort(5432)

        if (db.open()==False):
            QMessageBox.critical(None, "Database Error", db.lastError().text())

        ok = db.open()
        if ok:
            sql = "select cod_zona || cod_edificio ||'PB'||' - ' || txt_edificio ||' (PLANTA BAJA)' as zzee from edificios WHERE pb=true  UNION select cod_zona || cod_edificio ||'P1'||' - ' || txt_edificio ||' (PLANTA 1)'  as zzee from edificios WHERE p1=true UNION select cod_zona || cod_edificio ||'P2'||' - ' || txt_edificio ||' (PLANTA 2)' as zzee from edificios WHERE p2=true  UNION select cod_zona || cod_edificio ||'P3'||' - ' || txt_edificio ||' (PLANTA 3)' as zzee from edificios WHERE p3=true UNION select cod_zona || cod_edificio ||'P4'||' - ' || txt_edificio ||' (PLANTA 4)' as zzee from edificios WHERE p4=true  UNION select cod_zona || cod_edificio ||'PS'||' - ' || txt_edificio ||' (PLANTA SOTANO)' as zzee from edificios WHERE ps=true ORDER BY 1"
            query = db.exec_(sql)
            while query.next():
                zzeetxt = unicode(query.value(0))
                self.dlg.comboBoxEdificio.addItem(zzeetxt)

            db.close()
            self.dlg.show()
            # Acciones para botones
            self.dlg.aceptarButton.clicked.connect(self.cargaEdificio)
            self.dlg.cerrarButton.clicked.connect(self.dlg.close)
            # Desactivar botones
            self.dlg.testButton.setEnabled(False)
            self.dlg.colorButton.setEnabled(False)
            self.dlg.temaButton.setEnabled(False)
            self.dlg.tema2Button.setEnabled(False)
            self.dlg.mapaButton.setEnabled(False)
            self.dlg.labelButton.setEnabled(False)
            self.dlg.denoButton.setEnabled(False)
            self.dlg.mapaPlantillaButton.setEnabled(False)



    # función para cargar el edificio
    def cargaEdificio(self):
        # asignamos variables a las selecciones de los combos
        varZZEEPP = self.dlg.comboBoxEdificio.currentText()[:6]
        varPlanta = varZZEEPP[4:6]
        print varPlanta

        # asignamos el nombre de tabla PostGIS
        if (varPlanta == 'PB'):
            planta = 'sigpb'
        elif (varPlanta == 'P1'):
            planta = 'sigp1'
        elif (varPlanta == 'P2'):
            planta = 'sigp2'
        elif (varPlanta == 'P2'):
            planta = 'sigp2'
        elif (varPlanta == 'P3'):
            planta = 'sigp3'
        elif (varPlanta == 'P4'):
            planta = 'sigp4'
        elif (varPlanta == 'PS'):
            planta = 'sigps'

        varTocZZEEPP = 'E' + varZZEEPP
        # Añadir layer de PostGIS a QGIS
        uri = QgsDataSourceURI()
        # set host name, port, database name, username and password
        uri.setConnection(dbsettings.params[0], dbsettings.params[1],dbsettings.params[2],dbsettings.params[3], dbsettings.params[4])
        #uri.setConnection(host, port, dbname, user, password)
        sql="(SELECT e.gid, e.codigo,e.coddpto,d.txt_dpto_sigua,e.actividad,a.txt_actividad,a.activresum,e.denominaci,e.observacio,e.geometria FROM "+planta+" e, actividades a, departamentossigua d WHERE e.actividad = a.codactividad AND e.coddpto = d.cod_dpto_sigua AND e.codigo LIKE '"+varZZEEPP+"%')"
        # set database schema, table name, geometry column and optionaly subset (WHERE clause)
        #uri.setDataSource("public", planta, "geometria", "codigo like '"+varZZEEPP+"%'")
        uri.setDataSource("",sql,"geometria","","gid")
        # Definir la vlayer de PostGIS
        vLayer = QgsVectorLayer(uri.uri(), varTocZZEEPP, "postgres")
        # Set metadata
        vLayer.setShortName(varTocZZEEPP)
        vLayer.setTitle(u"Planta de edificio " + varTocZZEEPP )
        vLayer.setAbstract(u"Edificio procedente del Sistema de Información Geográfica de la Universidad de Alicante (SIGUA)")
        # Con esto añadimos la capa al TOC y se visualiza
        QgsMapLayerRegistry.instance().addMapLayer(vLayer)
        # Resultado de la creacion de la capa
        # Zoom a capa
        canvas = iface.mapCanvas()
        extent = vLayer.extent()
        canvas.setExtent(extent)
        #activar botones
        self.dlg.testButton.setEnabled(True)
        self.dlg.testButton.clicked.connect(self.test)
        self.dlg.colorButton.setEnabled(True)
        self.dlg.colorButton.clicked.connect(self.change_color)
        self.dlg.temaButton.setEnabled(True)
        self.dlg.temaButton.clicked.connect(self.tematico)
        self.dlg.tema2Button.setEnabled(True)
        self.dlg.tema2Button.clicked.connect(self.tematico2)
        self.dlg.mapaButton.setEnabled(True)
        self.dlg.mapaButton.clicked.connect(self.mapapdf)
        self.dlg.labelButton.setEnabled(True)
        self.dlg.labelButton.clicked.connect(self.labelCodigo)
        self.dlg.denoButton.setEnabled(True)
        self.dlg.denoButton.clicked.connect(self.labelDeno)
        self.dlg.mapaPlantillaButton.setEnabled(True)
        self.dlg.mapaPlantillaButton.clicked.connect(self.mapaPlantillaPdf)


    def test(self):
        uri = QgsDataSourceURI()
        uri.setConnection(dbsettings.params[0], dbsettings.params[1],dbsettings.params[2],dbsettings.params[3], dbsettings.params[4])
        lyr = self.iface.activeLayer()
        zzeepp = lyr.name()[1:7]
        planta = ("sig"+ zzeepp[4:6]).lower()
        QMessageBox.information(None, "Test", zzeepp + " " + planta)
        varTocZZEEPP = 'VACIOS-E' + zzeepp
        uri = QgsDataSourceURI()
        uri.setConnection(dbsettings.params[0], dbsettings.params[1],dbsettings.params[2],dbsettings.params[3], dbsettings.params[4])
        sql = "(select * from "+ planta +" where codigo like '"+ zzeepp + "%' and actividad in (7,8) and codigo not in (select codigo from todaspersonas where codigo like '"+ zzeepp + "%'))"
        uri.setDataSource("",sql,"geometria","","gid")
        # Definir la vlayer de PostGIS
        vLayer = QgsVectorLayer(uri.uri(), varTocZZEEPP, "postgres")
        vLayer.setShortName(varTocZZEEPP)
        vLayer.setTitle(u"Despachos vacíos " + varTocZZEEPP )
        vLayer.setAbstract(u"Despachos vacíos procedente del Sistema de Información Geográfica de la Universidad de Alicante (SIGUA)")
        QgsMapLayerRegistry.instance().addMapLayer(vLayer)
        # Zoom a capa
        canvas = iface.mapCanvas()
        extent = vLayer.extent()
        canvas.setExtent(extent)




    def change_color(self):
        layer = iface.activeLayer()
        # create a new single symbol renderer
        symbol = QgsSymbolV2.defaultSymbol(layer.geometryType())
        renderer = QgsSingleSymbolRendererV2(symbol)
        # define un simbolo
        properties = {'color': 'green', 'color_border': 'black'}
        symbol_layer = QgsSimpleFillSymbolLayerV2.create(properties)
        # assign the symbol layer to the symbol
        renderer.symbols()[0].changeSymbolLayer(0, symbol_layer)
        # assign the renderer to the layer
        layer.setRendererV2(renderer)
        self.iface.legendInterface().refreshLayerSymbology(layer)
        #self.iface.mapCanvas().freeze(True)
        self.iface.mapCanvas().refresh()
        layer.triggerRepaint()

    # crea un mapa temático de usos
    def tematico(self):
        layer = iface.activeLayer()
        usos = {
            u"Administración": ("#b3cde3", u"Administración"),
            "Despacho": ("#fbb4ae", "Despacho"),
            "Docencia": ("#ccebc5", "Docencia"),
            "Laboratorio": ("#decbe4", "Laboratorio"),
            "Salas": ("#fed9a6", "Salas"),
            "Muros": ("#808080", "Muros"),
            "": ("white", "Resto")}
        categorias = []
        for estancia, (color, label) in usos.items():
            sym = QgsSymbolV2.defaultSymbol(layer.geometryType())
            sym.setColor(QColor(color))
            category = QgsRendererCategoryV2(estancia, sym, label)
            categorias.append(category)

            field = "activresum"
            index = layer.fieldNameIndex("activresum")
            # comprueba que existe el campo activresum
            if (index == -1):
                QMessageBox.critical(None, "Field error", "No existe el campo activresum. Seleccione la capa adecuada")
                break

            renderer = QgsCategorizedSymbolRendererV2(field, categorias)
            layer.setRendererV2(renderer)
            QgsMapLayerRegistry.instance().addMapLayer(layer)
            layer.triggerRepaint()
            layer.setName(layer.name()[:6] + u' (uso)')
            # actualizar metadatos
            layer.setTitle(u"Planta de edificio " + layer.name()[:6] + u' (uso)' )
            layer.setAbstract(u"Edificio procedente del Sistema de Informacion Geografica de la Universidad de Alicante (SIGUA)")


    # crea un temático de unidades/dptos
    def tematico2(self):
        layer = iface.activeLayer()
        # array de dptos
        idx = layer.fieldNameIndex('txt_dpto_sigua')
        dptosArr = layer.uniqueValues( idx )
        total = len(dptosArr)
        if total < 3:
            coloresArr = colorbrewer.Set3[3]
        elif total <= 12:
            coloresArr = colorbrewer.Set3[total]
        else:
            exceso = total - 12
            if exceso < 3:
                coloresArr = colorbrewer.Set3[12] + colorbrewer.Paired[3]
            else:
                coloresArr = colorbrewer.Set3[12] + colorbrewer.Paired[exceso]

        print coloresArr
        dptoDic = {}
        for i in range(0, len(dptosArr)):
            if  dptosArr[i] == u"GESTIÓN DE ESPACIOS":
                dptoDic[dptosArr[i]] = ("white", dptosArr[i])
            else:
                dptoDic[dptosArr[i]] = (coloresArr[i], dptosArr[i])

        #print dptoDic
        categories = []
        for estancia, (color, label) in dptoDic.items():
            sym = QgsSymbolV2.defaultSymbol(layer.geometryType())
            sym.setColor(QColor(color))
            category = QgsRendererCategoryV2(estancia, sym, label)
            categories.append(category)

        field = "txt_dpto_sigua"
        renderer = QgsCategorizedSymbolRendererV2(field, categories)
        layer.setRendererV2(renderer)
        QgsMapLayerRegistry.instance().addMapLayer(layer)
        layer.triggerRepaint()
        layer.setName(layer.name()[:6] + u" (organización)")
        # actualizar metadatos
        layer.setTitle(u"Planta de edificio " + layer.name()[:6] + u" (organización)")
        layer.setAbstract(u"Edificio procedente del Sistema de Información Geográfica de la Universidad de Alicante (SIGUA)")

    def labelDeno(self):
        layer = iface.activeLayer()
        palyr = QgsPalLayerSettings()
        palyr.readFromLayer(layer)
        palyr.enabled = True
        palyr.bufferDraw = True
        palyr.bufferColor = QColor("white")
        palyr.bufferSize = 1
        palyr.scaleVisibility = True
        palyr.scaleMax = 2000
        palyr.isExpression = False
        palyr.fieldName = 'denominaci'
        palyr.size = 15
        palyr.textColor = QColor("black")
        palyr.drawLabels = True
        palyr.wrapChar = ' '
        #palyr.fitInPolygonOnly = True  #solo dibuja las label que caben dentro del poligono
        palyr.placement = QgsPalLayerSettings.OverPoint
        palyr.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, '7', '')
        palyr.writeToLayer(layer)
        iface.mapCanvas().refresh()

    def mapapdf(self):
        # inicio QgsComposition
        mapRenderer = self.iface.mapCanvas().mapRenderer()
        c = QgsComposition(mapRenderer)
        c.setPlotStyle(QgsComposition.Print)

        # horizontal o vertical
        layer = iface.activeLayer()
        canvas = iface.mapCanvas()
        extent = layer.extent()
        #extent.height()
        #extent.width()

        if (extent.width() > extent.height()):
            papel = "H"
            pagWidth = 297
            pagHeight = 210
        else:
            papel = "V"
            pagWidth = 210
            pagHeight = 297

        #mapa
        x, y = 0, 0
        w, h = pagWidth, pagHeight
        #w, h = c.paperWidth(), c.paperHeight()
        composerMap = QgsComposerMap(c, x, y, w, h)
        c.addItem(composerMap)

        # label
        composerLabel = QgsComposerLabel(c)
        composerLabel.setText(u'TITULO DEL MAPA')
        composerLabel.setFont(QFont('Droid Sans', 15, QFont.Bold))
        composerLabel.setItemPosition(15, 190, True)
        composerLabel.adjustSizeToText()
        c.addItem(composerLabel)

        # metadatos
        text = QgsComposerLabel(c)
        text.setText(u'PROYECCIÓN' + '\n' + 'UTM, Datum ETRS89, Huso 30' + '\n' + u'Autor: José Manuel Mira Martínez')
        text.setFont(QFont('Droid Sans', 15, QFont.Bold))
        text.setItemPosition(40, 40, True)
        text.adjustSizeToText()
        #text.setFrameEnabled(True)
        text.setMargin(-6)
        c.addItem(text)

        #legend
        legend = QgsComposerLegend(c)
        legend.setTitle('LEYENDA')
        legend.setStyleFont(QgsComposerLegendStyle.Title, QFont("Droid Sans", 14))
        legend.setStyleFont(QgsComposerLegendStyle.Group, QFont("Droid Sans", 12))
        legend.setStyleFont(QgsComposerLegendStyle.Subgroup, QFont("Droid Sans", 10))
        legend.setStyleFont(QgsComposerLegendStyle.SymbolLabel, QFont("Droid Sans", 8))


        legend.model().setLayerSet(mapRenderer.layerSet())
        #legend.modelV2().
        c.addItem(legend)

        # escala numérica
        item = QgsComposerScaleBar(c)
        item.setStyle('Numeric')  # optionally modify the style
        item.setComposerMap(composerMap)
        item.applyDefaultSize()
        c.addItem(item)

        # escala gráfica
        ScaleBar = QgsComposerScaleBar(c)
        ScaleBar.setComposerMap(composerMap)
        ScaleBar.setStyle('Line Ticks Up')  # optionally modify the style
        #ScaleBar.setFrame(False)
        ScaleBar.setUnitLabeling("m")
        ScaleBar.setNumMapUnitsPerScaleBarUnit(1)
        ScaleBar.setNumSegmentsLeft(4)
        ScaleBar.setNumSegments(4)
        ScaleBar.setNumUnitsPerSegment(5)
        ScaleBar.setItemPosition(120, 150)
        #ScaleBar.applyDefaultSize()
        #ScaleBar.update()
        c.addItem(ScaleBar)

        # Norte
        norte = QgsComposerPicture(c)
        norte.setPos(QPointF(50, 110))
        norte.setPictureFile("/home/jose/.qgis2/python/plugins/SiguaPlugin/norte.svg")
        norte.setSceneRect(QRectF(0, 100, 20, 20))
        c.addItem(norte)

        # Logo sigua
        logo = QgsComposerPicture(c)
        logo.setPos(QPointF(50, 110))
        logo.setPictureFile("/home/jose/.qgis2/python/plugins/SiguaPlugin/logo_sigua.svg")
        logo.setSceneRect(QRectF(200, 10, 30, 10))
        c.addItem(logo)

        # rectángulo borde sin relleno
        grey = {'color_border': '230, 230, 230, 255', 'style': 'no'}
        greysym = QgsFillSymbolV2.createSimple(grey)
        shape1 = QgsComposerShape(10, 10, pagWidth - 20, pagHeight - 20, c)
        shape1.setShapeType(1)
        shape1.setUseSymbolV2(True)
        shape1.setShapeStyleSymbol(greysym)
        c.addItem(shape1)

        # rectángulo shape rojo con borde azul
        red = {'color': '255,0,0,255', 'color_border': '0,0,255,255'}
        redsym = QgsFillSymbolV2.createSimple(red)
        shape1 = QgsComposerShape(10, 50, 10, 25, c)
        shape1.setShapeType(1)
        shape1.setUseSymbolV2(True)
        shape1.setShapeStyleSymbol(redsym)
        c.addItem(shape1)

        # elipse/circulo de 20x20 en posicion 100,100 shape rojo con borde azul
        red = {'color': '255, 0, 0, 255', 'color_border': '0, 0, 255, 255'}
        redsym = QgsFillSymbolV2.createSimple(red)
        shape1 = QgsComposerShape(100, 100, 20, 20, c)
        shape1.setShapeType(0)  # 0 elipse, 1 rectangulo, 2 triangulo
        shape1.setUseSymbolV2(True)
        shape1.setShapeStyleSymbol(redsym)
        c.addItem(shape1)

        #frame is drawn around each item by default. How to remove the frame
        #composerLabel.setFrame(False)

        # PDF
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        layer = self.iface.activeLayer()
        import time
        salida = "mapa_" + layer.name() + "_" + time.strftime("%Y%m%d%H%M%S") + ".pdf"
        printer.setOutputFileName(salida)
        printer.setPaperSize(QSizeF(pagWidth, pagHeight), QPrinter.Millimeter)
        printer.setFullPage(True)
        printer.setColorMode(QPrinter.Color)
        printer.setResolution(c.printResolution())

        pdfPainter = QPainter(printer)
        paperRectMM = printer.pageRect(QPrinter.Millimeter)
        paperRectPixel = printer.pageRect(QPrinter.DevicePixel)
        c.render(pdfPainter, paperRectPixel, paperRectMM)
        pdfPainter.end()
        QMessageBox.information(self.iface.mainWindow(), "Resultado", "El mapa " + salida + " ha sido creado existosamente.")

    def labelCodigo(self):
        layer = iface.activeLayer()
        palyr = QgsPalLayerSettings()
        palyr.readFromLayer(layer)
        palyr.enabled = True
        palyr.bufferDraw = True
        palyr.bufferColor = QColor("white")
        palyr.bufferSize = 1
        palyr.scaleVisibility = True
        palyr.scaleMax = 2000
        palyr.isExpression = True
        palyr.fieldName =  'if( "codigo" NOT LIKE \'%000\', right(  "codigo" ,3),"")'
        palyr.size = 15
        palyr.textColor = QColor("black")
        palyr.drawLabels = True
        palyr.fitInPolygonOnly = True  #solo dibuja las label que caben dentro del poligono
        palyr.placement = QgsPalLayerSettings.OverPoint
        palyr.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, '7', '')
        palyr.writeToLayer(layer)
        iface.mapCanvas().refresh()

    def mapaPlantillaPdf(self):
        import time

        registry = QgsMapLayerRegistry.instance()
        layers = registry.mapLayers().values()
        layerName = iface.activeLayer().name()
        # Add layer to map render
        myMapRenderer = QgsMapRenderer()
        myMapRenderer.setLayerSet(layerName)
        myMapRenderer.setProjectionsEnabled(False)

        # Load template
        layer = iface.activeLayer()
        canvas = iface.mapCanvas()
        extent = layer.extent()
        #canvas = QgsMapCanvas()
        ms = canvas.mapSettings()
        myComposition = QgsComposition(ms)

        # uso plantilla
        if (extent.width() > extent.height()):
            tipo = 'h'
            myFile = os.path.join(os.path.dirname(__file__), 'template_h2.qpt')
        else:
            # plantilla vertical
            tipo = 'v'
            myFile = os.path.join(os.path.dirname(__file__), 'template_v2.qpt')
        #myFile = '/home/jose/Documentos/pyqgis/template_h.qpt'
        myTemplateFile = file(myFile, 'rt')
        myTemplateContent = myTemplateFile.read()
        myTemplateFile.close()
        myDocument = QDomDocument()
        myDocument.setContent(myTemplateContent)
        myComposition.loadFromTemplate(myDocument)

        # Sustituir textos
        substitution_map = {'TITULO': u'TEMÁTICO','EDIFICIO':self.dlg.comboBoxEdificio.currentText(),'FECHA': time.strftime("%d/%m/%Y") ,'AUTOR': u'José Manuel Mira','ORGANISMO': 'Universidad de Alicante'}
        myComposition.loadFromTemplate(myDocument, substitution_map)

        # Zoom a capa
        myMap = myComposition.getComposerMapById(0)
        myExtent = iface.activeLayer().extent()
        myMap.setNewExtent(myExtent)

        # Save image
        salidaPNG = "mapa_" + layer.name() + "_" + time.strftime("%Y%m%d%H%M%S") + ".png"
        myImage = myComposition.printPageAsRaster(0)
        myImage.save(salidaPNG)

        # export PDF
        import time
        salidaPDF = "mapa_" + layer.name() + "_" + time.strftime("%Y%m%d%H%M%S") + ".pdf"
        myComposition.exportAsPDF(salidaPDF)

        QMessageBox.information(self.iface.mainWindow(), "Resultado", "Los mapas, " + salidaPNG + " y "+ salidaPDF+ " han sido creados exitosamente.")
