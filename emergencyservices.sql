-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 17, 2023 at 06:41 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `emergencyservices`
--

-- --------------------------------------------------------

--
-- Table structure for table `accepted_request`
--

CREATE TABLE `accepted_request` (
  `id` int(11) NOT NULL,
  `request_id` int(11) DEFAULT NULL,
  `service_provider_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accepted_request`
--

INSERT INTO `accepted_request` (`id`, `request_id`, `service_provider_id`) VALUES
(1, 1, 3),
(2, 1, 2),
(3, 1, 4),
(4, 1, 1),
(5, 2, 3),
(6, 2, 1),
(7, 2, 2),
(8, 2, 4),
(9, 3, 1),
(10, 3, 2),
(11, 3, 4),
(12, 3, 3),
(13, 5, 1),
(14, 6, 1),
(15, 6, 3);

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `request_id` int(11) DEFAULT NULL,
  `service_provider_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `rating` int(11) NOT NULL,
  `comments` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`id`, `request_id`, `service_provider_id`, `user_id`, `rating`, `comments`) VALUES
(1, 1, 1, 1, 5, 'Nice!'),
(2, 3, 1, 1, 5, 'nice!'),
(3, 6, 3, 1, 5, 'Nice Great Experience');

-- --------------------------------------------------------

--
-- Table structure for table `requests`
--

CREATE TABLE `requests` (
  `id` int(20) UNSIGNED NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `location` varchar(255) NOT NULL,
  `help_type` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL,
  `confirmed_service_provider_id` int(255) NOT NULL,
  `timestamp_column` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `requests`
--

INSERT INTO `requests` (`id`, `user_id`, `location`, `help_type`, `status`, `confirmed_service_provider_id`, `timestamp_column`) VALUES
(1, 1, 'Latitude: 18.43989, Longitude: 73.812186', 'medical', 'Completed', 1, '2023-11-25 07:32:06'),
(2, 1, 'Latitude: 18.43989, Longitude: 73.812186', 'medical', 'Completed', 1, '2023-11-25 07:32:06'),
(3, 1, 'Latitude: 18.483807, Longitude: 73.818919', 'medical', 'Completed', 1, '2023-11-25 07:32:06'),
(4, 1, 'Latitude: 18.504597, Longitude: 73.817191', 'fuel_delivery', 'Pending', 0, '2023-11-25 11:36:11'),
(5, 1, 'Latitude: 18.504296, Longitude: 73.817988', 'medical', 'Completed', 1, '2023-11-25 11:36:37'),
(6, 1, 'Latitude: 18.440022, Longitude: 73.812016', 'medical', 'Completed', 3, '2023-12-15 06:36:36');

-- --------------------------------------------------------

--
-- Table structure for table `service_provider`
--

CREATE TABLE `service_provider` (
  `id` int(11) NOT NULL,
  `provider_type` varchar(255) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `license_document_path` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `profile_pic_path` varchar(255) NOT NULL,
  `has_notification` tinyint(1) DEFAULT 0,
  `sender_user_id` int(11) DEFAULT NULL,
  `status` tinyint(1) DEFAULT 1,
  `rating_points` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `service_provider`
--

INSERT INTO `service_provider` (`id`, `provider_type`, `user_name`, `password`, `email`, `contact_number`, `license_document_path`, `location`, `profile_pic_path`, `has_notification`, `sender_user_id`, `status`, `rating_points`) VALUES
(1, 'doctor', 'sr', 'pbkdf2:sha256:260000$cD8MNRyhVAHt2Ni6$b584cf21fe7dfe89906a1b52b07a5e7497b846697ee8c1fe5b5fd49ac54fd96d', 'sanjotraut10000@gmail.com', '9075434497', 'serviceprovider_license\\antiragging_form IMCC FY.pdf', 'Latitude: 18.6317, Longitude: 73.7334', 'serviceprovider_profile_pic\\photo.jpg', 0, 1, 1, 10),
(2, 'doctor', 'priya', 'pbkdf2:sha256:260000$zGG6z8RDqFq8iz9T$82a4df00abadb38a1325a212223d2958500e5bc5e843ee3c5ce844cfbe3e6a78', 'priyakokate800@gmail.com', '09090909090', 'serviceprovider_license\\104600391_ExamForm.PDF', 'Latitude: 19.099641, Longitude: 74.767566', 'serviceprovider_profile_pic\\doctor-indian-38175791.webp', 0, NULL, 1, 10),
(3, 'doctor', 'ram', 'pbkdf2:sha256:260000$sPFT4IjmnE5POfwx$29021a90083952bd56c465f0995c8e6ad5ac52f6406d6b13b7a694be18e17509', 'rameshwarantarkar800@gmail.com', '8987968790', 'serviceprovider_license\\MCA CAP 2.pdf', 'Latitude: 19.218198, Longitude: 75.498171', 'serviceprovider_profile_pic\\th.jpeg', 1, 1, 1, 15),
(4, 'doctor', 'anita', 'pbkdf2:sha256:260000$bk7njix3Q8dtPDTm$cfe64a65edd9a7020b15d9738dd041434fb18a3c4aeefd3d49a787e1df53e567', 'anitaantarkar800@gmail.com', '7987968790', 'serviceprovider_license\\MCA CET Result.pdf', 'Latitude: 19.874565, Longitude: 75.356651', 'serviceprovider_profile_pic\\doctor-indian-38175791.webp', 0, NULL, 1, 10),
(5, 'mechanic', 'prashant', 'pbkdf2:sha256:260000$W0umX9JAQ3cIrkID$b3d19c21a7c652d6a42df72a0a78deef89cff01ced7ec723df482446ce43d3a8', 'prashantchitale2@gmail.com', '9087978779', 'serviceprovider_license\\MCA CET CAP 1 Option form with names.pdf', 'Latitude: 19.171923, Longitude: 75.175541', 'serviceprovider_profile_pic\\istockphoto-606675426-612x612.jpg', 0, NULL, 1, 10),
(6, 'fuel_provider', 'pritesh', 'pbkdf2:sha256:260000$UrUVaIaonSPJO4wL$d5871eacfd9e63fd30bea4f4378c98d0bf739b773c463d3e41991d928b27c663', 'priteshanwat2@gmail.com', '9370892143', 'serviceprovider_license\\MCA Registration.pdf', 'Latitude: 19.850178, Longitude: 74.008753', 'serviceprovider_profile_pic\\Fuel-Attendant-scaled.jpg', 0, NULL, 1, 10),
(7, 'mechanic', 'sunita', 'pbkdf2:sha256:260000$eLlOei2hrM217VXB$438d120d38e8e555b37285d61d6fb26e52750d29c7e9980dfbaf1b8ebb139de8', 'sunita2@gmail.com', '9370892143', 'serviceprovider_license\\antiragging_form IMCC FY.pdf', 'Latitude: 18.6317, Longitude: 73.7334', 'serviceprovider_profile_pic\\female-mechanic-servicing-a-car_1170-1238.avif', 0, NULL, 1, 10);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `profile_pic_path` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password_hash`, `email`, `full_name`, `phone_number`, `profile_pic_path`) VALUES
(1, 'sr', 'pbkdf2:sha256:260000$2TYJYm5YdVzTJgj7$c7cb1eeba7d71cc9b9b8db1f85c2eb5d942a4e0f39fb1d6182f3caf6407356da', 'sanjotraut10000@gmail.com', '', '9075434497', 'user_profile_pic\\th (1).jpeg'),
(2, 'priya', 'pbkdf2:sha256:260000$xX7bh0bWgImsgT24$d561e8f91affe1dfe56679be2402e4ebf2a2cc770ad82d591d1831ef152b28f2', 'priyakokate800@gmail.com', '', '09090909090', 'user_profile_pic\\th (3).jpeg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accepted_request`
--
ALTER TABLE `accepted_request`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `requests`
--
ALTER TABLE `requests`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `service_provider`
--
ALTER TABLE `service_provider`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accepted_request`
--
ALTER TABLE `accepted_request`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `requests`
--
ALTER TABLE `requests`
  MODIFY `id` int(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `service_provider`
--
ALTER TABLE `service_provider`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
