# UC-CF-12: Specify Candidate Relationship

**Status:** Draft
**Date Added:** 1/19/2026
**Source:** Reviewer feedback from David Fallon and Tony Byorick

## Use Case Description

A Civic Group Member or Voter may optionally specify their relationship to a candidate when creating or joining a Civic Group, or when submitting a question.

## Actors
- Voter
- Civic Group Member

## Preconditions
- User is registered or in the process of registering
- At least one candidate exists in the system

## Main Flow
1. During registration, group creation, or question submission, the system presents an optional "Candidate Relationship" field
2. The user may select from predefined relationship types or skip this step
3. If selected, the system records the relationship association
4. The relationship may be updated by the user at any time

## Relationship Types (Suggested)
- Supporter
- Volunteer
- Donor
- Undecided
- Opposition
- No affiliation
- Other (free text)

## Postconditions
- The candidate relationship is stored with the user's profile
- The relationship can be viewed and edited by the user
- The relationship may inform future features (e.g., candidate outreach, analytics)

## Notes
- This field is optional to encourage broad participation
- Privacy considerations should be reviewed before exposing relationship data to candidates
