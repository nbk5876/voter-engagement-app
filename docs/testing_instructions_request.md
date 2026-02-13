# Request for Claude Code: Create Testing Instructions for Call5 Democracy

## Context
You are creating comprehensive testing instructions for the Call5 Democracy application (v0.4.x). These instructions will be used by testers who need clear, step-by-step guidance to validate the application's functionality.

## Your Task
Write detailed, user-friendly testing instructions that cover the scenarios listed below. Since you have access to the actual codebase, you can provide accurate details about:
- Exact URL paths
- Button labels and text
- Field names
- Expected behaviors
- Error messages
- Visual elements

## Target Audience
Testers who may not be familiar with the application architecture but need to systematically validate functionality across different user flows.

## Required Testing Scenarios

### Scenario 1: New User Signup - Google Authentication with Invite Code
**Purpose:** Verify that new users can successfully create an account using Google OAuth when they have a valid invite code.

**Instructions should include:**
- How to obtain a test invite code (from an existing user's dashboard)
- The exact URL format with invite code (e.g., `/?ref=XXXXXX`)
- Step-by-step Google OAuth flow
- What happens after successful signup (redirect location, welcome message, etc.)
- How to verify the recruitment relationship was established
- What the user should see on their first dashboard visit

**Edge cases to document:**
- What happens with an invalid invite code
- What happens if user already has an account
- What happens if invite code is missing from URL

---

### Scenario 2: New User Signup - Local Authentication with Invite Code
**Purpose:** Verify that new users can create an account using email/password when they have a valid invite code.

**Instructions should include:**
- How to access the local signup form (exact URL or navigation path)
- All required fields (email, password, name, etc.)
- Password requirements/validation rules
- Email verification process (if applicable)
- Successful signup confirmation
- How the invite code is captured and linked
- First login experience

**Edge cases to document:**
- Duplicate email handling
- Weak password rejection
- Missing invite code scenarios

---

### Scenario 3: Returning User Login - Google Authentication Flow
**Purpose:** Verify existing users can log in via Google OAuth and navigate to their dashboard.

**Instructions should include:**
- Starting point (landing page URL)
- Location and appearance of "Sign in with Google" button
- Google account selection flow
- Post-login redirect to landing page
- What elements appear on landing page for authenticated users
- How to navigate from landing page to dashboard (button/link location)
- What should be visible on the dashboard (welcome message, stats, invite link, etc.)

**Verification points:**
- User email displayed in header
- Recruitment attribution (if applicable)
- Recruit count accuracy
- Invite code display

---

### Scenario 4: Returning User Login - Local Authentication Flow
**Purpose:** Verify existing users can log in with email/password and navigate to their dashboard.

**Instructions should include:**
- Login form location and fields
- Successful login redirect path
- Landing page appearance for authenticated users
- Navigation path to dashboard
- Dashboard elements to verify

**Edge cases to document:**
- Incorrect password handling
- Non-existent email handling
- Password reset flow (if implemented)

---

### Scenario 5: Viewing Concerns - Navigate and Read Full Text
**Purpose:** Verify users can browse the concerns list and view detailed concern content.

**Instructions should include:**
- How to navigate to "View All Concerns" page from dashboard
- Exact button/link location and text
- What the concerns list page displays (concern titles, authors, timestamps, etc.)
- How to identify the squirrel-related concern specifically
- How to click to view full concern text
- What the full concern view displays (complete text, author info, metadata, etc.)
- Navigation back to concerns list

**Specific requirements:**
- Describe the squirrel concern's appearance in the list (you should know this from the database)
- Explain any filtering or sorting options available
- Note whether concerns show preview text or full text in list view

---

### Scenario 6: Network Tree Visualization - Access and Interact
**Purpose:** Verify users can access the network tree visualization and view their recruitment network graphically.

**Instructions should include:**
- Navigation from dashboard to tree page (exact button/link location)
- Initial page state when tree page loads
- Which button(s) to click to generate/display the graphical tree
- What the graphical tree displays (nodes, connections, names, etc.)
- Interactive features (zoom, pan, click nodes for details, etc.)
- How to interpret the visualization (who recruited whom, network depth, etc.)
- Whether there's a tabbed interface (Text/Graph views mentioned in roadmap)

**Technical details to include:**
- Expected visualization library (vis.js based on context)
- Loading behavior
- Network structure clarity (parent-child relationships)

---

## Documentation Format Requirements

### For Each Scenario:
1. **Scenario Title** - Clear, descriptive name
2. **Prerequisites** - What needs to be set up beforehand (test accounts, invite codes, etc.)
3. **Step-by-Step Instructions** - Numbered, granular steps
4. **Expected Results** - What the tester should see/experience at each step
5. **Success Criteria** - How to know the test passed
6. **Troubleshooting** - Common issues and solutions

### Writing Style:
- Use imperative mood ("Click the button", "Enter your email")
- Be specific about UI elements ("Click the blue 'Sign in with Google' button in the top-right header")
- Include exact URLs where relevant
- Mention visual cues (colors, icons, positions)
- Assume tester has basic web browsing skills but no knowledge of the app

### Format:
- Use markdown formatting
- Include clear section headers
- Use numbered lists for sequential steps
- Use bullet points for non-sequential information
- Bold important UI element names
- Include screenshots placeholders where helpful (e.g., `[Screenshot: Dashboard showing invite link section]`)

---

## Additional Considerations

### Test Data Requirements
For each scenario, specify what test data needs to exist:
- Which users should be pre-created
- What invite codes should be available
- Whether any concerns need to exist in the database
- Any group memberships required

### Browser/Platform Notes
Mention any browser-specific behaviors or mobile considerations, especially given the mobile-friendly design preference.

### Version Information
Note that these instructions are for Call5 Democracy v0.4.x with the following features enabled:
- Google OAuth and local authentication
- Recruitment network tracking
- Dashboard with invite link sharing
- Concerns feature
- Network tree visualization (vis.js)
- Groups functionality

---

## Deliverable

Create a single comprehensive markdown document titled:
**"Call5 Democracy v0.4 - Tester Instructions"**

Include:
- Introduction explaining the purpose and scope
- Quick reference table of contents
- All six scenarios with complete documentation
- Appendix with test data setup instructions
- Appendix with common troubleshooting issues

The document should be polished, professional, and ready to send to testers without additional explanation.

---

## Example Template Structure

```markdown
# Call5 Democracy v0.4 - Tester Instructions

## Introduction
[Brief overview of the application and testing objectives]

## Table of Contents
1. [Scenario 1: New User Signup - Google Authentication](#scenario-1)
2. [Scenario 2: New User Signup - Local Authentication](#scenario-2)
...

## Test Environment
- **Application URL:** https://voter-engagement-app.onrender.com
- **Test Accounts:** [List of pre-configured accounts]
- **Required Materials:** Valid email addresses for new signups

---

## Scenario 1: New User Signup - Google Authentication with Invite Code

### Prerequisites
- [ ] Valid invite code obtained from existing user
- [ ] Google account for authentication
- [ ] Clear browser cache/use incognito mode

### Step-by-Step Instructions

1. **Obtain an invite code**
   - Log in as an existing user (e.g., tony.byorick@gmail.com)
   - Navigate to Dashboard
   - Locate the "Your Invite Link" section
   - Copy the 8-character code at the end of the URL (e.g., `OjQobOWu`)

2. **Access the signup page with invite code**
   - Open new incognito/private browser window
   - Navigate to: `https://voter-engagement-app.onrender.com/?ref=OjQobOWu`
   - You should see the landing page

[Continue with detailed steps...]

### Expected Results
- After step 2: Landing page displays with "Sign in with Google" button
- After step 3: Google account selection screen appears
...

### Success Criteria
✓ New user account created in database
✓ invited_by_user_id correctly links to inviter
✓ User redirected to dashboard after signup
✓ Dashboard displays "Recruited by: [Inviter Name]"

### Troubleshooting
**Issue:** "Invalid invite code" error
**Solution:** Verify the invite code is exactly 8 characters and exists in database

[etc.]
```

---

Please create this comprehensive testing documentation now.
