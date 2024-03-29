"""Single-layer Perceptron model for supervised machine learning.

Notes
-----
    This script is version v0. It provides the base for all subsequent
    iterations of the project.

Requirements
------------
    See "requirements.txt"
"""

#%% import libraries and modules
import numpy as np  
import matplotlib.pyplot as plt
import os

#%% figure parameters
plt.rcParams['figure.figsize'] = (6,6)
plt.rcParams['font.size']= 14
plt.rcParams['lines.linewidth'] = 3

#%%
class Perceptron:
    """Perceptron class."""
    
    def __init__(self, class_size=100, learning_rate=0.01, num_training_epochs=4):
        self.class_size = class_size
        self.learning_rate = learning_rate
        self.num_training_epochs = num_training_epochs
    
    def make_inputs(self):
        """Create input patterns."""
        # set random seed
        np.random.seed(40)
        # generate class A scatter
        class_a_inputs = np.random.randn(self.class_size, 2) + np.array([0, 4])
        # generate class B scatter
        class_b_inputs = np.random.randn(self.class_size, 2) + np.array([4, 0])
        # concatenate inputs
        input_patterns = np.vstack((class_a_inputs, class_b_inputs))
        return input_patterns
    
    def make_targets(self):
        """Create target patterns."""
        # set class A targets to +1
        class_a_targets = np.zeros([self.class_size, 1]) + 1
        # set class B targets to -1
        class_b_targets = np.zeros([self.class_size, 1]) - 1
        # concatenate targets
        target_patterns = np.vstack((class_a_targets, class_b_targets))
        return target_patterns
    
    def signum_function(self, linear_combiner_output):
        """Apply signum function as activation function."""
        quantized_response = np.sign(linear_combiner_output)
        return quantized_response
    
    def initialize_weights(self):
        """Initialize weights."""
        weights = np.zeros(shape=(1, 2))
        return weights
        
    def initialize_bias(self):
        """Initialize bias."""
        bias = np.array([0], dtype=np.float64)
        return bias
    
    def train_model(self, input_patterns, target_patterns):
        """Train the model parameters to find a linear boundary that separates the data into different classes."""
        # create empty list to store weights
        weights_data = []
        # create empty list to store bias
        bias_data = []
        # initialize weights
        weights = self.initialize_weights()
        # initialize bias
        bias = self.initialize_bias()
        # initialize epoch index
        epoch_index = 0
        while epoch_index < self.num_training_epochs:
            # select input_pattern and corresponding target pattern
            for input_pattern, target_pattern in zip(input_patterns, target_patterns):
                # compute output of linear combiner
                linear_combiner_output = np.dot(weights, input_pattern) + bias
                # apply signum function
                actual_pattern = self.signum_function(linear_combiner_output)
                # compute error
                error = target_pattern - actual_pattern
                # update weights
                weights = weights + self.learning_rate  * error * input_pattern
                # update bias
                bias = bias + self.learning_rate * error
            # store weights
            weights_data.append(weights)
            # store bias
            bias_data.append(bias)
            # increment epoch index
            epoch_index += 1
            
        return weights_data, bias_data

#%% instantiate Perceptron class
model = Perceptron()

#%% create input and target patterns
input_patterns = model.make_inputs()
target_patterns = model.make_targets()

#%% train model
weights_data, bias_data = model.train_model(input_patterns, target_patterns)

#%% plot figures
cwd = os.getcwd()                                                               # get current working directory
fileName = 'images'                                                             # specify filename

# filepath and directory specifications
if os.path.exists(os.path.join(cwd, fileName)) == False:                        # if path does not exist
    os.makedirs(fileName)                                                       # create directory with specified filename
    os.chdir(os.path.join(cwd, fileName))                                       # change cwd to the given path
    cwd = os.getcwd()                                                           # get current working directory
else:
    os.chdir(os.path.join(cwd, fileName))                                       # change cwd to the given path
    cwd = os.getcwd()                                                           # get current working directory

"""
   -----------------------------------------
   Ax + By + C = 0    |  w1x1 + w2x2 + b = 0
   By = -Ax -C        |  w2x2 = -w1x1 -b
   y  = -A/Bx -C/B    |  x2 = -w1/w2x1 -b/w2
   slope = -A/B       |  slope = -w1/w2
   y_intercept = -C/B |  y_intercept = -b/w2
   -----------------------------------------
"""

# specify x-axis data
x_min = input_patterns[:, 0].min()
x_max = input_patterns[:, 0].max()
x_data = np.linspace(x_min, x_max, 10)

# specify class A and class B from input patterns
class_a = input_patterns[:model.class_size, :]
class_b = input_patterns[model.class_size:, :]

# specify subplot parameters
num_subplots = model.num_training_epochs
nrows = int(np.ceil(np.sqrt(num_subplots)))
ncols = int(np.ceil(num_subplots / nrows))

# show subplots
fig, axes = plt.subplots(nrows=nrows, ncols=ncols)
axes = axes.ravel()
for epoch_index in range(model.num_training_epochs):
    slope = -weights_data[epoch_index].item(0)/weights_data[epoch_index].item(1)
    y_intercept = -bias_data[epoch_index]/weights_data[epoch_index].item(1)
    y_data = slope * x_data + y_intercept
    
    axes[epoch_index].scatter(class_a[:, 0], class_a[:, 1], s=20, color='red', marker='o', label='class A')
    axes[epoch_index].scatter(class_b[:, 0], class_b[:, 1], s=20, color='blue', marker='x', label='class B')
    axes[epoch_index].plot(x_data, y_data, color='k', linestyle='-')
    
    axes[epoch_index].set_xlim(x_min-1, x_max+1)
    axes[epoch_index].set_ylim(input_patterns[:, 1].min()-1, input_patterns[:, 1].max()+1)
    
    axes[epoch_index].set_xticks([])
    axes[epoch_index].set_yticks([])  
    
    axes[epoch_index].set_title(f'epoch {epoch_index+1}')    
    axes[epoch_index].set_xlabel('x')
    axes[epoch_index].set_ylabel('y')
fig.tight_layout()
fig.savefig(os.path.join(os.getcwd(), 'figure_1'))
