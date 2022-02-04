# See README.md for goals and lessons learned.

from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Item(Base):
    """An item that exists."""

    id = Column(Integer, primary_key=True)
    _tags = relationship(
        "Tag",
        cascade="all, delete-orphan",
        collection_class=set,
    )
    tags: set = association_proxy("_tags", "tag")

    __tablename__ = "item"


class Tag(Base):
    tag = Column(String(10))
    item_id = Column(ForeignKey(Item.id, ondelete="cascade"), index=True)

    __tablename__ = "tag"
    __table_args__ = (
        PrimaryKeyConstraint(tag, item_id),
        {},  # Not necessary to specify, but perhaps good practice.
    )

    def __init__(self, tag: str):
        self.tag = tag
