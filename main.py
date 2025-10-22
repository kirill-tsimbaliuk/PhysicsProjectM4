import streamlit as st
from numpy import radians

from schemas import *
from physics import Processer, get_time_when_finish_slippage


weight: float = st.sidebar.slider("Weight, kg", 1.0, 10.0, 2.0)
friction: float = st.sidebar.slider("Friction", 0.1, 0.5, 0.2)
alpha: float = radians(st.sidebar.slider("Alpha, deg", 0.0, 90.0, 30.0))
radius: float = st.sidebar.slider("Radius, meter", 10.0, 100.0, 5.0)
start_velocity: float = st.sidebar.slider("Start velocity, m/s", 0.0, 100.0, 5.0)
height: float = st.sidebar.slider("Height, meter", 0.0, 100.0, 10.0)

start = st.sidebar.button("Start")

if start:
    try:
        processor = Processer(
            ball=Ball(
                position=Vector(x=0.0, y=height),
                linear_velocity=start_velocity,
                angular_velocity=0.0,
                weight=weight,
                radius=radius
            ),
            env=Environment(
                friction=friction,
                alpha=alpha,
                gravity=9.81
            ),
        )
    except WrongStartValueError as e:
        st.error(str(e))
    else:
        st.write("## Charts")
        predicted_time = max(0, get_time_when_finish_slippage(processor.ball, processor.env))
        position = st.line_chart([processor.get_info()], x="position_x", y="position_y", x_label="x", y_label="y")
        col1, col2 = st.columns(2)
        with col1:
            lin_vel = st.line_chart([processor.get_info()], y='linear_velocity', x='time', x_label="time",
                                    y_label="linear velocity")
        with col2:
            angular_vel = st.line_chart([processor.get_info()], y='angular_velocity', x='time', x_label="time",
                                        y_label="angular velocity")

        while not processor.ball.position.y <= 0:
            processor.process(0.1)

            position.add_rows([processor.get_info()])
            lin_vel.add_rows([processor.get_info()])
            angular_vel.add_rows([processor.get_info()])

        st.write("## Results")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total time", f"{round(processor.time, 2)}")
        with col2:
            st.metric("Predicted slippage stopping time", f"{round(predicted_time, 2)}")