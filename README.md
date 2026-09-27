# Medical Data Validator

This project contains a Python script named `Workshop_medical_data_validor.py` that checks whether a list of medical patient records follows the expected format and rules.

The main goal is to validate the data before using it in a larger system, such as a hospital database, reporting tool, or API backend.

---

## What this script does

The script:

- stores sample patient records in a list
- checks each record for required fields
- validates the type and format of each field
- prints messages if something is invalid
- returns `True` when all records are valid and `False` if any record is invalid

---

## Why this is useful

In real applications, data often comes from forms, CSV files, APIs, or databases. Sometimes the information is missing, misspelled, or in the wrong format. Validation helps prevent bugs and bad data from reaching the rest of the system.

Example:

- `patient_id` must look like `P1001` or `p1001`
- `age` must be an integer of at least 18
- `gender` must be `male` or `female`
- `medications` must be a list of strings
- `last_visit_id` must look like `V2301` or `v2301`

---

## Data structures used

### 1. List
A list is an ordered collection of items.

```python
medical_records = [
    {'patient_id': 'P1001', 'age': 34},
    {'patient_id': 'P1002', 'age': 47}
]
```

Here, `medical_records` is a list. It holds multiple patient records.

### 2. Dictionary
A dictionary stores data as key-value pairs.

```python
{
    'patient_id': 'P1001',
    'age': 34,
    'gender': 'Female'
}
```

Each key is a field name, and each value is the actual data.

This is useful because each patient record contains many different kinds of information.

---

## Core Python concepts explained

### Functions
A function is a reusable block of code.

```python
def find_invalid_records(...):
    ...
```

Functions let us group logic into a single place. Instead of repeating the same validation checks again and again, we write them once and call the function whenever needed.

### `if` statements
An `if` statement checks a condition.

```python
if not is_sequence:
    print('Invalid format: expected a list or tuple.')
    return False
```

If the condition is `True`, Python runs the code inside. Otherwise, it skips it.

This is how the program decides whether the data is in the right format.

### `for` loops
A `for` loop repeats a block of code for each item in a collection.

```python
for index, dictionary in enumerate(data):
```

This means:

- `index` = the position of the current item
- `dictionary` = the actual record at that position

The script loops over every patient record to validate it.

### `enumerate()`
`enumerate()` gives both the index and the value while looping.

```python
for index, dictionary in enumerate(data):
```

This is useful when you want to print messages like "invalid record at position 2".

### `isinstance()`
`isinstance(value, type)` checks whether a value has a certain data type.

```python
isinstance(age, int)
```

This returns `True` only if `age` is an integer.

It is used to validate types like:

- string
- integer
- list
- dictionary

### Sets
A set is an unordered collection of unique values.

```python
key_set = {
    'patient_id', 'age', 'gender', 'diagnosis', 'medications', 'last_visit_id'
}
```

The script compares the keys in each dictionary to the expected set of keys. If a record has missing or extra keys, it is invalid.

### List comprehension
List comprehension is a compact way to create a list.

```python
return [key for key, value in constraints.items() if not value]
```

This means:

- look through each item in `constraints`
- keep only the keys whose value is `False`
- return them as a list

So if a field is invalid, its name is added to the list.

### `**dictionary` unpacking
In Python, `**dictionary` expands a dictionary into keyword arguments.

```python
find_invalid_records(**dictionary)
```

This is equivalent to passing each key-value pair as a separate argument:

```python
find_invalid_records(
    patient_id='P1001',
    age=34,
    gender='Female',
    ...
)
```

This is helpful when a record is already stored as a dictionary.

---

## Validation logic

### `find_invalid_records()`
This function validates one patient record.

It creates a dictionary called `constraints` where each field is checked with a condition.

```python
constraints = {
    'patient_id': ...,
    'age': ...,
    'gender': ...,
    'diagnosis': ...,
    'medications': ...,
    'last_visit_id': ...
}
```

Each key in the dictionary represents a field. Each value is either:

- `True` when valid
- `False` when invalid

Then the function returns only the invalid field names.

### Validation rules

#### `patient_id`
Must be a string and match the pattern `p` followed by digits.

Example valid:

- `P1001`
- `p1004`

Example invalid:

- `1001`
- `abc`
- `patient_1`

This check uses a regular expression.

#### `age`
Must be an integer and at least 18.

Valid examples:

- `18`
- `34`
- `56`

Invalid examples:

- `'34'` (string, not integer)
- `17`

#### `gender`
Must be a string and either `male` or `female`.

The script converts to lowercase using `.lower()` before comparing, so it accepts mixed case like:

- `Male`
- `FEMALE`
- `male`

#### `diagnosis`
Can be a string or `None`.

This means the field can be empty or not provided.

#### `medications`
Must be a list, and every item inside the list must be a string.

Example valid:

```python
['Metformin', 'Insulin']
```

Example invalid:

```python
['Metformin', 123]
```

#### `last_visit_id`
Must be a string matching `v` followed by digits.

Example valid:

- `V2301`
- `v2302`

---

## Regular expressions

Regular expressions are patterns used to match text.

The code uses:

```python
re.fullmatch(r'p\d+', patient_id, re.IGNORECASE)
```

This checks whether the value:

- starts with `p`
- followed by one or more digits
- ignoring case

Examples matched:

- `p1001`
- `P2002`

The pattern `\d+` means:

- `\d` = any digit
- `+` = one or more digits

The `r` before the string means raw string. This is important because in Python, `\d` must be written as a raw string in regex patterns to avoid escape warnings.

---

## Main validation function: `validate()`

This is the main function that checks the full dataset.

### Step 1: confirm the input is list-like

```python
is_sequence = isinstance(data, (list, tuple))
```

If the input is not a list or tuple, it stops immediately.

### Step 2: loop through each record

```python
for index, dictionary in enumerate(data):
```

Each item in the dataset should be a dictionary.

### Step 3: check dictionary structure

```python
if set(dictionary.keys()) != key_set:
```

This compares the keys in the record with the required keys.

If a record is missing a key or has extra keys, it is invalid.

### Step 4: validate values inside each record

```python
invalid_records = find_invalid_records(**dictionary)
```

This calls the helper function on that record.

### Step 5: mark invalid records

If a field is invalid, the script prints a message such as:

```python
Unexpected format 'age: 12' at position 1.
```

If any issues are found, the function returns `False`.

### Step 6: final result

```python
if is_invalid:
    return False

print('Valid format.')
return True
```

If everything passes, the script prints:

```python
Valid format.
```

---

## How to run the script

Open a terminal in the same folder and run:

```bash
python Workshop_medical_data_validor.py
```

On some systems, you may use:

```bash
python3 Workshop_medical_data_validor.py
```

Expected output:

```python
Valid format.
```

This means the sample records all match the allowed pattern.

---

## Example of invalid data

If one record had an invalid field, for example:

```python
'age': 12
```

The script would flag it because age must be at least 18.

If one record used the wrong key names, the script would also reject it.

---

## Summary

This project demonstrates several important programming ideas:

- storing structured data in lists and dictionaries
- validating user or system input
- checking both types and patterns of values
- using loops and functions to process data efficiently
- using regular expressions for rule-based matching

This is the foundation of many real-world data validation systems.

---

## File overview

- `Workshop_medical_data_validor.py` — the main validation script
- `README.md` — explanation of how the script works

---

## Final note

This script is a simple example, but it follows the same logic used in production systems for:

- form validation
- database checks
- data cleaning
- API request validation
- healthcare record quality checks
