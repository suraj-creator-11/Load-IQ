# engine.py
# Core greedy assignment for LoadIQ.
#
# Strategy:
#   1. Sort parcels by priority DESC (highest first).
#   2. Tiebreaker for equal priority: heavier parcel first.
#      Reason: a heavy parcel is harder to fit later, so place it early.
#   3. First-fit: walk vans in order, place the parcel in the first van
#      that has room by BOTH weight AND volume.
#   4. If no van accepts the parcel, record it as unloaded WITH a reason.
#
# Note: This is a GREEDY heuristic, not an optimal packer.
# True bin-packing is NP-hard. The problem statement asks for
# "highest priority first", which is exactly what this does.

def generate_load_plan(parcels, vans):
    """
    Build a load plan.

    Parameters
    ----------
    parcels : list[Parcel]
    vans    : list[Van]

    Returns
    -------
    (loaded, unloaded)
        loaded   : list of (parcel, van) tuples, in the order they were placed
        unloaded : list of (parcel, reason_string) tuples

    Side effect: resets and then fills each van in `vans` in place.
    """
    # ---- Step 0: reset vans so re-running the plan is safe ----
    for van in vans:
        van.used_weight_g = 0
        van.used_volume_cm3 = 0
        van.parcels = []

    # ---- Step 1: sort by priority DESC, then weight DESC ----
    # Python's sorted() is stable, so equal (priority, weight) keeps input order.
    sorted_parcels = sorted(
        parcels,
        key=lambda p: (-p.priority, -p.weight_g)
    )

    # ---- Step 2: precompute the biggest single-van capacity ----
    # Used to decide WHY an unloaded parcel could not be placed.
    max_van_weight = max((v.max_weight_g for v in vans), default=0)
    max_van_volume = max((v.max_volume_cm3 for v in vans), default=0)

    loaded = []
    unloaded = []

    # ---- Step 3: place each parcel, highest priority first ----
    for parcel in sorted_parcels:
        placed = False

        for van in vans:
            if van.can_fit(parcel):
                van.add_parcel(parcel)
                loaded.append((parcel, van))
                placed = True
                break   # first-fit: stop at the first van that accepts it

        if not placed:
            # ---- Step 4: explain WHY this parcel was not loaded ----
            too_big_for_any_van = (
                parcel.weight_g > max_van_weight
                or parcel.volume_cm3 > max_van_volume
            )

            if too_big_for_any_van:
                reason = "Exceeds total capacity of every van (even when empty)"
            else:
                reason = "No van has remaining capacity for this parcel"

            unloaded.append((parcel, reason))

    return loaded, unloaded