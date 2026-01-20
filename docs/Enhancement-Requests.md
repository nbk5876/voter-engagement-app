# Enhancement Requests

Tracked enhancement requests from document reviews and team discussions.

---

## ENH-001: Group Leaders as News/Event Channels
**Status:** Proposed
**Date:** 1/19/2026
**Source:** Concept Doc Review - Rajat Aggarwal, Tony Byorick

### Description
Enable Civic Group leaders to act as channels for news and events that members care about (budgets, security updates, local events, etc.). This addresses the intrinsic motivation challenge by giving members a reason to stay engaged between elections.

### Rationale
- Addresses the voluntary participation challenge
- Provides ongoing value to group members
- Creates a natural information flow through the network
- Keeps groups active during non-election periods

### Related Use Cases
- May require new use cases for posting/sharing news within groups

---

## ENH-002: Campaign Promise Repository
**Status:** Proposed
**Date:** 1/19/2026
**Source:** Concept Doc Review - Tony Byorick

### Description
The app becomes a repository for campaign promises, making it convenient for voters to see what was promised. This supports post-election accountability by allowing supporters to track whether candidates fulfill their commitments.

### Rationale
- Enables post-election network persistence
- Creates accountability mechanism for candidates-turned-office-holders
- Provides ongoing value to voters beyond election cycles
- Supports the "trust-driven" model by promoting transparency

### Related Use Cases
- UC for adding/managing campaign promises
- UC for viewing promise fulfillment status
- UC for voters to ask questions about specific promises

---

## ENH-003: AI-Powered Promise News Scanning
**Status:** Proposed (Future)
**Date:** 1/19/2026
**Source:** Concept Doc Review - Tony Byorick

### Description
Leverage AI (ChatGPT, Claude, etc.) to perform periodic web scans for news related to campaign promises. Automatically surface relevant news to group members about whether promises are being kept.

### Rationale
- Reduces manual effort for tracking promise fulfillment
- Provides timely, relevant information to voters
- Enhances the accountability features of the app
- Could increase engagement by surfacing interesting content

### Technical Considerations
- Requires integration with AI APIs
- Need to define scanning frequency and sources
- Content moderation/accuracy verification needed
- Cost considerations for API usage

### Related Use Cases
- Multiple new use cases will be needed if implemented

---

## ENH-004: Post-Election Network Persistence
**Status:** Proposed
**Date:** 1/19/2026
**Source:** Concept Doc Review - Tony Byorick, Rajat Aggarwal

### Description
Design the network to persist after elections, transforming from a campaign tool into a channel for candidates-turned-office-holders to remain accountable to their supporters.

### Rationale
- Addresses the "interest flux" problem (high during elections, trailing off after)
- Creates long-term value for participants
- Supports the "learn, follow, lead" progression model
- Differentiates from typical campaign tools that go dormant post-election

### Design Considerations
- Members can only join 1 group but can lead another (per Rajat's suggestion)
- Groups act as persistent support networks
- Clear transition from campaign mode to accountability mode

### Related Use Cases
- Existing UC-CF-4 (Prevent Multiple Civic Group Memberships) supports this
- May need UCs for post-election features

---

## ENH-005: Single Membership, Multiple Leadership Model
**Status:** Proposed
**Date:** 1/19/2026
**Source:** Concept Doc Review - Rajat Aggarwal

### Description
A person can only join one Civic Group as a member, but can lead/create another group of their own. This guarantees persistent relationships and creates a "learn, follow, lead" progression.

### Rationale
- Addresses the network cluster/duplicate contact problem
- Guarantees persistent relationships
- Creates clear progression path for engagement
- Members act like a support group with opportunity to learn, follow, and lead

### Related Use Cases
- UC-CF-4 already addresses preventing multiple memberships
- May need clarification on leadership vs membership distinction
