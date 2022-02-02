# See e01.md for goals and lessons learned.

from typing import List

from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Item(Base):
    """An item that exists."""

    id = Column(Integer, primary_key=True)
    _tags = relationship("Tag")
    tags = association_proxy("_tags", "tag")

    __tablename__ = "item"

    def __init__(self, tags: List[str]):
        self.tags = tags


class Tag(Base):
    tag = Column(String(10))
    item_id = Column(ForeignKey(Item.id), index=True)

    __tablename__ = "tag"
    __table_args__ = (
        PrimaryKeyConstraint(tag, item_id),
        {},  # Not necessary to specify, but perhaps good practice.
    )

    def __init__(self, tag: str):
        self.tag = tag
