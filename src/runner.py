import argparse
from validator import SchemaValidator

if __name__ == "__main__":
    args_to_parse = argparse.ArgumentParser()

    args_to_parse.add_argument(
        "json_path",
        help=(
            "The JSON path. A path to JSON formatted file containing events is expected."
            "E.g.: /data/events/website-events.json"
        ),
    )
    validator = SchemaValidator()
    path = args_to_parse.parse_args().json_path
    with open(path) as f:
        for event in f:
            validator.validate(event)
    validator.generate_report()
