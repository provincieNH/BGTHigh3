# Conversie repository

## setting up your local development

To set up your local development, first set up a virtual environment.

``` sh
cd /BGTHigh3/conversie
python3 -m venv conversie
. conversie/bin/activate
pip install -r requirements.txt
chmod +x /uploadexecutable/runtime/runEtl
```

## to install gdal follow the following guidelines

See this site: https://ljvmiranda921.github.io/notebook/2019/04/13/install-gdal/

``` sh
pip3 install --global-option=build_ext --global-option="-I/usr/include/gdal" GDAL==`gdal-config --version`
```

## Running the ETL locally
To run store your zipped files in the `/resources` directory.

Finally execute:

``` sh
./uploadexecutable/runtime/runEtl
```
This script will execute the python script in your local directory. Making sure that all the API-tokens are formulated correctly.

The data will be generated in the `/output` as .nt files.
