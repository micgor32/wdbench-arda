# WDBench-ARDA
This repo contains scripts that we used to recreate [WDBench benchmark](https://github.com/MillenniumDB/WDBench), as well as the results that we gathered.
The benchmark was performed on AWS instances of following specification: ![image](https://github.com/micgor32/wdbench-arda/assets/111281585/18385157-841c-42c5-a1ec-e2a630ca0890)

## Data import
Here you may find the instructions how we imported the data to both tested databases. The Wikidata data that we used may be found [here](https://figshare.com/s/50b7544ad6b1f51de060)

### Setup Neo4j
This part assumes you are connected to the AWS instance with at least 24GB of RAM and 350GB of free disk space. Some of the commands may require root access if you are using Amazon Linux as we did.
#### 1. Download Neo4J

- Download [Neo4J community edition](https://dist.neo4j.org/neo4j-community-4.3.5-unix.tar.gz). We used the version 4.3.5, same that was used in the original run.
- Extract the downloaded file
  - `tar -xf neo4j-community-4.*.*-unix.tar.gz`
- Enter to the folder:
  - `cd neo4j-community-4.*.*/`
- Set the variable `$NEO4J_HOME` pointing to the Neo4J folder.

#### 2. Edit configuration file

Edit the text file `conf/neo4j.conf`

- Set `dbms.default_database=wikidata`
- Uncomment the line `dbms.security.auth_enabled=false`
- Add the line `dbms.transaction.timeout=10m`

#### 3. Convert .nt to .csv files

Use the script [nt_to_neo4j.py](https://github.com/MillenniumDB/WDBench/DatabaseGeneration/nt_to_neo4j.py) to generate the .csv files `entities.csv`, `literals.csv` and `edges.csv`

#### 4. Bulk import and index

Execute the data import

```
bin/neo4j-admin import --database wikidata \
 --nodes=Entity=wikidata_csv/entities.csv \
 --nodes wikidata_csv/literals.csv \
 --relationships wikidata_csv/edges.csv \
 --delimiter "," --array-delimiter ";" --skip-bad-relationships true
```


Now we have to create the index for entities:

- Start the server: `bin/neo4j console`
- Open the cypher console (in another terminal):
  - `bin/cypher-shell`, and inside the console run the command:
    - `CREATE INDEX ON :Entity(id);`
    - Even though the above command returns immediately, you have to wait until is finished before interrupting the server. You can see the status of the index with the command `SHOW INDEXES;`.

### Setup Blazegraph
### 1. Split .nt file into smaller files

Blazegraph can't load big files in a reasonable time, so we need to split the .nt into smaller files (1M each)

- `mkdir splitted_nt`
- `cd splitted_nt`
- `split -l 1000000 -a 4 -d --additional-suffix=.nt [path_to_nt]`
- `cd ..`

### 2. Clone the Git repository and build

- `git clone --recurse-submodules https://gerrit.wikimedia.org/r/wikidata/query/rdf wikidata-query-rdf`
- `cd wikidata-query-rdf`
- `mvn package`
- `cd dist/target`
- `tar xvzf service-*-dist.tar.gz`
- `cd service-*/`
- `mkdir logs`

### 3. Edit the default script

- Edit the script file `runBlazegraph.sh`.
  - configure main memory here: `HEAP_SIZE=${HEAP_SIZE:-"64g"}` (You may use other value depending on how much RAM your machine has)
  - set the log folder `LOG_DIR=${LOG_DIR:-"/path/to/logs"}`, replace `/path/to/logs` with the absolute path of the `logs` dir you created in the previous step.
  - add `-Dorg.wikidata.query.rdf.tool.rdf.RdfRepository.timeout=60` to the `exec java` command to specify the timeout (value is in seconds).
  - also change `-Dcom.bigdata.rdf.sparql.ast.QueryHints.analyticMaxMemoryPerQuery=0` which removes per-query memory limits.

### 4. Load the splitted data

- Start the server: `./runBlazegraph.sh`
  - This process won't end until you interrupt it (Ctrl+C). Let this execute until the import ends. Run the next command in another terminal.
- Start the import: `./loadRestAPI.sh -n wdq -d [path_of_splitted_nt_folder]`
This step may take a while, on AWS instance that we used, it took around 4 days to finish.
