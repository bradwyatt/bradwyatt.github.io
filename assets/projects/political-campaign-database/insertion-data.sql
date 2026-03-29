--Deleting Existing Tables


if exists (
        select *
        from sys.tables
        where name = 'Election'
        and type = 'U')
BEGIN
drop table "Election"
END;


if exists (
        select *
        from sys.tables
        where name = 'Candidate'
        and type = 'U')
BEGIN
drop table "Candidate"
END;


if exists (
        select *
        from sys.tables
        where name = 'Donor'
        and type = 'U')
BEGIN
drop table "Donor"
END;


if exists (
        select *
        from sys.tables
        where name = 'Expense'
        and type = 'U')
BEGIN
drop table "Expense"
END;




if exists (
        select *
        from sys.tables
        where name = 'Volunteer'
        and type = 'U')
BEGIN
drop table "Volunteer"
END;


if exists (
        select *
        from sys.tables
        where name = 'Voter'
        and type = 'U')
BEGIN
drop table "Voter"
END;


if exists (
        select *
        from sys.tables
        where name = 'ContactMethod'
        and type = 'U')
BEGIN
drop table "ContactMethod"
END;


if exists (
        select *
        from sys.tables
        where name = 'Election-Vote'
        and type = 'U')
BEGIN
drop table "Election-Vote"
END;






-- Table structure for table “Election”


CREATE TABLE "Election" (
  "electionID" int NOT NULL default '0',
  "year" int default NULL,
  "position" varchar(100) default NULL,
  "district" varchar(100) default NULL,
  "type" varchar(100) default NULL,
  PRIMARY KEY  ("electionID")
);


---Election Table
INSERT INTO "Election" VALUES (001, 2012, 'Governor', '4', 'General')
INSERT INTO "Election" VALUES (002, 2014, 'President', '4', 'Primary')
INSERT INTO "Election" VALUES (003, 2014, 'State Representative', '4', 'General')
INSERT INTO "Election" VALUES (004, 2016, 'Mayor', '4', 'General')




-- Table structure for table “Candidate”


CREATE TABLE "Candidate" (
  "candidateID" int NOT NULL default '0',
  "fname" varchar(100) default NULL,
  "lname" varchar(100) default NULL,
  "gender" char(1) default NULL,
  "electionID" int default NULL,
  "party" varchar(100) default NULL,
  PRIMARY KEY  ("candidateID")
);


-- Candidate Table


--- INSERT INTO "Candidate" VALUES (CID, fname, lname, gender, ElectionID, Party)
INSERT INTO "Candidate" VALUES (11, 'Brad', 'Wyatt', 'M', '001', 'R')
INSERT INTO "Candidate" VALUES (22, 'Jeffrey', 'Chan', 'M', '001', 'D')
INSERT INTO "Candidate" VALUES (44, 'Dominic', 'Liu', 'M', '001', 'D')
INSERT INTO "Candidate" VALUES (33, 'Richa', 'Mohan', 'F', '002', 'D')
INSERT INTO "Candidate" VALUES (77, 'Brian', 'Hunt', 'M', '002', 'D')
INSERT INTO "Candidate" VALUES (55, 'Wolfgang', 'Gatterbauer', 'M', '003', 'I')
INSERT INTO "Candidate" VALUES (66, 'Subra', 'Suresh', 'M', '003', 'L')




-- Table structure for table “Donor”


CREATE TABLE "Donor" (
  "donorID" int NOT NULL default '0',
  "candidateID" int default NULL,
  "fname" varchar(100) default NULL,
  "lname" varchar(100) default NULL,
  "amount" varchar(100) default NULL,
  PRIMARY KEY  ("donorID"),
  FOREIGN KEY(candidateID) REFERENCES Candidate(candidateID)
);


-- Donor Table


-- INSERT INTO "Donor" VALUES (DonorID, CID, fname, lname, amount)
INSERT INTO "Donor" VALUES (1, 11, 'John', 'Park', 300)
INSERT INTO "Donor" VALUES (2, 33, 'Paul', 'Pierce', 500)
INSERT INTO "Donor" VALUES (3, 22, 'Lucas', 'Connors', 200)
INSERT INTO "Donor" VALUES (4, 44, 'Andrew', 'Bale', 150)
INSERT INTO "Donor" VALUES (5, 55, 'Sam', 'Smith', 500)
INSERT INTO "Donor" VALUES (6, 55, 'Christine', 'Nolan', 400)


-- Table structure for table “Expense”


CREATE TABLE "Expense" (
  "expenseID" int NOT NULL default '0',
  "candidateID" int default NULL,
  "date" varchar(100) default NULL,
  "purpose" varchar(100) default NULL,
  "amount" int default NULL,
  PRIMARY KEY  ("expenseID"),
  FOREIGN KEY(candidateID) REFERENCES Candidate(candidateID)
);


-- INSERT INTO "Expense" VALUES (ExpenseID, CID, Date, Purpose, Amount)


INSERT INTO "Expense" VALUES (01, 44, '03/14/2014', 'Advertising', 2000)
INSERT INTO "Expense" VALUES (02, 33, '03/15/2014', 'Canvassing', 300)
INSERT INTO "Expense" VALUES (03, 66, '03/16/2014', 'Polling', 40)
INSERT INTO "Expense" VALUES (04, 22, '03/19/2012', 'Canvassing', 500)
INSERT INTO "Expense" VALUES (05, 11, '03/21/2012', 'Signs', 1000)
INSERT INTO "Expense" VALUES (06, 55, '03/25/2014', 'Mailing', 700)
INSERT INTO "Expense" VALUES (07, 44, '03/14/2014', 'Signs', 1200)
INSERT INTO "Expense" VALUES (08, 33, '03/15/2014', 'Canvassing', 400)
INSERT INTO "Expense" VALUES (09, 66, '03/16/2014', 'Advertising', 5000)
INSERT INTO "Expense" VALUES (010, 22, '03/19/2012', 'Polling', 300)
INSERT INTO "Expense" VALUES (011, 11, '03/21/2012', 'Advertising', 2000)
INSERT INTO "Expense" VALUES (012, 55, '03/25/2014', 'Advertising', 2700)


-- Table structure for table “Volunteer”


CREATE TABLE "Volunteer" (
  "volunteerID" int NOT NULL default '0',
  "fname" varchar(100) default NULL,
  "lname" varchar(100) default NULL,
  "location" varchar(100) default NULL,
  "DOB" varchar(100) default NULL,
  "role" varchar(100) default NULL,
  PRIMARY KEY  ("volunteerID")
);


---Volunteer Table


---INSERT INTO "Volunteer" VALUES (VolunteerID, CID, fname, lname, location, DOB, role, managedby)


INSERT INTO "Volunteer" VALUES (1011, 'Jennifer', 'Huang', 'Pittsburgh, PA', '04/25/1984', 'Campaign Manager')
INSERT INTO "Volunteer" VALUES (1012, 'Tiffany', 'Lai', 'Pittsburgh, PA', '06/12/1993', 'Canvas Leader')
INSERT INTO "Volunteer" VALUES (1013, 'Jeffrey', 'Kang', 'Pittsburgh, PA', '02/17/1989', 'Calling Leader')
INSERT INTO "Volunteer" VALUES (1014, 'John', 'Smith', 'Pittsburgh, PA', '05/23/1993', 'Graphic Designer')
INSERT INTO "Volunteer" VALUES (1015, 'Ram', 'Gupta', 'Pittsburgh, PA', '07/12/1990', 'General Volunteer')
INSERT INTO "Volunteer" VALUES (1016, 'Tyrone', 'Singer', 'Pittsburgh, PA', '02/30/1988', 'Campaign Manager')
INSERT INTO "Volunteer" VALUES (1017, 'Donald', 'Sanders', 'Hazelwood, PA', '08/20/1991', 'General Volunteer')
INSERT INTO "Volunteer" VALUES (1018, 'Hilary', 'Trump', 'Pittsburgh, PA', '10/23/1995', 'General Volunteer')
INSERT INTO "Volunteer" VALUES (1019, 'Paul', 'Kim', 'Carnegie, PA', '03/03/1993', 'Event Organizer')


-- Table structure for table “Voter”


CREATE TABLE Voter (
  "voterID" int NOT NULL default '0',
  "fname" varchar(100) default NULL,
  "lname" varchar(100) default NULL,
  "address" varchar(100) default NULL,
  "town" varchar(100) default NULL,
  "gender" varchar(100) default NULL,
  "DOB" varchar(100) default NULL,  
  "district" varchar(100) default NULL,
  "party" varchar(100) default NULL,
  "Score" varchar(100) default NULL,
  "Rank" int default NULL,
  PRIMARY KEY  ("voterID"),
);


--Voter Table


INSERT INTO "Voter" VALUES (0001,'Lewis','Abernathy','20 Applepie Lane', 'Pittsburgh, PA', 'M', '11/07/1993', '4', 'R', 'A', 1);
INSERT INTO "Voter" VALUES (0002,'Mary','Ironson','15 Blueberrypie Lane', 'Carnegie, PA', 'F', '12/15/1988', '4', 'R', 'C', 2)
INSERT INTO "Voter" VALUES (0003,'Jessica','Mascetta','300 Grant Street', 'Hazelwood, PA', 'F', '1/19/1987', '4', 'D', 'B', 5)
INSERT INTO "Voter" VALUES (0004,'John','Campbell','56 Flower Drive', 'Pittsburgh, PA', 'M', '11/25/1956', '4', 'L', 'C', 3)
INSERT INTO "Voter" VALUES (0005,'Jeff','Oldroyd','78 Mulberry Lane', 'Carnegie, PA', 'M', '3/29/1955', '4', 'R', 'C', 1)
INSERT INTO "Voter" VALUES (0006,'Dom','Budz','55 Placket Drive', 'Hazelwood, PA', 'M', '4/18/1947', '4', 'R', 'A', 1)
INSERT INTO "Voter" VALUES (0007,'Brad','Cole','45 Circle Drive', 'Pittsburgh, PA', 'M', '6/03/1989', '4', 'I', 'A', 1)
INSERT INTO "Voter" VALUES (0008,'Wolfgang','Brown','1 Malcolm Lane', 'Carnegie, PA', 'M', '8/01/1965', '4', 'L', 'B', 1)
INSERT INTO "Voter" VALUES (0009,'Clark','Bombard','14 Ellsworth Avenue', 'Hazelwood, PA', 'M', '9/22/1972', '4', 'R', 'A', 1)
INSERT INTO "Voter" VALUES (00010,'Stephanie','Haitsma','12 Beeler Street', 'Pittsburgh, PA', 'F', '10/23/1983', '4', 'D', 'B', 4)
INSERT INTO "Voter" VALUES (00011, 'John', 'Park', '5283 Palisades Ave', 'Pittsburgh, PA', 'M', '12/30/1976', '4', 'R', 'A', 1)
INSERT INTO "Voter" VALUES (00012, 'Paul', 'Pierce', '32 Mill Road', 'Pittsburgh, PA', 'M', '3/22/1979', '4', 'D', 'A', 5)
INSERT INTO "Voter" VALUES (00013, 'Lucas', 'Connors', '91 Lynn Drive', 'Pittsburgh, PA', 'M', '6/11/1982', '4', 'R', 'A', 2)
INSERT INTO "Voter" VALUES (00014, 'Andrew', 'Bale', '47 Circle Drive', 'Pittsburgh, PA', 'M', '9/19/1969', '4', 'D', 'A', 5)
INSERT INTO "Voter" VALUES (00015, 'Sam', 'Smith', '300 Neville Ave', 'Carnegie, PA', 'M', '7/27/1971', '4', 'I', 'A', 3)
INSERT INTO "Voter" VALUES (00016, 'Christine', 'Nolan', '7822 Fifth Ave', 'Pittsburgh, PA', 'F', '2/28/1980', '4', 'I', 'A', 3)
INSERT INTO "Voter" VALUES (00017, 'Jennifer', 'Huang', '25 Road Road', 'Pittsburgh, PA', 'F', '04/25/1984', '4', 'R', 'A', 1)
INSERT INTO "Voter" VALUES (00018, 'Tiffany', 'Lai', '92 Modern Lane', 'Pittsburgh, PA', 'F', '06/12/1993', '4', 'R', 'A', 1)
INSERT INTO "Voter" VALUES (00019, 'Jeffrey', 'Kang', '123 Alphabet Way', 'Pittsburgh, PA', 'M', '02/17/1989', '4', 'D', 'B', 5)
INSERT INTO "Voter" VALUES (00020, 'John', 'Smith', '293 Jeff Ave', 'Pittsburgh, PA', 'M', '05/23/1993', '4', 'D', 'A', 5)
INSERT INTO "Voter" VALUES (00021, 'Rolf', 'Goldberg', '9300 Brad House', 'Carnegie, PA', 'M', '11/03/1987', '4', 'D', 'A', 4)
INSERT INTO "Voter" VALUES (00022, 'Ram', 'Gupta', '42 Madeline Place', 'Pittsburgh, PA', 'M', '07/12/1990', '4', 'D', 'B', 5)
INSERT INTO "Voter" VALUES (00023, 'Tyrone', 'Singer', '1 Something Drive', 'Pittsburgh, PA',  'M','02/30/1988', '4', 'D', 'B', 5)
INSERT INTO "Voter" VALUES (00024, 'Donald', 'Sanders', '23 Great Again', 'Hazelwood, PA', 'M', '08/20/1991', '4', 'D', 'A', 5)
INSERT INTO "Voter" VALUES (00025, 'Hilary', 'Trump', '943 Harrison Drive', 'Pittsburgh, PA', 'F', '10/23/1995', '4', 'D', 'A', 5)
INSERT INTO "Voter" VALUES (00026, 'Paul', 'Kim', '1422 Election Place', 'Carnegie, PA', 'M', '03/03/1993', '4', 'I', 'A', 3)


-- Table structure for table “Election-Voter”


CREATE TABLE "ElectionVoter" (
  "voterID" int NOT NULL default '0',
  "electionID" int NOT NULL default '0',
  FOREIGN KEY(voterID) REFERENCES Voter(voterID),
  FOREIGN KEY(electionID) REFERENCES Election(electionID)
);


---Election-Voter Table


INSERT INTO "ElectionVoter" VALUES (0001, 001)
INSERT INTO "ElectionVoter" VALUES (0001, 002)
INSERT INTO "ElectionVoter" VALUES (0001, 003)
INSERT INTO "ElectionVoter" VALUES (0002, 001)
INSERT INTO "ElectionVoter" VALUES (0002, 004)
INSERT INTO "ElectionVoter" VALUES (0003, 001)
INSERT INTO "ElectionVoter" VALUES (0003, 002)
INSERT INTO "ElectionVoter" VALUES (0004, 002)
INSERT INTO "ElectionVoter" VALUES (0005, 003)
INSERT INTO "ElectionVoter" VALUES (0006, 001)
INSERT INTO "ElectionVoter" VALUES (0006, 002)
INSERT INTO "ElectionVoter" VALUES (0006, 003)
INSERT INTO "ElectionVoter" VALUES (0006, 004)
INSERT INTO "ElectionVoter" VALUES (0007, 001)
INSERT INTO "ElectionVoter" VALUES (0007, 002)
INSERT INTO "ElectionVoter" VALUES (0007, 003)
INSERT INTO "ElectionVoter" VALUES (0008, 001)
INSERT INTO "ElectionVoter" VALUES (0008, 002)
INSERT INTO "ElectionVoter" VALUES (0008, 003)
INSERT INTO "ElectionVoter" VALUES (0009, 001)
INSERT INTO "ElectionVoter" VALUES (0009, 002)
INSERT INTO "ElectionVoter" VALUES (0009, 003)
INSERT INTO "ElectionVoter" VALUES (00010, 001)
INSERT INTO "ElectionVoter" VALUES (00011, 002)
INSERT INTO "ElectionVoter" VALUES (00012, 003)
INSERT INTO "ElectionVoter" VALUES (00013, 001)
INSERT INTO "ElectionVoter" VALUES (00014, 002)
INSERT INTO "ElectionVoter" VALUES (00015, 003)
INSERT INTO "ElectionVoter" VALUES (00016, 001)
INSERT INTO "ElectionVoter" VALUES (00017, 002)
INSERT INTO "ElectionVoter" VALUES (00018, 003)
INSERT INTO "ElectionVoter" VALUES (00019, 001)
INSERT INTO "ElectionVoter" VALUES (00019, 002)
INSERT INTO "ElectionVoter" VALUES (00019, 003)
INSERT INTO "ElectionVoter" VALUES (00020, 001)
INSERT INTO "ElectionVoter" VALUES (00021, 002)
INSERT INTO "ElectionVoter" VALUES (00022, 003)
INSERT INTO "ElectionVoter" VALUES (00023, 001)
INSERT INTO "ElectionVoter" VALUES (00024, 002)
INSERT INTO "ElectionVoter" VALUES (00020, 003)
INSERT INTO "ElectionVoter" VALUES (00018, 001)
INSERT INTO "ElectionVoter" VALUES (00010, 002)


-- Table structure for table “ContactMethod”


CREATE TABLE ContactMethod (
  "voterID" int default NULL,
  "volunteerID" int default NULL,
  "dateOfContact" varchar(100) default NULL,
  "method" varchar(100) default NULL,
  FOREIGN KEY(voterID) REFERENCES Voter(voterID),
  FOREIGN KEY(volunteerID) REFERENCES Volunteer(volunteerID)
);


-- ContactMethod Table


-- INSERT INTO "ContactMethod" VALUES (voterID, VolunteerID, DateOfContact, Method)


INSERT INTO "ContactMethod" VALUES (1, 1011, '01/15/2015', 'DoorKnock')
INSERT INTO "ContactMethod" VALUES (1, 1011, '05/15/2011', 'mail')
INSERT INTO "ContactMethod" VALUES (1, 1011, '01/15/2013', 'Phonecall')
INSERT INTO "ContactMethod" VALUES (2, 1012, '03/18/2015', 'DoorKnock')
INSERT INTO "ContactMethod" VALUES (3, 1013, '01/15/2015', 'mail')
INSERT INTO "ContactMethod" VALUES (3, 1013, '08/21/2011', 'mail')
INSERT INTO "ContactMethod" VALUES (4, 1014, '01/25/2011', 'Phonecall')
INSERT INTO "ContactMethod" VALUES (5, 1015, '08/15/2014', 'DoorKnock')
INSERT INTO "ContactMethod" VALUES (6, 1016, '07/18/2016', 'DoorKnock')
INSERT INTO "ContactMethod" VALUES (6, 1016, '02/15/2012', 'mail')
INSERT INTO "ContactMethod" VALUES (6, 1016, '9/15/2014', 'Phonecall')
INSERT INTO "ContactMethod" VALUES (7, 1017, '07/08/2016', 'DoorKnock')
INSERT INTO "ContactMethod" VALUES (7, 1017, '06/25/2012', 'Phonecall')
INSERT INTO "ContactMethod" VALUES (7, 1017, '05/18/2014', 'DoorKnock')
INSERT INTO "ContactMethod" VALUES (8, 1018, '03/05/2016', 'mail')
INSERT INTO "ContactMethod" VALUES (8, 1018, '05/19/2012', 'DoorKnock')
INSERT INTO "ContactMethod" VALUES (8, 1018, '07/25/2014', 'mail')
INSERT INTO "ContactMethod" VALUES (9, 1019, '02/27/2016', 'mail')
INSERT INTO "ContactMethod" VALUES (9, 1019, '12/15/2011', 'DoorKnock')
INSERT INTO "ContactMethod" VALUES (9, 1019, '05/11/2014', 'Phonecall')








CREATE TABLE Volunteering (
  "VolunteerID" int default NULL,
  "CandidateID" int default NULL,
  "ElectionID" int default NULL,
  FOREIGN KEY(VolunteerID) REFERENCES Volunteer(volunteerID),
  FOREIGN KEY(CandidateID) REFERENCES Candidate(CandidateID),
  FOREIGN KEY(ElectionID) REFERENCES Election(ElectionID)
);


--Volunteering Table


INSERT INTO "Volunteering" VALUES (1011, 11, 001);
INSERT INTO "Volunteering" VALUES (1011, 77, 002);
INSERT INTO "Volunteering" VALUES (1013, 22, 001)
INSERT INTO "Volunteering" VALUES (1012, 11, 001)
INSERT INTO "Volunteering" VALUES (1014, 22, 002)
INSERT INTO "Volunteering" VALUES (1015, 33, 002)
INSERT INTO "Volunteering" VALUES (1016, 33, 002)
INSERT INTO "Volunteering" VALUES (1017, 33, 002)
INSERT INTO "Volunteering" VALUES (1018, 44, 001)
INSERT INTO "Volunteering" VALUES (1019, 44, 002)