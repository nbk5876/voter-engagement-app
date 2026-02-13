# Request for Claude Code: Revise Testing Instructions - Separate by User Role

## Context

The current testing instructions (`Call5_v0_4_Tester_Instructions.md`) were written assuming testers would simulate both roles (invitor and invitee). However, these instructions will be used by **real beta testers** recruited from Tony's Nextdoor community outreach, not internal QA staff.

**Actual Use Case:**
- Tony recruits real people from Nextdoor to join Call5
- He sends them an invite link
- They are NEW to the platform and will only experience the invitee side
- Existing members (like Tony) need separate instructions for invitor activities

## The Problem

Current Scenario 1 combines both roles:
- **Part A:** "Obtain an Invite Code" - assumes tester logs in as existing user
- **Part B:** "Sign Up as a New User" - assumes same tester switches to incognito

This doesn't match reality:
- New invitees **won't have** an existing account to log into for Part A
- Existing invitors **don't need** detailed signup instructions from Part B

## Your Task

Reorganize the testing instructions document to **separate instructions by user role**:

### Structure the Document This Way:

```markdown
# Call5 Democracy v0.4 - User Guide & Testing Instructions

## Introduction
[Brief overview of Call5 and document purpose]

---

## Part 1: For Existing Members (Invitors)

### Your Role
You're an existing Call5 member who wants to recruit new members to grow the network.

### Section 1.1: How to Get Your Invite Link
[Current Scenario 1, Part A - steps for finding invite link on Dashboard]

### Section 1.2: How to Share Your Invite Link
- Copy the link and send via:
  - Nextdoor private message
  - Email
  - Text message
  - Social media DM
- Include a brief message explaining what Call5 is

### Section 1.3: How to Verify Your Recruits
- Check your Dashboard recruit count
- View your network tree

### Section 1.4: Messaging Your Recruits
[Relevant parts from current Scenario 4 or dashboard docs]

### Section 1.5: Creating and Managing Groups
[Brief overview if relevant to invitors]

### Section 1.6: Viewing and Posting Concerns
[Current Scenario 5 adapted for existing members]

---

## Part 2: For New Members (Invitees)

### Your Role
You've received an invite link from an existing Call5 member and are joining for the first time.

### Section 2.1: What to Expect
- You'll receive a link that looks like: `https://voter-engagement-app.onrender.com/?ref=XXXXXXXXXXXXXXXXXXXX`
- This link connects you to the person who invited you
- Keep this link - you'll need it to sign up

### Section 2.2: Signing Up with Google (Option 1)
[Current Scenario 1, Part B - Google OAuth signup flow]
- Prerequisites
- Step-by-step instructions
- What you'll see after signup
- Troubleshooting

### Section 2.3: Signing Up with Email/Password (Option 2)
[Current Scenario 2 - Local auth signup flow]
- Prerequisites
- Step-by-step instructions  
- Email verification
- What you'll see after signup
- Troubleshooting

### Section 2.4: First Time on Your Dashboard
- What the Dashboard shows
- Your invite link (for recruiting others)
- Seeing who recruited you
- Navigation overview

### Section 2.5: Logging In on Future Visits (Google)
[Current Scenario 3 - simplified for new users]

### Section 2.6: Logging In on Future Visits (Email/Password)
[Current Scenario 4 - simplified for new users]

### Section 2.7: Viewing Your Network Tree
[Current Scenario 6 - adapted for new users who may have zero recruits initially]

### Section 2.8: Exploring Concerns
[Current Scenario 5 - viewing concerns as a new member]

---

## Appendices
[Keep current appendices but organize by relevance to each role]
```

## Key Changes to Make

### 1. Remove All "Simulation" Language
- Delete phrases like "Part A is performed by..." or "You'll need to play two roles"
- Write as if reader is ONLY their actual role
- No instructions to "log in as different users"

### 2. Adjust Tone and Assumptions

**For Invitors (Part 1):**
- Assume they're already familiar with the platform
- Focus on recruiting, managing, and organizing
- Can reference other features briefly
- More concise, bullet-point style acceptable

**For Invitees (Part 2):**
- Assume zero knowledge of the platform
- Very detailed, step-by-step
- Warm, welcoming tone
- Explain "why" not just "how"

### 3. Rewrite Step Numbers

Current: "1. Log in as existing user... 7. Open incognito window..."
New: Each section starts at 1, no confusing gaps

### 4. Handle Prerequisites Differently

**For Invitors:**
- Prerequisites: "You must be a registered Call5 member with at least one recruit"

**For Invitees:**  
- Prerequisites: "You need an invite link from an existing Call5 member (you should have already received this)"

### 5. Separate Edge Cases by Role

**Invitor edge cases:**
- What if I don't see my new recruit in my count?
- Can I invite someone without their email?

**Invitee edge cases:**
- What if my invite link doesn't work?
- What if I already signed up before receiving the link?

### 6. Update Introduction Text

Current introduction doesn't explain the two-role structure. New intro should:
- Explain that Call5 works through invite-based recruitment
- Clearly state: "Choose the section below that matches YOUR role"
- Set expectations for each role

## Content to Preserve

Keep all the excellent detail from the current document:
- Exact button locations and colors
- Screenshot placeholders
- Success criteria checklists  
- Troubleshooting tables
- Expected results tables
- Professional formatting
- Appendices on test data and common issues

## Deliverable

Create a revised document titled:
**"Call5 Democracy v0.4 - User Guide & Testing Instructions"**

The document should:
- Be immediately usable by Tony to send appropriate sections to beta testers
- Allow him to send "Part 2" to new Nextdoor recruits
- Allow him to reference "Part 1" himself and share with other existing members
- Maintain the same level of professional quality as the current version
- Be 100% clear about which role is reading each section

## Example Opening

```markdown
# Call5 Democracy v0.4 - User Guide & Testing Instructions

## Welcome to Call5 Democracy

Call5 Democracy is a civic engagement platform that grows through personal networks. Each member recruits others using their unique invite link, creating an exponential "call-5" network of engaged citizens.

## How to Use This Guide

**Are you NEW to Call5?** 
→ Jump to [Part 2: For New Members](#part-2-for-new-members)

**Are you ALREADY a Call5 member?** 
→ See [Part 1: For Existing Members](#part-1-for-existing-members)

---

## Part 1: For Existing Members (Invitors)

**This section is for you if:**
- You already have a Call5 account
- You want to recruit new members
- You want to manage your network and groups

[Continue with invitor instructions...]

---

## Part 2: For New Members (Invitees)

**This section is for you if:**
- You received an invite link from someone
- You're signing up for the first time
- You want to understand how to use Call5

**Before you start:** You should have received an invite link that looks like:
`https://voter-engagement-app.onrender.com/?ref=XXXXXXXXXXXXXXXXXXXX`

If you don't have this link yet, ask the person who invited you to send it.

[Continue with invitee instructions...]
```

Please create the revised document now.
