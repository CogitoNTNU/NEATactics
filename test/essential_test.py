import platform

def test_os_check():

    os_name = platform.system()
    assert os_name != "Windows", "Your mom is fat!"

