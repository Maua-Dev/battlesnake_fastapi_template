from src.app.main import create_item, read_item, read_root


class Test_App:
    def test_read_root(self):
        resp = read_root()
        
        assert resp == {"Hello": "World"}

    def test_get_item(self):
        
        resp = read_item(1)

        assert resp == {"item_id": 1}

    def test_post_item(self):
        request = {"item_id": 1,
                   "name": "test"}

        resp = create_item(request)

        assert resp == {"item_id": 1,
                        "name": "test"}