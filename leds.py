"""
leds.py

LED Display Module

Creates a realistic FPGA-style LED panel.
"""

import streamlit as st
import streamlit.components.v1 as components
import textwrap


def display_led_panel(binary_string):
    """
    Displays FPGA style LED output.
    """

    html = f"""
    <div style="
        background:#1b1b1b;
        border:2px solid #444;
        border-radius:12px;
        padding:25px;
        margin:10px 0;
    ">

        <h3 style="
            color:white;
            text-align:center;
        ">
            LED OUTPUT
        </h3>

        <div style="
            display:flex;
            justify-content:center;
            gap:25px;
        ">
    """

    total_bits = len(binary_string)

    for index, bit in enumerate(binary_string):

        led_number = total_bits - index - 1

        if bit == "1":

            led_color = "#00ff55"
            glow = "0 0 20px #00ff55"

        else:

            led_color = "#202020"
            glow = "inset 0 0 10px black"


        html += f"""

        <div style="
            text-align:center;
            color:white;
        ">

            <div>
                LED {led_number}
            </div>

            <div style="
                width:50px;
                height:50px;
                border-radius:50%;
                background:{led_color};
                box-shadow:{glow};
                margin:10px;
            ">
            </div>

            <div>
                {bit}
            </div>

        </div>

        """


    html += """

        </div>

    </div>

    """
    components.html(
    html,
    height=250
)

def display_binary_information(counter):
    """
    Displays binary, decimal and hexadecimal values.
    """

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Binary",
            counter.binary()
        )

    with col2:

        st.metric(
            "Decimal",
            counter.decimal()
        )

    with col3:

        st.metric(
            "Hexadecimal",
            counter.hexadecimal()
        )


def display_progress(counter):
    """
    Shows how close the counter is to overflow.
    """

    st.subheader("Counter Progress")

    st.progress(
        counter.progress()
    )

    st.caption(
        f"{counter.decimal()} / {counter.maximum_value}"
    )


def display_status(running):
    """
    Running / Paused indicator.
    """

    if running:

        st.success("🟢 Counter Running")

    else:

        st.error("🔴 Counter Paused")