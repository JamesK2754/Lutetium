SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


CREATE TABLE `files` (
  `dlID` int(11) NOT NULL,
  `dlName` varchar(100) NOT NULL,
  `dlURL` varchar(100) NOT NULL,
  `Type` int(11) NOT NULL,
  `Status` int(11) NOT NULL,
  `dateAdded` varchar(100) DEFAULT NULL,
  `dateCompleted` varchar(100) DEFAULT NULL,
  `timeTaken` varchar(100) DEFAULT NULL,
  `Locations` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `files`
  ADD PRIMARY KEY (`dlID`);

ALTER TABLE `files`
  MODIFY `dlID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
COMMIT;