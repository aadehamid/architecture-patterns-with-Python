from datetime import date, timedelta
import pytest
from model import OrderLine, Batch

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)
class AllocationTests:

    def make_batch_and_line(self, sku, batch_qty, line_qty):
        return (Batch("batch-001", sku, batch_qty, eta=today),
            OrderLine("order-123", sku, line_qty),
        )
    def test_allocating_to_a_batch_reduces_available_qty(self):
        batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=today)
        line = OrderLine("order-ref", "SMALL-TABLE", 2)

        batch.allocate(line)

        assert batch.available_quantity == 18

    def test_can_allocate_if_available_more_than_required_order_line(self):
        large_batch, small_line = self.make_batch_and_line("ELEGANT-LAMP", 20, 2)
        assert large_batch.can_allocate(small_line)

    def test_cannot_allocate_if_available_less_than_required_order_line(self):
        pytest.fail("todo")

    def test_can_allocate_if_available_equal_required_order_line(self):
        pytest.fail("todo")

    def test_cannot_repeat_allocation(self):
        pytest.fail("todo")

    def test_prefers_warehouse_batches_to_shipment(self):
        pytest.fail("todo")

    def test_eta_present_in_current_shipping_batches(self):
        pytest.fail("todo")

    def test_prefer_earlier_batches_of_shipment(self):
        pytest.fail("todo")
