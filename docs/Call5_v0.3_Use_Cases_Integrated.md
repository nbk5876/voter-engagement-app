# Call5 Democracy - Use Cases v0.3
## Hub-and-Spoke Engagement Architecture

**Status:** Draft (Collaborative)  
**Owner:** Tony  
**Last Updated:** January 27, 2026  
**Version:** 0.3 - Integrated Use Cases

**Note on Versioning:** Starting with v0.3, Call5 Democracy uses v0.x numbering to reflect prototype/pre-production status, reserving v1.0 for public launch. Previous milestones (foundational work through database integration) were documented as v1.0-v1.2.

---

## Document History

| Date | Description |
|------|-------------|
| 1/27/2026 | Updated versioning scheme to v0.x (was v1.3, now v0.3) |
| 1/27/2026 | Integrated Hub-and-Spoke architecture with Living Document use cases |
| 1/20/2026 | Original Living Document version |
| 1/19/2026 | Changed Civic Unit to Civic Group |
| 1/19/2026 | Add City label to Civic Group |
| 1/19/2026 | Added UC-CF-8, UC-CF-9, UC-CF-10, UC-CF-11 |
| 1/19/2026 | Added Future Enhancements |

---

## Introduction

Call5 Democracy faces a fundamental challenge common to all civic engagement platforms: citizens are distributed across multiple communication channels—Nextdoor, Bluesky, Mastodon, Facebook, email—each with its own community norms and user preferences. Traditional approaches force a choice: either fragment conversations across platforms or require everyone to adopt a new tool.

The **Hub-and-Spoke Engagement** model solves this by meeting people where they already are while maintaining conversation depth and community coherence. Call5 serves as the central hub—the orchestration layer that coordinates notifications, tracks network growth, and hosts substantive dialogue. Platform-specific channels (Nextdoor, Bluesky, email) serve as spokes—delivering timely notifications to members based on their preferences.

This approach enables:
- **Exponential network growth**: Group leaders recruit through familiar platforms while Call5 tracks the Call-5 cascade
- **Sustained post-election engagement**: Notifications keep civic groups active beyond traditional campaign cycles
- **Platform flexibility**: Members choose their preferred notification channels without missing critical updates
- **Conversation coherence**: Deeper discussions converge in Call5 rather than fragmenting across platforms

This document captures the comprehensive use cases for Call5 Democracy v0.3, integrating the Hub-and-Spoke notification architecture with core voter engagement and civic organizing features. It is intended to:
- Provide a shared understanding of how voters, candidates, civic groups, and the notification system interact
- Guide database design and technical architecture decisions
- Surface assumptions and support discussion among team members and collaborators
- Serve as the foundation for v0.3 development planning

This is a living document. Feedback is welcome via comments, especially around clarity, realism, and missing scenarios.

---

## Hub-and-Spoke Engagement Concept

The Hub-and-Spoke Engagement model positions Call5 as the central hub that coordinates civic engagement across multiple communication platforms. Rather than requiring all members to abandon their preferred platforms, Call5 orchestrates notifications through the "spokes"—Nextdoor, Bluesky, Mastodon, email—based on each member's preferences.

The diagram below illustrates how this works in practice. The Oak Street Civic Group (hub) connects to five members, each receiving notifications through their preferred platforms. Sarah Martinez, as Group Leader, coordinates group activities and recruitment while members participate according to their communication preferences. This flexibility enables the Call-5 exponential growth model while respecting platform diversity.

```
                    Oak Street Civic Group
                         (5 Members)
                              |
        ┌─────────────┬───────┼───────┬─────────────┐
        ▼             ▼       ▼       ▼             ▼
   👑 Sarah      Marcus   Aisha    David        Lisa
   Group Leader  Member   Member   Member       Member
   📱 Nextdoor   📱 Bluesky 📱 Mastodon 📱 Nextdoor   📧 Email only
   📧 Email      📧 Email   📧 Email    📱 Bluesky
                                      📧 Email
```

### Platform Preferences
- **Nextdoor**: Sarah, David (neighborhood focus)
- **Bluesky**: Marcus, David (social media)
- **Mastodon**: Aisha (federated social)
- **Email**: Everyone has email as fallback

---

## Actors

### Voter
An individual who uses the application to submit a question or comment intended for a political candidate. The voter provides basic identifying information and the content of their inquiry. The voter's primary goal is to express a concern, ask a question, or seek clarification related to a candidate's campaign or public positions.

**Note**: A Voter does not need to be a Civic Group Member to use the question submission feature.

### Civic Group Member
An individual who belongs to a Civic Group within the Call Five People feature. A Civic Group Member may:
- Invite others to join the group
- Accept invitations
- View group membership
- Specify platform preferences for receiving notifications
- Submit questions to AI candidates
- Participate in group discussions in Call5

A Civic Group Member may also be a Voter, but Civic Group membership is not required to submit a question to a candidate.

### Group Leader
A Civic Group Member who founded or leads a civic group. Group Leaders have additional capabilities:
- Create and name their civic group
- Post announcements and updates to the group
- Recruit new members (Call-5 model)
- Act as a news/event channel for group members
- Receive notifications via their preferred platforms

### Candidate
A political candidate who is the intended recipient of voter questions. In the current implementation, candidate responses are generated by the system based on candidate-specific context rather than being authored directly by the candidate. The candidate actor represents the perspective and policy stance that informs the response.

### Call5 Democracy Platform
The system that facilitates interactions between voters, candidates, and civic groups. The platform:
- Collects voter input and generates AI candidate responses
- Manages civic group formation and membership
- Routes notifications through multiple platforms based on user preferences
- Tracks Call-5 recruitment networks
- Maintains conversation coherence by hosting discussions in the central hub
- Applies validation, logging, and configuration

### Administrator
An individual responsible for managing system configuration, candidate context, operational settings, and campaign promises. This role includes:
- Reviewing logs and system health
- Adding, modifying, or removing candidates
- Managing campaign promise repository
- Controlling feature availability
- Updating candidate-specific context files

---

## Core Use Cases

### Voter Questions

#### UC-VQ-1: Submit Question
**Actor**: Voter  
**Precondition**: None (anonymous submission supported)

**Flow**:
1. Voter navigates to Call5 Democracy question submission page
2. Voter selects a candidate from available options
3. Voter provides basic identifying information:
   - Name
   - Voter ID
   - Address
   - Email (optional for anonymous users; verified via Google OAuth for authenticated users)
4. Voter enters question or comment text
5. System validates required fields
6. System records submission with timestamp
7. System generates AI candidate response (UC-VQ-2)

**Post-condition**: Question is stored in database and AI response is triggered

---

#### UC-VQ-2: Candidate Response
**Actor**: System  
**Precondition**: Question has been submitted (UC-VQ-1)

**Flow**:
1. System retrieves candidate-specific context file
2. System generates AI response based on question and candidate context
3. System presents response to voter via web interface
4. System sends email notification to voter (if email provided)
5. If voter is a Civic Group Member, system triggers hub-and-spoke notification (UC-HS-2)

**Post-condition**: Voter receives AI candidate response; civic group optionally notified

---

### Call Five People - Civic Group Formation

#### UC-CF-1: Create a Civic Group
**Actor**: Civic Group Member (becomes Group Leader)  
**Precondition**: User has authenticated via Google OAuth

**Flow**:
1. User navigates to "Create Civic Group" feature
2. User enters:
   - Group name
   - Personal information (name, address, voter ID, email)
   - Platform preferences for notifications (Nextdoor, Bluesky, Mastodon, email)
3. System validates information
4. System creates new civic group with user as founding member and Group Leader
5. System assigns city name from founding member's address to the civic group
6. System generates unique invite link for the group
7. System displays confirmation and invite link

**Post-condition**: New civic group exists with one member (Group Leader); unique invite link is available

---

#### UC-CF-2: Invite People to Join Civic Group
**Actor**: Civic Group Member  
**Precondition**: User is member of a civic group

**Flow**:
1. Member navigates to "Invite Members" page
2. System displays unique invite link for their civic group
3. Member copies invite link
4. Member shares link via their preferred method:
   - Email
   - Direct message on social platform
   - Phone/SMS
   - In-person (QR code, text)
5. System tracks that this member sent invitation (timestamp, link usage)

**Post-condition**: Invite link is shared; system tracks invitation activity

---

#### UC-CF-3: Accept Invitation and Join Civic Group
**Actor**: New member (becomes Civic Group Member)  
**Precondition**: User has received invite link

**Flow**:
1. User clicks invite link
2. System displays civic group information and invitation context
3. User authenticates via Google OAuth
4. User provides:
   - Name
   - Address
   - Voter ID
   - Email
   - Phone (optional)
   - Platform preferences for notifications
5. System validates that user is not already member of another civic group (UC-CF-4)
6. System adds user as civic group member
7. System records who invited this member (network tracking - UC-CF-6)
8. System sends welcome notification to new member via their platform preferences
9. System notifies existing group members via hub-and-spoke (UC-HS-1)

**Post-condition**: User is civic group member; inviter and group are notified; network relationship is recorded

---

#### UC-CF-4: Prevent Multiple Civic Group Memberships
**Actor**: System  
**Precondition**: User attempts to join civic group while already being member of another

**Flow**:
1. System checks user's existing civic group membership
2. System detects existing membership
3. System prevents join action
4. System displays message: "You are already a member of [Group Name]. Each person can only be a member of one civic group, though you can lead your own group while being a member of another."
5. System offers option to view current group or learn about creating their own group

**Post-condition**: User remains in original civic group; duplicate membership prevented

---

#### UC-CF-5: Grow Beyond Five Members
**Actor**: Civic Group Member  
**Precondition**: Civic group already has five members

**Flow**:
1. Member invites additional person (UC-CF-2)
2. New person accepts invitation (UC-CF-3)
3. System allows group to grow beyond five members
4. System records growth milestone (for tracking exponential expansion)

**Post-condition**: Civic group has more than five members

**Note**: While five is the recommended "Call 5" size for each member's direct network, groups can grow organically beyond this threshold.

---

#### UC-CF-6: Track Who Invited Whom
**Actor**: System  
**Precondition**: Invitation accepted (UC-CF-3)

**Flow**:
1. System records invitation relationship:
   - Inviting member ID
   - New member ID
   - Timestamp
   - Civic group ID
2. System stores network growth path
3. System enables future analytics on:
   - Exponential growth patterns
   - Most active recruiters
   - Network depth and breadth

**Post-condition**: Invitation network is recorded for analysis and visualization

---

#### UC-CF-7: View Civic Group Membership
**Actor**: Civic Group Member  
**Precondition**: User is member of civic group

**Flow**:
1. Member navigates to "My Civic Group" page
2. System retrieves active members of user's civic group
3. System displays:
   - Group name
   - City
   - List of active members (names only for privacy)
   - Member count
   - Group Leader indicator
4. System does not display:
   - Inactive/removed members
   - Member contact information (privacy protection)
   - Platform preferences of other members

**Post-condition**: Member views current group roster

---

#### UC-CF-8: Maintain Political Issues List
**Actor**: Civic Group Members  
**Precondition**: Civic group exists

**Flow**:
1. Group Leader or members propose political issues important to the group
2. System stores issue list associated with civic group
3. Members can view, discuss, and update issue priorities
4. System uses issue list to:
   - Suggest relevant candidate questions
   - Filter news and updates (future enhancement ENH-003)
   - Guide group discussion topics

**Post-condition**: Civic group has curated list of priority issues

---

#### UC-CF-9: Platform Preference Management
**Actor**: Civic Group Member  
**Precondition**: User is member of civic group

**Flow**:
1. Member navigates to "Notification Preferences"
2. System displays current platform preferences
3. Member can enable/disable notification channels:
   - Nextdoor (if applicable to their neighborhood)
   - Bluesky
   - Mastodon
   - Email (always available)
   - Future: Facebook, SMS, other platforms
4. System validates at least one notification channel is enabled
5. System saves updated preferences
6. System confirms changes to user

**Post-condition**: Member's platform preferences are updated; future notifications route accordingly

---

#### UC-CF-10: Active Members Group List Access
**Actor**: Civic Group Member  
**Precondition**: User is member of civic group

**Flow**:
1. Member accesses group member list (UC-CF-7)
2. System filters to show only active members
3. System displays basic status:
   - Last activity date
   - Member since date
4. System respects privacy by not showing:
   - Contact details
   - Platform preferences
   - Personal demographic information

**Post-condition**: Member views active group roster with appropriate privacy protections

---

#### UC-CF-11: Google OAuth Authentication
**Actor**: Voter or Civic Group Member  
**Precondition**: User wants to verify email or access authenticated features

**Flow**:
1. User selects "Sign in with Google"
2. System redirects to Google OAuth consent screen
3. User authorizes Call5 Democracy
4. Google returns authentication token
5. System validates token
6. System creates or retrieves user session
7. System verifies user's email address via Google account
8. System grants access to authenticated features:
   - Email-based question responses
   - Civic group creation
   - Civic group membership
   - Notification preferences
   - Saved questions and responses

**Post-condition**: User is authenticated; email is verified; enhanced features are accessible

---

#### UC-CF-12: Specify Candidate Relationship
**Actor**: Civic Group Member or Voter  
**Precondition**: User is creating/joining civic group or submitting question

**Flow**:
1. User is prompted to optionally specify relationship to candidate:
   - Supporter
   - Undecided voter
   - Opponent
   - Not specified
2. User selects relationship (optional field)
3. System stores relationship preference
4. System uses relationship to:
   - Personalize AI candidate responses (tone, focus)
   - Filter relevant campaign promises
   - Customize notification content

**Post-condition**: User's candidate relationship is recorded and applied to interactions

---

### Hub-and-Spoke Notifications

#### UC-HS-1: Group Leader Posts Announcement
**Actor**: Group Leader  
**Precondition**: User is Group Leader of civic group

**Scenario**: Sarah Martinez wants to notify her Oak Street Civic Group about an upcoming town hall meeting.

**Flow**:
1. Sarah creates announcement in Call5 (text, links, optional attachments)
2. Sarah submits announcement to group
3. System stores announcement in civic group timeline
4. System triggers notification routing based on member preferences:
   - Marcus: Notification posted to his Bluesky feed + email sent
   - Aisha: Notification posted to her Mastodon feed + email sent
   - David: Notifications posted to Nextdoor AND Bluesky + email sent
   - Lisa: Email notification sent
5. Each notification includes:
   - Brief preview of announcement
   - Link back to Call5 for full details
   - Call-to-action (RSVP, respond, discuss)
6. Members click through to Call5 to view full announcement and participate in discussion

**Post-condition**: All members receive notification via preferred platforms; discussion happens in Call5

**Key Benefit**: One announcement reaches everyone on their preferred platform; no manual cross-posting required; conversation stays coherent in hub.

---

#### UC-HS-2: AI Candidate Response Shared with Group
**Actor**: System  
**Precondition**: Civic Group Member submits question to AI candidate (UC-VQ-1, UC-VQ-2)

**Scenario**: Marcus wants to ask the AI candidate personality about housing policy, and wants his civic group to see the response.

**Flow**:
1. Marcus submits housing policy question through Call5 interface
2. System generates AI candidate response
3. Marcus indicates "Share with my civic group" (optional checkbox)
4. System stores question and response
5. System triggers hub-and-spoke notifications to Oak Street Civic Group:
   - Sarah: Notification on Nextdoor + email
   - Marcus: Notification on Bluesky + email (original questioner)
   - Aisha: Notification on Mastodon + email
   - David: Notifications on Nextdoor + Bluesky + email
   - Lisa: Email notification
6. Notifications include:
   - "Marcus asked about housing policy"
   - Brief excerpt of AI response
   - Link to full Q&A in Call5
7. Group members discuss the AI response in Call5, building collective understanding

**Post-condition**: Group sees member's question; AI response is shared; discussion happens in hub

**Key Benefit**: AI candidate Q&A becomes a group learning experience, not isolated inquiry.

---

#### UC-HS-3: Call-5 Recruitment with Platform Integration
**Actor**: Civic Group Member  
**Precondition**: User is recruiting new members

**Scenario**: David Chen successfully recruits five new members to form his own civic group using his Nextdoor presence.

**Flow**:
1. David shares Call5 invite link in his Nextdoor neighborhood group
2. Post reaches his five neighbors who are active on Nextdoor
3. Neighbors click invite link and create accounts
4. Each neighbor specifies their platform preferences (varied: some Nextdoor, some Bluesky, some email-only)
5. System tracks David's recruitment success
6. System creates Maple Avenue Civic Group with David as Group Leader
7. David remains a member of Oak Street Civic Group (single membership rule)
8. David now leads Maple Avenue group (multiple leadership allowed - ENH-005)
9. Future announcements from David route to Maple Avenue members via their diverse preferences
10. Both Oak Street and Maple Avenue groups can interact, share AI candidate responses, and coordinate on civic issues

**Post-condition**: Exponential growth occurs; David is member of one group, leader of another; platform diversity is accommodated

**Key Benefit**: Exponential growth happens naturally through existing social networks while Call5 maintains the connection framework and respects platform diversity.

---

#### UC-HS-4: Cross-Platform Discussion Thread
**Actor**: Civic Group Member  
**Precondition**: Civic group exists with diverse platform preferences

**Scenario**: Aisha's question about transit policy generates significant interest across multiple platforms.

**Flow**:
1. Aisha submits transit question to AI candidate through Call5
2. AI responds with detailed policy position
3. Notifications go out through all platform preferences:
   - Sarah sees notification on Nextdoor
   - Marcus sees notification on Bluesky
   - David sees notifications on both Nextdoor AND Bluesky
   - Lisa receives email
4. Members click through to Call5 to read full AI response
5. Discussion happens in Call5 (not fragmented across platforms)
6. Sarah references the conversation when posting to broader Nextdoor community
7. New interested neighbors click through to join Oak Street Civic Group
8. New members specify their platform preferences during signup

**Post-condition**: Deep discussion stays coherent in Call5; platform-specific outreach attracts new members with diverse preferences

**Key Benefit**: Discussion coherence + platform-specific recruitment + no forced platform adoption.

---

#### UC-HS-5: Post-Election Network Persistence
**Actor**: Group Leader  
**Precondition**: Election has ended; civic group remains active

**Scenario**: Election ends, but the civic group continues engaging on local issues using hub-and-spoke notifications.

**Flow**:
1. Campaign AI personalities transition to tracking elected officials' promise fulfillment (ENH-002)
2. Sarah posts update about city council decision on housing
3. System routes notification via hub-and-spoke to all member preferences
4. Group discusses implications in Call5
5. AI candidate provides analysis based on campaign promises vs. actual votes (ENH-003)
6. Network remains active for:
   - Next election cycle
   - Local initiatives and ballot measures
   - Ongoing civic participation
   - Community organizing
7. Hub-and-spoke notifications maintain engagement through members' preferred platforms

**Post-condition**: Infrastructure built during campaign continues serving community; post-election silence is broken

**Key Benefit**: Sustained engagement beyond election cycles; community network persists; platform flexibility supports long-term participation.

---

#### UC-HS-6: Platform Migration Flexibility
**Actor**: Civic Group Member  
**Precondition**: User wants to change platform preferences

**Scenario**: David decides to reduce his Bluesky usage and focus more on Nextdoor.

**Flow**:
1. David navigates to "Notification Preferences" in Call5
2. David unchecks Bluesky
3. David keeps Nextdoor and Email checked
4. System saves updated preferences
5. Future notifications route to Nextdoor and email only
6. No disruption to group communication
7. David maintains full participation regardless of platform shifts
8. Other members' preferences remain unchanged

**Post-condition**: David's notifications now route to updated preferences; civic engagement continuity is maintained

**Key Benefit**: Platform preference changes don't break civic engagement continuity; members can adapt to evolving social media landscape.

---

### Admin Use Cases

#### UC-ADM-1: Monitor System Health
**Actor**: Administrator  
**Precondition**: Admin has system access

**Flow**:
1. Admin accesses monitoring dashboard
2. System displays:
   - Active users count
   - Questions submitted (daily/weekly/monthly)
   - Civic groups created
   - Network growth metrics (Call-5 cascade depth)
   - Email delivery rates (MailGun)
   - Platform notification success rates
   - API usage and performance
3. Admin reviews for anomalies
4. Admin takes corrective action if needed

**Post-condition**: System health is monitored; issues are identified

---

#### UC-ADM-2: Review Logs and Analytics
**Actor**: Administrator  
**Precondition**: Admin has system access

**Flow**:
1. Admin accesses logs and analytics
2. System provides:
   - Error logs
   - User activity patterns
   - Popular candidate questions
   - Network growth visualizations
   - Platform preference distributions
   - Notification delivery analytics
3. Admin analyzes trends
4. Admin generates reports for stakeholders

**Post-condition**: System usage patterns are understood; reports are generated

---

#### UC-ADM-3: Manage Feature Flags
**Actor**: Administrator  
**Precondition**: Admin has system access

**Flow**:
1. Admin accesses feature flag configuration
2. Admin can enable/disable:
   - Call Five People feature
   - Hub-and-Spoke notifications (per platform)
   - Campaign promise repository (ENH-002)
   - AI news scanning (ENH-003)
   - Group chat (if implemented)
3. System applies configuration changes
4. Features become available/unavailable to users accordingly

**Post-condition**: Feature availability is controlled; gradual rollout is supported

---

#### UC-ADM-4: Add/Modify/Delete a Candidate
**Actor**: Administrator  
**Precondition**: Admin has system access

**Flow**:
1. Admin navigates to "Manage Candidates"
2. Admin selects action:
   - **Add**: Enter candidate name, upload context file, set active status
   - **Modify**: Update candidate name or context file
   - **Delete**: Remove candidate (system warns if questions exist)
3. System validates input
4. System applies changes to database
5. System updates candidate selection dropdown for voters

**Post-condition**: Candidate roster is updated; AI responses use updated context

---

#### UC-ADM-5: Add/Manage Campaign Promises
**Actor**: Administrator  
**Precondition**: Admin has system access; ENH-002 is implemented

**Flow**:
1. Admin navigates to "Campaign Promises"
2. Admin selects candidate
3. Admin adds new promise:
   - Promise text
   - Category (housing, transit, education, etc.)
   - Date made
   - Source link
4. Admin can modify or delete existing promises
5. System stores promise in repository
6. System makes promise available for:
   - AI candidate responses
   - Post-election tracking
   - Group discussions
   - News scanning (ENH-003)

**Post-condition**: Campaign promise repository is updated; promises are tracked

---

## Future Enhancements

### ENH-001: Group Leaders as News/Event Channels
**Status**: Planned for v0.4+

**Description**: Enable Civic Group leaders to act as channels for news and events that members care about (budgets, security updates, local events, etc.). This addresses the intrinsic motivation challenge by giving members a reason to stay engaged between elections.

**Hub-and-Spoke Integration**: 
- Group Leader posts news/event via Call5
- Hub-and-spoke notifications route to all member platform preferences
- Members engage in Call5; conversation stays coherent
- Platform diversity accommodated without fragmenting discussion

**Use Case**: Sarah shares a City Council budget update affecting local parks. Marcus (Bluesky), Aisha (Mastodon), David (Nextdoor + Bluesky), and Lisa (email) all receive notifications on their preferred platforms, but discuss in Call5.

---

### ENH-002: Campaign Promise Repository
**Status**: Planned for v0.4+

**Description**: The app becomes a repository for campaign promises, making it convenient for voters to see what was promised. This supports post-election accountability by allowing supporters to track whether candidates fulfill their commitments.

**Hub-and-Spoke Integration**:
- Admin adds campaign promises (UC-ADM-5)
- AI candidate responses reference promises
- Group Leaders share promise updates
- Hub-and-spoke notifications alert members to promise tracking
- Members discuss promise fulfillment in Call5

**Use Case**: Three months after election, Sarah posts "City Council votes on housing density promise today." All members receive notification via preferences; group discusses in Call5 whether elected official is keeping promise.

---

### ENH-003: AI-Powered Promise News Scanning
**Status**: Planned for v0.4+

**Description**: Leverage AI (ChatGPT, Claude, etc.) to perform periodic web scans for news related to campaign promises. Automatically surface relevant news to group members about whether promises are being kept.

**Hub-and-Spoke Integration**:
- AI scans news for promise-related updates
- System generates notification when relevant news found
- Hub-and-spoke routes notification to all members via platform preferences
- Members click through to Call5 to view AI analysis and discuss
- Conversation stays coherent despite platform diversity

**Use Case**: AI detects news article: "City approves 500 new affordable housing units." System recognizes this relates to housing promise. Automated notification goes to all Oak Street members via their platforms (Nextdoor, Bluesky, Mastodon, email). Group discusses in Call5 whether promise was fulfilled.

---

### ENH-004: Post-Election Network Persistence
**Status**: Core to hub-and-spoke model; continuous implementation

**Description**: Design the network to persist after elections, transforming from a campaign tool into a channel for candidates-turned-office-holders to remain accountable to their supporters.

**Hub-and-Spoke Integration**:
- Already addressed by UC-HS-5
- Platform flexibility supports long-term engagement
- Members don't abandon groups post-election because notifications still reach them on familiar platforms
- Call5 becomes ongoing civic infrastructure, not just campaign tool

---

### ENH-005: Single Membership, Multiple Leadership Model
**Status**: Partially implemented; database schema supports this

**Description**: A person can only join one Civic Group as a member, but can lead/create another group of their own. This guarantees persistent relationships and creates a "learn, follow, lead" progression.

**Hub-and-Spoke Integration**:
- Already supported by UC-CF-4 (prevent multiple memberships) and UC-HS-3 (David scenario)
- Members maintain notification preferences in their member group
- Leaders can have separate notification preferences for their leadership group
- Platform flexibility allows members to participate in member group on one platform, lead leadership group on another

**Database Requirements**:
- User can have role "member" in one civic group
- Same user can have role "leader" in different civic group
- Each group-user relationship stores platform preferences separately

---

## Database Design Implications

The integrated use cases inform the v0.3 database schema design (Roadmap item 6.2):

### Core Entities
1. **Users**: Authentication, email verification (Google OAuth)
2. **Voters**: Question submissions, optional civic group membership
3. **Civic Groups**: Name, city, founding date, Group Leader
4. **Civic Group Memberships**: User-group relationships, join date, role (member/leader)
5. **Platform Preferences**: User-platform associations (Nextdoor, Bluesky, Mastodon, email, etc.)
6. **Invitations**: Network tracking (who invited whom, timestamps)
7. **Questions**: Voter submissions with candidate, timestamp
8. **AI Responses**: Generated responses linked to questions
9. **Announcements**: Group Leader posts with timestamps
10. **Campaign Promises** (ENH-002): Text, category, date, source, candidate
11. **Notifications**: Log of sent notifications (platform, timestamp, delivery status)

### Key Relationships
- User → Civic Group (member of one, leader of another)
- Civic Group → Members (one-to-many)
- User → Platform Preferences (one-to-many)
- Invitation → User (inviter and invitee)
- Question → AI Response (one-to-one or one-to-many)
- Announcement → Civic Group (one-to-many)
- Notification → User + Platform (tracking delivery)

### Critical Constraints
- User can be member of only ONE civic group (UC-CF-4)
- User can be leader of DIFFERENT civic group simultaneously (ENH-005)
- Each user must have at least one platform preference enabled (email fallback)
- Invitation tracking preserves network growth history (UC-CF-6)

---

## Notes for v0.3 Development

1. **Notification Routing Logic**: Core hub-and-spoke functionality requires platform API integrations (Nextdoor, Bluesky, Mastodon) in addition to existing MailGun email.

2. **Database Schema Expansion**: Roadmap item 6.3 requires adding platform preferences table, notification log table, and invitation tracking fields.

3. **Platform API Research**: Investigate API availability and authentication for:
   - Nextdoor: Limited API; may require manual posting or browser automation
   - Bluesky: AT Protocol; full API available
   - Mastodon: ActivityPub; API available per instance
   - Future: Facebook Graph API, Twitter/X API (if relationships normalize)

4. **Privacy Considerations**: Platform preferences are user-specific and private; other members cannot see them (UC-CF-7, UC-CF-10).

5. **Testing Strategy**: Hub-and-spoke functionality requires integration testing with actual platform APIs in sandbox/development environments.

6. **Scalability**: Notification routing at scale requires queuing system (e.g., Celery, RabbitMQ) for asynchronous delivery.

---

## Conclusion

This integrated use case document provides the comprehensive foundation for Call5 Democracy v0.3 development. By combining the Hub-and-Spoke notification architecture with the proven voter engagement and civic organizing features, Call5 is positioned to:

- Meet voters where they already are (platform flexibility)
- Enable exponential network growth (Call-5 model)
- Maintain conversation coherence (hub for discussion)
- Support post-election persistence (sustained engagement)
- Respect user privacy and preferences (platform choice, single membership)

The next step is detailed database design (Roadmap item 6.2) based on these use cases, followed by schema expansion and implementation (Roadmap item 6.3).

---

**Document Status**: Ready for collaborative review and refinement.

**Feedback Welcome**: Comments on clarity, missing scenarios, technical feasibility, and user experience implications are encouraged.
