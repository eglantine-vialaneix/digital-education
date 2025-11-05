import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


# CATALOGUE:
# convex functions we define and use for this exercice

# Shifted squared
def shifted_squared(x):
    return x**2 + 0.5*x
def grad_shifted_squared(x):
    return 2*x + 0.5

# Oscillating square
def square_sin(x):
    return x * x + 0.1 * np.sin(10 * x)
def grad_square_sin(x):
    return 2 * x + np.cos(10 * x)

# Absolute value, non-differentiable at 0
def absolute(x):
    return np.abs(x)
def grad_absolute(x):
    return np.sign(x) # fyi: np.sign(0) = 0

# Log barrier (convex on x > 0 only)
def log_barrier(x):
    return -np.log(x) if x > 0 else np.inf
def grad_log_barrier(x):
    return -1/x if x > 0 else 0


class GradientDescent:
    def __init__(self, X_MIN, X_MAX, sim_counter, n_pts = 400, max_iter = 15):
        # Defining the ranges of x values that the function will take
        # Those are the max and min of the plotted window
        self.X_MIN = X_MIN
        self.X_MAX = X_MAX
        self.n_pts = n_pts
        
        # Defining the variables we will need during the algorithm
        self.max_iter = max_iter
        self.a_0 = None
        self.eta = None
        self.df_gd = None
    
        # User data
        self.simulation_counter = sim_counter# count how many times the user runs the simulation

        # Defining the convex functions we will be working with
        self.all_fs = [shifted_squared, square_sin, absolute, log_barrier] 
        self.all_grad_fs = [grad_shifted_squared, grad_square_sin, grad_absolute, grad_log_barrier] 
        self.f = self.all_fs[(sim_counter // 3) % len(self.all_fs)]
        self.grad_f = self.all_grad_fs[(sim_counter // 3) % len(self.all_fs)]
        self.true_min = None # storing the true min value of the function for computations
        


    def set_eta(self, eta_value):
        """Set the learning rate (eta) to the given value."""
        self.eta = eta_value
        print(f"Using a learning rate eta η = {self.eta}")

    def set_a_0(self, a_0_value):
        """Set the initial point (a₀) to the given value."""
        self.a_0 = a_0_value
        print(f"Using the initial point a₀: {self.a_0}")

    def gradient_descent(self):
        # Checking requirements before running the algorithm
        assert self.eta is not None, "Please use self.set_eta to define the learning rate before running the algorithm."
        assert self.a_0 is not None, "Please use self.set_a_0 to define the initial point before running the algorithm."

        #initial point
        a_n = self.a_0
        #list of all th a_ns
        a_ns = np.zeros(self.max_iter)
        a_ns[0] = self.a_0
        #list of corresponding losses
        losses = np.zeros(self.max_iter)
        losses[0] = self.compute_loss(self.a_0)
        
        #perform the algorithm
        for i in range(1, self.max_iter):
            a_n_1 =  a_n - self.eta * self.grad_f(a_n) 
            a_ns[i] = a_n_1
            losses[i] = self.compute_loss(a_n_1)
            a_n = a_n_1
        
        # Storing the steps of the algorithm into a dataframe
        self.df_gd = pd.DataFrame({'a_ns': a_ns, 'f_a_ns': self.f(a_ns), 'losses': losses, 'iteration': np.arange(self.max_iter)})
        
        return self.df_gd


    def find_min_f(self):
        # 1D for now but should be 2D later on
        x = np.linspace(self.X_MIN, self.X_MAX, self.n_pts)
        true_min = x[np.argmin(self.f(x))]
        return true_min # returns the x of the actual minimum, not f(x)
    
    def set_true_min(self):
        self.true_min = self.find_min_f()
        #print(f"The actual minimum of f is at x = {self.true_min:.2f} with f(x) = {self.f(self.true_min):.2f}")
    
    def compute_loss(self, x):
        if self.true_min is None:
            self.set_true_min()
        return abs(self.f(x) - self.f(self.true_min))
    
    
    def plot_iterations_and_loss(self):
        """Plot the function f and the iterative steps of the proposed algorithm, along with the corresponding losses"""
        
        # Create subplot layout (1 row, 2 columns)
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Gradient Descent Path", "Loss Curve"))

        # ===== Left subplot: f(x) + GD path =====
        
        # f(x)
        x = np.linspace(self.X_MIN, self.X_MAX, self.n_pts)
        fig.add_trace(
            go.Scatter(
                x=x,
                y=self.f(x),
                mode="lines",
                name="f(x)",
                line=dict(color="lightgray"),
            ),
            row=1, col=1
        )
        
        # top boundary of green goal area (loss between 0 and 0.05)
        fig.add_trace(
            go.Scatter(
                x=x,
                y=[self.f(self.true_min) + 0.05] * self.n_pts ,
                fill=None,
                mode='lines',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ),
            row=1, col=1
        )
        # bottom boundary of green goal area
        fig.add_trace(
            go.Scatter(
                x=x,
                y=[self.f(self.true_min)] * self.n_pts,
                fill='tonexty',
                mode='lines',
                line=dict(width=0),
                fillcolor='rgba(144, 238, 144, 0.3)',  # light green with transparency
                showlegend=False,
                hoverinfo='skip'
            ),
            row=1, col=1
        )
        
        
        # # Circle around true minimum on f 
        # fig.add_trace(
        #     go.Scatter(
        #         x=[self.true_min],
        #         y=[self.f(self.true_min)],
        #         mode='markers',
        #         marker=dict(
        #             size=15,
        #             color='rgba(144, 238, 144, 0)',  # transparent fill
        #             line=dict(color='lightgreen', width=2)
        #         ),
        #         name='Minimum',
        #         showlegend=False,
        #         hoverinfo='skip'
        #     ),
        #     row=1, col=1
        # )
        
        # GD path
        fig.add_trace(
            go.Scatter(
                x=[self.df_gd['a_ns'].iloc[0]],
                y=[self.df_gd['f_a_ns'].iloc[0]],
                mode="markers",
                marker=dict(color="red", size=7),
                name="GD Path"
            ),
            row=1, col=1
        )

        # ===== Right subplot: Loss curve =====
        
        # loss curve
        fig.add_trace(
            go.Scatter(
                x=[],
                y=[],
                mode="markers+lines",
                marker=dict(color="red", size=7),
                name="Loss"
            ),
            row=1, col=2
        )
        
        # top boundary of green goal area (loss between 0 and 0.05)
        fig.add_trace(
            go.Scatter(
                x=[self.df_gd['iteration'].min() - 1, self.df_gd['iteration'].max() + 1],
                y=[0.05, 0.05],
                fill=None,
                mode='lines',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ),
            row=1, col=2
        )
        # bottom boundary of green goal area
        fig.add_trace(
            go.Scatter(
                x=[self.df_gd['iteration'].min() - 1, self.df_gd['iteration'].max() + 1],
                y=[0, 0],
                fill='tonexty',
                mode='lines',
                line=dict(width=0),
                fillcolor='rgba(144, 238, 144, 0.3)',  # light green with transparency
                showlegend=False,
                hoverinfo='skip'
            ),
            row=1, col=2
        )

        # ===== Frames: update ALL traces =====
        frames = []
        for i in self.df_gd['iteration'].unique():
            frames.append(
                go.Frame(
                    data=[
                        # Trace 0: Keep the function line unchanged
                        go.Scatter(x=x, y=self.f(x)),
                        # Trace 1: Keep the green circle unchanged
                        # go.Scatter(
                        #     x=[self.true_min],
                        #     y=[self.f(self.true_min)],
                        #     mode='markers',
                        #     marker=dict(
                        #         size=15,
                        #         color='rgba(144, 238, 144, 0)',
                        #         line=dict(color='lightgreen', width=2)
                        #     )
                        # ),
                        # Trace 1.1: Keep green band top line unchanged
                        go.Scatter(
                            x=x,
                            y=[self.f(self.true_min) + 0.05] * self.n_pts,
                            fill=None,
                            mode='lines',
                            line=dict(width=0)
                        ),
                        # Trace 1.2: Keep green band bottom line unchanged
                        go.Scatter(
                            x=x,
                            y=[self.f(self.true_min)] * self.n_pts,
                            fill='tonexty',
                            mode='lines',
                            line=dict(width=0),
                            fillcolor='rgba(144, 238, 144, 0.3)'
                        ),
                        # Trace 2: Update GD points
                        go.Scatter(
                            x=self.df_gd.loc[self.df_gd['iteration'] <= i, 'a_ns'],
                            y=self.df_gd.loc[self.df_gd['iteration'] <= i, 'f_a_ns'],
                            marker=dict(color="red", size=7)
                        ),
                        # Trace 3: Update loss curve
                        go.Scatter(
                            x=self.df_gd.loc[self.df_gd['iteration'] <= i, 'iteration'],
                            y=self.df_gd.loc[self.df_gd['iteration'] <= i, 'losses'],
                            mode="markers+lines",
                            marker=dict(color="red", size=7)
                        ),
                        # Trace 4.1: Keep green band top line unchanged
                        go.Scatter(
                            x=[self.df_gd['iteration'].min() - 1, self.df_gd['iteration'].max() + 1],
                            y=[0.05, 0.05],
                            fill=None,
                            mode='lines',
                            line=dict(width=0)
                        ),
                        # Trace 4.2: Keep green band bottom line unchanged
                        go.Scatter(
                            x=[self.df_gd['iteration'].min() - 1, self.df_gd['iteration'].max() + 1],
                            y=[0, 0],
                            fill='tonexty',
                            mode='lines',
                            line=dict(width=0),
                            fillcolor='rgba(144, 238, 144, 0.3)'
                        )
                    ],
                    name=str(i)
                )
            )

        fig.frames = frames

        # ===== Layout with shared controls =====
        fig.update_layout(
            height=700,
            title="Gradient Descent Animation",
            xaxis=dict(range=[self.X_MIN - 0.2, self.X_MAX + 0.2], title="x"),
            yaxis=dict(range=[min(self.f(x)) - 0.3, max(self.f(x)) + 0.3], title="f(x)"),
            xaxis2=dict(range=[-1, self.max_iter], title="Iteration"),
            yaxis2=dict(range=[-0.1, max(self.df_gd['losses']) + 0.1], title="Loss"),
            showlegend=False,
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [
                    {
                        'label': 'Play',
                        'method': 'animate',
                        'args': [None, {
                            'frame': {'duration': 600, 'redraw': True},
                            'fromcurrent': True,
                            'transition': {'duration': 200}
                        }]
                    },
                    {
                        'label': 'Pause',
                        'method': 'animate',
                        'args': [[None], {
                            'frame': {'duration': 0, 'redraw': False},
                            'mode': 'immediate',
                            'transition': {'duration': 0}
                        }]
                    }
                ]
            }],
            sliders=[{
                'steps': [
                    {
                        'args': [[str(i)], {
                            'frame': {'duration': 0, 'redraw': True},
                            'mode': 'immediate'
                        }],
                        'label': str(i),
                        'method': 'animate'
                    }
                    for i in self.df_gd['iteration'].unique()
                ],
                'transition': {'duration': 200},
                'x': 0,
                'y': -0.2,
                'currentvalue': {'prefix': 'Iteration: '}
            }]
        )
        
        return fig 


    def plot_loss(self):
        # Create base figure
        fig = go.Figure()

        # Add an empty trace (to be animated later)
        fig.add_trace(
            go.Scatter(
                x=[],
                y=[],
                mode="markers+lines",
                marker=dict(color="red", size=7),
                name="Loss"
            )
        )

        # Create frames for animation
        frames = []
        for i in self.df_gd['iteration'].unique():
            frames.append(
                go.Frame(
                    data=[
                        # leave line untouched → only scatter trace (2nd trace, index 1)
                        go.Scatter(
                            x=self.df_gd.loc[self.df_gd['iteration'] <= i, 'iteration'],
                            y=self.df_gd.loc[self.df_gd['iteration'] <= i, 'losses'],
                            mode="markers+lines",
                            marker=dict(color='red', size=7)
                        )
                    ],
                    name=str(i)
                )
            )

        fig.frames = frames

        # Add animation controls
        fig.update_layout(
            height = 700,
            xaxis_range=[-1, self.max_iter],
            yaxis_range=[-0.1, max(self.df_gd.losses) + 0.1],
            title='Gradient Descent Loss',
            showlegend=True,
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [
                    {
                        'label': 'Play',
                        'method': 'animate',
                        'args': [None, {
                            'frame': {'duration': 600, 'redraw': True},
                            'fromcurrent': True,
                            'transition': {'duration': 200}
                        }]
                    },
                    {
                        'label': 'Pause',
                        'method': 'animate',
                        'args': [[None], {
                            'frame': {'duration': 0, 'redraw': False},
                            'mode': 'immediate',
                            'transition': {'duration': 0}
                        }]
                    }
                ]
            }],
            sliders=[{
                'steps': [
                    {
                        'args': [[str(i)], {'frame': {'duration': 0, 'redraw': True},
                                            'mode': 'immediate'}],
                        'label': str(i),
                        'method': 'animate'
                    }
                    for i in self.df_gd['iteration'].unique()
                ],
                'transition': {'duration': 200},
                'x': 0,
                'y': -0.2,
                'currentvalue': {'prefix': 'Iteration: '}
            }]
        )

        fig.show()


    def plot_iterations(self):

        # Create base figure with the function line
        x = np.linspace(self.X_MIN, self.X_MAX, self.n_pts)
        fig = go.Figure()

        # Add the function line (will stay static in background)
        fig.add_trace(
            go.Scatter(
                x=x,
                y=self.f(x),
                mode='lines',
                name='f(x)',
                line=dict(color='lightgray'),
            )
        )

        # Add the animated scatter points
        fig.add_trace(
            go.Scatter(
                x=[self.df_gd['a_ns'][0]],
                y=[self.df_gd['f_a_ns'][0]],
                mode='markers',
                name='Gradient Descent',
                marker=dict(
                    color='red',
                    size=7
                )
            )
        )

        # Add animation settings
        fig.update_layout(
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [{
                    'label': 'Play',
                    'method': 'animate',
                    'args': [None, {
                        'frame': {'duration': 600, 'redraw': True},
                        'fromcurrent': True,
                        'transition': {'duration': 200}
                    }]
                },
                    {
                        'label': 'Pause',
                        'method': 'animate',
                        'args': [[None], {
                            'frame': {'duration': 0, 'redraw': False},
                            'mode': 'immediate',
                            'transition': {'duration': 0}
                        }]
                    }
                ]
            }],
            sliders=[{
                'steps': [
                    {
                        'args': [[str(i)], {'frame': {'duration': 0, 'redraw': True},
                                            'mode': 'immediate'}],
                        'label': str(i),
                        'method': 'animate'
                    }
                    for i in self.df_gd['iteration'].unique()
                ],
                'transition': {'duration': 200},
                'x': 0,
                'y': -0.2,
                'currentvalue': {'prefix': 'Iteration: '}
            }]
        )

        # Create frames for animation
        frames = [
            go.Frame(
                data=[
                    # Keep the line trace unchanged
                    go.Scatter(x=x, y=self.f(x)),
                    # Update only the scatter points
                    go.Scatter(
                        x=self.df_gd[self.df_gd['iteration'] <= i]['a_ns'],
                        y=self.df_gd[self.df_gd['iteration'] <= i]['f_a_ns']
                    )
                ],
                name=str(i)
            )
            for i in self.df_gd['iteration'].unique()
        ]

        fig.frames = frames

        # Update layout
        fig.update_layout(
            height = 700,
            #width = 800,
            xaxis_range=[self.X_MIN, self.X_MAX],
            yaxis_range=[min(self.f(x)), max(self.f(x))],
            title='Gradient Descent Animation',
            showlegend=True
        )

        fig.show()