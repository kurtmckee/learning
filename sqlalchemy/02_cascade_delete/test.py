import os
from typing import Callable

import pytest
from sqlalchemy import create_engine
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Session, selectinload

from cascade_delete import Base, Item, Tag

# The database URI must be specified in the DB_URI environment variable.
# For example:
#
# DB_URI="postgresql://{USER}:{PASS}@{HOST}/{NAME}" python test.py
#
database_uri = os.environ["DB_URI"]
engine = create_engine(database_uri)


@pytest.fixture(autouse=True)
def setup():
    setup_session = Session(engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    setup_session.commit()
    setup_session.close()


@pytest.fixture
def session():
    session_ = Session(engine)
    yield session_
    session_.close()


query_count = 0
interrupt = False


# Count all queries.
@listens_for(engine, "after_cursor_execute", named=True)
def listener(*_, **kwargs):
    if interrupt:
        breakpoint()
        print(kwargs)  # press 'n' to see the kwargs
    global query_count
    query_count += 1


@pytest.fixture(autouse=True)
def reset_query_counter() -> Callable[[], None]:
    def reset():
        global query_count
        query_count = 0

    reset()
    yield reset


@pytest.mark.parametrize("tags_type", (list, set, tuple))
def test_create_new_item(session, reset_query_counter, tags_type):
    assert session.query(Item).count() == 0

    reset_query_counter()
    session.add(Item(tags=tags_type(["a", "b", "c"])))
    session.commit()
    assert query_count == 2

    reset_query_counter()
    items = session.query(Item).options(selectinload(Item._tags)).all()
    assert len(items) == 1
    assert items[0].tags == {"a", "b", "c"}


def test_modify_item(session, reset_query_counter):
    assert session.query(Item).count() == 0

    reset_query_counter()
    session.add(Item(tags=["a", "b", "c"]))
    session.commit()
    assert query_count == 2
    assert session.query(Tag).count() == 3

    items = session.query(Item).options(selectinload(Item._tags)).all()
    assert len(items) == 1
    item = items[0]

    assert item.tags == {"a", "b", "c"}

    reset_query_counter()
    item.tags.add("d")
    session.commit()
    assert query_count == 1
    assert session.query(Tag).count() == 4

    reset_query_counter()
    item.tags.remove("d")
    session.commit()
    assert query_count == 3
    # Why 3 queries? These are the queries that are executed:
    #
    # 1.    SELECT item.id AS item_id
    #       FROM item
    #       WHERE item.id = %(pk_1)s
    #       'parameters': {'pk_1': 1}
    #
    # 2.    SELECT tag.tag AS tag_tag, tag.item_id AS tag_item_id
    #       FROM tag
    #       WHERE %(param_1)s = tag.item_id'
    #       'parameters': {'param_1': 1}
    #
    # 3.    DELETE FROM tag WHERE tag.tag = %(tag)s AND tag.item_id = %(item_id)s
    #       'parameters': {'tag': 'd', 'item_id': 1}
    #
    # It *looks* like sqlalchemy is doing extra work to re-get the item and its tag.
    #
    assert session.query(Tag).count() == 3

    reset_query_counter()
    item.tags = set()
    session.commit()
    assert query_count == 3
    assert session.query(Tag).count() == 0


def test_delete_an_item(session, reset_query_counter):
    session.add(Item(tags=["a", "b", "c"]))
    session.commit()

    reset_query_counter()
    session.query(Item).filter(Item.id == 1).delete()
    assert query_count == 1
    session.commit()

    assert session.query(Item).count() == 0
    assert session.query(Tag).count() == 0
