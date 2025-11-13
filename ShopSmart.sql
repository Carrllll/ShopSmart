-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 13, 2025 at 06:31 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ShopSmart`
--

-- --------------------------------------------------------

--
-- Table structure for table `Category`
--

CREATE TABLE `Category` (
  `category_id` int(11) NOT NULL,
  `name` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Category`
--

INSERT INTO `Category` (`category_id`, `name`) VALUES
(9, 'Automotive'),
(4, 'Beauty'),
(5, 'Books'),
(3, 'Clothing'),
(1, 'Electronics'),
(10, 'Garden'),
(8, 'Groceries'),
(2, 'Home'),
(7, 'Sports'),
(6, 'Toys');

-- --------------------------------------------------------

--
-- Table structure for table `Customer`
--

CREATE TABLE `Customer` (
  `customer_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Customer`
--

INSERT INTO `Customer` (`customer_id`, `name`, `email`, `created_at`) VALUES
(1, 'Ava Reed', 'ava.reed@example.com', '2025-11-12 12:56:23'),
(2, 'Noah King', 'noah.king@example.com', '2025-11-12 12:56:23'),
(3, 'Liam Scott', 'liam.scott@example.com', '2025-11-12 12:56:23'),
(4, 'Olivia James', 'olivia.james@example.com', '2025-11-12 12:56:23'),
(5, 'Emma Johnson', 'emma.johnson@example.com', '2025-11-12 12:56:23'),
(6, 'Sophia Carter', 'sophia.carter@example.com', '2025-11-12 12:56:23'),
(7, 'Ethan Moore', 'ethan.moore@example.com', '2025-11-12 12:56:23'),
(8, 'Isabella Hill', 'isabella.hill@example.com', '2025-11-12 12:56:23'),
(9, 'Mason Allen', 'mason.allen@example.com', '2025-11-12 12:56:23'),
(10, 'Mia Davis', 'mia.davis@example.com', '2025-11-12 12:56:23');

-- --------------------------------------------------------

--
-- Table structure for table `Inventory`
--

CREATE TABLE `Inventory` (
  `product_id` int(11) NOT NULL,
  `quantity_on_hand` int(11) NOT NULL CHECK (`quantity_on_hand` >= 0),
  `reorder_level` int(11) NOT NULL CHECK (`reorder_level` >= 0),
  `last_restocked_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Inventory`
--

INSERT INTO `Inventory` (`product_id`, `quantity_on_hand`, `reorder_level`, `last_restocked_at`) VALUES
(1, 25, 5, '2025-11-12 12:57:15'),
(2, 40, 8, '2025-11-12 12:57:15'),
(3, 10, 3, '2025-11-12 12:57:15'),
(4, 15, 5, '2025-11-12 12:57:15'),
(5, 20, 4, '2025-11-12 12:57:15'),
(6, 12, 3, '2025-11-12 12:57:15'),
(7, 30, 10, '2025-11-12 12:57:15'),
(8, 18, 5, '2025-11-12 12:57:15'),
(9, 22, 6, '2025-11-12 12:57:15'),
(10, 14, 3, '2025-11-12 12:57:15');

-- --------------------------------------------------------

--
-- Table structure for table `Order`
--

CREATE TABLE `Order` (
  `order_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `order_date` datetime NOT NULL DEFAULT current_timestamp(),
  `status` enum('PENDING','PAID','SHIPPED','CANCELLED') NOT NULL DEFAULT 'PENDING',
  `total_amount` decimal(12,2) NOT NULL DEFAULT 0.00 CHECK (`total_amount` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Order`
--

INSERT INTO `Order` (`order_id`, `customer_id`, `order_date`, `status`, `total_amount`) VALUES
(1, 1, '2025-11-12 12:57:24', 'PENDING', 0.00),
(2, 2, '2025-11-12 12:57:24', 'PENDING', 0.00),
(3, 3, '2025-11-12 12:57:24', 'PENDING', 0.00),
(4, 4, '2025-11-12 12:57:24', 'PAID', 0.00),
(5, 5, '2025-11-12 12:57:24', 'PAID', 0.00),
(6, 6, '2025-11-12 12:57:24', 'PENDING', 0.00),
(7, 7, '2025-11-12 12:57:24', 'PAID', 0.00),
(8, 8, '2025-11-12 12:57:24', 'PAID', 0.00),
(9, 9, '2025-11-12 12:57:24', 'PAID', 0.00),
(10, 10, '2025-11-12 12:57:24', 'PENDING', 0.00);

-- --------------------------------------------------------

--
-- Table structure for table `OrderItem`
--

CREATE TABLE `OrderItem` (
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL CHECK (`quantity` >= 1),
  `unit_price` decimal(10,2) NOT NULL CHECK (`unit_price` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `OrderItem`
--

INSERT INTO `OrderItem` (`order_id`, `product_id`, `quantity`, `unit_price`) VALUES
(1, 1, 1, 79.99),
(1, 2, 2, 19.99),
(2, 3, 1, 149.50),
(3, 5, 1, 59.99),
(4, 6, 2, 69.50),
(5, 7, 1, 24.99),
(6, 8, 1, 15.99),
(7, 9, 2, 49.99),
(8, 4, 1, 89.00),
(9, 10, 1, 25.00);

--
-- Triggers `OrderItem`
--
DELIMITER $$
CREATE TRIGGER `trg_after_orderitem_insert` AFTER INSERT ON `OrderItem` FOR EACH ROW BEGIN
  UPDATE Inventory
  SET quantity_on_hand = quantity_on_hand - NEW.quantity
  WHERE product_id = NEW.product_id;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_update_order_total` AFTER INSERT ON `OrderItem` FOR EACH ROW BEGIN
  UPDATE `Order`
  SET total_amount = (
      SELECT SUM(quantity*unit_price)
      FROM OrderItem WHERE order_id = NEW.order_id
  )
  WHERE order_id = NEW.order_id;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `Payment`
--

CREATE TABLE `Payment` (
  `payment_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `method` enum('CARD','PAYPAL','CASH') NOT NULL,
  `amount` decimal(12,2) NOT NULL CHECK (`amount` >= 0),
  `status` enum('PENDING','PAID','FAILED') NOT NULL DEFAULT 'PENDING',
  `paid_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Payment`
--

INSERT INTO `Payment` (`payment_id`, `order_id`, `method`, `amount`, `status`, `paid_at`) VALUES
(1, 1, 'CARD', 119.97, 'PAID', '2025-11-12 12:58:09'),
(2, 2, 'PAYPAL', 149.50, 'PAID', '2025-11-12 12:58:09'),
(3, 3, 'CARD', 59.99, 'PENDING', NULL),
(4, 4, 'CARD', 139.00, 'PAID', '2025-11-12 12:58:09'),
(5, 5, 'CARD', 24.99, 'PAID', '2025-11-12 12:58:09'),
(6, 6, 'PAYPAL', 15.99, 'PENDING', NULL),
(7, 7, 'CARD', 99.98, 'PAID', '2025-11-12 12:58:09'),
(8, 8, 'CASH', 89.00, 'PAID', '2025-11-12 12:58:09'),
(9, 9, 'CARD', 25.00, 'PAID', '2025-11-12 12:58:09'),
(10, 10, 'PAYPAL', 0.00, 'PENDING', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `Product`
--

CREATE TABLE `Product` (
  `product_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL,
  `price` decimal(10,2) NOT NULL CHECK (`price` > 0),
  `avg_rating` decimal(3,2) NOT NULL DEFAULT 0.00,
  `review_count` int(11) NOT NULL DEFAULT 0 CHECK (`review_count` >= 0),
  `description` text DEFAULT NULL,
  `sku` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Product`
--

INSERT INTO `Product` (`product_id`, `category_id`, `name`, `price`, `avg_rating`, `review_count`, `description`, `sku`) VALUES
(1, 1, 'Wireless Earbuds', 79.99, 0.00, 0, NULL, 'ELEC-001'),
(2, 1, 'Smartphone Charger', 19.99, 0.00, 0, NULL, 'ELEC-002'),
(3, 2, 'Vacuum Cleaner', 149.50, 0.00, 0, NULL, 'HOME-001'),
(4, 2, 'Air Fryer', 89.00, 0.00, 0, NULL, 'HOME-002'),
(5, 3, 'Denim Jacket', 59.99, 0.00, 0, NULL, 'CLOTH-001'),
(6, 3, 'Sneakers', 69.50, 0.00, 0, NULL, 'CLOTH-002'),
(7, 4, 'Moisturizing Cream', 24.99, 0.00, 0, NULL, 'BEAUTY-001'),
(8, 5, 'Self-Help Book', 15.99, 0.00, 0, NULL, 'BOOK-001'),
(9, 6, 'Lego Building Set', 49.99, 0.00, 0, NULL, 'TOY-001'),
(10, 7, 'Yoga Mat', 25.00, 0.00, 0, NULL, 'SPORT-001');

-- --------------------------------------------------------

--
-- Table structure for table `Review`
--

CREATE TABLE `Review` (
  `review_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `rating` tinyint(4) NOT NULL CHECK (`rating` between 1 and 5),
  `comment` varchar(500) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Review`
--

INSERT INTO `Review` (`review_id`, `product_id`, `customer_id`, `rating`, `comment`, `created_at`) VALUES
(1, 1, 1, 5, 'Excellent sound quality', '2025-11-12 12:57:49'),
(2, 2, 2, 4, 'Fast charging', '2025-11-12 12:57:49'),
(3, 3, 3, 5, 'Very powerful cleaner', '2025-11-12 12:57:49'),
(4, 4, 4, 4, 'Great for quick meals', '2025-11-12 12:57:49'),
(5, 5, 5, 3, 'Nice jacket but fits large', '2025-11-12 12:57:49'),
(6, 6, 6, 5, 'Comfortable and stylish', '2025-11-12 12:57:49'),
(7, 7, 7, 4, 'Soft skin after use', '2025-11-12 12:57:49'),
(8, 8, 8, 5, 'Motivating read', '2025-11-12 12:57:49'),
(9, 9, 9, 5, 'Fun and creative set', '2025-11-12 12:57:49'),
(10, 10, 10, 4, 'Good grip and support', '2025-11-12 12:57:49');

--
-- Triggers `Review`
--
DELIMITER $$
CREATE TRIGGER `trg_after_review_insert` AFTER INSERT ON `Review` FOR EACH ROW BEGIN
  UPDATE Product p
  JOIN (SELECT product_id, AVG(rating) avg_r, COUNT(*) cnt
        FROM Review WHERE product_id = NEW.product_id) r
  ON p.product_id = r.product_id
  SET p.avg_rating = ROUND(r.avg_r,2),
      p.review_count = r.cnt;
END
$$
DELIMITER ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Category`
--
ALTER TABLE `Category`
  ADD PRIMARY KEY (`category_id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `Customer`
--
ALTER TABLE `Customer`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `Inventory`
--
ALTER TABLE `Inventory`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `Order`
--
ALTER TABLE `Order`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- Indexes for table `OrderItem`
--
ALTER TABLE `OrderItem`
  ADD PRIMARY KEY (`order_id`,`product_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `Payment`
--
ALTER TABLE `Payment`
  ADD PRIMARY KEY (`payment_id`),
  ADD UNIQUE KEY `order_id` (`order_id`);

--
-- Indexes for table `Product`
--
ALTER TABLE `Product`
  ADD PRIMARY KEY (`product_id`),
  ADD UNIQUE KEY `sku` (`sku`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `Review`
--
ALTER TABLE `Review`
  ADD PRIMARY KEY (`review_id`),
  ADD UNIQUE KEY `product_id` (`product_id`,`customer_id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Category`
--
ALTER TABLE `Category`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `Customer`
--
ALTER TABLE `Customer`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `Order`
--
ALTER TABLE `Order`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `Payment`
--
ALTER TABLE `Payment`
  MODIFY `payment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `Product`
--
ALTER TABLE `Product`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `Review`
--
ALTER TABLE `Review`
  MODIFY `review_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Inventory`
--
ALTER TABLE `Inventory`
  ADD CONSTRAINT `inventory_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `Product` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Order`
--
ALTER TABLE `Order`
  ADD CONSTRAINT `order_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `Customer` (`customer_id`) ON UPDATE CASCADE;

--
-- Constraints for table `OrderItem`
--
ALTER TABLE `OrderItem`
  ADD CONSTRAINT `orderitem_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `Order` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `orderitem_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `Product` (`product_id`) ON UPDATE CASCADE;

--
-- Constraints for table `Payment`
--
ALTER TABLE `Payment`
  ADD CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `Order` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Product`
--
ALTER TABLE `Product`
  ADD CONSTRAINT `product_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `Category` (`category_id`) ON UPDATE CASCADE;

--
-- Constraints for table `Review`
--
ALTER TABLE `Review`
  ADD CONSTRAINT `review_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `Product` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `review_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `Customer` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
