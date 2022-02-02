import os
import random
import time

from sqlalchemy import create_engine
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Session, joinedload, selectinload

from e01_association_proxy import Base, Item

# The database URI may be specified in the DB_URI environment variable.
# For example:
#
# DB_URI="postgresql://{USER}:{PASS}@{HOST}/{NAME}" python e01_test.py
#
database_uri = os.getenv("DB_UI", "sqlite:///:memory:")
engine = create_engine(database_uri)
session = Session(engine)


def setup():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    start_time_ = time.time()

    # Generate 10 unique tag names.
    tag_names = []
    while len(tag_names) < 10:
        tag_name = "".join(chr(random.randint(ord("a"), ord("z"))) for _ in range(3))
        if tag_name not in tag_names:
            tag_names.append(tag_name)

    # Create 100,000 items with 3 tags each.
    for _ in range(100_000):
        session.add(Item(tags=random.sample(tag_names, random.randint(0, 3))))

    print(f"SETUP: Objects generated after {time.time() - start_time_:.2f} seconds")

    # Commit all changes.
    session.commit()

    print(f"SETUP: Setup completed after {time.time() - start_time_:.2f} seconds")


setup()


# Count all queries.
@listens_for(engine, "after_cursor_execute", named=True)
def listener(*args, **kwargs):
    global query_count
    query_count += 1


def test_unoptimized():
    for item in session.query(Item):
        item.tags


def test_select_in():
    for item in session.query(Item).options(selectinload(Item._tags)):
        item.tags


def test_select_in_yield_per():
    for item in session.query(Item).options(selectinload(Item._tags)).yield_per(1000):
        item.tags


def test_select_in_all():
    for item in session.query(Item).options(selectinload(Item._tags)).all():
        item.tags


def test_join():
    for item in session.query(Item).options(joinedload(Item._tags)):
        item.tags


def test_join_all():
    for item in session.query(Item).options(joinedload(Item._tags)).all():
        item.tags


tests = (
    test_unoptimized,
    test_join,
    test_join_all,
    test_select_in,
    test_select_in_yield_per,
    test_select_in_all,
)

for test in tests:
    prefix = " ".join(test.__name__.split("_")[1:]).upper()
    query_count = 0
    start_time = time.time()
    test()
    print(f"{prefix:<19}: {query_count:>6} queries in {time.time() - start_time: >5.2f} seconds")
