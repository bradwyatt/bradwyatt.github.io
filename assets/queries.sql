-- 1) Gets the number of elections each voter has ever voted in
with X as (select V.voterID, V.lname, V.fname, EV.electionID
from Voter as V left join ElectionVoter as EV
on V.voterID = EV.voterID)
select voterId, lname, fname, count(electionID) as ElectionsVotedIn
from X
group by voterID, lname, fname
order by ElectionsVotedIn desc;


--Gets the voters that voted in all elections
with X as (select V.voterID, V.lname, V.fname, EV.electionID
from Voter as V left join ElectionVoter as EV
on V.voterID = EV.voterID)
select voterId, lname, fname, count(electionID) as ElectionsVotedIn
from X
group by voterID, lname, fname
having  count(electionID) >=ALL
        (select count(electionID)
        from X
        group by voterID)
order by lname;


--Gets the voters who registered to vote but have least amount of votes
with X as (select V.voterID, V.lname, V.fname, EV.electionID
from Voter as V left join ElectionVoter as EV
on V.voterID = EV.voterID)
select voterId, lname, fname, count(electionID) as ElectionsVotedIn
from X
group by voterID, lname, fname
having  count(electionID) <=ALL
        (select count(electionID)
        from X
        group by voterID)
order by lname


-- 2) Candidates that have above average expenditure
with Alias as(select CandidateID, fname, lname, sum(amount) as TotalExpenses
        from (select C.candidateID, C.fname, C.lname, E.amount
                from candidate as C left join Expense as E
                on C.candidateId = E.CandidateID) as X
                group by CandidateID, fname, lname)
select lname, fname, TotalExpenses
from Alias
where TotalExpenses > (select avg(TotalExpenses) from Alias)
order by TotalExpenses DESC


-- 3) Donors and their parties
select D.fname, D.lname, C.party 
from Donor as D join Candidate as C
on D.CandidateID = C.CandidateID


--Donors who are also registered voters, Note: one of the donors is not a voter
select V.fname, V.lname, V.party
from  (select D.fname, D.lname, C.party 
        from Donor as D join Candidate as C
        on D.CandidateID = C.CandidateID) as X, Voter as V
where V.fname = X.fname
AND V.lname = X.lname
AND V.party = X.party


--Top donors for each candidate
WITH alias as (SELECT Candidate.fname, Candidate.lname, Candidate.candidateID, max(Donor.amount) as topDonorAmount
FROM Donor, Candidate
WHERE Candidate.candidateID = Donor.candidateID
GROUP BY Candidate.candidateID, Candidate.fname, Candidate.lname)
SELECT alias.fname, alias.lname, topDonorAmount, Donor.fname, Donor.lname
FROM alias, Donor
WHERE Donor.amount = topDonorAmount and 
alias.candidateID = Donor.candidateID




-- 4) Volunteers who volunteered for multiple candidates/elections
WITH alias as (SELECT distinct V.volunteerID, V.fname, V.lname, Volunteering.ElectionID
FROM Volunteer as V, Volunteering
WHERE V.volunteerID = Volunteering.VolunteerID
GROUP BY V.volunteerID, V.fname, V.lname, Volunteering.ElectionID)
SELECT alias.volunteerID, alias.fname, alias.lname, count(alias.ElectionID) as MultElections
FROM alias
GROUP BY alias.volunteerID, alias.fname, alias.lname
HAVING count(alias.ElectionID) > 1;



-- Modifications Queries:


-- Adding a family of three who just moved into the district without any prior voting history (in regards to score and rank):
-- INSERT INTO "Voter" VALUES (00027,'Arnold','Smith','43 Oak Nut Street', 'Pittsburgh, PA', 'M', '01/20/1998', '4', 'D', null, null)
-- INSERT INTO "Voter" VALUES (00028,'Sally','Smith','43 Oak Nut Street', 'Pittsburgh, PA', 'F', '01/20/1975', '4', 'D', null, null)
-- INSERT INTO "Voter" VALUES (00029,'Bob','Smith','43 Oak Nut Street', 'Pittsburgh, PA', 'M', '05/14/1974', '4', 'D', null, null)


-- Updating candidate “Brad Wyatt” to “Bradford Wyatt”:
-- UPDATE Candidate
-- SET fname = 'Bradford'
-- WHERE candidateID = '11';