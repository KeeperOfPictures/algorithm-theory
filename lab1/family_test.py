from my_family import get_family_height

def test_family_heights():
    father_height, overall_height = get_family_height()
    assert father_height == 180
    assert overall_height == 180 + 164 + 180