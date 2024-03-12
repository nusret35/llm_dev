import json

class Message:
    def __init__(self,data):
        self.data = data

class SetMessage(Message):
    def __str__(self):
        return(json.dumps({"type":"setMesssage", "message":self.data}))

class AllProcessess(Message):
    def __str__(self):
        return(json.dumps({"type":"allProcesses","message":self.data}))

class Process(Message):
    def __str__(self):
        return(json.dumps({"type":"process","message":self.data}))


class ProcessCompleted(Message):
    def __str__(self):
        return(json.dumps({"type":"processCompleted","message":self.data}))

class ReportCompleted(Message):
    def __str__(self):
        return(json.dumps({"type":"reportCompleted", "message":self.data}))

class ErrorMessage(Message):
    def __str__(self):
        return(json.dumps({"type":"error", "message":self.data}))
