""" Event Mechanism """

class Event:
    ''' Some Private Property That Is Helping In Implementing An Event Based Mechanism'''
    __events: list = [str]
    __callbacks: dict = {}

    # Static Method For Register An Event And Its Appropriate Callbacks
    @staticmethod
    def on(event: str, callback):
        Event.__events.append(str)
        Event.__callbacks.update({
            event: callback
        })

        
    # Static Method For Executing And Passing Data To The Callbacked That Is Associated To An Certain Event
    @staticmethod
    def emmit(event: str, data = None):
        callback = Event.__callbacks.get(event)
        if callback is not None:
            if data is not None:
                callback(data)
            else:
                callback()
