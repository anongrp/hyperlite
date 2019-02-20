""" Event Mechanism """


class Event:
    """   Initialization of default Event Object.   """
    events: list = []
    callbacks: dict = {}

    # Method For Register An Event And Its Appropriate Callbacks
    @staticmethod
    def on(event: str, callback):
        Event.events.append(event)
        Event.callbacks.update({
            event: callback
        })

    @staticmethod
    def off(event: str):
        Event.events.pop(Event.events.index(event))

    # Method For Executing And Passing Data To The Callbacked That Is Associated To An Certain Event
    @staticmethod
    def emmit(event: str, data=None):
        callback = Event.callbacks.get(event)
        if callback is not None:
            if data is not None:
                callback(data)
            else:
                callback()



if __name__ == '__main__':
    input = int(input("Hey enter some key : "))
    print()
    onKeyPressed = lambda key: print(f"Hey you entered {key}")
    Event.on("on1Pressed", onKeyPressed)
    Event.on("on2Pressed", onKeyPressed)
    Event.on("on3Pressed", onKeyPressed)
    Event.on("on4Pressed", onKeyPressed)
    Event.on("on5Pressed", onKeyPressed)

    if (input == 1):
        Event.emmit("on1Pressed", 1)
    if (input == 2):
        Event.emmit("on2Pressed", 2)
    if (input == 3):
        Event.emmit("on3Pressed", 3)
    if (input == 4):
        Event.emmit("on4Pressed", 4)
    if (input == 5):
        Event.emmit("on5Pressed", 5)
