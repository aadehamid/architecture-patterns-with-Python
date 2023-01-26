# architecture-patterns-with-Python

## Business Problem
A furniture business asked for an exciting new way of allocating stock. Until now, the business has been presenting stock and lead times based on what is physically available in the warehouse. If and when the warehouse runs out, a product is listed as “out of stock” until the next shipment arrives from the manufacturer.

Here is what they want to achieve with the new system: if we have a system that can keep track of all our shipments and when they’re due to arrive, we can treat the goods on those ships as real stock and part of our inventory, just with slightly longer lead times. Fewer goods will appear to be out of stock, we’ll sell more, and the business can save money by keeping lower inventory in the domestic warehouse.


## Section 1: A conversation with a doamin expert about the allocation system to understand the requirements, which will be an input into our domain modeling.

### Workflow Description
A product is identified by a SKU, pronounced “skew,” which is short for stock-keeping unit. Customers place orders. An order is identified by an order reference and comprises multiple order lines, where each line has a SKU and a quantity. For example:

- 10 units of RED-CHAIR

- 1 unit of TASTELESS-LAMP

The purchasing department orders small batches of stock. A batch of stock has a unique ID called a reference, a SKU, and a quantity.

### Business Rules
1. We need to allocate order lines to batches. When we’ve allocated an order line to a batch, we will send stock from that specific batch to the customer’s delivery address. When we allocate x units of stock to a batch, the available quantity is reduced by x. For example:

We have a batch of 20 SMALL-TABLE, and we allocate an order line for 2 SMALL-TABLE.

The batch should have 18 SMALL-TABLE remaining.

2. We can’t allocate to a batch if the available quantity is less than the quantity of the order line. For example:

We have a batch of 1 BLUE-CUSHION, and an order line for 2 BLUE-CUSHION.

We should not be able to allocate the line to the batch.

3. We can’t allocate the same line twice. For example:

We have a batch of 10 BLUE-VASE, and we allocate an order line for 2 BLUE-VASE.

If we allocate the order line again to the same batch, the batch should still have an available quantity of 8.

4. Batches have an ETA if they are currently shipping, or they may be in warehouse stock. We allocate to warehouse stock in preference to shipment batches. We allocate to shipment batches in order of which has the earliest ETA.
