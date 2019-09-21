# README

## Description
This is simple HTTP REST server, that can load RAM memory and CPU.
It is written in ```Python 3```.

The directory ```/tmp``` should be mounted in RAM using TMPFS for correct working.
The home directory of user that executes server should contains [CPULoadGenerator](https://github.com/GaetanoCarlucci/CPULoadGenerator) utility.

By default, server uses ```HTTP``` port ```8888```.


## Content of repository
This repository contains following files:

- ```README.md``` - this file with general description;
- ```.gitignore``` - wildcard of files, that will not save in repository;
- ```loadup.py``` - main file, that start server;
- ```restserver.py``` - module with main handlers of work logic;
- ```codes.py``` - module with codes of error and error messages;
- ```html/index.html``` - dummy HTML page;
- ```img/favicon.ico``` - favicon icon;
- ```css/``` - empty directory;
- ```js/``` - empty director.


## Dependencies
There is dependency ```Python 3``` package for server:

 - ```tornado```

There are 3 dependencies ```Python 3``` packages for [CPULoadGenerator](https://github.com/GaetanoCarlucci/CPULoadGenerator):

 - ```matplotlib```
 - ```psutil```
 - ```twisted```


## Run
Interpret file ```loadup.py``` without arguments using ```python3```:
```
python3 loadup.py
```


## REST API

Commands list with arguments:

 - ```load_mem``` - load RAM memory;
   - ```size``` - size of loadable memory (in kilo, mega or giga);
   - ```modifier``` - modifer letter of size: K, M and G for kilo, mega or giga respectively.
 - ```clear_mem``` - clear loaded memory;
 - ```load_cpu``` -  loaded one of the CPU cores;
    - ```cpu_number``` - number of loaded CPU;
    - ```percentage``` - percentage of loading as float (more then 0, less then 1);
    - ```time``` - time of loading in seconds.

Send command as ```POST``` request to ```http://IP:8888``` using ```JSON``` serialization.


## REST API Examples

#### load_mem

###### REQUEST

```
{
    "command": "load_mem",
    "args": {
        "size":100,
        "modifier":"M"
    }
}
```

###### RESPONSE

```
{
    "command": "load_mem",
    "error": "",
    "error_code": 0,
    "args": null
}
```

#### clear_mem

###### REQUEST

```
{
    "command": "clear_mem",
    "args": {}
}
```

###### RESPONSE

```
{
    "command": "clear_mem",
    "error": "",
    "error_code": 0,
    "args": null
}
```

#### load_cpu

###### REQUEST

```
{
    "command": "load_cpu",
    "args": {
        "cpu_number":0,
        "percentage":0.6,
        "time":3
    }
}
```

###### RESPONSE

```
{
    "command": "load_cpu",
    "error": "",
    "error_code": 0,
    "args": null
}
```


### Errors
List of error messages:

| name | code | eng message |
|:-----:|:-----:|:-----:|
| NO_ERROR | 0 | |
| MISS_ARG | 1 | Missing argument |
| INVALID_ARG | 2 | Invalid argumnet or its type |
| INVALID_COMMAND | 3 | Don't exist command with this name |
