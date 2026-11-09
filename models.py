# models.py
# Data model for LoadIQ.
# All weight/volume stored as integers (grams, cm^3) to avoid float bugs.

class Parcel:
    def __init__(self, pid, weight_g, volume_cm3, priority, dest=""):
        self.pid = pid
        self.weight_g = weight_g
        self.volume_cm3 = volume_cm3
        self.priority = priority      # 1 = low, 5 = high
        self.dest = dest

    def __str__(self):
        return (f"{self.pid} | {self.weight_g/1000:.2f} kg | "
                f"{self.volume_cm3/1_000_000:.3f} m^3 | "
                f"Priority {self.priority} | Dest: {self.dest or '-'}")


class Van:
    def __init__(self, vid, max_weight_g, max_volume_cm3):
        self.vid = vid
        self.max_weight_g = max_weight_g
        self.max_volume_cm3 = max_volume_cm3
        self.used_weight_g = 0
        self.used_volume_cm3 = 0
        self.parcels = []          # list of Parcel objects

    def can_fit(self, parcel):
        """Return True only if BOTH weight and volume fit."""
        return (self.used_weight_g + parcel.weight_g <= self.max_weight_g
                and self.used_volume_cm3 + parcel.volume_cm3 <= self.max_volume_cm3)

    def add_parcel(self, parcel):
        self.parcels.append(parcel)
        self.used_weight_g += parcel.weight_g
        self.used_volume_cm3 += parcel.volume_cm3

    def free_weight_g(self):
        return self.max_weight_g - self.used_weight_g

    def free_volume_cm3(self):
        return self.max_volume_cm3 - self.used_volume_cm3

    def __str__(self):
        return (f"{self.vid} | Cap: {self.max_weight_g/1000:.1f} kg / "
                f"{self.max_volume_cm3/1_000_000:.2f} m^3 | "
                f"Used: {self.used_weight_g/1000:.2f} kg / "
                f"{self.used_volume_cm3/1_000_000:.3f} m^3")