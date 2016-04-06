# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from ui_control import ui_Control
# initialize Qt resources from file resouces.py
import psycopg2
import resources


class SiguaPlugin:
  def __init__ ( self , iface ):
    # Guardar referencia a la interface QGIS
    self.iface = iface

  def initGui( self ):
    # Configuracion por defecto del plugin
    self.action = QAction(QIcon(":/plugins/sigua/sigua.png"), "Carga de edificios SIGUA", self.iface.getMainWindow())
    QObject.connect(self.action, SIGNAL("activated()"), self.run)

    # Agregar boton al menu y barra de herramientas
    self.iface.addToolBarIcon(self.action)
    self.iface.addPluginMenu("&Nueva capa Sigua...", self.action)

  def unload(self ):
    # Deshabilitar el plugin del menu y barra de herramientas
    self.iface.removePluginMenu("&Nueva capa Sigua...", self.action)
    self.iface.removeToolBarIcon(self.action)

  def run(self ):
    # create and show a configuration dialog or something similar
    flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint  # QgisGui.ModalDialogFlags
    self.pluginGui = ui_Control(self.iface.getMainWindow(), flags)
    # definir comportamiento para los elementos del formulario
    QObject.connect(self.pluginGui.buttonBox,SIGNAL("accepted()"),self.cargaEdificio)

    # Cargar formulario desde consulta pg para combo de edificios
    dbname = "sigua"
    host = "localhost"
    port = "5432"
    user = "postgres"
    password = "j3m"
    
    connText = "dbname=%(dbname)s host=%(host)s port=%(port)s user=%(user)s password=%(password)s" %vars()
    conn = psycopg2.connect(connText)
    #conn = psycopg2.connect("dbname=sigua host=localhost port=5432 user=postgres password=j3m")

    curs = conn.cursor()
    curs.execute("select cod_zona || cod_edificio ||' - ' || txt_edificio as zzee from edificios")
    rows = curs.fetchall()
    for i in range(len(rows)):
        zzeetxt = rows[i][0]
	zzee = zzeetxt[:4]
        self.pluginGui.comboBoxEdificio.addItem(zzeetxt)
    conn.commit()
    #conn.close()
    # anyadimos el combo de plantas
    self.pluginGui.comboBoxPlantas.addItems(['PB','P1','P2','P3','P4','PS'])
    #sacamos el formulario
    self.pluginGui.show()
    

    
# función para cargar el edificio
  def cargaEdificio(self):
    # asignamos variables a las selecciones de los combos
    varZZEE = self.pluginGui.comboBoxEdificio.currentText()[:4]
    varPlanta = self.pluginGui.comboBoxPlantas.currentText()
    # asignamos el nombre de tabla PostGIS
    if (varPlanta == 'PB'):
      planta = 'sigpb'
    if (varPlanta == 'P1'):
      planta = 'sigp1'
    if (varPlanta == 'P2'):
      planta = 'sigp2'
    if (varPlanta == 'P2'):
      planta = 'sigp2'
    if (varPlanta == 'P3'):
      planta = 'sigp3'
    if (varPlanta == 'P4'):
      planta = 'sigp4'
    if (varPlanta == 'PS'):
      planta = 'sigps'

    varZZEEPP = varZZEE + varPlanta + '%'
    varTocZZEEPP = 'E'+varZZEE + varPlanta
    # Añadir layer de PostGIS a QGIS
    uri = QgsDataSourceURI()
    # set host name, port, database name, username and password
    dbname = "sigua"
    host = "localhost"
    port = "5432"
    user = "postgres"
    password = "j3m"
    uri.setConnection(host, port, dbname, user, password)
    # set database schema, table name, geometry column and optionaly subset (WHERE clause)
    uri.setDataSource("public", planta, "geometria", "codigo like '"+varZZEEPP+"'")
    # Definir la vlayer de PostGIS
    vlayer = QgsVectorLayer(uri.uri(), varTocZZEEPP, "postgres")
    # Con esto añadimos la capa al TOC y se visualiza
    QgsMapLayerRegistry.instance().addMapLayer(vlayer)
    # Resultado de la creacion de la capa
    QMessageBox.information(None, "Resultados", "La capa " + varTocZZEEPP + " ha sido creada existosamente.")
