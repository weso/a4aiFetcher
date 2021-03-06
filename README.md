# a4aiFetcher
Python module that will parse the data for the A4AI 2014 Affordability Index

## Environements
This code has been tested for the next Python versions:
- Python 2.7

## Installation

**Dependences:**
- xlrd


**Integration with a4aidom repository:**

a4aiFetcher uses code of a4aidom: model objects, utilities, communication with MongoDB… When cloning the a4aiFetcher repository, the root should be placed within the structure of an a4aidom repository package tree, in the path:
*/a4aidom/application/a4aiFetcher*


 **Execution**
 
 If you want to execute a4aiFetcher from console, move to the path:
*{parent_directory_of_root}/a4aidom/application/a4aiFetcher*

Then, execute:
`python main.py`

a4aiFetcher depends on certain files, specified through configuration using relative paths. If you want to execute this module from a different execution point, you should:
- Modify the configuration.ini file, turning every relative path into an absolute one, or relative to the new execution point.
- Execute main.py using `python –m`.

**Expected result**

a4aiFetcher parses the information of several local files (xsl and json) and a REST API, and persist it in a database. The current implementation works with MongoDB and uses the source info to feed three different mongo collections with documents:
- areas: documents about countries and continents.
- indicators: documents of metadata of each a4ai indicatros.
- observations: pieces of information that links a value with certain area, date and indicator.

An example of the resulting state of those collections after a succesfull execution of a4aiFetcher can be found in [sample\_files/output](https://github.com/weso/a4aiFetcher/tree/develop/sample_files/output).

## Modules of a4aiFetcher
main.py launches the execution of different tasks, each one encapsuled in a single method that relies in a differenced internal module.

### Parsing process 
Method `parse()` in `main.run()`. It parses the information represented in an xsl file about indicators and observations. It will read the data, transform it into internal model objects and finally introduce them in the database. 
The code is expects to find a MongoDB instance deployed in localhost:27017. IP and port can be configured modifying the file *a4aidom/infrastructure/mongo_repos/config.py*
Different parsing sub-processes are invoked when executing the `parse()` method. Each process cannot be activated/unactivated through configuration, but by commenting internal lines in the `parse()` method.


- IndicatorParser: it will introduce metadata about indicators in the the database (collection "indicators"). It expects to find that collection empty when it begins. If not, there will not be an error executing this process, but indicators will be duplicated, causing problems to other modules.
- SecondaryObservationParser: it will introduce secondary observations in the database (collection "observations). It does not check if the data already exists when persisting an observation. I.e., if Mongo already contains an observation for certain indicator and certain date, it will be duplicated. It expects to work with a repository with the collections "areas" and "indicators" full of data.
- PrimaryObservationParser: it will introduce primary observations in the database (collection "observations"). Conditions about collections and duplicates are the same of the previous case.
- GroupedObservationParser: it will introduce grouped observations (collection "observations"). Conditions about collections and duplicates are the same of the previous case.

### Ranking process 
It divides all the observations in the database in groups of objects with the same date and year. Then, it will sort all the values within each group, actualizing each observation in the database with the rank position in its group. It expects to work with a repository full of observations.

### Enrichment process
It will update items of the “areas” collection, adding information about some special indicators.

#### WorldBank indicators 
The information is obtained querying a REST API: *http://api.worldbank.org/*. Errors in this module can probably be caused by changes in that API. The indicators tracked can be modified through editing the filed `WB\_INDICATOR\_CODES` of the file configuration.ini placed at the root of the project.

#### ITU indicators 
The information is obtained parsing some local JSON files with identical structure.  [Sample files](https://github.com/weso/a4aiFetcher/tree/develop/sample_files/input) are included in this documentation. Those files provide observations that are going to be included in objects of the "areas" collection. However, the date of those observations is not included in the files. All of them are persisted in teh database with the value ITU\_DATA\_YEAR specified in configuration.ini

### Preconditions summary
Depending on the processes launched, the previous state of the database should be different in order to reach a correct and complete result. Combinations:

- Areas: there is no module parsing data of countries. The "areas" collection should ALWAYS be full of data in the database before the execution.
- Enrichment: the enrichment process expect to find areas in the database, but it has nothing to do with the rest of collections (observations, indicators).
- Indicators + Observations + Ranking: There should be areas in the database, but there should not be indicators. Regarding observations, only old items (observations with a date different from the data that are being parsed) can be in the database.
- Observations + Ranking: There should be complete areas and indicators in the database. Regarding observations, only old ones can be in the database.
- Ranking: All the areas, indicators and observations should be already in the database.

## Importation/exportation of data to mongo
Command to import a collection in MongoDB:
`mongoimport --db a4ai --collection {collection\_name} --file {path\_to\_json\_file}`
Command to export a collection from MongoDB:
`mongoexport  --db a4ai --collection {collection\_name} --out {path\_to\_json\_file}`
With these commands, three different orders should be executed in a raw to import all the collections, one per each collection (areas, indicators, observations). 
There is an alternative couple of commands handy for this purpose that can handle every collection of the database with a single order: mongodump and mongorestore. However, the database dumps that we have been produced were produced with `mongoexport` commands.


##Local files

###Excell with observations
[Sample here](https://github.com/weso/a4aiFetcher/blob/develop/sample_files/input/data.xlsx). This excell file should contain all the parseable information about indicators and observations. Future executions should fit in the structure of the sheets of the sample file: location of IDs, location and name of countries, locations questions, data location… 
The main sheets are:
- For grouped observations: “Primary & Secondary”. Relative position sheet: 3rd.
- For primary observations: “Survey scores and clusters”. Relative position sheet: 4th.
- For secondary observations: “Inputed Secondary Data”. Relative position sheet: 6th.

The content of the rest of sheets in the xsl file do not have influence in the parsing process.

There are many parsing aspects configurable through editing the file configuration.ini placed in the root of the project: relative position of target sheets, initial row/column of data… however, to avoid unnecessary problems, probably the best idea is trying to fit the new data with the current structure.

### ITU special indicators
[Samples here](https://github.com/weso/a4aiFetcher/tree/develop/sample_files/input). ITU special indicators to enrich “areas” collection are taken from several json files. The name, location and quantity of those files could be changed by editing the filed ITU_FILE_NAMES of configuration.ini file. However, the structure of the json files should be always coherent with the structure of the sample files.


##Issues##
###Areas###
There is no module parsing data areas, so that collection should be reused in future data importations.

###Indicators###
The data sheet used in the last execution of the data importer does not include matadata of indicators, so the old indicator collection had been used.

###Dates###
The fetcher works assuming that all the parsed data is related to the same date. In fact, there is no “date” field in the original excel containing the data to be parsed. The date of the new observations introduced in the database is currently hardcoded in a4aiFetcher/parsing/utils and should be modified in future executions.

