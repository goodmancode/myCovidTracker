class State:
    name = None
    metrics = None

    def __init__(self, name, metrics):
        self.name = name
        self.metrics = metrics

    def get_name(self):
        return self.name

    def get_metrics(self):
        return self.metrics