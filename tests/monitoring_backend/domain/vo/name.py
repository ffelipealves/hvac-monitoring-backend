from pydantic_core import ValidationError
import pytest
from monitoring_backend.domain.vo.name import Name
from monitoring_backend.domain.exceptions.common import InvalidNameException

@pytest.fixture
def valid_names():
    return [
        "João Silva",
        "Maria",
        "A" * 100,
        "  Carlos Alberto  ",
        "José",
        "Ana Paula",
        "Luiz",
        "Érica",
        "O'Connor",
        "Jean-Luc",
    ]

@pytest.mark.parametrize("name", [
    "João Silva",
    "Maria",
    "A" * 100,
    "  Carlos Alberto  ",
    "José",
    "Ana Paula",
    "Luiz",
    "Érica",
    "O'Connor",
    "Jean-Luc",
])
def test_valid_name_creation(name):
    obj = Name(value=name)
    assert isinstance(obj, Name)
    assert obj.value == name.strip()
    assert str(obj) == obj.value
    assert repr(obj) == f"Name(value={obj.value!r})"

@pytest.mark.parametrize("name", [
    "",
    "  ",
    "A",
    "AB",
    "A" * 101,
    None,
])
def test_invalid_name_creation(name):
    if name is None:
        with pytest.raises(ValidationError):
            Name(value=name)
    else:
        with pytest.raises(InvalidNameException):
            Name(value=name)

def test_equality_with_name_and_str(valid_names):
    for name in valid_names:
        obj = Name(value=name)
        # Equality with another Name instance
        obj2 = Name(value=name)
        assert obj == obj2
        # Equality with string
        assert obj == name.strip()
        # Inequality with different name
        assert obj != "Outro Nome"

def test_inequality_with_other_types(valid_names):
    obj = Name(value=valid_names[0])
    assert obj != 123
    assert obj != None
    assert obj != ["João Silva"]

def test_frozen_object(valid_names):
    obj = Name(value=valid_names[0])
    with pytest.raises(ValidationError):
        obj.value = "Novo Nome"

def test_strip_whitespace_on_creation():
    obj = Name(value="   João   ")
    assert obj.value == "João"

def test_repr_and_str_methods():
    obj = Name(value="Maria")
    assert repr(obj) == "Name(value='Maria')"
    assert str(obj) == "Maria"