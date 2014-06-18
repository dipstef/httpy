from httpy.connection import is_disconnected, host_is_down, site_is_down


def main():
    for i in range(100):
        assert not is_disconnected()

    assert not host_is_down('google.com')
    assert host_is_down('google.foo')
    assert not site_is_down('http://google.com')
    assert site_is_down('http://google.foo')

if __name__ == '__main__':
    main()