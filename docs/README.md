# simpledb
SimpleDB is developed by Edward Sciore.

http://www.cs.bc.edu/~sciore/simpledb (This page is unavailable now as Prof. Sciore is retired.)

## Quick Start

### start the server

```bash
java -cp build/libs/simpledb-3.3.jar simpledb.server.Startup studentdb
```

### seed database

```bash
java -cp build/libs/simpledb-3.3.jar;build/classes/java/test  studentClient.simpledb.CreateStudentDB
```

### query records

```bash
java -cp build/libs/simpledb-3.3.jar;build/classes/java/test  studentClient.simpledb.FindMajors math
```

## Roadmap

