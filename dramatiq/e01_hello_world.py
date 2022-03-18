import sys

import dramatiq
from dramatiq.brokers.redis import RedisBroker


dramatiq.set_broker(RedisBroker())


@dramatiq.actor
def count_to(n: int):
    for i in range(n):
        print(i)


if __name__ == "__main__":
    sys.exit(count_to.send(int(sys.argv[1])))
