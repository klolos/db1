-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 08, 2014 at 12:11 AM
-- Server version: 5.5.37
-- PHP Version: 5.3.10-1ubuntu3.11

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `ProjectDB`
--

-- --------------------------------------------------------

--
-- Table structure for table `Customer`
--

CREATE TABLE IF NOT EXISTS `Customer` (
  `id` varchar(30) NOT NULL,
  `Surname` varchar(100) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Middle Name` varchar(100) NOT NULL,
  `State` varchar(30) NOT NULL,
  `City` varchar(30) NOT NULL,
  `Municipality` varchar(30) NOT NULL,
  `Street` varchar(100) NOT NULL,
  `Street No` varchar(10) NOT NULL,
  `Zipcode` int(10) NOT NULL,
  `Phone` varchar(30) NOT NULL,
  `Mobile Phone` varchar(30) NOT NULL,
  `Fax` varchar(30) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Credit Card` varchar(30) NOT NULL,
  `Expires` varchar(20) NOT NULL,
  `VIP` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Customer`
--

INSERT INTO `Customer` (`id`, `Surname`, `Name`, `Middle Name`, `State`, `City`, `Municipality`, `Street`, `Street No`, `Zipcode`, `Phone`, `Mobile Phone`, `Fax`, `Email`, `Credit Card`, `Expires`, `VIP`) VALUES
('3104765', 'Florou', 'Maria', 'Dimitrios', 'Trikala', 'Trikala', 'Kastania', 'Kolokotroni', '28', 42100, '2431012345', '6973010459', '2431054321', 'mflorou@hotmail.com', '348625756860412', '2017-05', 0),
('3105739', 'Oikonomou', 'Anastasios', 'Georgios', 'Messenia', 'Kalamata', 'Andrusas', '3 Septemvriou', '8', 24100, '2721012345', '6973540261', '2721054321', 'aoikonomou@yahoo.com', '5118331166713617', '2017-05-16', 0),
('3106146', 'Papalouka', 'Elisavet', 'Georgios', 'Evros', 'Alexandroupoli', 'Soufli', 'Lada', '23', 68100, '2551012345', '6992950210', '2551054321', 'epapalouka@yahoo.com', '4485581680111064', '2018-05', 0),
('3107639', 'Makri', 'Despoina', 'Aleksandros', 'Aetolia-Acarnania', 'Agrinio', 'Astakos', 'Omirou', '1', 30100, '2641012345', '6942550230', '2641054321', 'dmakri@hotmail.com', '30156878448616', '2016-05-25', 0),
('3108164', 'Tsapelas', 'Ioannis', 'Theodoros', 'Heraklion', 'Heraklion', 'Gazi', 'Pelopida', '22', 71500, '2810123456', '6974370221', '2810654321', 'itsapelas@gmail.com', '30338672855531', '2017-05-21', 0),
('3108743', 'Ksenaki', 'Anastasia', 'Panagiotis', 'Dodecanese', 'Rhodes', 'Ialisos', 'Menandrou', '56', 85100, '2241012345', '6946120556', '2241054321', 'aksenaki@yahoo.com', '214918923788207', '2016-05-09', 0),
('3109412', 'Emmanouilidis', 'Paraskevas', 'Petros', 'Pieria', 'Katerini', 'Litoxoro', 'Lykourgou', '16', 60100, '2351012345', '6996620197', '2351054321', 'pemmanouilidis@hotmail.com', '5597341203683244', '2016-05-22', 0),
('3109423', 'Gkazouni', 'Aikaterini', 'Vasileios', 'Serres', 'Serres', 'Amfipoli', 'Dragatsanou', '72', 62124, '2321012345', '6998780380', '2321054321', 'agkazouni@hotmail.com', '201470144602077', '2017-06-08', 0),
('3109666', 'Ieronimakis', 'Georgios', 'Athanasios', 'Phthiotis', 'Lamia', 'Atalanti', 'Pandrosou', '7', 35100, '2231012345', '6974630319', '2231054321', 'gieronimakis@hotmail.com', '869959254577767', '2018-04-16', 0),
('3109748', 'Rigas', 'Filippos', 'Konstantinos', 'Kozani', 'Kozani', 'Neapoli', 'Aiolou', '33', 50100, '2461023456', '6972090399', '2461065432', 'frigas@gmail.com', '201467215007418', '2018-04-14', 0),
('3109789', 'Iliopoulos', 'Xristos', 'Stefanos', 'Kavala', 'Kavala', 'Nestos', 'Rizari', '48', 65403, '2510123456', '6943210329', '2510654321', 'xiliopoulos@hotmail.com', '30375659849426', '2017-04-17', 0),
('3110005', 'Davaris', 'Stavros', 'Fotios', 'Imathia', 'Veria', 'Vergina', 'Voukourestiou', '39', 59100, '2331012345', '6992796531', '2331054321', 'sdavaris@yahoo.com', '3088848462304305', '2017-03-21', 0),
('3110027', 'Apostolakis', 'Sotirios', 'Nikolaos', 'Chania', 'Chania', 'Souda', 'Miltiados', '5', 73134, '2821012345', '6941870597', '2821054321', 'sapostolakis@gmail.com', '6011715031849166', '2017-03-03', 0),
('3110035', 'Savva', 'Vasiliki', 'Ioannis', 'Euboea', 'Chalcis', 'Avlida', 'Filopoimenos', '65', 34100, '2221012345', '6974610173', '2221054321', 'vsavva@yahoo.com', '869982656831830', '2018-03-25', 0),
('3110051', 'Valsamidis', 'Stamatios', 'Andreas', 'Attica', 'Athens', 'Peristeri', 'Alexandras', '280', 17364, '2103456789', '6944680377', '2109876543', 'svalsamidis@yahoo.com', '342851339569389', '2016-03-06', 0),
('3110085', 'Zafeiroudi', 'Kiriaki', 'Spiridon', 'Larissa', 'Larissa', 'Elassona', 'Athanasiou Diakou', '81', 41334, '2410123456', '6997201061', '2410654321', 'kzafeiroudi@gmail.com', '214905357327453', '2018-05-27', 0),
('3110112', 'Lekas', 'Ilias', 'Dionisios', 'Thessaloniki', 'Thessaloniki', 'Evosmos', 'Konstantinoupoleos', '108', 54629, '2310234567', '6940930367', '2310765432', 'ilekas@gmail.com', '869910581678885', '2018-05-31', 0),
('3110152', 'Thanasogeorgiou', 'Konstantina', 'Apostolos', 'Attica', 'Athens', 'Kallithea', '28 Oktovriou', '220', 19212, '2102345678', '6976460305', '2108765432', 'kthanasogeorgiou@hotmail.com', '3112015245548539', '2018-07-20', 0),
('3110674', 'Kalomoiri', 'Marina', 'Simeon', 'Thessaloniki', 'Thessaloniki', 'Sikies', 'Lampsakou', '95', 54633, '2310123456', '6946360689', '2310654321', 'mkalomoiri@yahoo.com', '30331941430665', '2017-02-07', 0),
('3110684', 'Dimitriou', 'Andriana', 'Pantelis', 'Chios', 'Chios', 'Omiroupoli', 'Aristeidou', '10', 82104, '2271012345', '6994130314', '2271054321', 'adimitriou@gmail.com', '3096615565506205', '2016-05-30', 0),
('3110761', 'Aggeli', 'Spiridoula', 'Omiros', 'Magnesia', 'Volos', 'Iolkos', 'Agiou Konstantinou', '40', 38221, '2421012345', '6944150558', '2421054321', 'saggeli@hotmail.com', '4024007180359589', '2017-04-30', 0),
('3110807', 'Mauroeidakos', 'Theodoros', 'Ilias', 'Attica', 'Athens', 'Kifisia', 'Andrea Syngrou', '450', 13845, '2101234567', '6974170466', '2107654321', 'tmauroeidakos@gmail.com', '341274488730937', '2017-06-22', 1),
('3111734', 'Nikolaou', 'Vasileios', 'Odisseas', 'Kozani', 'Ptolemaida', 'Ellispondou', 'Voreou', '15', 50200, '2461012345', '6940610251', '2461054321', 'vnikolaou@yahoo.com', '6011475884394733', '2018-09-12', 0),
('3111737', 'Kolivas', 'Evangelos', 'Gerasimos', 'Lefkada', 'Lefkada', 'Kalamos', 'Santaroza', '9', 31082, '2645012345', '6941350408', '2645054321', 'ekolivas@gmail.com', '5284502269682523', '2019-03-10', 1),
('3112628', 'Lolos', 'Konstantinos', 'Aristotelis', 'Achaea', 'Patras', 'Kalavrita', 'Vyssis', '4', 26332, '2610123456', '6992211167', '2610654321', 'klolos@gmail.com', '4916328841286834', '2016-05-26', 1);

--
-- Triggers `Customer`
--
DROP TRIGGER IF EXISTS `DeleteCustomer_DeleteRervation`;
DELIMITER //
CREATE TRIGGER `DeleteCustomer_DeleteRervation` AFTER DELETE ON `Customer`
 FOR EACH ROW DELETE FROM Reservation WHERE Reservation.id = old.id
//
DELIMITER ;

-- --------------------------------------------------------

--
-- Stand-in structure for view `Debtor`
--
CREATE TABLE IF NOT EXISTS `Debtor` (
`id` varchar(30)
,`Surname` varchar(100)
,`Name` varchar(100)
,`VIP` tinyint(1)
,`Mobile Phone` varchar(30)
,`Phone` varchar(30)
,`Debt` decimal(32,0)
);
-- --------------------------------------------------------

--
-- Stand-in structure for view `DebtorIDs`
--
CREATE TABLE IF NOT EXISTS `DebtorIDs` (
`id` varchar(30)
,`Debt` decimal(32,0)
);
-- --------------------------------------------------------

--
-- Table structure for table `Hotel`
--

CREATE TABLE IF NOT EXISTS `Hotel` (
  `Hotel Name` varchar(100) NOT NULL,
  `State` varchar(30) NOT NULL,
  `City` varchar(30) NOT NULL,
  `Municipality` varchar(30) NOT NULL,
  `Street` varchar(100) NOT NULL,
  `Street No` varchar(10) NOT NULL,
  `Phone` varchar(30) NOT NULL,
  `Fax` varchar(30) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `WiFi` tinyint(1) NOT NULL,
  `Parking` tinyint(1) NOT NULL,
  `Gym` tinyint(1) NOT NULL,
  `Pool` tinyint(1) NOT NULL,
  `Restaurant` tinyint(1) NOT NULL,
  PRIMARY KEY (`Hotel Name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Hotel`
--

INSERT INTO `Hotel` (`Hotel Name`, `State`, `City`, `Municipality`, `Street`, `Street No`, `Phone`, `Fax`, `Email`, `WiFi`, `Parking`, `Gym`, `Pool`, `Restaurant`) VALUES
('Athens Hilton Hotel', 'Attica', 'Athens', 'Glifada', 'Amalias', '200', '2107281000', '2107281010', 'hiltonathens@gmail.com', 1, 0, 1, 0, 1),
('Classical Macedonia Palace', 'Thessaloniki', 'Thessaloniki', 'Thermi', 'Mesogeion', '520', '2310897000', '2310897010', 'macedoniapalace@gmail.com', 1, 1, 0, 1, 0),
('Corfu Holiday Palace', 'Corfu', 'Corfu', 'Palaiokastriton', 'Vasilissis Sofias', '100', '2661036000', '2661036010', 'corfuholiday@gmail.com', 1, 1, 0, 1, 0),
('Grande Bretagne Hotel Athens', 'Attica', 'Athens', 'Zografou', 'Lenorman', '180', '2103330000', '2103330010', 'gbretagneathens@gmail.com', 1, 1, 0, 1, 1),
('Kentrikon Hotel Ioannina', 'Ioannina', 'Ioannina', 'Konitsa', 'Panepistimiou', '30', '2651071000', '2651071010', 'kentrikonioannina@gmail.com', 1, 1, 1, 1, 1),
('Kydon Hotel Chania', 'Chania', 'Chania', 'Kissamos', 'Kifissias', '120', '2821052000', '2821052010', 'kydonchania@gmail.com', 0, 1, 0, 1, 1),
('Rodos Palace Resort Hotel', 'Dodecanese', 'Rodos', 'Petaloudes', 'Dionysiou Areopagitou', '20', '2241025000', '2241025010', 'rodospalace@gmail.com', 0, 1, 0, 0, 1),
('Santorini Kastelli Resort', 'Cyclades', 'Fira', 'Fira', 'Vouliagmenis', '80', '2286031000', '2286031010', 'santorinikastelli@gmail.com', 0, 0, 1, 0, 0);

--
-- Triggers `Hotel`
--
DROP TRIGGER IF EXISTS `DeleteHotel_DeleteRoom`;
DELIMITER //
CREATE TRIGGER `DeleteHotel_DeleteRoom` AFTER DELETE ON `Hotel`
 FOR EACH ROW DELETE FROM Room WHERE Room.`Hotel Name` = old.`Hotel Name`
//
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `Reservation`
--

CREATE TABLE IF NOT EXISTS `Reservation` (
  `Rid` int(11) NOT NULL AUTO_INCREMENT,
  `Hotel Name` varchar(100) NOT NULL,
  `Room No` int(11) NOT NULL,
  `id` varchar(30) NOT NULL,
  `Res Date` datetime NOT NULL,
  `Arrival` date NOT NULL,
  `Departure` date NOT NULL,
  `Payment Method` varchar(100) NOT NULL,
  `Cost` int(11) NOT NULL,
  `Remainder` int(11) NOT NULL,
  PRIMARY KEY (`Rid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=18 ;

--
-- Dumping data for table `Reservation`
--

INSERT INTO `Reservation` (`Rid`, `Hotel Name`, `Room No`, `id`, `Res Date`, `Arrival`, `Departure`, `Payment Method`, `Cost`, `Remainder`) VALUES
(1, 'Athens Hilton Hotel', 102, '3104765', '2014-04-14 14:33:00', '2014-04-25', '2014-04-29', 'Credit Card', 800, 600),
(2, 'Athens Hilton Hotel', 204, '3105739', '2014-04-24 23:04:42', '2014-05-07', '2014-05-10', 'Credit Card', 750, 500),
(3, 'Classical Macedonia Palace', 104, '3106146', '2014-04-25 02:07:02', '2014-06-04', '2014-06-09', 'Credit Card', 125, 100),
(4, 'Classical Macedonia Palace', 203, '3108164', '2014-04-25 02:08:54', '2014-05-14', '2014-05-30', 'Credit Card', 120, 60),
(5, 'Corfu Holiday Palace', 202, '3112628', '2014-04-25 02:11:38', '2014-06-02', '2014-06-05', 'Cash', 150, 100),
(6, 'Kydon Hotel Chania', 101, '3111734', '2014-05-06 04:09:15', '2014-05-14', '2014-05-20', 'Cash', 120, 70),
(7, 'Kydon Hotel Chania', 102, '3110761', '2014-04-28 23:19:18', '2014-05-25', '2014-05-28', 'Credit Card', 90, 0),
(8, 'Kydon Hotel Chania', 103, '3110684', '2014-04-28 23:19:21', '2014-05-09', '2024-05-12', 'Credit Card', 300, 150),
(9, 'Kydon Hotel Chania', 201, '3110674', '2014-04-28 23:20:05', '2014-07-01', '2024-07-04', 'Credit Card', 75, 25),
(10, 'Kydon Hotel Chania', 202, '3110152', '2014-04-28 23:26:27', '2014-05-20', '2014-05-22', 'Cash', 80, 0),
(11, 'Grande Bretagne Hotel Athens', 101, '3110112', '2014-04-29 01:48:21', '2014-05-27', '2014-05-28', 'Credit Card', 35, 30),
(12, 'Grande Bretagne Hotel Athens', 202, '3110807', '2014-05-03 09:40:24', '2014-06-10', '2014-06-14', 'Credit Card', 180, 150),
(13, 'Rodos Palace Resort Hotel', 201, '3109748', '2014-05-06 18:29:35', '2014-06-02', '2014-06-05', 'Credit Card', 60, 50),
(14, 'Kentrikon Hotel Ioannina', 101, '3111737', '2014-05-20 10:32:20', '2014-07-01', '2014-07-31', 'Cash', 450, 0),
(15, 'Kentrikon Hotel Ioannina', 201, '3111737', '2014-05-20 10:32:25', '2014-08-01', '2014-08-31', 'Cash', 700, 500),
(16, 'Athens Hilton Hotel', 103, '3104765', '2014-05-06 20:39:00', '2012-12-18', '2012-12-26', 'Cash', 810, 810),
(17, 'Kydon Hotel Chania', 202, '3112628', '2014-05-07 00:34:02', '2014-05-23', '2014-05-25', 'Credit Card', 400, 250);

-- --------------------------------------------------------

--
-- Table structure for table `Room`
--

CREATE TABLE IF NOT EXISTS `Room` (
  `Room No` int(11) NOT NULL,
  `Hotel Name` varchar(100) NOT NULL,
  `Price` int(11) NOT NULL,
  `Beds` int(11) NOT NULL,
  `TV` tinyint(1) NOT NULL,
  `AC` tinyint(1) NOT NULL,
  `Suite` tinyint(1) NOT NULL,
  `Balcony` tinyint(1) NOT NULL,
  PRIMARY KEY (`Room No`,`Hotel Name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Room`
--

INSERT INTO `Room` (`Room No`, `Hotel Name`, `Price`, `Beds`, `TV`, `AC`, `Suite`, `Balcony`) VALUES
(101, 'Athens Hilton Hotel', 90, 3, 1, 1, 0, 0),
(101, 'Classical Macedonia Palace', 100, 4, 1, 0, 0, 1),
(101, 'Corfu Holiday Palace', 100, 2, 0, 0, 1, 1),
(101, 'Grande Bretagne Hotel Athens', 80, 2, 1, 1, 0, 0),
(101, 'Kentrikon Hotel Ioannina', 30, 2, 1, 1, 1, 1),
(101, 'Kydon Hotel Chania', 65, 2, 0, 0, 0, 0),
(101, 'Rodos Palace Resort Hotel', 70, 2, 0, 1, 1, 1),
(101, 'Santorini Kastelli Resort', 80, 3, 1, 1, 0, 1),
(102, 'Athens Hilton Hotel', 90, 3, 1, 1, 0, 0),
(102, 'Classical Macedonia Palace', 100, 4, 1, 0, 0, 1),
(102, 'Corfu Holiday Palace', 100, 2, 0, 0, 1, 1),
(102, 'Grande Bretagne Hotel Athens', 30, 4, 0, 1, 0, 0),
(102, 'Kydon Hotel Chania', 40, 2, 0, 0, 0, 0),
(102, 'Rodos Palace Resort Hotel', 40, 3, 1, 1, 0, 0),
(102, 'Santorini Kastelli Resort', 120, 2, 0, 0, 1, 0),
(103, 'Athens Hilton Hotel', 90, 3, 1, 1, 0, 0),
(103, 'Classical Macedonia Palace', 120, 4, 1, 0, 0, 1),
(103, 'Grande Bretagne Hotel Athens', 80, 2, 0, 1, 1, 0),
(103, 'Kydon Hotel Chania', 25, 2, 1, 0, 0, 0),
(103, 'Rodos Palace Resort Hotel', 65, 4, 1, 1, 0, 0),
(103, 'Santorini Kastelli Resort', 40, 4, 1, 1, 0, 1),
(104, 'Athens Hilton Hotel', 90, 3, 1, 1, 0, 0),
(104, 'Classical Macedonia Palace', 100, 4, 1, 0, 0, 1),
(104, 'Rodos Palace Resort Hotel', 105, 2, 1, 0, 1, 1),
(104, 'Santorini Kastelli Resort', 85, 3, 0, 1, 1, 1),
(201, 'Athens Hilton Hotel', 90, 3, 1, 1, 0, 0),
(201, 'Classical Macedonia Palace', 120, 4, 1, 0, 0, 1),
(201, 'Corfu Holiday Palace', 100, 2, 0, 0, 1, 1),
(201, 'Grande Bretagne Hotel Athens', 20, 2, 0, 1, 0, 0),
(201, 'Kentrikon Hotel Ioannina', 20, 2, 1, 1, 1, 1),
(201, 'Kydon Hotel Chania', 50, 2, 0, 0, 0, 0),
(201, 'Rodos Palace Resort Hotel', 45, 2, 0, 1, 0, 1),
(201, 'Santorini Kastelli Resort', 85, 2, 1, 0, 1, 1),
(202, 'Athens Hilton Hotel', 90, 3, 1, 1, 0, 0),
(202, 'Classical Macedonia Palace', 120, 4, 1, 0, 0, 1),
(202, 'Corfu Holiday Palace', 100, 2, 0, 0, 1, 1),
(202, 'Grande Bretagne Hotel Athens', 80, 2, 0, 0, 1, 1),
(202, 'Kydon Hotel Chania', 50, 2, 0, 0, 0, 0),
(202, 'Rodos Palace Resort Hotel', 30, 2, 1, 1, 0, 0),
(202, 'Santorini Kastelli Resort', 50, 4, 0, 0, 0, 0),
(203, 'Athens Hilton Hotel', 60, 2, 1, 1, 1, 1),
(203, 'Classical Macedonia Palace', 120, 4, 1, 0, 0, 1),
(203, 'Grande Bretagne Hotel Athens', 90, 2, 0, 1, 0, 1),
(203, 'Kydon Hotel Chania', 55, 2, 1, 1, 0, 0),
(203, 'Rodos Palace Resort Hotel', 100, 3, 1, 1, 1, 1),
(203, 'Santorini Kastelli Resort', 70, 3, 1, 1, 0, 0),
(204, 'Athens Hilton Hotel', 60, 2, 1, 1, 1, 1),
(204, 'Classical Macedonia Palace', 120, 4, 1, 0, 0, 1),
(204, 'Rodos Palace Resort Hotel', 80, 2, 1, 1, 1, 1),
(204, 'Santorini Kastelli Resort', 95, 2, 1, 0, 1, 1);

--
-- Triggers `Room`
--
DROP TRIGGER IF EXISTS `DeleteRoom_DeleteReservation`;
DELIMITER //
CREATE TRIGGER `DeleteRoom_DeleteReservation` AFTER DELETE ON `Room`
 FOR EACH ROW DELETE FROM Reservation WHERE Reservation.`Hotel Name` = old.`Hotel Name`
AND Reservation.`Room No` = old.`Room No`
//
DELIMITER ;

-- --------------------------------------------------------

--
-- Stand-in structure for view `VIPCustomer`
--
CREATE TABLE IF NOT EXISTS `VIPCustomer` (
`id` varchar(30)
,`Surname` varchar(100)
,`Name` varchar(100)
,`Middle Name` varchar(100)
,`State` varchar(30)
,`City` varchar(30)
,`Municipality` varchar(30)
,`Street` varchar(100)
,`Street No` varchar(10)
,`Zipcode` int(10)
,`Phone` varchar(30)
,`Mobile Phone` varchar(30)
,`Fax` varchar(30)
,`Email` varchar(100)
,`Credit Card` varchar(30)
,`Expires` varchar(20)
,`VIP` tinyint(1)
);
-- --------------------------------------------------------

--
-- Structure for view `Debtor`
--
DROP TABLE IF EXISTS `Debtor`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `Debtor` AS select `Customer`.`id` AS `id`,`Customer`.`Surname` AS `Surname`,`Customer`.`Name` AS `Name`,`Customer`.`VIP` AS `VIP`,`Customer`.`Mobile Phone` AS `Mobile Phone`,`Customer`.`Phone` AS `Phone`,`DebtorIDs`.`Debt` AS `Debt` from (`Customer` join `DebtorIDs`) where (`Customer`.`id` = `DebtorIDs`.`id`);

-- --------------------------------------------------------

--
-- Structure for view `DebtorIDs`
--
DROP TABLE IF EXISTS `DebtorIDs`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `DebtorIDs` AS select `Reservation`.`id` AS `id`,sum(`Reservation`.`Remainder`) AS `Debt` from `Reservation` group by `Reservation`.`id` having (sum(`Reservation`.`Remainder`) > 100) order by sum(`Reservation`.`Remainder`) desc;

-- --------------------------------------------------------

--
-- Structure for view `VIPCustomer`
--
DROP TABLE IF EXISTS `VIPCustomer`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `VIPCustomer` AS select `Customer`.`id` AS `id`,`Customer`.`Surname` AS `Surname`,`Customer`.`Name` AS `Name`,`Customer`.`Middle Name` AS `Middle Name`,`Customer`.`State` AS `State`,`Customer`.`City` AS `City`,`Customer`.`Municipality` AS `Municipality`,`Customer`.`Street` AS `Street`,`Customer`.`Street No` AS `Street No`,`Customer`.`Zipcode` AS `Zipcode`,`Customer`.`Phone` AS `Phone`,`Customer`.`Mobile Phone` AS `Mobile Phone`,`Customer`.`Fax` AS `Fax`,`Customer`.`Email` AS `Email`,`Customer`.`Credit Card` AS `Credit Card`,`Customer`.`Expires` AS `Expires`,`Customer`.`VIP` AS `VIP` from `Customer` where (`Customer`.`VIP` = '1');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
