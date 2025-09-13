from uuid import UUID

def is_valid_uuid(uuid_string, version=None):
    """
    Checks if a string is a valid UUID.

    Parameters:
    uuid_string (str): The string to test for UUID validity.
    version (int, optional): The expected UUID version (1, 2, 3, or 4).
                             If None, any valid UUID version is accepted.

    Returns:
    bool: True if uuid_string is a valid UUID (and optionally, of the specified version),
          False otherwise.
    """
    try:
        # Attempt to create a UUID object from the string
        uuid_obj = UUID(uuid_string, version=version)
        # Ensure the string representation of the created UUID matches the input
        # This handles cases where UUID() might successfully parse a partial or
        # malformed string, but not represent the *exact* input.
        return str(uuid_obj) == uuid_string
    except ValueError:
        return False
    except AttributeError: # Handles cases like UUID(0) where the input type is wrong
        return False