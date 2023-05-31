# PrepareForAttack
The CounterStrike coaching staff has requested we get as much insight as possible about our opponents so that we can learn their common strategies in order to predict future behavior and, of course, increase our chances of winning 😈🏆

# Output
[Click here to view the output of this code](https://docs.google.com/document/d/15f7w2Pmxhxv6r1r70ZA09LzP9v7w18PZt18cW-m9eUk/edit#heading=h.5ellydiuruqq "Output")
NOTE:
The `game_state_frame_data.pickle` file was too large to be included in this repo. However, be sure to include it in your local repository when running this code.

# SolutionForStakeholders
Here's a potential solution for stakeholders who want to get relevant and useful information out of this code without actually having to run it themselves.

We should implement a user-friendly web interface using HTML, CSS, and JavaScript. The interface should have intuitive controls like dropdown menus or checkboxes to select the desired analysis/insights. The back-end can be built using a web framework like Flask or Django in Python and will handle user requests, interact with the data, and perform the necessary calculations and filtering. Upon selecting the desired analysis or metrics, the relevant output should be displayed.  

# Required Libraries 
Be sure to install the required libraries below:
- `pandas` to create DataFrame object and make reading and writing data from the pickle file easier.
- `matplotlib` for data visulization
- `seaborn` to plot the heatmap with values added by scipy
- `shapely` to create polygon object and check if point is within boundary
- `scipy` griddata adds grid values using the existing data points
- `numpy` for array
