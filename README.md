# Opengrok workspace manager
Wrapper to easily create and manage opengrok workspaces along with their deployment and the addition/removal of their modules.

# Overview
```
usage: opengrokw.py [-h] [--opengrokdir OPENGROKDIR] {init,index,add,remove,list} ...
```

Opengrok workspace manager

positional arguments:
  {init,index,add,remove,list}

optional arguments:
  -h, --help            show this help message and exit
  --opengrokdir OPENGROKDIR
                        Opengrok workspace directory. If none, the working
                        directory will be used.

```
usage: opengrokw.py init [--webappsdir WEBAPPSDIR] [--name NAME]
```

Initialise and deploy a new opengrok workspace.

optional arguments:
  --webappsdir WEBAPPSDIR
                        Directory into which deploy the webapp associated to
                        the opengrok workspace.
  --name NAME           Name used to access the opengrok workspace from the
                        webserver.

```
usage: opengrokw.py index [module [module ...]]
```

Index the opengrok workspace.

positional arguments:
  module  A list of module to index. If none all modules will be indexed.

```
usage: opengrokw.py add [--name NAME] path
```

Add a new module to the opengrok workspace.

positional arguments:
  path         The path of the module sources used for indexing.

optional arguments:
  --name NAME  Name of the module. If none, the module sources directory name
               will be used.

```
usage: opengrokw.py remove [module [module ...]]
```

Remove module(s) from the opengrok workspace.

positional arguments:
  module  Module to remove from the opengrok workspace. If none, the whole
          workspace will be deleted and undeployed (requires confirmation)

```
usage: opengrokw.py list
```

List the opengrok worspace modules.

NOTE: most of those commands will require a web server restart in order to take effect.
