CREATE TABLE CUSTOMER(
CustID int(3) NOT NULL PRIMARY KEY, 
Name varchar(30), 
Phone varchar(15));

CREATE TABLE RENTAL(
CustID int(3) NOT NULL, 
VehicleID varchar(20) NOT NULL, 
StartDate date, 
OrderDate date, 
RentalType int(1) NOT NULL, 
Qty int(1), 
ReturnDate date, 
TotalAmount int(5), 
PaymentDate date,
FOREIGN KEY (VehicleID) REFERENCES vehicle(VehicleID),
FOREIGN KEY (CustID) REFERENCES customer(CustID));

CREATE TABLE VEHICLE(
VehicleID char(17) NOT NULL PRIMARY KEY,
Description varchar(200),
Year int(4),
Type int(1),
Category int(1));


CREATE TABLE RATE(
Type int(1),
Category int(1),
Weekly float,
Daily float,
FOREIGN KEY (Type) REFERENCES vehicle(Type),
FOREIGN KEY (Category) REFERENCES vehicle(Category));

ALTER TABLE RENTAL ADD COLUMN Returned int; 

UPDATE RENTAL SET Returned=0 WHERE PaymentDate IS NULL; 

UPDATE RENTAL SET Returned=1 WHERE PaymentDate IS NOT NULL; 

CREATE VIEW vRentalInfo AS 
SELECT OrderDate, StartDate, ReturnDate, 
JULIANDAY(ReturnDate)-JULIANDAY(StartDate)+1 AS TotalDays, 
V.VehicleID AS VIN, Description AS 'Vehicle', 
CASE WHEN Type = 1 THEN 'Compact' 
WHEN Type = 2 THEN 'Medium' 
WHEN Type = 3 THEN 'Large' 
WHEN Type = 4 THEN 'SUV' 
WHEN Type = 5 THEN 'Truck' 
WHEN Type = 6 THEN 'VAN' 
END AS Type, 
CASE WHEN Category = 0 THEN 'Basic' 
WHEN Category = 1 THEN 'Luxury' 
END AS Category, 
C.CustID AS CustomerID, Name AS CustomerName, TotalAmount AS OrderAmount, 
CASE WHEN PaymentDate = "NULL" THEN TotalAmount 
ELSE 0 END AS RentalBalance 
FROM RENTAL AS R, VEHICLE AS V, CUSTOMER AS C 
WHERE R.VehicleID = V.VehicleID AND C.CustID=R.CustID;  

SELECT * FROM vRentalInfo;

SELECT COUNT(*) AS Num_of_rows FROM vRentalInfo; 