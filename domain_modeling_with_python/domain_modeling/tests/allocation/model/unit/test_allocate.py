from datetime import date, timedelta
import pytest
from model import OrderLine, Batch, allocate, OutOfStock

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)

class AllocateTests:
    # def test_cannot_repeat_allocation(self):
    #         pytest.fail("todo")

    def test_prefers_current_stock_batches_to_shipments(self):
      in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
      shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
      line = OrderLine("oref", "RETRO-CLOCK", 10)

      allocate(line, [in_stock_batch, shipment_batch])

      assert in_stock_batch.available_quantity == 90
      assert shipment_batch.available_quantity == 100

    def test_prefer_earlier_batches_of_shipment(self):
         earliest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=today)
         medium = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=tomorrow)
         latest = Batch("slow-batch", "MINIMALIST-SPOON", 100, eta=later)
         line = OrderLine("oref", "MINIMALIST-SPOON", 10)

         allocate(line, [medium, earliest, latest])

         assert earliest.available_quantity == 90
         assert medium.available_quantity == 100
         assert latest.available_quantity == 100

    def test_returns_allocated_batch_reference(self):
        in_stock_batch = Batch("in-stock-batch-ref", "HIGHBROW-POSTER", 100, eta=None)
        shipment_batch = Batch("shipment-batch-ref", "HIGHBROW-POSTER", 100, eta=tomorrow)
        line = OrderLine("oref", "HIGHBROW-POSTER", 10)
        allocation = allocate(line, [in_stock_batch, shipment_batch])
        assert allocation == in_stock_batch.reference

    def test_raises_out_of_stock_exception_if_cannot_allocate(self):
        batch = Batch("batch1", "SMALL-FORK", 10, eta=today)
        allocate(OrderLine("order1", "SMALL-FORK", 10), [batch])
        with pytest.raises(OutOfStock, match="SMALL-FORK"):
            allocate(OrderLine("order2", "SMALL-FORK", 1), [batch])
