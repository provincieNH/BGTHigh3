# Conversie repository

## Setting up your local development 
### Linux

To set up your local development, first set up a virtual environment.

``` sh
cd /BGTHigh3/conversie
python3 -m venv conversie
. conversie/bin/activate
pip install -r requirements.txt
chmod +x /uploadexecutable/runtime/runEtl
```

#### Windows

``` 
cd BGTHigh3\conversie
python -m venv conversie
cd conversie\scripts\activate
pip install -r D:\BGTHigh3\conversie\requirements.txt
chmod +x /uploadexecutable/runtime/runEtl
```


## To install gdal follow the following guidelines
#### Linux
See this site: https://ljvmiranda921.github.io/notebook/2019/04/13/install-gdal/

``` sh
pip3 install --global-option=build_ext --global-option="-I/usr/include/gdal" GDAL==`gdal-config --version`
```
#### Windows

https://pythongisandstuff.wordpress.com/2016/04/13/installing-gdal-ogr-for-python-on-windows/

## Running the ETL locally

To run store your zipped GML file in the `/resources` directory. At the moment this script will only convert a zip file with GML's.

Finally execute:

``` sh
./uploadexecutable/runtime/runEtl
```
This script will execute the python script in your local directory. Making sure that all the API-tokens are formulated correctly.

The data will be generated in the `/output` as .nt files.
A zip file will be generated in `/outputZipped` as .zip file
