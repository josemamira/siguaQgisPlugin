from SiguaPlugin import SiguaPlugin
def name():
  return "SIGUA plugin"
def description():
  return "Cargar edificios de SIGUA."
def version():
  return "Version 0.1"
def plugin_type():
  return QgisPlugin.UI # UI plugin
def classFactory(iface):
  return SiguaPlugin(iface)
