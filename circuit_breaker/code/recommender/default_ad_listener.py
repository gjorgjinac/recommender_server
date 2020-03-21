import pybreaker

class DefaultListener(pybreaker.CircuitBreakerListener):
    "Listener used by circuit breakers that execute database operations."

    def before_call(self, cb, func, *args, **kwargs):
        "Called before the circuit breaker `cb` calls `func`."
        print('before_call')
        pass

    def state_change(self, cb, old_state, new_state):
        "Called when the circuit breaker `cb` state changes."
        msg = "State Change: Old state: {0}, New State: {1}".format(old_state, new_state)
        print(msg)
        pass

    def failure(self, cb, exc):
        "Called when a function invocation raises a system error."
        print('failure')
        pass

    def success(self, cb):
        "Called when a function invocation succeeds."
        print('success')
        pass