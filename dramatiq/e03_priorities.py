import sys
import threading
import time

import dramatiq
from dramatiq.brokers.redis import RedisBroker


dramatiq.set_broker(RedisBroker())


# dramatiq-recommended best practice: Use priority constants.
HIGH_PRIORITY = 1
LOW_PRIORITY = 100


@dramatiq.actor(priority=HIGH_PRIORITY)
def greet_customer(name: str):
    print(
        "*" * len(f"Hello, {name}!")
        + f"\nHello, {name}!\n"
        + "*" * len(f"Hello, {name}!")
    )


@dramatiq.actor(priority=LOW_PRIORITY)
def do_nothing(message: int):
    print(f"{threading.current_thread().name}: Message {message}: Sleeping")
    time.sleep(1)


if __name__ == "__main__":
    try:
        if sys.argv[1] == "greet":
            sys.exit(greet_customer.send(sys.argv[2]))
        elif sys.argv[1] == "sleep":
            sys.exit(do_nothing.send())
        elif sys.argv[1] == "auto":
            for i in range(100):
                do_nothing.send(i)
            greet_customer.send("User")
            sys.exit(0)
    except IndexError:
        pass

    print("Either use 'auto', 'sleep', or use 'greet' with a name.")
    sys.exit(1)
