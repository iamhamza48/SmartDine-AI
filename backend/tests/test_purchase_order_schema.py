from app.graph.hitl_graph import PurchaseOrderDraft


def test_purchase_order_schema_has_no_unsupported_additional_properties():
    schema = PurchaseOrderDraft.model_json_schema()
    assert "additionalProperties" not in str(schema)
