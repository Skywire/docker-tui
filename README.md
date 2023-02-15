# Docker TUI 

A terminal user interface for managing Docker

## Install

* Download the release package for your system from the [releases page](https://github.com/Skywire/docker-tui/releases)
* Extract the tar.gz and open the directory in a terminal
```
sudo chmod +x bin/docker-tui
sudo mv bin/docker-tui /usr/local/bin/
```

## Configuration

The config file will be created in `~/.docker-tui/.config.yml` on the first application run

Options are:
    
* project_home - The default path for your project directories, this will be used by the project finder screen, leave blank to keep it as your home directory
