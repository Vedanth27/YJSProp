import streamlit as st
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Plotly Dark Example", page_icon="🌌")

st.title("Plotly Dark Template Example")

# Example data
x = [1, 2, 3, 4, 5]
y = [10, 15, 13, 17, 14]

# Create Plotly figure with dark template
fig = go.Figure(
    data=go.Scatter(x=x, y=y, mode='lines+markers', name='Example'),
    layout=dict(
        template="plotly_dark",
        title="Plotly Dark Template Example",
        xaxis_title="X Axis",
        yaxis_title="Y Axis"
    )
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)
