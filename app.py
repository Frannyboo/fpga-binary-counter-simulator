"""
==========================================================
FPGA Binary Counter Simulator
Author: Frances Ugwu
==========================================================
"""

# ==========================================================
# IMPORTS
# ==========================================================

import streamlit as st
import pandas as pd

from datetime import datetime

from streamlit_autorefresh import st_autorefresh

from counter import BinaryCounter

from leds import (
    display_led_panel,
    display_binary_information,
    display_progress,
    display_status
)

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(

    page_title="FPGA Binary Counter Simulator",

    page_icon="🔢",

    layout="wide"

)

# ==========================================================
# LOAD CSS
# ==========================================================

try:

    with open("style.css") as css:

        st.markdown(

            f"<style>{css.read()}</style>",

            unsafe_allow_html=True

        )

except:

    pass


# ==========================================================
# SESSION STATE
# ==========================================================

if "counter" not in st.session_state:

    st.session_state.counter = BinaryCounter(bits=4)


if "running" not in st.session_state:

    st.session_state.running = False


if "history" not in st.session_state:

    st.session_state.history = []


if "speed" not in st.session_state:

    st.session_state.speed = 1.0


if "step" not in st.session_state:

    st.session_state.step = 1


if "direction" not in st.session_state:

    st.session_state.direction = "Up"


if "bits" not in st.session_state:

    st.session_state.bits = 4


# ==========================================================
# AUTO REFRESH + COUNTER UPDATE
# ==========================================================


if st.session_state.running:

    st_autorefresh(

        interval=int(st.session_state.speed * 1000),

        key="counter_refresh"

    )


    if st.session_state.direction == "Up":

        st.session_state.counter.increment(
            st.session_state.step
        )

    else:

        st.session_state.counter.decrement(
            st.session_state.step
        )


# ==========================================================
# PAGE TITLE
# ==========================================================

st.title("🔢 FPGA Binary Counter Simulator")

# ==========================================================
# MAIN LAYOUT
# ==========================================================

left_column, right_column = st.columns([3,1])


# ==========================================================
# RIGHT PANEL
# ==========================================================

with right_column:

    st.subheader("Counter Controls")

    bits = st.radio(

        "Counter Size",

        [4,8],

        horizontal=True

    )

    direction = st.radio(

        "Counting Direction",

        ["Up","Down"],

        horizontal=True

    )

    step = st.selectbox(

        "Step Size",

        [1,2,4,8]

    )

    speed = st.slider(

        "Clock Period (seconds)",

        0.2,

        5.0,

        1.0,

        0.1

    )

    st.divider()

    start = st.button(

        "▶ Start",

        use_container_width=True

    )

    pause = st.button(

        "⏸ Pause",

        use_container_width=True

    )

    reset = st.button(

        "■ Reset",

        use_container_width=True

    )

# ==========================================================
# SAVE SETTINGS
# ==========================================================

# Detect whether the counter size changed

if bits != st.session_state.bits:

    st.session_state.bits = bits

    st.session_state.counter.set_bits(bits)

    # Clear history when changing hardware configuration

    st.session_state.history.clear()

    st.toast(
    "Counter reset.",
    icon="🔄"
    )

else:

    pass

# Save remaining settings

st.session_state.direction = direction

st.session_state.step = step

st.session_state.speed = speed

# ==========================================================
# BUTTONS
# ==========================================================

if start:

    st.session_state.running = True


if pause:

    st.session_state.running = False


if reset:

    st.session_state.running = False

    st.session_state.counter.reset()

    st.session_state.history.clear()

    st.toast(
    "Counter reset.",
    icon="🔄"
    )

st.divider()

# ==========================================================
# COUNTER ENGINE
# ==========================================================

# Calculate the equivalent clock frequency
frequency = 1 / st.session_state.speed

# Display current status
display_status(st.session_state.running)

# Hardware Information
st.subheader("Hardware Information")

info1, info2, info3 = st.columns(3)

with info1:

    st.metric(
        "Counter Size",
        f"{st.session_state.bits}-bit"
    )

    st.metric(
        "Clock Period",
        f"{st.session_state.speed:.1f} s"
    )

with info2:

    st.metric(
        "Clock Frequency",
        f"{frequency:.2f} Hz"
    )

    st.metric(
        "Direction",
        st.session_state.direction
    )

with info3:

    st.metric(
        "Step Size",
        st.session_state.step
    )

    st.metric(
        "Modulo",
        st.session_state.counter.modulus
    )

st.divider()


# ==========================================================
# PART 4 - COUNTER STATISTICS
# ==========================================================

st.subheader("📊 Counter Statistics")

s1, s2, s3, s4 = st.columns(4)


with s1:

    st.metric(
        "Current Decimal",
        st.session_state.counter.decimal()
    )


with s2:

    st.metric(
        "Total Counts",
        st.session_state.counter.total_counts
    )


with s3:

    st.metric(
        "Overflow Events",
        st.session_state.counter.overflow_count
    )


with s4:

    st.metric(
        "History Samples",
        len(st.session_state.history)
    )


st.divider()


# ==========================================================
# PART 3 - DISPLAY SECTION
# ==========================================================

with left_column:


    st.subheader("💡 FPGA LED Output")


    # Physical LED representation

    display_led_panel(

        st.session_state.counter.binary()

    )


    st.write("")


    # Binary / Decimal / Hex information

    display_binary_information(

        st.session_state.counter

    )


    st.write("")


    # Progress through counter range

    display_progress(

        st.session_state.counter

    )


    st.divider()


    # # ======================================================
    # # BINARY VALUE DISPLAY
    # # ======================================================

    # st.subheader("Binary Representation")


    # b1, b2, b3 = st.columns(3)


    # with b1:

    #     st.metric(

    #         "Binary",

    #         st.session_state.counter.binary()

    #     )


    # with b2:

    #     st.metric(

    #         "Decimal",

    #         st.session_state.counter.decimal()

    #     )


    # with b3:

    #     st.metric(

    #         "Hexadecimal",

    #         st.session_state.counter.hexadecimal()

    #     )



# ==========================================================
# PART 4 - HISTORY TABLE
# ==========================================================

st.subheader("📜 Counter History")


if len(st.session_state.history) > 0:


    history_df = pd.DataFrame(

        st.session_state.history

    )


    st.dataframe(

        history_df,

        use_container_width=True,

        hide_index=True

    )


else:


    st.info(

        "No counter history available. Start the counter to generate data."

    )



# ==========================================================
# PART 4 - GRAPHICAL HISTORY
# ==========================================================

if len(st.session_state.history) > 1:


    st.subheader("📈 Counter Behaviour")


    chart_data = pd.DataFrame(

        st.session_state.history

    )


    chart_data = chart_data.set_index(

        "Time"

    )


    st.line_chart(

        chart_data["Decimal"]

    )



# ==========================================================
# PART 4 - OVERFLOW STATUS
# ==========================================================

if st.session_state.counter.overflow_count > 0:

    st.warning(
        f"Overflow events: {st.session_state.counter.overflow_count}"
    )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(

    """
    FPGA Binary Counter Simulator |
    Implemented using Python + Streamlit |
    Equivalent behaviour to a VHDL synchronous counter
    """
)