import importlib

import app.graph.persistent_graph as persistent_graph


def test_get_app_graph_falls_back_to_memory_when_postgres_is_unavailable(monkeypatch):
    class FakePostgresSaver:
        @staticmethod
        def from_conn_string(_):
            raise RuntimeError("DB connection unavailable")

    monkeypatch.setitem(importlib.sys.modules, "langgraph.checkpoint.postgres", type("Mod", (), {"PostgresSaver": FakePostgresSaver}))

    graph = persistent_graph.get_app_graph()

    assert graph is not None
    assert hasattr(graph, "invoke")
