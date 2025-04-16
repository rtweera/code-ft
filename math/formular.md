# Formular

## 1. Inference memory requirement

**Note:** Memory refers to the total amount of RAM or GPU memory required to store the model parameters, activations, and gradients during inference.

> Memory = Parameter count * Precision

e.g. for a model with 1 billion parameters and using 16-bit precision (aka half precision), the memory requirement would be:

memory = 1 billion * 2 bytes = 2 billion bytes = 2 GB