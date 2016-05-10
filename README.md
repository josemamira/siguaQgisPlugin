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
Copy entire folder into Qgis plugin repository
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


### Repository

Sources are in public Github repository: https://github.com/josemamira/siguaQgisPlugin
```sh
$ git clone [git-repo-url] siguaQgis
$ copy siguaQgis /home/<username>/.qgis2/python/plugins
```


