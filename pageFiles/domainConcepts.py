class Categories:
    def __init__(self, categoryID, categoryName):
        self.categoryID = categoryID
        self.categoryName = categoryName


class Customers:
    def __init__(
        self,
        customerID,
        customerName,
        customerEmail,
        customerPhoneNumber,
        customerAddress,
    ):
        self.customerID = customerID
        self.customerName = customerName
        self.customerEmail = customerEmail
        self.customerPhoneNumber = customerPhoneNumber
        self.customerAddress = customerAddress


class Items:
    def __init__(
        self,
        itemID,
        itemName,
        manufacturerID,
        categoryID,
        purchaseOrderID,
        sku,
        discount,
        price,
        quantity,
        numberSold,
        createdBy,
        updatedBy,
        createdAt,
        updatedAt,
        saleID,
        sizes,
        purchaseOrderNumber,
    ):
        self.itemID = itemID
        self.itemName = itemName
        self.manufacturerID = manufacturerID
        self.categoryID = categoryID
        self.purchaseOrderID = purchaseOrderID
        self.sku = sku
        self.discount = discount
        self.price = price
        self.quantity = quantity
        self.numberSold = numberSold
        self.createdBy = createdBy
        self.updatedBy = updatedBy
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.saleID = saleID
        self.sizes = sizes
        self.purchaseOrderNumber = purchaseOrderNumber


class Manufacturers:
    def __init__(self, manufacturerID, manufacturerName, countryOfOrigin):
        self.manufacturerID = manufacturerID
        self.manufacturerName = manufacturerName
        self.countryOfOrigin = countryOfOrigin


class OnlineSales:
    def __init__(
        self,
        onlineOrderID,
        customerName,
        totalPrice,
        fulfilmentStatus,
        deliveryMethod,
        tags,
        itemID,
    ):
        self.onlineOrderID = onlineOrderID
        self.customerName = customerName
        self.totalPrice = totalPrice
        self.fulfilmentStatus = fulfilmentStatus
        self.deliveryMethod = deliveryMethod
        self.tags = tags
        self.itemID = itemID


class PurchaseOrders:
    def __init__(
        self,
        purchaseOrderID,
        purchaseOrderNumber,
        itemID,
        manufacturerID,
        sku,
        price,
        createdBy,
        updatedBy,
        createdAt,
        updatedAt,
        sizes,
        deliveryDate,
        quantity,
    ):
        self.purchaseOrderID = purchaseOrderID
        self.purchaseOrderNumber = purchaseOrderNumber
        self.itemID = itemID
        self.manufacturerID = manufacturerID
        self.sku = sku
        self.price = price
        self.createdBy = createdBy
        self.updatedBy = updatedBy
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.sizes = sizes
        self.deliveryDate = deliveryDate
        self.quantity = quantity


class Retail:
    def __init__(
        self,
        locationID,
        locationName,
    ):
        self.locationID = locationID
        self.locationName = locationName


class Sales:
    def __init__(
        self,
        salesID,
        staffID,
        itemID,
        locationID,
    ):
        self.salesID = salesID
        self.staffID = staffID
        self.itemID = itemID
        self.locationID = locationID


class Staff:
    def __init__(
        self,
        staffID,
        staffName,
        locationID,
        departmentName,
    ):
        self.staffID = staffID
        self.staffName = staffName
        self.locationID = locationID
        self.departmentName = departmentName


class Transfers:
    def __init__(
        self,
        transferID,
        transferNumber,
        itemName,
        sendersLocation,
        receiversLocation,
        createedAt,
        receivedAt,
    ):
        self.transferID = transferID
        self.transferNumber = transferNumber
        self.itemName = itemName
        self.sendersLocation = sendersLocation
        self.receiversLocation = receiversLocation
        self.createedAt = createedAt
        self.receivedAt = receivedAt


class User:
    def __init__(self, userID, userFirstName, userLastName, email, password):
        self.userID = userID
        self.userFirstName = userFirstName
        self.userLastName = userLastName
        self.email = email
        self.password = password
