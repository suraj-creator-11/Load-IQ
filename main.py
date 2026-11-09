# main.py
# LoadIQ: Priority-Driven Delivery Load Optimisation Engine
# CP-048 Capstone Project
#
# Menu-driven console app. Run with:  python main.py

from models import Parcel, Van
from engine import generate_load_plan
from io_utils import read_int, read_priority


# ---- In-memory state (resets when the program exits) ----
parcels = []
vans = []
next_parcel_num = 1
next_van_num = 1


# ---------------- Feature 1: Add Parcel ----------------
def add_parcel():
    global next_parcel_num
    print("\n--- Add Parcel ---")
    pid = f"P-{next_parcel_num:03d}"
    weight_g = read_int("Weight (grams): ", min_val=1)
    volume_cm3 = read_int("Volume (cm^3): ", min_val=1)
    priority = read_priority()
    dest = input("Destination (optional): ").strip()

    parcels.append(Parcel(pid, weight_g, volume_cm3, priority, dest))
    next_parcel_num += 1
    print(f"  ✓ Parcel {pid} added.")


# ---------------- Feature 2: Add Van ----------------
def add_van():
    global next_van_num
    print("\n--- Add Van ---")
    vid = f"V-{next_van_num:02d}"
    max_w = read_int("Max weight capacity (grams): ", min_val=1)
    max_v = read_int("Max volume capacity (cm^3): ", min_val=1)

    vans.append(Van(vid, max_w, max_v))
    next_van_num += 1
    print(f"  ✓ Van {vid} added.")


# ---------------- View helpers ----------------
def view_parcels():
    print("\n--- All Parcels ---")
    if not parcels:
        print("  (none)")
        return
    for p in parcels:
        print(f"  {p}")


def view_vans():
    print("\n--- All Vans ---")
    if not vans:
        print("  (none)")
        return
    for v in vans:
        print(f"  {v}")


# ---------------- Feature 5: Generate Load Plan ----------------
def run_load_plan():
    print("\n--- Generate Load Plan ---")

    if not parcels:
        print("  ! No parcels to load. Add some first.")
        return
    if not vans:
        print("  ! No vans available. Add some first.")
        return

    loaded, unloaded = generate_load_plan(parcels, vans)

    print(f"\n  Loaded  : {len(loaded)} parcel(s)")
    print(f"  Unloaded: {len(unloaded)} parcel(s)")

    # ---- Load sheet per van ----
    print("\n--- Load Sheet per Van ---")
    for van in vans:
        print(f"\n  {van.vid}")
        print(f"    Capacity : {van.max_weight_g/1000:.2f} kg | "
              f"{van.max_volume_cm3/1_000_000:.3f} m^3")
        print(f"    Used     : {van.used_weight_g/1000:.2f} kg | "
              f"{van.used_volume_cm3/1_000_000:.3f} m^3")
        print(f"    Free     : {van.free_weight_g()/1000:.2f} kg | "
              f"{van.free_volume_cm3()/1_000_000:.3f} m^3")

        if not van.parcels:
            print("    Parcels  : (empty)")
        else:
            print(f"    Parcels  : {len(van.parcels)}")
            for p in van.parcels:
                print(f"      - {p.pid} (P{p.priority}, {p.weight_g/1000:.2f} kg)")

    # ---- Unloaded parcels with reasons ----
    if unloaded:
        print("\n--- Unloaded Parcels ---")
        for p, reason in unloaded:
            print(f"  {p.pid} (P{p.priority}, {p.weight_g/1000:.2f} kg) — {reason}")
    else:
        print("\n  All parcels were loaded.")


# ---------------- Menu ----------------
def show_menu():
    print("\n===== LoadIQ: Delivery Load Optimiser =====")
    print("1. Add Parcel")
    print("2. Add Van")
    print("3. View All Parcels")
    print("4. View All Vans")
    print("5. Generate Load Plan")
    print("6. Exit")


def main():
    while True:
        show_menu()
        choice = read_int("Enter choice: ", min_val=1, max_val=6)

        if choice == 1:
            add_parcel()
        elif choice == 2:
            add_van()
        elif choice == 3:
            view_parcels()
        elif choice == 4:
            view_vans()
        elif choice == 5:
            run_load_plan()
        elif choice == 6:
            print("\nGoodbye.")
            break


if __name__ == "__main__":
    main()