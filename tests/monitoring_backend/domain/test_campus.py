from monitoring_backend.domain.entity.campus import Campus
from monitoring_backend.domain.vo.name import Name


def test_add_and_remove_water_system():
    campus = Campus(name=Name(value="AcquaTech"))
    
    found = campus.get_water_system(1)
    assert found.name == Name(value="Poço Central")

    campus.remove_water_system(1)
    assert len(campus.water_systems) == 0
    
    assert campus.get_water_system(1) is None