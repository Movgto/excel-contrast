from typing import Callable

class Subscription:
    _cb: Callable        

    def __init__(self, cb: Callable):
        self._cb = cb
    
    def run(self):
        self._cb()

class Signal[T]:
    _value: T
    _subscriptions: list[Subscription] = []

    def __init__(self, value: T):
        self._value = value

    def _notify(self):
        for sub in self._subscriptions:
            sub.run()
    
    def subscribe(self, cb: Callable):
        subs = Subscription(cb)
        self._subscriptions.append(subs)

        return subs

    def unsubscribe(self, subs: Subscription):
        self._subscriptions.remove(subs)

    def get(self): return self._value

    def set(self, new_value: T):
        self._value = new_value
        self._notify() 
