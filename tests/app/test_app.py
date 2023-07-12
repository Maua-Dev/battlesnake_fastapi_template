from src.app.main import read_root


class Test_App:
    def test_read_root(self):
        resp = read_root()
        
        assert resp == {"Hello": "World"}
