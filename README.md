# Opengrok workspace manager
Wrapper to easily create and manage [OpenGrok](https://github.com/oracle/opengrok) workspaces along with their deployment and the addition/removal of their associated projects.

## Terminology

### Workspace
Holds a set of projects, searches can me done on a whole workspace across all the different projects associated to it. A workspace effectively represent one deployment of the OpenGrok web app on your web server and is therefore accessible from the following URL:

```
http://localhost:8080/your-workspace
```

### Project
Projects are ultimately what holds the source code, they can be added or removed on an invidiual basis without having to re-index all the projects in the workspace.

## Setup
### Arch linux
This repository holds an AUR build script you can use to automatically install everything that is needed:
``` shell
makepkg -s
sudo pacman -U opengrok-x.x.x.-x-any.pkg.tar.zst
```
You'll still need to manually add yourself to the tomcat10 user group in order to deply workspaces:
``` shell
sudo gpasswd -a yourself tomcat10
```

### Other distributions
You will need to install:
* Java 11 or higher
* [OpenGrok](https://github.com/oracle/opengrok) under `/usr/share/java/opengrok`
* A servlet container like [GlassFish](https://glassfish.org/) or [Tomcat](http://tomcat.apache.org/) 10.0 or later

You'll also need to have write access to your servlet container deployment directory in order to be able to deploy workspaces.

## Usage
Create and initialise you workspace:

``` shell
mkdir -p ~/opengrok/your-workspace
cd ~/opengrok/your-workspace
opengrokw  init
```

Add a project to your workspace and restart your servlet container to reflect the changes:
``` shell
opengrokw add ~/some-directory/your-project
sudo systemctl restart tomcat10
xdg-open http://localhost:8080/your-workspace
```

List all the projects in your workspace:
``` shell
opengrokw list
``` 

Remove a project from your workspace and restart your servlet container to reflect the changes
``` shell
opengrokw remove your-project
sudo systemctl restart tomcat10
```

## License
This software is licensed under the [MIT license](LICENSE)

Copyright &#169; 2021 All rights reserved. XdevL
