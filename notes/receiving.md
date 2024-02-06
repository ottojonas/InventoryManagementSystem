---
modified: 2024-02-06T13:16:09.325Z
title: Receiving Stock
---

collect user input data.

update ItemStock purchase orders:
    - onOrder levels to go be decreased and to show the checking in of stock.
    - warehouseStock levels to increased and to show the checking in of stock.
    - totalStock levels to be increased and to show the checking in of stock.

update PurchaseOrders:
    - receivedDate to show the day it was checked in.

update ItemStock transfers:
    - onOrder levels to go be decreased and to show the checking in of stock.
    - sending and receiving location stock levels to increased and to show the checking in of stock.

            if self.receivingLocation == "Warehouse":
                self.db.executeDatabaseQuery(
                    """
                    UPDATE ItemStock 
                    SET warehouseStock = warehouseStock + ? 
                    WHERE itemID = ? 
                    AND itemSize = ? 
                    """,
                    (
                        self.quantityBeingSent,
                        itemID[0],
                        self.selectedItemSize,
                    ),
                )

            if self.receivingLocation == "Lower Sloane Street":
                self.db.executeDatabaseQuery(
                    """
                    UPDATE ItemStock 
                    SET sloaneStock = sloaneStock + ? 
                    WHERE itemID = ? 
                    AND itemSize = ? 
                    """,
                    (
                        self.quantityBeingSent,
                        itemID[0],
                        self.selectedItemSize,
                    ),
                )

            if self.receivingLocation == "Jermyn Street":
                self.db.executeDatabaseQuery(
                    """
                    UPDATE ItemStock 
                    SET jermynStock = jermynStock + ? 
                    WHERE itemID = ? 
                    AND itemSize = ? 
                    """,
                    (
                        self.quantityBeingSent,
                        itemID[0],
                        self.selectedItemSize,
                    ),
                )
