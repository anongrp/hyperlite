""" Event Mechanism """

class Event:

    '''   Initialization of default Event Object.   '''
    def __init__(self):
        self.events: list = []
        self.callbacks: dict = {}                      # Dictionary of lists   ''' callback, data = [0,1]  '''

    # Method For Register An Event And Its Appropriate Callbacks
    def on(self, event: str, callback):
        self.events.append(event)
        self.callbacks.update({
            event: callback
        })

        
    # Method For Executing And Passing Data To The Callbacked That Is Associated To An Certain Event
    def emmit(self, event: str):
        callback = self.callbacks.get(event)[0]
        data = self.callbacks.get(event)[1]
        if callback is not None:
            if data is not None:
                callback(data)
            else:
                callback()
