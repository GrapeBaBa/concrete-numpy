# Compiling and Executing a Numpy Function

## Importing necessary components

Everything you need to compile and execute homomorphic functions is included in a single module. You can import it like so:

```python
import concrete.numpy as hnp
```

## Defining a function to compile

You need to have a python function that follows the [limits](../explanation/fhe_and_framework_limits.md) of **Concrete Numpy**. Here is a simple example:

<!--pytest-codeblocks:cont-->
```python
def f(x, y):
    return x + y
```

## Compiling the function

To compile the function, you need to identify the inputs that it is expecting. In the example function above, `x` and `y` could be scalars or tensors (though, for now, only dot between tensors are supported), they can be encrypted or clear, they can be signed or unsigned, they can have different bit-widths. So, we need to know what they are beforehand. We can do that like so:

<!--pytest-codeblocks:cont-->
```python
x = "encrypted"
y = "encrypted"
```

In this configuration, both `x` and `y` will be encrypted values.

We also need an inputset. It is to determine the bit-widths of the intermediate results. It should be an iterable yielding tuples in the same order as the inputs of the function to compile. There should be at least 10 inputs in the input set to avoid warnings (except for functions with less than 10 possible inputs). The warning is there because the bigger the input set, the better the bounds will be.

<!--pytest-codeblocks:cont-->
```python
inputset = [(2, 3), (0, 0), (1, 6), (7, 7), (7, 1), (3, 2), (6, 1), (1, 7), (4, 5), (5, 4)]
```

Finally, we can compile our function to its homomorphic equivalent.

<!--pytest-codeblocks:cont-->
```python
compiler = hnp.NPFHECompiler(
    f, {"x": x, "y": y},
)
circuit = compiler.compile_on_inputset(inputset)

# If you want, you can separate tracing and compilation steps like so:

# You can either evaluate in one go:
compiler.eval_on_inputset(inputset)

# Or progressively:
for input_values in inputset:
    compiler(*input_values)

# You can print the traced graph:
print(str(compiler))

# Outputs

# %0 = x                  # EncryptedScalar<uint3>
# %1 = y                  # EncryptedScalar<uint3>
# %2 = add(%0, %1)        # EncryptedScalar<uint4>
# return %2

# Or draw it
compiler.draw_graph(show=True)

circuit = compiler.get_compiled_fhe_circuit()

```

Here is the graph from the previous code block drawn with `draw_graph`:

![Drawn graph of previous code block](../../_static/howto/compiling_and_executing_example_graph.png)

## Performing homomorphic evaluation

You can use `.run(...)` method of `FHECircuit` returned by `hnp.compile_numpy_function(...)` to perform fully homomorphic evaluation. Here are some examples:

<!--pytest-codeblocks:cont-->
```python
circuit.run(3, 4)
# 7
circuit.run(1, 2)
# 3
circuit.run(7, 7)
# 14
circuit.run(0, 0)
# 0
```

```{caution}
Be careful about the inputs, though.
If you were to run with values outside the range of the inputset, the result might not be correct.
```

Today, we cannot simulate a client / server API in python, but it is for very soon. Then, we will have:
    - a `keygen` API, which is used to generate both public and private keys
    - an `encrypt` API, which happens on the user's device, and is using private keys
    - a `run_inference` API, which happens on the untrusted server and only uses public material
    - a `encrypt` API, which happens on the user's device to get final clear result, and is using private keys

## Further reading

- [Working With Floating Points Tutorial](../tutorial/working_with_floating_points.md)
- [Table Lookup Tutorial](../tutorial/table_lookup.md)
- [Compiling a torch model](../howto/compiling_torch_model.md)
