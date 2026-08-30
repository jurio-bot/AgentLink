# Image benchmark dimension boundary

A benchmark may use the default score dimensions or a custom score schema, but every record in the same benchmark must use the same set of score dimensions.

This prevents an incomplete record with only one easy-to-score dimension from being ranked directly against a record evaluated across five dimensions. Category coverage alone is not enough to make those means comparable.

Custom schemas remain valid when they are consistent across all records. Dimension key order does not matter; the set of keys does.

The validator fails before ranking when a record is missing a benchmark dimension or introduces an extra one.
