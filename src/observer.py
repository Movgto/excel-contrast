from typing import Callable, Any

class Subscription:
    _cb: Callable
    _obs: Any = None

    def __init__(self, cb: Callable):
        self._cb = cb
    
    def run(self):
        self._cb(self._obs.get())

class Signal[T]:
    _value: T
    _subscriptions: list[Subscription] = []

    def __init__(self, value: T):
        self._value = value

    def _notify(self):
        for sub in self._subscriptions:
            sub.run()
    
    def subscribe(self, cb: Callable[[T], Any]):
        subs = Subscription(cb)
        subs._obs = self
        self._subscriptions.append(subs)

        return subs

    def unsubscribe(self, subs: Subscription):
        self._subscriptions.remove(subs)

    def get(self): return self._value

    def set(self, new_value: T):
        self._value = new_value
        self._notify() 
