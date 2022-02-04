# Technologies in use

* Python
* sqlalchemy
* postgres (sqlite does not work in my testing)


# Target goal(s)

* Understand sqlalchemy [association proxies] better.
* Understand sqlalchemy's cascading options.
* Try to use a set-like association proxy (rather than a list).
* Try to avoid an `__init__()` method that explicitly changes the `tags` type.

  That is, if the incoming information is in a `list`, perhaps it can be transformed to a `set` automatically.


# Lessons learned

## Cascading

* If only `cascade="all, delete-orphan"` is set on the `Item._tags` association proxy,
  it is not possible to delete an `Item` because its associated `Tag`s are not also deleted.
* If only `ondelete="cascade"` is set on the `Tag.item_id` foreign key relationship,
  it is not possible to remove a `Tag` from an `Item`.
* To do everything I want (and tested), both bullet points 1 and 2 must be set.


## Object types

* Setting `collection_type=set` on the `Item._tags` association proxy worked great.
  No need to override `Item.__init__()` to get the functionality I wanted.


## Future learning

* I think association proxy operations (and perhaps relationship in general) could be more optimized.
  Removing a single Tag from an Item generated 3 queries, so perhaps this can be improved for bulk operations.


[association proxies]: https://docs.sqlalchemy.org/en/14/orm/extensions/associationproxy.html
