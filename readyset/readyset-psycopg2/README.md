# Folder Description
This folder contains the code for the readyset-psycopg2 package.

# Program Description
The program offers two prototypes to query data from a PostgreSQL database.

## Prototype 1
The `app.py` file contains the code for the first prototype. This prototype uses the ReadySet caching server to query data from a PostgreSQL database.

## Prototype 2
The `direct_access.py` file contains the code for the second prototype. This prototype directly queries data from a PostgreSQL database.

# Main File
The `main.py` file runs both prototypes and compares the results. This file takes an input from the `query.txt` file and runs the query on both prototypes. The results are stored in the `results.txt` file.

Then, the file compares and prints the results to the console. The plot is also provided as `plot.png`.