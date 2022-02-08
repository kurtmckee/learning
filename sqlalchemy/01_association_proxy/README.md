# Technologies in use

* Python
* sqlalchemy
* postgres or sqlite


# Target goal(s)

* Understand sqlalchemy [association proxies].


# Lessons learned

## Indexes

* An [index] on the `Tag.item_id` foreign key relationship significantly speeds up JOIN and SELECT IN queries.
  Unexpectedly, though, adding the index reduced initial setup times by multiple seconds.


## Primary keys

* It's possible to create a composite primary key by specifying `primary=True` multiple times.
  However, this seems like it might make it less obvious that a composite primary key is in use.
  Perhaps it's better to use [PrimaryKeyConstraint].


## Association proxies

* An association proxy makes a relationship feel like a list of scalar values.
* Loading values from the database through the relationship requires consideration of various factors:
  * Memory use must be considered.
  * Using a `joinedload` prevents the use of `yield_per()` but uses exactly one round-trip with the database.
  * Using a `selectinload` allows the use of `yield_per()` but increases the amount of database I/O.
    This is manageable -- for 100,000 items, `selectinload` only required 201 queries.
    The number of queries only increased for very low `yield_per()` numbers, like `yield_per(200)`.
* A custom `__init__()` was required so the relationship field's values could be instantiated.
  See the `Tag` class for this.
* The `association_proxy()` syntax feels odd.
  The first argument is the name of the relationship field in the proxy's same class.
  The second argument is the name of the field _in the class pointed to by the relationship_.


## Performance

On my machine, I saw the following output for Postgres with 100,000 items with tags:

```text
UNOPTIMIZED        : 100001 queries in 26.67 seconds
JOIN               :      1 queries in  3.57 seconds
JOIN ALL           :      1 queries in  1.44 seconds
SELECT IN          :    201 queries in  9.60 seconds
SELECT IN YIELD PER:    201 queries in  1.75 seconds
SELECT IN ALL      :    201 queries in  2.61 seconds
```


I got these numbers for sqlite with 100,000 items with tags:

```
UNOPTIMIZED        : 100001 queries in 20.08 seconds
JOIN               :      1 queries in  1.33 seconds
JOIN ALL           :      1 queries in  9.19 seconds
SELECT IN          :    201 queries in  1.76 seconds
SELECT IN YIELD PER:    201 queries in  4.41 seconds
SELECT IN ALL      :    201 queries in  5.31 seconds
```


## Future learning

* I cannot account for why sqlite and Postgres have flipped performance characteristics.


[association proxies]: https://docs.sqlalchemy.org/en/14/orm/extensions/associationproxy.html
[index]: https://docs.sqlalchemy.org/en/14/core/constraints.html#indexes
[PrimaryKeyConstraint]: https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint
