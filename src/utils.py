import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def f(x):
    # ultimate goal: find a 2D function
    return x * x + 0.1 * np.sin(10 * x)

def grad_f(x):
    return 2 * x + np.cos(10 * x)

class GradientDescent:
    def __init__(self, X_MIN, X_MAX, n_pts = 300, max_iter = 15):
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
        
        # Defining the convex function we will be working with
        self.f = f
        self.grad_f = grad_f


    def set_eta(self, eta_value):
        """Set the learning rate (eta) to the given value."""
        self.eta = eta_value
        print(f"Using a learning rate eta (η) = {self.eta}")

    def set_a_0(self, a_0_value):
        """Set the initial point (a_0) to the given value."""
        self.a_0 = a_0_value
        print(f"Using the initial point a_0: {self.a_0}")

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
            a_n_1 = a_n - self.eta * self.grad_f(a_n) #TODO: this formula should be modified by the guess of the user
            a_ns[i] = a_n_1
            losses[i] = self.compute_loss(a_n_1)
            a_n = a_n_1
        
        # Storing the steps of the algorithm into a dataframe
        self.df_gd = pd.DataFrame({'a_ns': a_ns, 'f_a_ns': self.f(a_ns), 'losses': losses, 'iteration': np.arange(self.max_iter)})
        
        return self.df_gd


    def find_min_f(self):
        # 1D for now but should be 2D later on
        x = np.linspace(self.X_MIN, self.X_MAX, self.n_pts)
        true_min = min(self.f(x))
        
        return true_min
    
    def compute_loss(self, x):
        true_min = self.find_min_f()
        return abs(x - true_min)
    
    
    
    
    def plot_iterations_and_loss(self):
        """Plot the function f and the iterative steps of the proposed algorithm, along with the corresponding losses"

        Args:
            f (function): convex function
        """
        # Create subplot layout (1 row, 2 columns)
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Gradient Descent Path", "Loss Curve"))

        # ===== Left subplot: f(x) + GD path =====
        x = np.linspace(self.X_MIN, self.X_MAX, 300)
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
                x=[],
                y=[],
                mode="markers+lines",
                marker=dict(color="red", size=7),
                name="Loss"
            ),
            row=1, col=2
        )

        # ===== Frames: update both subplots together =====
        frames = []
        for i in self.df_gd['iteration'].unique():
            frames.append(
                go.Frame(
                    data=[
                        # Left: 
                        # Keep the line trace unchanged
                        go.Scatter(x=x, y=f(x)),
                        # Then update GD points
                        go.Scatter(
                            x=self.df_gd.loc[self.df_gd['iteration'] <= i, 'a_ns'],
                            y=self.df_gd.loc[self.df_gd['iteration'] <= i, 'f_a_ns'],
                            marker=dict(color="red", size=7)
                        ),
                        # Right: update loss curve
                        go.Scatter(
                            x=self.df_gd.loc[self.df_gd['iteration'] <= i, 'iteration'],
                            y=self.df_gd.loc[self.df_gd['iteration'] <= i, 'losses'],
                            mode="markers+lines",
                            marker=dict(color="red", size=7)
                        )
                    ],
                    name=str(i)
                )
            )

        fig.frames = frames

        # ===== Layout with shared controls =====
        fig.update_layout(
            height=700,
            #width=1000,
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

        fig.show()


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