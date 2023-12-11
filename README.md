# WDBench-ARDA
This repo contains scripts that we used to recreate [WDBench benchmark](https://github.com/MillenniumDB/WDBench), as well as the results that we gathered.
The benchmark was performed on AWS instances of following specification: ![image](https://github.com/micgor32/wdbench-arda/assets/111281585/18385157-841c-42c5-a1ec-e2a630ca0890)

## Data import
Here you may find the instructions how we imported the data to both tested databases.

### Setup Neo4j
#### 1. Download Neo4J

- Download [Neo4J community edition](https://dist.neo4j.org/neo4j-community-4.3.5-unix.tar.gz). We used the version 4.3.5, same that was used in the original run.
- Extract the downloaded file
  - `tar -xf neo4j-community-4.*.*-unix.tar.gz`
- Enter to the folder:
  - `cd neo4j-community-4.*.*/`
- Set the variable `$NEO4J_HOME` pointing to the Neo4J folder.

### 2. Edit configuration file

Edit the text file `conf/neo4j.conf`

- Set `dbms.default_database=wikidata`
- Uncomment the line `dbms.security.auth_enabled=false`
- Add the line `dbms.transaction.timeout=10m`

### 3. Convert .nt to .csv files

Use the script [nt_to_neo4j.py](https://github.com/MillenniumDB/WDBench/DatabaseGeneration/nt_to_neo4j.py) to generate the .csv files `entities.csv`, `literals.csv` and `edges.csv`

### 4. Bulk import and index

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
