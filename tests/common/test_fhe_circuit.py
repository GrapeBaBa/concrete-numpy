"""Test module for Circuit class"""

import filecmp

import concrete.numpy as hnp
from concrete.common.debugging import draw_graph, format_operation_graph


def test_circuit_str(default_compilation_configuration):
    """Test function for `__str__` method of `Circuit`"""

    def f(x):
        return x + 42

    x = hnp.EncryptedScalar(hnp.UnsignedInteger(3))

    inputset = range(2 ** 3)
    circuit = hnp.compile_numpy_function(f, {"x": x}, inputset, default_compilation_configuration)

    assert str(circuit) == format_operation_graph(circuit.op_graph)


def test_circuit_draw(default_compilation_configuration):
    """Test function for `draw` method of `Circuit`"""

    def f(x):
        return x + 42

    x = hnp.EncryptedScalar(hnp.UnsignedInteger(3))

    inputset = range(2 ** 3)
    circuit = hnp.compile_numpy_function(f, {"x": x}, inputset, default_compilation_configuration)

    assert filecmp.cmp(circuit.draw(), draw_graph(circuit.op_graph))
    assert filecmp.cmp(circuit.draw(vertical=False), draw_graph(circuit.op_graph, vertical=False))


def test_circuit_run(default_compilation_configuration):
    """Test function for `run` method of `Circuit`"""

    def f(x):
        return x + 42

    x = hnp.EncryptedScalar(hnp.UnsignedInteger(3))

    inputset = range(2 ** 3)
    circuit = hnp.compile_numpy_function(f, {"x": x}, inputset, default_compilation_configuration)

    for x in inputset:
        assert circuit.run(x) == circuit.engine.run(x)
