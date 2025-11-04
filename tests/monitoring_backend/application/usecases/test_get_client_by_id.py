import pytest
from unittest.mock import MagicMock
from monitoring_backend.application.usecases.campus.get_campus_by_id import GetCampusById
from monitoring_backend.application.usecases.interfaces.campus.get_campus_by_id import GetCampusByIdInputDTO
from monitoring_backend.domain.entity.campus import Campus
from monitoring_backend.domain.vo.name import Name
from monitoring_backend.application.dto.errors import ErrorResponseDTO

@pytest.fixture
def valid_id():
    return 1

@pytest.fixture(params=[None, -1, 0, 999])
def invalid_ids(request):
    return request.param

@pytest.fixture
def valid_name():
    return Name(value="Empresa Teste")

@pytest.fixture
def campus_repository_mock():
    repo = MagicMock()
    repo.get.return_value = None
    return repo

@pytest.fixture
def usecase(campus_repository_mock):
    return GetCampusById(campus_repository=campus_repository_mock)

# Caminho de sucesso
def test_get_campus_by_id_success(usecase, valid_id, valid_name, valid_cnpj, campus_repository_mock):
    campus = Campus(id=valid_id, name=valid_name, cnpj=valid_cnpj)
    campus_repository_mock.get.return_value = campus
    input_dto = GetCampusByIdInputDTO(id=valid_id)
    output = usecase.execute(input_dto)
    assert output.id == valid_id
    assert output.name == str(valid_name)
    assert output.cnpj == str(valid_cnpj)
    campus_repository_mock.get.assert_called_once_with(valid_id)

# Campuse não encontrado
def test_get_campus_by_id_not_found(usecase, valid_id, campus_repository_mock):
    campus_repository_mock.get.return_value = None
    input_dto = GetCampusByIdInputDTO(id=valid_id)
    output = usecase.execute(input_dto)
    assert isinstance(output, ErrorResponseDTO)
    assert any(e.code == "CLIENT_NOT_FOUND" for e in output.errors)
    assert any(str(valid_id) in e.message for e in output.errors)

# Testa ids inválidos
def test_get_campus_by_id_invalid_id(usecase, invalid_ids, campus_repository_mock):
    campus_repository_mock.get.return_value = None
    input_dto = GetCampusByIdInputDTO(id=invalid_ids)
    output = usecase.execute(input_dto)
    assert isinstance(output, ErrorResponseDTO)
    assert any(e.code == "CLIENT_NOT_FOUND" for e in output.errors)

# Independência dos testes
def test_get_campus_by_id_independence(usecase, valid_id, campus_repository_mock):
    campus_repository_mock.get.return_value = None
    input_dto = GetCampusByIdInputDTO(id=valid_id)
    output1 = usecase.execute(input_dto)
    campus_repository_mock.get.return_value = Campus(id=valid_id, name=Name(value="Empresa X"))
    output2 = usecase.execute(input_dto)
    assert isinstance(output1, ErrorResponseDTO)
    assert hasattr(output2, "id")
