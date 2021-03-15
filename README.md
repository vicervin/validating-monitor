# validating-monitor
A Python project for validating and monitoring events in JSON format. 

## Steps to run

1. Build the docker image for running the script, Run the following code in the repository's root path.


        docker build -t validating-monitor .

2. The following statement can be used for validating the events of a given JSON file, although the file will need to be mounted on the docker container. To do this, the path to the file should replace `INPUT_JSON_FILE`.

        docker run -v <INPUT_JSON_FILE>:/data/input.json validating-monitor python /src/runner.py /data/input.json
3. A report will be displayed at the enf for all of the events aggregated by date.
