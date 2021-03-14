from validator import SchemaValidator 

if __name__ == "__main__":

    sv = SchemaValidator()
    with open("sample.json") as f:
        for event in f:
            sv.validate(event)
    sv.generate_report()