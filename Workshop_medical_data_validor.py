# Import the regular expression module to validate ID formats like patient_id and last_visit_id.
# re is used to match patterns such as 'p1234' or 'v5678' using rules like 'starts with p and then digits'.
import re

# Sample medical records used to test the validator.
# A list stores multiple records in order, and each record is a dictionary.
# A dictionary is a key-value structure like {'patient_id': 'P1001', 'age': 34}.
# This is a common Python data structure used to represent a single row of data.
medical_records = [
    {
        'patient_id': 'P1001',
        'age': 34,
        'gender': 'Female',
        'diagnosis': 'Hypertension',
        'medications': ['Lisinopril'],
        'last_visit_id': 'V2301',
    },
    {
        'patient_id': 'P1002',
        'age': 47,
        'gender': 'male',
        'diagnosis': 'Type 2 Diabetes',
        'medications': ['Metformin', 'Insulin'],
        'last_visit_id': 'v2302',
    },
    {
        'patient_id': 'P1003',
        'age': 29,
        'gender': 'female',
        'diagnosis': 'Asthma',
        'medications': ['Albuterol'],
        'last_visit_id': 'v2303',
    },
    {
        'patient_id': 'p1004',
        'age': 56,
        'gender': 'Male',
        'diagnosis': 'Chronic Back Pain',
        'medications': ['Ibuprofen', 'Physical Therapy'],
        'last_visit_id': 'V2304',
    }
]

# This function checks whether each field in a single patient record follows the required rules.
# It takes the values of all required keys and returns a list of fields that are invalid.
# This is an example of a reusable function: we can call it for different patient records.
def find_invalid_records(
    patient_id, age, gender, diagnosis, medications, last_visit_id
):
    # A dictionary of validation rules for each field.
    # Each value is a boolean expression that returns True if the field is valid.
    # In Python, booleans are either True or False, and they are often used for validation checks.
    constraints = {
        # patient_id must be a string matching the pattern p followed by digits, ignoring case.
        # \d means any digit in a regular expression, so this matches values like p1001.
        'patient_id': isinstance(patient_id, str)
        and re.fullmatch(r'p\d+', patient_id, re.IGNORECASE),

        # age must be an integer and at least 18.
        'age': isinstance(age, int) and age >= 18,

        # gender must be a string and be either male or female, ignoring case.
        'gender': isinstance(gender, str) and gender.lower() in ('male', 'female'),

        # diagnosis can be a string or None.
        'diagnosis': isinstance(diagnosis, str) or diagnosis is None,

        # medications must be a list, and every item inside it must be a string.
        'medications': isinstance(medications, list)
        and all([isinstance(i, str) for i in medications]),

        # last_visit_id must be a string matching the pattern v followed by digits, ignoring case.
        # Using a raw string here avoids accidental escape-sequence issues in Python.
        'last_visit_id': isinstance(last_visit_id, str)
        and re.fullmatch(r'v\d+', last_visit_id, re.IGNORECASE)
    }

    # Return all keys whose validation rule evaluated to False.
    # This uses list comprehension: a compact way to create a list based on a condition.
    # Example: [key for key, value in dictionary.items() if not value]
    return [key for key, value in constraints.items() if not value]

# This function validates a whole collection of records.
# It ensures the input is a list/tuple and each dictionary has the correct keys and valid values.
# This is the main validation logic that checks the entire dataset, not just one record.
def validate(data):
    # Check whether the entire dataset is a list or tuple.
    # isinstance(value, (list, tuple)) returns True when the value is either a list or tuple.
    is_sequence = isinstance(data, (list, tuple))

    # If the input is not a list or tuple, stop immediately.
    if not is_sequence:
        print('Invalid format: expected a list or tuple.')
        return False

    # Track whether any invalid record was found.
    # is_invalid starts as False and becomes True if at least one record fails validation.
    is_invalid = False

    # Define the exact set of expected keys for every patient record.
    # A set is an unordered collection of unique values.
    # It is useful here to compare the keys in a dictionary exactly.
    key_set = set(
        ['patient_id', 'age', 'gender', 'diagnosis', 'medications', 'last_visit_id']
    )

    # Loop over each record in the dataset.
    # enumerate(data) gives both the index and the item at that index.
    for index, dictionary in enumerate(data):
        # Each item in the dataset must itself be a dictionary.
        if not isinstance(dictionary, dict):
            print(f'Invalid format: expected a dictionary at position {index}.')
            is_invalid = True
            continue

        # Every dictionary must contain exactly the required keys.
        # set(dictionary.keys()) converts the keys into a set so they can be compared to key_set.
        if set(dictionary.keys()) != key_set:
            print(
                f'Invalid format: {dictionary} at position {index} has missing and/or invalid keys.'
            )
            is_invalid = True
            continue

        # Validate the values inside the dictionary using the helper function.
        # **dictionary unpacks the dictionary into keyword arguments, so the function receives each value by name.
        invalid_records = find_invalid_records(**dictionary)

        # Print each invalid field and mark the dataset as invalid.
        for key in invalid_records:
            print(f"Unexpected format '{key}: {dictionary[key]}' at position {index}.")
            is_invalid = True

    # If any invalid record was found, return False.
    if is_invalid:
        return False

    # Otherwise, print success message and return True.
    print('Valid format.')
    return True

# Run the validator on the sample dataset to check whether the records are valid.
validate(medical_records)