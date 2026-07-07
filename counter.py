"""
counter.py

Binary Counter Logic

Author: Frances Ugwu
Project: FPGA Binary Counter Simulator

This module implements the behaviour of a binary counter
similar to one designed in VHDL.
"""


class BinaryCounter:
    """
    Binary Counter

    Features
    --------
    ✔ 4-bit and 8-bit operation
    ✔ Up counting
    ✔ Down counting
    ✔ Variable step size
    ✔ Overflow detection
    ✔ Binary conversion
    ✔ LED state generation
    """

    def __init__(self, bits=4):

        self.bits = bits
        self.count = 0

        self.total_counts = 0
        self.overflow_count = 0

    # -------------------------------------------------
    # Properties
    # -------------------------------------------------

    @property
    def modulus(self):
        return 2 ** self.bits

    @property
    def maximum_value(self):
        return self.modulus - 1

    # -------------------------------------------------
    # Configuration
    # -------------------------------------------------

    def set_bits(self, bits):
        """
        Change counter size.

        Supports:
        4-bit
        8-bit
        """

        if bits not in (4, 8):
            raise ValueError(
                "Counter size must be 4 or 8 bits."
            )

        self.bits = bits

        self.count %= self.modulus

    # -------------------------------------------------
    # Counter Control
    # -------------------------------------------------

    def reset(self):
        """
        Reset the counter.
        """

        self.count = 0
        self.total_counts = 0
        self.overflow_count = 0

    def increment(self, step=1):
        """
        Count upwards.
        """

        previous = self.count

        self.count = (
            self.count + step
        ) % self.modulus

        self.total_counts += 1

        if self.count < previous:
            self.overflow_count += 1

    def decrement(self, step=1):
        """
        Count downwards.
        """

        previous = self.count

        self.count = (
            self.count - step
        ) % self.modulus

        self.total_counts += 1

        if self.count > previous:
            self.overflow_count += 1

    # -------------------------------------------------
    # Data Output
    # -------------------------------------------------

    def decimal(self):
        """
        Decimal value of counter.
        """

        return self.count

    def binary(self):
        """
        Binary representation.

        Example

        5

        returns

        0101
        """

        return format(
            self.count,
            f"0{self.bits}b"
        )

    def hexadecimal(self):
        """
        Hexadecimal representation.
        """

        digits = self.bits // 4

        return format(
            self.count,
            f"0{digits}X"
        )

    # -------------------------------------------------
    # LED States
    # -------------------------------------------------

    def led_states(self):
        """
        Returns

        Example

        1010

        becomes

        [True, False, True, False]
        """

        return [
            bit == "1"
            for bit in self.binary()
        ]

    # -------------------------------------------------
    # Progress
    # -------------------------------------------------

    def progress(self):
        """
        Returns progress percentage.

        Used for the progress bar.
        """

        return self.count / self.maximum_value

    # -------------------------------------------------
    # Hardware Information
    # -------------------------------------------------

    def hardware_information(self):

        return {

            "Counter Size":
                f"{self.bits}-bit",

            "Modulo":
                self.modulus,

            "Maximum Value":
                self.maximum_value,

            "Current Decimal":
                self.decimal(),

            "Current Binary":
                self.binary(),

            "Current Hex":
                self.hexadecimal(),

            "Total Counts":
                self.total_counts,

            "Overflow Count":
                self.overflow_count
        }

    # -------------------------------------------------
    # String Representation
    # -------------------------------------------------

    def __str__(self):

        return (
            f"{self.bits}-bit Counter | "
            f"Decimal={self.decimal()} | "
            f"Binary={self.binary()}"
        )