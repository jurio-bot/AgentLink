# Retry Guard receipt flag boundary

`receipt_present` is a JSON boolean evidence flag, not a truthy/falsy convenience value.

Valid examples:

```json
{"receipt_present": true}
{"receipt_present": false}
```

A string such as `"false"`, a number, or another non-boolean value is rejected instead of being coerced with Python truthiness. This prevents a string value from being interpreted as proof that a durable completion receipt exists.

When `receipt_present` is the real boolean `false`, normal retry classification continues to depend on `status`, `side_effect`, and the retry budget. Retry Guard does not invent completion evidence from another field.
