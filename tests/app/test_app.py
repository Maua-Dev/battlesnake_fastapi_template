from src.app.main import read_root, start, move, end

class Test_App:
    def test_read_root(self):
        resp = read_root()

        assert resp == {
            "apiversion": "1",
            "author": "Maua-Dev",
            "color": "#8B0000",
            "head": "tiger-king",
            "tail": "hook",
            "version": "1.0.0"
        }
        
    def test_start(self):
        resp = start()

        assert resp == "ok"
        
    def test_move(self):
        resp = move({"hello": "world"})

        assert resp["move"] in ["up", "down", "left", "right"]
        assert resp["shout"] == f"I'm moving {resp['move']}!"
        
    def test_end(self):
        resp = end()

        assert resp == "ok"