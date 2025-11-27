import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from sympy import latex, sympify


# CATALOGUE:
# convex functions we define and use for the PS activity

# Shifted squared
def shifted_squared(x):
    return x**2 + 0.5*x
def grad_shifted_squared(x):
    return 2*x + 0.5

# Oscillating square
def square_sin(x):
    return x ** 2 + 0.1 * np.sin(10 * x)
def grad_square_sin(x):
    return 2 * x + np.cos(10 * x)

# Absolute value, non-differentiable at 0
def absolute(x):
    return np.abs(x)
def grad_absolute(x):
    return np.sign(x) # fyi: np.sign(0) = 0

# Double valley - polynomial function that has 2 minima
def double_valley(x):
    return ((x + 4) ** 4 - 15 * (x + 4) ** 3 + 80 * (x + 4) ** 2 - 180 * (x + 4) + 144) / 10
def grad_double_valley(x):
    return (-4 - 8 * x + 3 * x ** 2 + 4 * x ** 3) / 10

#TODO: NB i am not sure using these 2 functions is a good idea, computing their loss function might be too confusing for the students
#
# # Cubic function: has no minima, either global nor minimum TODO: dangerous computation of its loss!!!
# def cube(x):
#     return x ** 3
# def grad_cube(x):
#     return 3 * x ** 2

# # Another cubic function that has no global minimum but a local one
# def deep_cubic(x):
#     return x ** 3 - 4 * x
# def grad_deep_cubic(x):
#     return 3* x ** 2 - 4 

# Should we change the function every 5 simulations? Every 3 simulations?
change_every = 3
fs = [shifted_squared, square_sin, absolute, double_valley]#, cube, deep_cubic] 
grads = [grad_shifted_squared, grad_square_sin, grad_absolute, grad_double_valley]#, grad_cube, grad_deep_cubic] 
fs_latex = ["x**2 + 0.5*x", "x ** 2 + 0.1 * sin(10 * x)", "abs(x)", "((x + 4) ** 4 - 15 * (x + 4) ** 3 + 80 * (x + 4) ** 2 - 180 * (x + 4) + 144) / 10"]

class GradientDescent:
    def __init__(self, X_MIN, X_MAX, sim_counter, n_pts = 500, max_iter = 15):
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
        self.all_fs = fs
        self.all_grad_fs = grads
        self.all_fs_latex = [latex(sympify(f)) for f in fs_latex]
        # We loop over all functions to get a different one every X run of simulation (X set by change_every)
        self.f = self.all_fs[(sim_counter // change_every) % len(self.all_fs)]
        self.grad_f = self.all_grad_fs[(sim_counter // change_every) % len(self.all_fs)]
        self.f_in_latex = self.all_fs_latex[(sim_counter // change_every) % len(self.all_fs_latex)]
        
        # Useful variables to store for computations
        self.true_min = None # storing the true min value of the function for computations
        


    def set_eta(self, eta_value, verbose=False):
        """Set the learning rate (eta) to the given value."""
        self.eta = eta_value
        if verbose:
            print(f"Using a learning rate eta η = {self.eta}")


    def set_a_0(self, a_0_value, verbose=False):
        """Set the initial point (a₀) to the given value."""
        self.a_0 = a_0_value
        if verbose:
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
    
    
    def set_true_min(self, verbose=False):
        self.true_min = self.find_min_f()
        if verbose:
            print(f"The actual minimum of f is at x = {self.true_min:.2f} with f(x) = {self.f(self.true_min):.2f}")
    
    
    def compute_loss(self, x):
        if self.true_min is None:
            self.set_true_min()
        return abs(self.f(x) - self.f(self.true_min))
    

    def plot_naked_function(self):
        """Plot the shape of the current function to give insight on what the fucntion looks like"""

        x = np.linspace(self.X_MIN, self.X_MAX, self.n_pts)
        fig = px.line(x=x, y=self.f(x))
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        
        return fig


    def plot_iterations_and_loss(self):
        """Plot the function f and the iterative steps of the proposed algorithm, along with the corresponding losses"""
        
        # Create subplot layout (1 row, 2 columns)
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Gradient Descent Path", "Loss Curve"))

        # ===== Left subplot: f(x) + GD path =====
        
        x = np.linspace(self.X_MIN, self.X_MAX, self.n_pts)
        fig.add_trace(
            go.Scatter(x=x, y=self.f(x), mode="lines", name="f(x)", line=dict(color="lightgray")),
            row=1, col=1
        )
        
        # Green goal area around f(true_min)
        for fill_y, fill_opt in [
            ([self.f(self.true_min) + 0.05] * self.n_pts, None),
            ([self.f(self.true_min) - 0.05] * self.n_pts, 'tonexty')
        ]:
            fig.add_trace(
                go.Scatter(
                    x=x, y=fill_y,
                    fill=fill_opt,
                    mode='lines',
                    line=dict(width=0),
                    fillcolor='rgba(144, 238, 144, 0.3)' if fill_opt else None,
                    showlegend=False,
                    hoverinfo='skip'
                ),
                row=1, col=1
            )
        
        # Circle around true minimum
        fig.add_trace(
            go.Scatter(
                x=[self.true_min], y=[self.f(self.true_min)],
                mode='markers',
                marker=dict(size=7, color='rgba(144, 238, 144, 0.5)',
                            line=dict(color='lightgreen', width=2)),
                showlegend=False, hoverinfo='skip'
            ),
            row=1, col=1
        )
        
        # GD initial point
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
        fig.add_trace(
            go.Scatter(
                x=[], y=[],
                mode="markers+lines",
                marker=dict(color="red", size=7),
                name="Loss"
            ),
            row=1, col=2
        )

        # Green goal band for loss
        for fill_y, fill_opt in [([0.05, 0.05], None), ([0, 0], 'tonexty')]:
            fig.add_trace(
                go.Scatter(
                    x=[self.df_gd['iteration'].min() - 1, self.df_gd['iteration'].max() + 1],
                    y=fill_y,
                    fill=fill_opt,
                    mode='lines',
                    line=dict(width=0),
                    fillcolor='rgba(144, 238, 144, 0.3)' if fill_opt else None,
                    showlegend=False,
                    hoverinfo='skip'
                ),
                row=1, col=2
            )

        # ===== Frames =====
        frames = []
        xshift, yshift = 20, 10  # fixed offset for all labels

        for i in self.df_gd['iteration'].unique():
            data_up_to_i = self.df_gd[self.df_gd['iteration'] <= i]

            # Only show labels for visible points
            annotations = [
                dict(
                    x=row['a_ns'],
                    y=row['f_a_ns'],
                    text=f"a{int(row['iteration'])}",
                    showarrow=False,
                    xshift=xshift,
                    yshift=yshift,
                    font=dict(size=12, color="darkred"),
                    xref='x', yref='y'
                )
                for _, row in data_up_to_i.iterrows()
            ]

            frames.append(
                go.Frame(
                    data=[
                        # Left plot traces
                        go.Scatter(x=x, y=self.f(x)),  # f(x)
                        go.Scatter(x=x, y=[self.f(self.true_min) + 0.05]*self.n_pts),
                        go.Scatter(x=x, y=[self.f(self.true_min) - 0.05]*self.n_pts),
                        go.Scatter(x=[self.true_min], y=[self.f(self.true_min)]),
                        go.Scatter(
                            x=data_up_to_i['a_ns'],
                            y=data_up_to_i['f_a_ns'],
                            mode="markers",
                            marker=dict(color="red", size=7)
                        ),
                        # Right plot traces
                        go.Scatter(
                            x=data_up_to_i['iteration'],
                            y=data_up_to_i['losses'],
                            mode="markers+lines",
                            marker=dict(color="red", size=7)
                        ),
                        go.Scatter(x=[self.df_gd['iteration'].min() - 1, self.df_gd['iteration'].max() + 1], y=[0.05, 0.05]),
                        go.Scatter(x=[self.df_gd['iteration'].min() - 1, self.df_gd['iteration'].max() + 1], y=[0, 0])
                    ],
                    layout=go.Layout(annotations=annotations),
                    name=str(i)
                )
            )

        fig.frames = frames

        # ===== Layout =====
        fig.update_layout(
            height=700,
            xaxis=dict(range=[self.X_MIN - 0.2, self.X_MAX + 0.2], title="x"),
            yaxis=dict(range=[min(self.f(x)) - 0.3, max(self.f(x)) + 0.3], title="f(x)"),
            xaxis2=dict(range=[-1, self.max_iter], title="Iteration"),
            yaxis2=dict(range=[-0.1, max(self.df_gd['losses']) + 0.1], title="Loss"),
            showlegend=False,
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [
                    {'label': 'Play', 'method': 'animate',
                    'args': [None, {'frame': {'duration': 600, 'redraw': True},
                                    'fromcurrent': True, 'transition': {'duration': 200}}]},
                    {'label': 'Pause', 'method': 'animate',
                    'args': [[None], {'frame': {'duration': 0, 'redraw': False},
                                    'mode': 'immediate', 'transition': {'duration': 0}}]}
                ]
            }],
            sliders=[{
                'steps': [
                    {'args': [[str(i)], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate'}],
                    'label': str(i), 'method': 'animate'}
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