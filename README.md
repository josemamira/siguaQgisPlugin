# siguaQgisPlugin
This Qgis plugin provide functionality to load vector layer building from University of Alicante (UA). You can also:

  - Get a legend ready to print. Two options are provider: landuse or departments 
  - Get labels from room code 
  - Print to PDF file using predefined templates with automatic align (horizontal/vertical) 

### Version
0.1

### Author
* José Manuel Mira Martínez - Laboratorio de Geomática (UA)

### Installation
Copy entire folder SiguaPlugin in your Qgis plugin repository
* Linux: /home/<username>/.qgis2/python/plugins
* Windows: C:\users\<username>\.qgis2\python\plugins
> This folders are hidden

Create a python file named dbsettings.py with this content

```sh
#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.0.0'
VERSION = tuple(map(int, __version__.split('.')))

# Edit this line to set your PostgreSQL connection
params = ['<your host>', "5432",'<your database>', '<username>', '<password>']
```
### Development

* 1. Copy the entire directory containing your new plugin to the QGIS plugin directory
* 2. Compile the ui file using pyuic4
* 3. Compile the resources file using pyrcc4
* 4. Test the plugin by enabling it in the QGIS plugin manager
* 5. Customize it by editing the implementation file "sigua_plugin.py"
* 6. Create your own custom icon, replacing the default "icon.png"
* 7. Modify your user interface by opening "sigua_plugin_dialog_base.ui" in Qt Designer (don't forget to compile it with pyuic4 after changing it)
* 8. You can use the Makefile to compile your Ui and resource files when you make changes. This requires GNU make (gmake) 

### Repository

Sources are in public Github repository: https://github.com/josemamira/siguaQgisPlugin
```sh
$ git clone [git-repo-url] siguaQgis
$ copy siguaQgis /home/<username>/.qgis2/python/plugins
```


