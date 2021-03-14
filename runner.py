from validator import SchemaValidator 
#from monitor import EventMonitor

if __name__ == "__main__":

    sv = SchemaValidator()
    #em = EventMonitor()
    with open("sample.json") as f:
        for event in f:
            sv.validate(event)
            #em.count(event)