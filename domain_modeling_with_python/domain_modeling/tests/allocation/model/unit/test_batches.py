from datetime import date, timedelta
import pytest
from model import OrderLine, Batch

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)

class BatchTests:

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
        small_batch, large_line = self.make_batch_and_line("ELEGANT-LAMP", 2, 20)
        assert small_batch.can_allocate(large_line) is False

    def test_can_allocate_if_available_equal_required_order_line(self):
        batch, line = self.make_batch_and_line("ELEGANT-LAMP", 2, 2)
        assert batch.can_allocate(line)

    def test_cannot_allocate_if_skus_do_not_match(self):
        batch = Batch("batch-001", "UNCOMFORTABLE-CHAIR", 100, eta=None)
        different_sku_line = OrderLine("order-123", "EXPENSIVE-TOASTER", 10)
        assert batch.can_allocate(different_sku_line) is False


    def test_allocation_is_idempotent(self):
        batch, unallocated_line = self.make_batch_and_line("DECORATIVE-TRINKET", 20, 2)
        batch.allocate(unallocated_line)
        batch.allocate(unallocated_line)
        assert batch.available_quantity == 18

    def test_can_only_deallocate_allocated_lines(self):
        batch, unallocated_line = self.make_batch_and_line("DECORATIVE-TRINKET", 20, 2)
        batch.deallocate(unallocated_line)
        assert batch.available_quantity == 20

    def test_deallocate(self):
        batch, line = self.make_batch_and_line("EXPENSIVE-FOOTSTOOL", 20, 2)
        batch.allocate(line)
        batch.deallocate(line)
        assert batch.available_quantity == 20
