import plotly.graph_objects as go
import matplotlib.pyplot as plt

def plot_bus_voltage(bus: object)->None:
    """
    Plot bus voltage using matplotlib.pyplot

    Parameter
    -------------
    bus: object
        an instalce of the Bus class
    """
    plt.figure(figsize=(10, 6))
    plt.plot(bus.bus_i, bus.Vm, 'b-o', label = 'Voltage Magnitude')
    plt.xlabel('Bus Number')
    plt.ylabel('Voltage Magnitude')
    plt.title('Bus Voltage Magnitude Plot')
    plt.legend('Vmag')
    plt.grid()

    # save the plot
    plt.savefig('bus_voltage_magnitude_plot', dpi=400, format="png", bbox_inches="tight")

    plt.show()

def interactive_plot(bus: object):
    """
    Create Interactive plot using plotly.graph_objects

    Parameter
    ------------
    bus: object
        as instance of the Bus class
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=bus.bus_i, y=bus.Vm, name="Voltage Magnitude"))

    fig.update_layout(
        title="Bus Voltage Profile",
        xaxis_title="Bus Number",
        yaxis_title="Voltage (p.u.)"
    )  

    # save as HTML file
    fig.write_html("voltage_profile_interactive.html")
