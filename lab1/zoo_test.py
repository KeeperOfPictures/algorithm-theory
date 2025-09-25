from zoo import zoo

def test_zoo():
    final_list, lion_pos, lark_pos = zoo()

    assert final_list == ['lion', 'bear', 'kangaroo', 'monkey', 'rooster', 'ostrich', 'lark']
    assert lion_pos == 1
    assert lark_pos == 7