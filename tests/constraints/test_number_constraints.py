from contextlib import suppress
from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis.errors import InvalidArgument
from hypothesis.strategies import decimals, floats, integers
from pydantic import condecimal, confloat, conint

from pydantic_factories.constraints.numbers import (
    handle_constrained_decimal,
    handle_constrained_float,
    handle_constrained_int,
)

# floats


def test_handle_constrained_float_without_constraints():
    result = handle_constrained_float(confloat())
    assert isinstance(result, float)


@given(floats(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000))
def test_handle_constrained_float_handles_ge(minimum):
    result = handle_constrained_float(confloat(ge=minimum))
    assert result >= minimum


@given(floats(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000))
def test_handle_constrained_float_handles_gt(minimum):
    result = handle_constrained_float(confloat(gt=minimum))
    assert result > minimum


@given(floats(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000))
def test_handle_constrained_float_handles_le(maximum):
    result = handle_constrained_float(confloat(le=maximum))
    assert result <= maximum


@given(floats(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000))
def test_handle_constrained_float_handles_lt(maximum):
    result = handle_constrained_float(confloat(lt=maximum))
    assert result < maximum


@given(floats(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000))
def test_handle_constrained_float_handles_multiple_of(multiple_of):
    result = handle_constrained_float(confloat(multiple_of=multiple_of))
    assert result % multiple_of == 0 if multiple_of != 0 else True


def test_handle_constrained_float_handles_multiple_of_zero_value():
    # due to a bug in the pydantic hypothesis plugin, this code can only be tested in isolation
    # see: https://github.com/samuelcolvin/pydantic/issues/3418
    assert handle_constrained_float(confloat(multiple_of=0)) == 0


@given(
    floats(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000),
    floats(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000),
)
def test_handle_constrained_float_handles_multiple_of_with_lt(val1, val2):
    multiple_of, max_value = sorted([val1, val2])
    if multiple_of != 0:
        if multiple_of < max_value - 0.0001:
            result = handle_constrained_float(confloat(multiple_of=multiple_of, lt=max_value))
            assert result % multiple_of == 0 if multiple_of != 0 else True
        else:
            with pytest.raises(AssertionError):
                handle_constrained_float(confloat(multiple_of=multiple_of, lt=max_value))


@given(
    floats(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000),
    floats(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000),
)
def test_handle_constrained_float_handles_multiple_of_with_le(val1, val2):
    multiple_of, max_value = sorted([val1, val2])
    if multiple_of != 0:
        if multiple_of < max_value:
            result = handle_constrained_float(confloat(multiple_of=multiple_of, le=max_value))
            assert result % multiple_of == 0
        else:
            with pytest.raises(AssertionError):
                handle_constrained_float(confloat(multiple_of=multiple_of, le=max_value))


@given(
    floats(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000),
    floats(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000),
)
def test_handle_constrained_float_handles_multiple_of_with_ge(val1, val2):
    min_value, multiple_of = sorted([val1, val2])
    if multiple_of != 0:
        result = handle_constrained_float(confloat(multiple_of=multiple_of, ge=min_value))
        assert result % multiple_of == 0


@given(
    floats(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000),
    floats(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000),
)
def test_handle_constrained_float_handles_multiple_of_with_gt(val1, val2):
    min_value, multiple_of = sorted([val1, val2])
    if multiple_of != 0:
        result = handle_constrained_float(confloat(multiple_of=multiple_of, gt=min_value))
        assert result % multiple_of == 0


@given(
    floats(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000),
    floats(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000),
    floats(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000),
)
def test_handle_constrained_float_handles_multiple_of_with_ge_and_le(val1, val2, val3):
    min_value, multiple_of, max_value = sorted([val1, val2, val3])
    with suppress(InvalidArgument):
        # again, a pydantic / hypothesis error
        if round(multiple_of) != 0:
            if multiple_of < max_value and min_value < max_value:
                result = handle_constrained_float(confloat(multiple_of=multiple_of, ge=min_value, le=max_value))
                assert round(result, 2) % round(multiple_of, 2) == 0
            else:
                with pytest.raises(AssertionError):
                    handle_constrained_float(confloat(multiple_of=multiple_of, ge=min_value, le=max_value))


# ints


def test_handle_constrained_int_without_constraints():
    result = handle_constrained_int(conint())
    assert isinstance(result, int)


@given(integers(min_value=-1000000000, max_value=1000000000))
def test_handle_constrained_int_handles_ge(minimum):
    result = handle_constrained_int(conint(ge=minimum))
    assert result >= minimum


@given(integers(min_value=-1000000000, max_value=1000000000))
def test_handle_constrained_int_handles_gt(minimum):
    result = handle_constrained_int(conint(gt=minimum))
    assert result > minimum


@given(integers(min_value=-1000000000, max_value=1000000000))
def test_handle_constrained_int_handles_le(maximum):
    result = handle_constrained_int(conint(le=maximum))
    assert result <= maximum


@given(integers(min_value=-1000000000, max_value=1000000000))
def test_handle_constrained_int_handles_lt(maximum):
    result = handle_constrained_int(conint(lt=maximum))
    assert result < maximum


@given(integers(min_value=-1000000000, max_value=1000000000))
def test_handle_constrained_int_handles_multiple_of(multiple_of):
    result = handle_constrained_int(conint(multiple_of=multiple_of))
    assert result % multiple_of == 0 if multiple_of != 0 else True


def test_handle_constrained_int_handles_multiple_of_zero_value():
    # due to a bug in the pydantic hypothesis plugin, this code can only be tested in isolation
    # see: https://github.com/samuelcolvin/pydantic/issues/3418
    assert handle_constrained_int(conint(multiple_of=0)) == 0


@given(
    integers(min_value=-1000000000, max_value=1000000000),
    integers(min_value=-1000000000, max_value=1000000000),
)
def test_handle_constrained_int_handles_multiple_of_with_lt(val1, val2):
    multiple_of, max_value = sorted([val1, val2])
    if multiple_of != 0:
        if multiple_of < max_value - 1:
            result = handle_constrained_int(conint(multiple_of=multiple_of, lt=max_value))
            assert result % multiple_of == 0 if multiple_of != 0 else True
        else:
            with pytest.raises(AssertionError):
                handle_constrained_int(conint(multiple_of=multiple_of, lt=max_value))


@given(
    integers(min_value=-1000000000, max_value=1000000000),
    integers(min_value=-1000000000, max_value=1000000000),
)
def test_handle_constrained_int_handles_multiple_of_with_le(val1, val2):
    multiple_of, max_value = sorted([val1, val2])
    if multiple_of != 0:
        if multiple_of < max_value:
            result = handle_constrained_int(conint(multiple_of=multiple_of, le=max_value))
            assert result % multiple_of == 0
        else:
            with pytest.raises(AssertionError):
                handle_constrained_int(conint(multiple_of=multiple_of, le=max_value))


@given(
    integers(min_value=-1000000000, max_value=1000000000),
    integers(min_value=-1000000000, max_value=1000000000),
)
def test_handle_constrained_int_handles_multiple_of_with_ge(val1, val2):
    min_value, multiple_of = sorted([val1, val2])
    if multiple_of != 0:
        result = handle_constrained_int(conint(multiple_of=multiple_of, ge=min_value))
        assert result % multiple_of == 0


@given(
    integers(min_value=-1000000000, max_value=1000000000),
    integers(min_value=-1000000000, max_value=1000000000),
)
def test_handle_constrained_int_handles_multiple_of_with_gt(val1, val2):
    min_value, multiple_of = sorted([val1, val2])
    if multiple_of != 0:
        result = handle_constrained_int(conint(multiple_of=multiple_of, gt=min_value))
        assert result % multiple_of == 0


@given(
    integers(min_value=-1000000000, max_value=1000000000),
    integers(min_value=-1000000000, max_value=1000000000),
    integers(min_value=-1000000000, max_value=1000000000),
)
def test_handle_constrained_int_handles_multiple_of_with_ge_and_le(val1, val2, val3):
    min_value, multiple_of, max_value = sorted([val1, val2, val3])
    with suppress(InvalidArgument):
        # again, a pydantic / hypothesis error
        if round(multiple_of) != 0:
            if multiple_of < max_value and min_value < max_value:
                result = handle_constrained_int(conint(multiple_of=multiple_of, ge=min_value, le=max_value))
                assert round(result, 2) % round(multiple_of, 2) == 0
            else:
                with pytest.raises(AssertionError):
                    handle_constrained_int(conint(multiple_of=multiple_of, ge=min_value, le=max_value))


# decimals


def test_handle_constrained_decimal_without_constraints():
    result = handle_constrained_decimal(condecimal())
    assert isinstance(result, Decimal)


@given(decimals(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000))
def test_handle_constrained_decimal_handles_ge(minimum):
    result = handle_constrained_decimal(condecimal(ge=minimum))
    assert result >= minimum


@given(decimals(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000))
def test_handle_constrained_decimal_handles_gt(minimum):
    result = handle_constrained_decimal(condecimal(gt=minimum))
    assert result > minimum


@given(decimals(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000))
def test_handle_constrained_decimal_handles_le(maximum):
    result = handle_constrained_decimal(condecimal(le=maximum))
    assert result <= maximum


@given(decimals(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000))
def test_handle_constrained_decimal_handles_lt(maximum):
    result = handle_constrained_decimal(condecimal(lt=maximum))
    assert result < maximum


def test_handle_constrained_decimal_raises_for_non_zero_multiple_of():
    with pytest.raises(AssertionError):
        handle_constrained_decimal(condecimal(multiple_of=Decimal(1)))


def test_handle_constrained_decimal_handles_multiple_of_zero_value():
    # due to a bug in the pydantic hypothesis plugin, this code can only be tested in isolation
    # see: https://github.com/samuelcolvin/pydantic/issues/3418
    assert handle_constrained_decimal(condecimal(multiple_of=0)) == 0