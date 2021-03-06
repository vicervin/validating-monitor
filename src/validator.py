import json
import re
import logging
import pandas as pd
from dateutil.parser import parse

logger = logging.getLogger("Validation-log")
logging.basicConfig(level=logging.INFO)


class SchemaValidator:
    def __init__(self):
        self.id_pattern = re.compile(
            "[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12}$"
        )
        self.common_fields = [
            "received_at",
            "event",
            "sent_at",
            "original_timestamp",
            "anonymous_id",
            "context_device_model",
            "context_device_type",
            "context_network_carrier",
            "context_traits_taxfix_language",
            "context_locale",
            "event_text",
            "context_os_name",
            "id",
            "context_device_manufacturer",
            "context_network_wifi",
            "timestamp",
        ]

        self.time_fields = ["received_at", "sent_at", "timestamp", "original_timestamp"]
        self.id_fields = ["id", "anonymous_id"]
        self.event_fields = ["event", "event_text"]
        self.events_report = pd.DataFrame(
            {"Event": pd.Series([], dtype="str"), "Date": pd.Series([], dtype="str"),}
        )

    def is_ts_valid(self, ts_str):
        try:
            return parse(ts_str)
        except ValueError:
            pass
        return None

    def is_id_valid(self, id_str):
        return bool(self.id_pattern.match(id_str))

    def validate_json(self, str_json):
        try:
            dict_json = json.loads(str_json)
            return dict_json
        except json.decoder.JSONDecodeError:
            return False

    def update_report(self, event_dict):
        event_name = event_dict.get("event", "N/A")
        timestamp = event_dict.get("original_timestamp")
        datetime = self.is_ts_valid(timestamp)
        date = datetime.date() if datetime else "N/A"
        self.events_report = self.events_report.append(
            {"Event": event_name, "Date": date}, ignore_index=True
        )

    def validate(self, event_str):

        event_dict = self.validate_json(event_str)
        if not event_dict:
            logger.error("Event data was not in a valid JSON format")
            return

        missing_fields = set(self.common_fields) - set(event_dict.keys())
        empty_fields = []
        mismatched_fields = []
        key_fields = set(self.common_fields).intersection(set(event_dict.keys()))
        for field in key_fields:
            value = event_dict[field]
            if value == None or value == "":
                empty_fields.append(field)
            if field in self.id_fields and not self.is_id_valid(value):
                mismatched_fields.append(field)
            if field in self.time_fields and not self.is_ts_valid(value):
                mismatched_fields.append(field)

        self.update_report(event_dict)

        validation_log = {}

        if missing_fields:
            validation_log["Missing Fields"] = list(missing_fields)

        if mismatched_fields:
            validation_log["Mismatched Fields"] = mismatched_fields

        if empty_fields:
            validation_log["Empty Fields"] = empty_fields

        if validation_log:
            logger.warning(
                (
                    f"Schema mismatch from ({event_dict.get('event')}) "
                    f"with ID ({event_dict.get('id')}) : \n {str(validation_log)}"
                )
            )

    def generate_report(self):
        final_report = (
            self.events_report[["Event", "Date"]].value_counts().to_frame("Count")
        )
        logger.info("\n\nEvents Report: \n" + final_report.to_string())
        final_report.to_csv("report.csv")
