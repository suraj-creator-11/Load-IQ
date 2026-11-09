# io_utils.py
# Safe input helpers — every prompt re-asks on bad input instead of crashing.
# This file is the ONLY place that touches input(), so validation logic
# lives in one place and every menu option gets the same protection.

def read_int(prompt, min_val=None, max_val=None):
    """
    Read a whole number from the user.
    Re-prompts on non-numeric input or out-of-range values.
    """
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("  ! Please enter a whole number.")
            continue

        if min_val is not None and value < min_val:
            print(f"  ! Must be at least {min_val}.")
            continue
        if max_val is not None and value > max_val:
            print(f"  ! Must be at most {max_val}.")
            continue

        return value


def read_nonempty(prompt):
    """
    Read a non-empty string. Whitespace-only input is rejected.
    """
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print("  ! Input cannot be empty.")


def read_priority(prompt="Priority (1-5): "):
    """
    Priority is constrained to 1..5 for every parcel.
    Wraps read_int so the range lives in one place.
    """
    return read_int(prompt, min_val=1, max_val=5)