# Call5 Democracy v0.4.01 UI Documentation

**Version:** v0.4.01  
**Date:** February 5, 2026  
**Features:** Group Broadcast Messaging, Dashboard, Admin Tools, Network Tree

---

## Overview

This document provides visual documentation of the Call5 Democracy platform user interface as of version 0.4.01. Screenshots demonstrate the complete user journey from landing page through authentication, dashboard access, group management, messaging, and administrative tools.

---

## Authentication Flow

### Landing Page (Pre-Login)

**Screenshot:** `landing page pre-login.png`

**Description:**  
The entry point for all users. Displays the Voter Engagement Response Form branding with two authentication options:

**Key Features:**
- **"Sign in with Google"** button - OAuth authentication for users with Google accounts
- **"Sign up with Email"** button - Local authentication alternative (v0.4.03)
- **"Already have an account? Log in"** link
- Mobile-responsive design
- Clean, professional branding

**User Actions:**
- New users: Click either signup option
- Returning users: Click "Log in" link
- Anonymous users: Can still submit voter questions (form below)

**Technical Notes:**
- Both auth methods create same User record structure
- Session management unified regardless of auth type
- Invite code tracking via `?ref=` parameter in URL

---

### Landing Page (Post-Login)

**Screenshot:** `landing page post-login.png`

**Description:**  
Same landing page, but header now shows authenticated user state.

**Key Features:**
- User email displayed in header: "tony.byorick@gmail.com"
- **"Dashboard"** button - Navigate to main user interface
- **"Sign Out"** button - Clear session and return to pre-login state
- Voter question form remains accessible

**User Actions:**
- Submit voter questions (now attributed to authenticated user)
- Navigate to Dashboard for network management
- Sign out when finished

---

## Main Dashboard

### Dashboard (Welcome Screen)

**Screenshot:** `dashboard.png`

**Description:**  
Central hub for authenticated users. Displays network statistics, invite link management, and navigation to all platform features.

**Key Features:**

**Header Section:**
- "Call5 Democracy" branding
- User email: "tony.byorick@gmail.com"
- "Sign Out" button

**Welcome Card:**
- Personalized greeting: "Welcome, Tony Byorick!"
- Recruit count: "3 People Recruited"
- (Optional) "Recruited by: [name]" if user was recruited

**Invite Link Section:**
- Unique referral URL: `https://voter-engagement-app.onrender.com/?ref=OjQobOWu`
- **"Copy"** button - Clipboard API with "Copied!" feedback
- Encourages network growth through personal sharing

**Action Buttons:**
- **"Share Your Invite Link"** - Navigate to platform-specific sharing options
- **"Message Your Recruiter"** - Send 1:1 message to person who recruited you
- **"Message Your Recruits"** - Broadcast or individual messages to your network
- **"Messages"** - View message inbox
- **"Create Group"** - Start a new group (requires recruit_count > 0)
- **"Your Groups"** - List all groups you've created or joined
- **"Submit Voter Question"** - Return to voter form
- **"Admin"** - Access admin tools (only visible if is_admin=TRUE)
- **"Tree"** - View network visualization

**Technical Implementation:**
- All buttons conditional based on user state
- Copy button uses `navigator.clipboard.writeText()`
- Mobile-responsive button stacking

---

## Group Management

### Create Group

**Screenshot:** `create group.png`

**Description:**  
Form for creating a new civic group within the Call5 network.

**Key Features:**

**Header:**
- Page title: "Create a Group"
- Subtitle: "Create a civic group to organize your community."

**Form Fields:**
- **Group Name** (required) - Example: "54 Ave Group"
- **Description** (optional) - Purpose or focus of the group

**Action Buttons:**
- **"Create Group"** - Submit form and create group record
- **"Back to Dashboard"** - Cancel and return

**Business Rules:**
- Only users with `recruit_count > 0` can create groups
- User automatically becomes group founder
- Creates records in `groups` and `group_members` tables

**User Flow:**
1. Click "Create Group" from dashboard
2. Fill in group name (required)
3. Optionally add description
4. Submit → Redirected to group management page
5. Can immediately start inviting recruits to join

---

### Your Groups

**Screenshot:** `your groups.png`

**Description:**  
List of all groups the user has created or joined.

**Key Features:**

**Header:**
- "Your Groups" title
- Subtitle: "Groups you belong to or have created."

**Group List:**
Each group displayed as a card with:
- **Group Name** - "54 Ave Group", "15th Ave NW", "See Out My Space group"
- **Role Badge** - "Founder" (blue) for creator, "Member" for invitees
- **Member Count** - Total group members (e.g., "3 members")
- **Created By** - Founder's name: "Tony Byorick"
- **Created Date** - When group was created

**Action Buttons:**
- **"Create Group"** - Add a new group
- **"Back to Dashboard"** - Return to main screen

**User Actions:**
- Click on group name → Navigate to group management page
- View all groups at a glance
- See role in each group

**Technical Notes:**
- Queries `group_members` table joined with `groups`
- Displays both founded and joined groups
- Sorted by creation date (most recent first)

---

## Messaging System

### New Message (Compose)

**Screenshot:** `new message.png`

**Description:**  
Form for composing a new 1:1 message to a recruit or recruiter.

**Key Features:**

**Header:**
- "New Message" title

**Form Fields:**
- **To:** - Dropdown to select recipient
  - Shows only valid messaging relationships
  - Recruiter sees all their recruits
  - Recruit sees their recruiter only
- **Subject (optional)** - Defaults to "Message from [sender name]"
- **Message** - Text area for message body (required)

**Action Buttons:**
- **"Send Message"** - Submit and deliver message
- **"Back to Messages"** - Cancel and return to inbox

**User Flow:**
1. Click "Message Your Recruits" from dashboard OR "New Message" from inbox
2. Select recipient from dropdown
3. Optionally customize subject
4. Write message (1-2000 characters)
5. Click "Send Message"
6. Email notification sent via MailGun
7. Redirected to conversation view

**Technical Implementation:**
- Access control: `can_message()` validation
- Email delivery: `send_message_notification()`
- Message stored in `messages` table

---

### Messages (Inbox)

**Screenshot:** `messages.png`

**Description:**  
List of all conversations with recruiters and recruits.

**Key Features:**

**Header:**
- "Messages" title
- Subtitle: "Your conversations with recruiters and recruits."

**Conversation List:**
Each conversation displayed as a card:
- **Contact Name** - "Max Girouard", "Jeff Jordan"
- **Message Preview** - First ~100 characters of most recent message
- **Timestamp** - When last message was sent
- **Unread Indicator** (future) - Badge showing unread count

**Action Buttons:**
- **"New Message"** - Compose message to recruit or recruiter
- **"Back to Dashboard"** - Return to main screen

**User Actions:**
- Click on conversation → Open full conversation thread
- View all active conversations
- See recent message activity

**Technical Implementation:**
- Queries `messages` table grouped by conversation partner
- Shows both sent and received messages
- Sorted by most recent activity

**Future Enhancements:**
- Unread message count
- Search conversations
- Archive old threads

---

## Administrative Tools

### Admin Report

**Screenshot:** `admin page.png`

**Description:**  
Comprehensive user report for platform administrators (Tony and Max).

**Key Features:**

**Access Control:**
- Only visible to users with `is_admin=TRUE`
- URL: `/admin`
- Unauthorized users redirected to dashboard

**Registered Users Section:**
Table showing all authenticated users:
- **ID** - Database primary key
- **Name** - User's display name
- **Email** - Registered email address
- **Invite Code** - Unique 8-character referral code

**Data Visible:**
Sample users shown:
- Alex Carter (alec.carter58@gmx.com)
- Jeff Jordan (jeffjordan5676@gmail.com)
- Irene Ferrante (gble1050@gmail.com)
- TB Bryan (tbbryan76@gmail.com)
- Max Girouard (maxatisd@gmail.com)
- Tony Byorick (tony.byorick@gmail.com)

**Anonymous Submissions Section:**
Table showing unregistered question submitters:
- **Name** - Provided when submitting question
- **Email** - Optional contact email
- **Voter ID** - Optional voter registration number
- **Submissions** - Count of questions submitted

**Use Cases:**
- Track platform growth
- Identify potential recruits (anonymous users)
- Verify referral tracking
- Data for outreach decisions

**Technical Implementation:**
- Query 1: `SELECT * FROM users ORDER BY created_at DESC`
- Query 2: `SELECT name, email, voter_id, COUNT(*) FROM voter_submissions WHERE user_id IS NULL GROUP BY name, email, voter_id`

---

### Network Tree

**Screenshot:** `network tree.png`

**Description:**  
Visual representation of the Call5 recruitment network.

**Key Features:**

**Header:**
- "Network Tree" title

**Tree Visualization:**
Hierarchical display of recruitment relationships:
- **Tony Byorick (3 recruits)** - Root/founder
  - Max Girouard (0 recruits)
  - TB Bryan (1 recruit)
    - Alex Carter (0 recruits)
  - Jeff Jordan (0 recruits)
  - Irene Ferrante (0 recruits)

**Display Elements:**
- User names with recruit count in parentheses
- Indentation shows parent-child relationships
- Click on name → Navigate to user details (future)

**Action Buttons:**
- **"← Back to Dashboard"** - Return to main screen

**Use Cases:**
- Visualize network growth patterns
- Identify top recruiters
- Track recruitment chains
- Verify referral relationships

**Technical Implementation:**
- Recursive query on `users.invited_by_user_id`
- Builds tree structure from database
- Future: Interactive visualization with D3.js or similar

**Future Enhancements:**
- Collapsible branches
- Search/filter by user
- Export network data
- Highlight groups within tree

---

## User Journey Examples

### New User Signup & First Actions

1. **Land on site** → See pre-login landing page
2. **Click "Sign in with Google"** → OAuth flow → Account created
3. **Arrive at dashboard** → See welcome message, recruit count (0)
4. **Copy invite link** → Share with friends via Nextdoor/email
5. **Create first group** → Name it "54 Ave Group"
6. **Friend signs up via invite link** → Recruit count becomes 1
7. **Invite friend to group** → Group now has 2 members
8. **Send message to recruit** → "Welcome to Call5!"

### Recruiter Communication Flow

1. **Dashboard** → Click "Message Your Recruits"
2. **Select recipient** → Choose Max Girouard
3. **Compose message** → "Hey Max, check out the new group feature!"
4. **Send** → Max receives email notification
5. **Max clicks email link** → Opens conversation thread
6. **Max replies** → "Thanks! Just joined 54 Ave Group"
7. **Conversation visible in inbox** → Both users can see full history

### Group Organization Flow

1. **Create group** → "RAI Network" for Responsible AI community
2. **Dashboard** → Shows "RAI Network" in groups list
3. **Click group name** → Opens group management page
4. **Invite members** → Select David, TB Bryan, Irene from recruits
5. **Members join** → Group now has 4 members
6. **Send broadcast** → Message all group members at once
7. **Group appears on member dashboards** → All can access group page

---

## Mobile Responsiveness

All screens are designed for mobile-first experience:

**Breakpoints:**
- Desktop: 1024px+
- Tablet: 768px - 1023px
- Mobile: < 768px

**Mobile Adaptations:**
- Buttons stack vertically
- Tables scroll horizontally or collapse
- Forms fill full width
- Touch-friendly button sizes (min 44px)
- Readable font sizes (min 16px for body text)

---

## Design System

### Colors

**Primary Blue:**
- Header backgrounds: `#2c5aa0`
- Buttons: `#1e3a8a`
- Hover states: `#1e40af`

**Accent Colors:**
- Success green: `#10b981`
- Warning yellow: `#f59e0b`
- Error red: `#ef4444`

**Neutrals:**
- Background: `#f9fafb`
- Cards: `#ffffff`
- Borders: `#e5e7eb`
- Text: `#1f2937`

### Typography

**Font Family:** Arial, sans-serif

**Sizes:**
- H1: 32px (2rem)
- H2: 28px (1.75rem)
- H3: 24px (1.5rem)
- Body: 16px (1rem)
- Small: 14px (0.875rem)

### Buttons

**Primary Button:**
- Background: `#1e3a8a`
- Text: White
- Padding: 12px 24px
- Border radius: 6px
- Hover: Darker blue

**Secondary Button:**
- Background: White
- Border: 1px solid `#e5e7eb`
- Text: `#1f2937`
- Padding: 12px 24px

**Disabled Button:**
- Background: `#e5e7eb`
- Text: `#9ca3af`
- Cursor: not-allowed

---

## Feature Availability by Version

### v0.4.01 (Current)
✅ Google OAuth authentication  
✅ Dashboard with invite link  
✅ Group creation and management  
✅ Group broadcast messaging  
✅ Admin user report  
✅ Network tree visualization  
✅ 1:1 recruiter ↔ recruit messaging  

### v0.4.02 (Planned)
🔄 Full 1:1 messaging with conversation threading  
🔄 Message inbox with unread counts  
🔄 Email notifications for all messages  
🔄 Network tree quick message links  

### v0.4.03 (Planned)
🔄 Local email/password authentication  
🔄 Email verification system  
🔄 Password reset flow  
🔄 Account security (rate limiting, lockout)  

### Future Enhancements
⏳ Group member-to-member messaging  
⏳ Message search and filtering  
⏳ Rich text message formatting  
⏳ File attachments in messages  
⏳ Campaign promise tracking  
⏳ Analytics dashboard  

---

## Technical Notes for Developers

### Screenshot Maintenance

**When to Update:**
- UI changes in any release
- New features added
- Bug fixes that affect visual appearance
- Before stakeholder presentations

**Naming Convention:**
- Use descriptive names: `feature-name.png`
- Keep consistent with existing names
- Store in versioned folders: `/docs/screenshots/v0.x.xx/`

### Taking Screenshots

**Browser Settings:**
- Use Chrome or Firefox in standard profile
- Window size: 1280x800 (desktop) or 375x812 (mobile)
- No browser extensions visible
- Clear test data, use realistic sample content

**Content Standards:**
- Use real user names (Tony, Max, David, etc.)
- Show actual feature functionality
- Include UI in active/interactive state
- Capture complete workflows, not just static pages

### Documentation Updates

This document should be updated:
- After each version release
- When UI changes significantly
- When new features are added
- Before stakeholder reviews

---

## Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| v0.4.01 | 2026-02-05 | Initial UI documentation with 9 screenshots | Tony Byorick |

---

**Next Update:** After v0.4.02 implementation (1:1 messaging enhancement)