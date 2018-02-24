# [promiedos.com.ar](http://promiedos.com.ar) scrapper

## Instalación

Este repo está pensando para ser usado con `python 3.6.3`, `pip` y `virtualenv`. 

Proceso de instalación:

```bash
$ git clone git@github.com:iheredia/promiedos-scrapper.git
$ cd promiedos-scrapper
# crear virtualenv: 
$ virtualenv -p python3 venv
# activar virtualenv:  
$ . venv/bin/activate
# instalar dependencias 
$ pip install -r requirements.txt 

```

## Estructura del repo 

El scrapper consta de 2 partes. 
- La primera consta del archivo `./scrapper/spider.py` el cual está basado en [scrappy](https://scrapy.org/) y se encarga de navegar el sitio de promiedos y de extraer datos crudos, guardandolos en la carpeta `./tmp`.
- La segunda parte está compuesta por `./scrapper/parser.py` y `./scrapper/match.py`. Estos scripts interpretan la información cruda del sitio y vuelcan el resultado en la carpeta `data`.

```
.
├── data                    # Archivos json con el resultado de la ejecución del scrapper
├── scrapper                # Scripts de python
│   ├── __init__.py
│   ├── helpers.py          # Rutinas comunes para el proyecto
│   ├── match.py            # Clase que representa un partido 
│   ├── parser.py           # Parser que se encarga de interpretar la data cruda e instanciar 
│   │                       # las clases de los partidos
│   └── spider.py           # Spider de scrappy para navegar el stiio
├── .gitignore
├── LICENSE
├── main.py                 # Script principal para ejecutar el scrapper
├-─ README.md
└── requirements.txt        # Dependencias del proyecto
```

## Ejecución

Una vez instaladas las dependencias, ejecutar alguna de las siguientes alternativas
 
```bash
# Para ejecutar el proceso entero (spider + parser):
$ python main.py 

# Para ejecutar solo el spider de scrappy y obtener una copia de los datos crudos
# en la carpeta tmp:
$ python main.py --only-spider

# Para ejectuar solo el parser y obtener los datos finales en la carpeta data 
# (es necesario contar con data cruta en la carpeta tmp):  
$ python main.py --only-parser 
```
