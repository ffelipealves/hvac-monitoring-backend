import pytest
from unittest.mock import MagicMock
from monitoring_backend.application.usecases.campus.create_campus import CreateCampus
from monitoring_backend.application.usecases.interfaces.campus.create_campus import CreateCampusInputDTO
from monitoring_backend.domain.vo.name import Name
from monitoring_backend.domain.entity.campus import Campus
from monitoring_backend.application.dto.errors import ErrorResponseDTO

# Fixtures para dados válidos e inválidos
@pytest.fixture
def valid_name():
    return "Empresa Teste"

@pytest.fixture
def valid_cnpj():
    return "12345678000195"  # CNPJ válido (ajuste conforme lib validate_docbr)

@pytest.fixture
def campus_repository_mock():
    repo = MagicMock()
    repo.find_by_name.return_value = None
    repo.find_by_cnpj.return_value = None
    repo.create.side_effect = lambda campus: Campus(id=1, name=campus.name, cnpj=campus.cnpj)
    return repo

@pytest.fixture
def usecase(campus_repository_mock):
    return CreateCampus(campus_repository=campus_repository_mock)

# Caminho de sucesso
def test_create_campus_success(usecase, valid_name, valid_cnpj, campus_repository_mock):
    input_dto = CreateCampusInputDTO(name=valid_name, cnpj=valid_cnpj)
    output = usecase.execute(input_dto)
    assert hasattr(output, "id")
    assert output.name == valid_name
    assert output.cnpj == valid_cnpj
    campus_repository_mock.create.assert_called_once()

# Nome duplicado
def test_create_campus_duplicate_name(usecase, valid_name, valid_cnpj, campus_repository_mock):
    campus_repository_mock.find_by_name.return_value = Campus(id=2, name=Name(value=valid_name))
    input_dto = CreateCampusInputDTO(name=valid_name, cnpj=valid_cnpj)
    output = usecase.execute(input_dto)
    assert isinstance(output, ErrorResponseDTO)
    assert any(e.code == "DUPLICATE_NAME" for e in output.errors)

# CNPJ duplicado
def test_create_campus_duplicate_cnpj(usecase, valid_name, valid_cnpj, campus_repository_mock):
    campus_repository_mock.find_by_cnpj.return_value = Campus(id=3, name=Name(value=valid_name))
    input_dto = CreateCampusInputDTO(name=valid_name, cnpj=valid_cnpj)
    output = usecase.execute(input_dto)
    assert isinstance(output, ErrorResponseDTO)
    assert any(e.code == "DUPLICATE_CNPJ" for e in output.errors)

# Dados inválidos no VO Name
@pytest.mark.parametrize("invalid_name", ["", "A", "AB", None, "  "])
def test_create_campus_invalid_name(usecase, invalid_name, valid_cnpj):
    input_dto = CreateCampusInputDTO(name=invalid_name, cnpj=valid_cnpj)
    output = usecase.execute(input_dto)
    assert isinstance(output, ErrorResponseDTO)
    assert any(e.code == "INVALID_NAME" for e in output.errors)

# Dados inválidos no VO Cnpj
@pytest.mark.parametrize("invalid_cnpj", ["123", "00000000000000", "abcdefghijklmno", None])
def test_create_campus_invalid_cnpj(usecase, valid_name, invalid_cnpj):
    input_dto = CreateCampusInputDTO(name=valid_name, cnpj=invalid_cnpj)
    output = usecase.execute(input_dto)
    assert isinstance(output, ErrorResponseDTO)
    assert any(e.code == "INVALID_CNPJ" for e in output.errors)

# Testa múltiplos erros
def test_create_campus_multiple_errors(usecase):
    input_dto = CreateCampusInputDTO(name="", cnpj="123")
    output = usecase.execute(input_dto)
    assert isinstance(output, ErrorResponseDTO)
    codes = [e.code for e in output.errors]
    assert "INVALID_NAME" in codes
    assert "INVALID_CNPJ" in codes
