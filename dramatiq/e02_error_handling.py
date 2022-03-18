import sys

import dramatiq
from dramatiq.brokers.redis import RedisBroker


dramatiq.set_broker(RedisBroker())


@dramatiq.actor
def unhandled(n: int):
    if n == 17:
        raise ValueError("17 always raises a ValueError")
    for i in range(n):
        print(i)


@dramatiq.actor
def handled(n: int):
    try:
        if n == 17:
            raise ValueError(17)
        for i in range(n):
            print(i)
    except ValueError as error:
        print(f"Message dropped due to bad value: {error.args[0]}")


if __name__ == "__main__":
    # CLI: python e02... <handled|unhandled> <n>
    if sys.argv[1] == "unhandled":
        sys.exit(unhandled.send(int(sys.argv[2])))
    elif sys.argv[1] == "handled":
        sys.exit(handled.send(int(sys.argv[2])))
