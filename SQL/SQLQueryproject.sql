USE Sales_Analytics;
GO

SELECT COUNT(*) AS Total_Records
FROM dbo.Superstore_Cleaned;
SELECT TOP 10 *
FROM dbo.Superstore_Cleaned;

SELECT Row_ID, COUNT(*) AS Duplicate_Count
FROM dbo.Superstore_Cleaned
GROUP BY Row_ID
HAVING COUNT(*) > 1;

SELECT
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit
FROM dbo.Superstore_Cleaned;

SELECT
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit
FROM dbo.Superstore_cleaned;

SELECT TOP 10
    Product_Name,
    SUM(Sales) AS Total_Sales
FROM dbo.Superstore_Cleaned
GROUP BY Product_Name
ORDER BY Total_Sales DESC;

SELECT
    Region,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit
FROM dbo.Superstore_cleaned
GROUP BY Region
ORDER BY Total_Sales DESC;

SELECT TOP 10
    Product_Name,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit
FROM dbo.Superstore_Cleaned
GROUP BY Product_Name
ORDER BY Total_Sales DESC;

SELECT
    Category,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    SUM(Quantity) AS Total_Quantity
FROM dbo.Superstore_Cleaned
GROUP BY Category
ORDER BY Total_Sales DESC;

SELECT
    Category,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    ROUND(
        SUM(Profit) * 100.0 / NULLIF(SUM(Sales), 0), 2
    ) AS Profit_Margin_Percentage
FROM dbo.Superstore_Cleaned
GROUP BY Category
ORDER BY Profit_Margin_Percentage DESC;

SELECT
    Category,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    SUM(Quantity) AS Total_Quantity
FROM dbo.Superstore_Cleaned
GROUP BY Category
ORDER BY Total_Sales DESC;

SELECT
    YEAR(Order_Date) AS Sales_Year,
    MONTH(Order_Date) AS Sales_Month,
    SUM(Sales) AS Monthly_Sales,
    SUM(Profit) AS Monthly_Profit
FROM dbo.Superstore_Cleaned
GROUP BY
    YEAR(Order_Date),
    MONTH(Order_Date)
ORDER BY
    Sales_Year,
    Sales_Month;
    
    SELECT TOP 10
    Customer_Name,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit
FROM dbo.Superstore_Cleaned
GROUP BY Customer_Name
ORDER BY Total_Sales DESC;

SELECT
    Customer_Name,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit
FROM dbo.Superstore_Cleaned
GROUP BY Customer_Name
HAVING SUM(Profit) < 0
ORDER BY Total_Profit ASC;

SELECT
    COUNT(*) AS Loss_Making_Customers
FROM (
    SELECT Customer_Name
    FROM dbo.Superstore_Cleaned
    GROUP BY Customer_Name
    HAVING SUM(Profit) < 0
) AS Loss_Customers;

SELECT
    Region,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    ROUND(
        SUM(Profit) * 100.0 / NULLIF(SUM(Sales), 0), 2
    ) AS Profit_Margin_Percentage
FROM dbo.Superstore_Cleaned
GROUP BY Region
ORDER BY Profit_Margin_Percentage DESC;

SELECT
    Region,
    SUM(Profit) AS Total_Profit
FROM dbo.Superstore_Cleaned
GROUP BY Region
ORDER BY Total_Profit ASC;
SELECT COUNT(*) AS Total_Records
FROM dbo.Superstore_Cleaned;

SELECT TOP 5
    Row_ID,
    Order_ID,
    Customer_Name,
    Sales
FROM dbo.Superstore_Cleaned
ORDER BY Row_ID;

SELECT
    COUNT(*) AS Total_Rows,
    COUNT(DISTINCT Row_ID) AS Unique_Row_IDs,
    MIN(Row_ID) AS First_Row_ID,
    MAX(Row_ID) AS Last_Row_ID
FROM dbo.Superstore_Cleaned;

SELECT
    SUM(CASE WHEN Order_ID IS NULL THEN 1 ELSE 0 END) AS Null_Order_ID,
    SUM(CASE WHEN Order_Date IS NULL THEN 1 ELSE 0 END) AS Null_Order_Date,
    SUM(CASE WHEN Sales IS NULL THEN 1 ELSE 0 END) AS Null_Sales,
    SUM(CASE WHEN Profit IS NULL THEN 1 ELSE 0 END) AS Null_Profit
FROM dbo.Superstore_Cleaned;

SELECT Order_ID, Product_ID, COUNT(*) AS Cnt
FROM dbo.Superstore_Cleaned
GROUP BY Order_ID, Product_ID
HAVING COUNT(*) > 1;

SELECT
    MIN(Order_Date) AS First_Order,
    MAX(Order_Date) AS Last_Order,
    SUM(CASE WHEN Ship_Date < Order_Date THEN 1 ELSE 0 END) AS Bad_Ship_Dates
FROM dbo.Superstore_Cleaned;

SELECT
    SUM(CASE WHEN Sales <= 0 THEN 1 ELSE 0 END) AS NonPositive_Sales,
    SUM(CASE WHEN Quantity <= 0 THEN 1 ELSE 0 END) AS NonPositive_Qty,
    SUM(CASE WHEN Discount < 0 OR Discount > 1 THEN 1 ELSE 0 END) AS Bad_Discount,
    SUM(CASE WHEN Profit < 0 THEN 1 ELSE 0 END) AS Loss_Making_Rows
FROM dbo.Superstore_Cleaned;

USE Sales_Analytics;
GO

SELECT *
FROM dbo.Superstore_Cleaned
WHERE Row_ID = 10194;

SELECT *
FROM dbo.Superstore_Cleaned
WHERE Row_ID = 10194;