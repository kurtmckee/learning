# Test performance of writing a CSV file with a dataclass.
#
# Sample output:
#
#     Building database of 300000 instances...done
#     Implementation 1: 1.86 seconds
#     Implementation 2: 1.96 seconds
#     Implementation 3: 2.02 seconds
#     Implementation 4: 0.79 seconds
#
# Lessons learned:
#
# The performance bottleneck happens because of calls to `dataclasses.asdict()`.
# If this is eliminated, then the performance increases significantly.
#

import csv
import dataclasses
import io
import itertools
import sys
import timeit


@dataclasses.dataclass
class Instance:
    v1: str
    v2: str
    v3: str
    flag: bool = False


strings = itertools.cycle("abcdefghijklmnopqrstuvwxyz")
bools = itertools.cycle((True, False))


def implementation_1(instances: list[Instance]):
    """This is the original implementation."""

    with open(f"instances.csv", "w") as f:
        fieldnames = [field.name for field in dataclasses.fields(Instance)]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        for instance in instances:
            writer.writerow(dataclasses.asdict(instance))


def implementation_2(instances: list[Instance]):
    """Write to memory, then dump to a file."""

    stream = io.StringIO()
    fieldnames = [field.name for field in dataclasses.fields(Instance)]
    writer = csv.DictWriter(stream, fieldnames=fieldnames)
    writer.writeheader()
    for instance in instances:
        writer.writerow(dataclasses.asdict(instance))

    stream.seek(0)
    with open(f"instances.csv", "w") as f:
        f.write(stream.read())


def implementation_3(instances: list[Instance]):
    """Call `.writerows()` instead of `.writerow()`."""

    with open(f"instances.csv", "w") as f:
        fieldnames = [field.name for field in dataclasses.fields(Instance)]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataclasses.asdict(instance) for instance in instances)


def implementation_4(instances: list[Instance]):
    """Avoid calls to `dataclasses.asdict()`."""

    with open(f"instances.csv", "w") as f:
        fieldnames = [field.name for field in dataclasses.fields(Instance)]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(
            {
                "v1": instance.v1,
                "v2": instance.v2,
                "v3": instance.v3,
                "flag": instance.flag,
            }
            for instance in instances
        )


def main():
    try:
        size = int(sys.argv[-1])
    except ValueError:
        size = 300_000

    print(f"Building database of {size} instances...", end="")
    big_db = [
        Instance(
            v1=next(strings) * 40,
            v2=next(strings) * 40,
            v3=next(strings) * 40,
            flag=next(bools),
        )
        for _ in range(size)
    ]
    print("done")

    print("Implementation 1: ", end="")
    values = timeit.repeat(
        "implementation_1(big_db)", globals=globals() | locals(), number=1, repeat=10
    )
    print(f"{min(values):.2f} seconds")

    print("Implementation 2: ", end="")
    values = timeit.repeat(
        "implementation_2(big_db)", globals=globals() | locals(), number=1, repeat=10
    )
    print(f"{min(values):.2f} seconds")

    print("Implementation 3: ", end="")
    values = timeit.repeat(
        "implementation_3(big_db)", globals=globals() | locals(), number=1, repeat=10
    )
    print(f"{min(values):.2f} seconds")

    print("Implementation 4: ", end="")
    values = timeit.repeat(
        "implementation_4(big_db)", globals=globals() | locals(), number=1, repeat=10
    )
    print(f"{min(values):.2f} seconds")


if __name__ == "__main__":
    main()
