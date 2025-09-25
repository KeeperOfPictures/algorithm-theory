from secret import decrypt_message

def test_decrypt_message():
    decrypted = decrypt_message()
    assert decrypted == 'в бане веник дороже денег'