# Call5 Democracy v0.4 - Tester Instructions

## Introduction

Call5 Democracy is a hub-and-spoke civic engagement platform that helps citizens organize, recruit, and advocate for civic issues through their social networks. This document provides step-by-step testing instructions for validating core functionality across six key scenarios.

All tests should be performed against the production application unless otherwise noted.

## Table of Contents

1. [Test Environment](#test-environment)
2. [Scenario 1: New User Signup - Google Authentication with Invite Code](#scenario-1-new-user-signup---google-authentication-with-invite-code)
3. [Scenario 2: New User Signup - Local Authentication with Invite Code](#scenario-2-new-user-signup---local-authentication-with-invite-code)
4. [Scenario 3: Returning User Login - Google Authentication Flow](#scenario-3-returning-user-login---google-authentication-flow)
5. [Scenario 4: Returning User Login - Local Authentication Flow](#scenario-4-returning-user-login---local-authentication-flow)
6. [Scenario 5: Viewing Concerns - Navigate and Read Full Text](#scenario-5-viewing-concerns---navigate-and-read-full-text)
7. [Scenario 6: Network Tree Visualization - Access and Interact](#scenario-6-network-tree-visualization---access-and-interact)
8. [Appendix A: Test Data Setup](#appendix-a-test-data-setup)
9. [Appendix B: Common Troubleshooting](#appendix-b-common-troubleshooting)

---

## Test Environment

- **Application URL:** `https://voter-engagement-app.onrender.com/`
- **Version:** v0.4.07b
- **Supported Browsers:** Chrome, Firefox, Safari, Edge (latest versions)
- **Mobile:** Responsive design; all pages work on mobile browsers
- **Required Materials:**
  - A Google account (for Google OAuth scenarios)
  - A unique email address not already registered (for local signup scenarios)
  - An invite code from an existing user (for signup scenarios)

---

## Scenario 1: New User Signup - Google Authentication with Invite Code

### Purpose
Verify that a new user can create an account using Google OAuth when they have a valid invite code, and that the recruitment relationship is correctly established.

### Prerequisites
- [ ] A valid invite code obtained from an existing user (see Step 1 below)
- [ ] A Google account that has **never** been used to sign into Call5
- [ ] Use an incognito/private browser window to ensure a clean session

### Step-by-Step Instructions

**Part A: Obtain an Invite Code**

1. Open a browser and navigate to `https://voter-engagement-app.onrender.com/`
2. Log in as an existing user (Google or local auth).
3. On the landing page, click the **"Dashboard"** button in the blue header bar (top center, white semi-transparent button).
4. On the Dashboard page, locate the **"Your Invite Link"** section below the stats card. It contains a read-only text field with a URL in this format:
   ```
   https://voter-engagement-app.onrender.com/?ref=XXXXXXXXXXXXXXXXXXXX
   ```
5. Click the blue **"Copy"** button next to the invite link. The button text will briefly change to **"Copied!"** to confirm.
6. Save this URL. The invite code is the 20-character string after `?ref=`.

   `[Screenshot: Dashboard showing the "Your Invite Link" section with Copy button]`

**Part B: Sign Up as a New User**

7. Open a **new incognito/private browser window** (important: do not reuse the window from Part A).
8. Paste the invite URL into the address bar and press Enter. Example:
   ```
   https://voter-engagement-app.onrender.com/?ref=XXXXXXXXXXXXXXXXXXXX
   ```
9. The **Landing Page** loads. In the top-right corner, the page label reads "Landing Page". The title reads **"Voter Engagement Response Form"**.
10. In the blue header, locate the authentication section. You should see three options:
    - A white **"Sign in with Google"** button with the Google logo (four-color G icon)
    - A semi-transparent **"Sign up with Email"** button below a divider line with "or"
    - A text link: "Already have an account? **Log in**"
11. Click the white **"Sign in with Google"** button.

    `[Screenshot: Landing page showing the three auth options for unauthenticated users]`

12. Google's account selection screen appears. Select the Google account you want to use for the new Call5 account.
13. If prompted, approve the OAuth consent screen for Call5 Democracy.
14. After authorization, you are redirected back to the Landing Page (`/`).

**Part C: Verify Account Creation**

15. The landing page should now show your Google email address in the blue header area, along with a **"Dashboard"** button and a **"Sign Out"** button.
16. Click the **"Dashboard"** button.
17. The Dashboard page loads. Verify the following:
    - The heading reads **"Welcome, [Your Name]!"** (your Google account name)
    - Below the welcome heading, you see: **"Recruited by: [Inviter's Name]"** (the name of the user whose invite code you used)
    - The stats card shows **"0"** with the label **"People Recruited"**
    - The **"Your Invite Link"** section displays your own unique invite URL
    - All action buttons are visible (some may be grayed out/disabled)

    `[Screenshot: New user's Dashboard showing "Recruited by" and initial stats]`

### Expected Results

| Step | Expected Result |
|------|----------------|
| 9 | Landing page loads with "Sign in with Google" button visible |
| 14 | Redirect back to landing page after Google auth |
| 15 | User email appears in header with Dashboard and Sign Out buttons |
| 17 | Dashboard shows welcome message, recruiter attribution, and 0 recruits |

### Success Criteria
- [ ] New user account created successfully
- [ ] "Recruited by: [Inviter Name]" displays correctly on dashboard
- [ ] Stats show 0 People Recruited
- [ ] User's own unique invite link is generated and displayed
- [ ] Inviter's recruit count increased by 1 (verify by logging in as the inviter)

### Edge Cases

**Invalid invite code:**
- Navigate to `https://voter-engagement-app.onrender.com/?ref=INVALIDCODE123`
- Sign in with Google
- **Expected:** Account is created successfully, but **no** "Recruited by" line appears on the dashboard. The invalid code is silently ignored.

**User already has an account:**
- Navigate to the invite URL and click "Sign in with Google"
- Select a Google account that is already registered in Call5
- **Expected:** User is logged in as normal. The invite code does NOT overwrite any existing recruitment relationship. Redirect to the landing page.

**Missing invite code (no `?ref=` parameter):**
- Navigate to `https://voter-engagement-app.onrender.com/` (no ref parameter)
- Sign in with Google using a new account
- **Expected:** Account is created with no recruiter. Dashboard shows welcome message but no "Recruited by" line.

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Google sign-in button does nothing | Check that pop-ups are not blocked. Try a different browser. |
| Redirected to an error page after Google auth | Clear cookies and try again. The OAuth session may have expired. |
| "Recruited by" not showing | Verify the invite code was in the URL when you first loaded the landing page. The code is captured on page load, not on sign-in. |

---

## Scenario 2: New User Signup - Local Authentication with Invite Code

### Purpose
Verify that a new user can create an account using email and password when they have a valid invite code.

### Prerequisites
- [ ] A valid invite code obtained from an existing user (see Scenario 1, Part A)
- [ ] An email address that is **not** already registered in Call5
- [ ] Use an incognito/private browser window to ensure a clean session

### Step-by-Step Instructions

**Part A: Navigate to the Signup Page**

1. Open an **incognito/private browser window**.
2. Paste the invite URL into the address bar and press Enter:
   ```
   https://voter-engagement-app.onrender.com/?ref=XXXXXXXXXXXXXXXXXXXX
   ```
3. The Landing Page loads. The invite code is now stored in your session.
4. In the blue header, click the semi-transparent **"Sign up with Email"** button (below the "or" divider).

   `[Screenshot: Landing page with "Sign up with Email" button highlighted]`

5. The **Sign Up** page loads (`/signup`). The page has:
   - A blue header with "Call5 Democracy" and "Create your account"
   - Page label "Sign Up" in the top-right corner of the header
   - Heading: **"Sign Up with Email"**
   - Subtitle: "Join Call5 to engage with your civic community."

**Part B: Fill Out the Registration Form**

6. Fill in the following fields:

   | Field | Input | Notes |
   |-------|-------|-------|
   | **Full Name** | Your full name | Required. Placeholder: "Your name" |
   | **Email Address** | A valid, unused email | Required. Placeholder: "you@example.com" |
   | **Password** | A strong password | Required. Placeholder: "Create a password" |
   | **Confirm Password** | Same password again | Required. Placeholder: "Confirm your password" |

7. Note the password requirements displayed below the Password field:
   > "At least 8 characters with uppercase, lowercase, and a number"

8. Click the blue **"Create Account"** button.

   `[Screenshot: Signup form with all fields filled in]`

**Part C: Email Verification**

9. A green success banner appears at the top of the Login page:
   > "Account created! Please check your email to verify your account."
10. Check the email inbox for the address you registered with. Look for a verification email from Call5 Democracy.
11. Click the verification link in the email.
12. After verification, navigate to the Login page: `https://voter-engagement-app.onrender.com/login`

**Part D: First Login**

13. On the **Log In** page (`/login`):
    - Page label reads "Log In" in the top-right of the blue header
    - Heading: **"Log In"**
    - Subtitle: "Sign in to your Call5 account."
14. Enter your **Email Address** and **Password**.
15. Click the blue **"Log In"** button.
16. A green success banner appears: **"Welcome back, [Your Name]!"**
17. You are redirected to the **Dashboard** page.
18. Verify the dashboard displays:
    - **"Welcome, [Your Name]!"**
    - **"Recruited by: [Inviter's Name]"** (confirming the invite code was captured)
    - **"0"** People Recruited
    - Your unique invite link

   `[Screenshot: Dashboard after first local auth login showing recruiter attribution]`

### Expected Results

| Step | Expected Result |
|------|----------------|
| 5 | Signup page loads with all four form fields |
| 9 | Green success message on login page, verification email sent |
| 16 | "Welcome back" message appears |
| 18 | Dashboard shows recruiter name and 0 recruits |

### Success Criteria
- [ ] Account created with email/password
- [ ] Verification email received
- [ ] Login successful after verification
- [ ] "Recruited by: [Inviter Name]" displays correctly
- [ ] Inviter's recruit count increased by 1

### Edge Cases

**Duplicate email:**
- Attempt to sign up with an email that is already registered
- **Expected:** Red error banner: **"Email already registered. Please log in."** Redirects to the Login page.

**Weak password (missing uppercase):**
- Enter a password like `password1` (no uppercase letter)
- **Expected:** Red error banner with a message indicating the password does not meet requirements.

**Weak password (too short):**
- Enter a password like `Ab1` (under 8 characters)
- **Expected:** Red error banner indicating minimum length not met.

**Passwords do not match:**
- Enter different values in Password and Confirm Password
- **Expected:** Red error banner: **"Passwords do not match"**

**Missing fields:**
- Leave one or more fields empty and click "Create Account"
- **Expected:** Red error banner: **"All fields are required"** (or browser native validation prevents submission)

**Missing invite code:**
- Navigate directly to `https://voter-engagement-app.onrender.com/signup` without first visiting the landing page with a `?ref=` code
- **Expected:** Account is created but no recruiter is assigned. Dashboard shows no "Recruited by" line.

### Troubleshooting

| Issue | Solution |
|-------|----------|
| No verification email received | Check spam/junk folder. Wait up to 5 minutes for delivery. |
| "Please verify your email before logging in" | Click the verification link in your email first. If the link expired, use the "resend verification" option on the login page. |
| Account locked message | After 5 failed login attempts, the account locks for 30 minutes. Wait and try again. |

---

## Scenario 3: Returning User Login - Google Authentication Flow

### Purpose
Verify that an existing user can log in via Google OAuth and navigate to their dashboard with all expected data displayed.

### Prerequisites
- [ ] An existing Call5 account created with Google OAuth
- [ ] Know which Google account was used for registration

### Step-by-Step Instructions

1. Open a browser and navigate to: `https://voter-engagement-app.onrender.com/`
2. The **Landing Page** loads with the title **"Voter Engagement Response Form"**.
3. In the blue header, locate the authentication buttons. For an unauthenticated user, you see:
   - A white **"Sign in with Google"** button with the four-color Google logo
   - A semi-transparent **"Sign up with Email"** button
   - A link: "Already have an account? **Log in**"

   `[Screenshot: Landing page for unauthenticated user showing auth buttons]`

4. Click the white **"Sign in with Google"** button.
5. Google's account selection screen appears. Select your previously registered Google account.
6. You are redirected back to the **Landing Page** (`/`).
7. The header now shows:
   - Your **email address** displayed in the blue header area
   - A **"Dashboard"** button (white semi-transparent, to the right of your email)
   - A **"Sign Out"** button (white semi-transparent, next to Dashboard)
   - The Name field in the form below is now **hidden** (only the Comment field remains)

   `[Screenshot: Landing page for authenticated user showing email, Dashboard, and Sign Out]`

8. Click the **"Dashboard"** button in the header.
9. The **Dashboard** page loads (`/dashboard`). Verify the following elements:

   **Header Section:**
   - Page label "Dashboard" in top-right corner
   - Title: **"Call5 Democracy"**
   - Your name displayed below the title
   - **"Sign Out"** button

   **Welcome Section:**
   - **"Welcome, [Your Name]!"**
   - If you were recruited: **"Recruited by: [Recruiter's Name]"**

   **Stats Card:**
   - A large blue number showing your **recruit count**
   - Label: **"People Recruited"**

   **Invite Link Section:**
   - Label: **"Your Invite Link"**
   - A read-only text field with your invite URL
   - A blue **"Copy"** button

   **Action Buttons** (vertical stack of full-width blue buttons):
   - **"Share Your Invite Link"**
   - **"Message Your Recruiter"** (grayed out if no recruiter, showing "(No Recruiter)")
   - **"Message Your Recruits"** (grayed out if 0 recruits, showing "(No Recruits)")
   - **"Messages"**
   - **"Create Group"** (grayed out if 0 recruits, showing "(Recruit first)")
   - **"Your Groups"**
   - **"View All Concerns"**
   - **"Submit Voter Question"**
   - **"Admin"** (visible only if you are an admin user)
   - **"Tree"**

   `[Screenshot: Full dashboard showing all sections and action buttons]`

### Expected Results

| Step | Expected Result |
|------|----------------|
| 6 | Redirected to landing page with email shown in header |
| 7 | Dashboard and Sign Out buttons visible; Name field hidden |
| 9 | Dashboard loads with welcome message, stats, invite link, and all action buttons |

### Success Criteria
- [ ] Google OAuth login completes without errors
- [ ] Landing page shows user email, Dashboard button, and Sign Out button
- [ ] Dashboard displays correct user name
- [ ] Recruit count is accurate
- [ ] Invite link is present and the Copy button works
- [ ] Recruiter attribution shows correctly (if applicable)
- [ ] Disabled buttons display with gray styling and explanatory text

### Verification Points
- **User email in header:** Visible on both landing page (after login) and dashboard
- **Recruitment attribution:** "Recruited by: [Name]" only shows if the user was recruited
- **Recruit count accuracy:** The number should match the actual count of users who signed up using this user's invite code
- **Invite code display:** The invite URL should contain a 20-character code unique to this user

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Stuck on Google account selection | Clear browser cookies for Google, then retry |
| Dashboard shows wrong recruit count | Refresh the page. Counts are computed on page load. |
| "Dashboard" button not visible | You may not be logged in. Check that your email appears in the header. |

---

## Scenario 4: Returning User Login - Local Authentication Flow

### Purpose
Verify that an existing user can log in with their email and password and navigate to their dashboard.

### Prerequisites
- [ ] An existing Call5 account created with email/password (local auth)
- [ ] Know the registered email and password
- [ ] Email has been verified

### Step-by-Step Instructions

1. Open a browser and navigate to: `https://voter-engagement-app.onrender.com/`
2. The **Landing Page** loads.
3. In the blue header, click the **"Log in"** text link below the auth buttons. (Text reads: "Already have an account? **Log in**")
4. The **Log In** page loads (`/login`).
   - Blue header with "Call5 Democracy" and "Welcome back"
   - Page label "Log In" in top-right of header
   - Heading: **"Log In"**
   - Subtitle: "Sign in to your Call5 account."

   `[Screenshot: Login page with email and password fields]`

5. Enter your **Email Address** in the first field (placeholder: "you@example.com").
6. Enter your **Password** in the second field (placeholder: "Your password").
7. Click the blue **"Log In"** button.
8. A green success banner appears at the top: **"Welcome back, [Your Name]!"**
9. You are redirected to the **Dashboard** page (`/dashboard`).
10. Verify all dashboard elements as described in Scenario 3, Step 9.

    `[Screenshot: Dashboard after successful local auth login]`

### Expected Results

| Step | Expected Result |
|------|----------------|
| 4 | Login page loads with email, password fields, and "Forgot password?" link |
| 8 | Green "Welcome back" banner appears |
| 9 | Redirected to Dashboard with all expected elements |

### Success Criteria
- [ ] Login with correct credentials succeeds
- [ ] "Welcome back" message includes user's name
- [ ] Dashboard displays all expected sections and buttons
- [ ] Recruit count, invite link, and recruiter attribution are accurate

### Edge Cases

**Incorrect password:**
- Enter a valid email but wrong password
- **Expected:** Red error banner: **"Invalid email or password"**. Stay on the login page.

**Non-existent email:**
- Enter an email that has never been registered
- **Expected:** Red error banner: **"Invalid email or password"** (same message as incorrect password for security).

**Unverified email:**
- Attempt to log in before verifying your email
- **Expected:** Red error banner: **"Please verify your email before logging in. Check your inbox or resend verification."**

**Account lockout (brute force protection):**
- Enter the wrong password 5 times in a row
- **Expected:** Red error banner: **"Account locked for 30 minutes due to multiple failed login attempts"**. All further login attempts show: **"Account locked for X more minutes due to failed login attempts"**

**Forgot password:**
- Click the **"Forgot password?"** link below the password field (right-aligned, blue text)
- **Expected:** Navigates to the password reset page where you can request a reset email

### Additional Navigation
- The Login page also has:
  - A **"Sign in with Google"** button (full-width, white with gray border) below an "or" divider
  - A **"Sign up"** link at the bottom: "Don't have an account? **Sign up**"

### Troubleshooting

| Issue | Solution |
|-------|----------|
| "Invalid email or password" but credentials are correct | Check for typos. Ensure you're using the correct email (case-sensitive for local auth). |
| Account locked | Wait 30 minutes, or contact an admin to unlock. |
| No "Welcome back" banner | If redirected to dashboard without the banner, login still succeeded. The banner may have been dismissed. |

---

## Scenario 5: Viewing Concerns - Navigate and Read Full Text

### Purpose
Verify that users can browse the concerns list, view individual concern details, and interact with the rich text content.

### Prerequisites
- [ ] Logged in as any authenticated user
- [ ] At least one concern exists in the system (see Appendix A for test data)

### Step-by-Step Instructions

**Part A: Navigate to All Concerns**

1. From the **Dashboard**, scroll down the action buttons to find the **"View All Concerns"** button. It is a full-width blue button located after "Your Groups" and before "Submit Voter Question".

   `[Screenshot: Dashboard action buttons with "View All Concerns" highlighted]`

2. Click **"View All Concerns"**.
3. The **All Concerns** page loads (`/concerns/all`). Verify the following:
   - Blue header with "Call5 Democracy" and your name
   - **"Sign Out"** button in the header
   - Page label "All Concerns" in the top-right of the header
   - Heading: **"All Concerns"**
   - Subheading: "Civic issues from across the Call5 community"
   - A concern count line: **"X total concern(s)"** (e.g., "3 total concerns")

   `[Screenshot: All Concerns page showing the concerns list]`

**Part B: Browse the Concerns List**

4. Each concern is displayed as a **card** with the following information:
   - **Title** (clickable, in dark text that turns blue on hover)
   - **Scope badge** on the right side of the header:
     - **"Group Only"** - light blue badge (blue text on pale blue background)
     - **"Network-Wide"** - green badge (green text on pale green background)
   - **Metadata line:** "Posted by [Author Name] &bull; [Group Name] &bull; [Date]"
   - **Preview text:** First 200 characters of the concern description (HTML tags stripped), followed by "..." if truncated

5. Concerns are sorted with the **most recent first** (newest at the top).
6. Note: There is no client-side filtering or search. All visible concerns are shown.

**Part C: View a Specific Concern**

7. Click on a **concern title** to view its full details.
8. The **Concern View** page loads (`/concerns/[id]`). Verify:
   - A **back link** at the top: **"&larr; Back to [Group Name]"** (clicking this returns to the group page)
   - **Concern title** displayed as a large heading
   - **Metadata row** with:
     - "Posted by **[Author Name]**"
     - Full date and time (e.g., "February 10, 2026 at 03:45 PM")
     - Group name
     - Scope badge (Group Only or Network-Wide)
   - **Full description** rendered as rich text (with formatting: bold, italic, headings, bullet lists, numbered lists, blockquotes, and links)

   `[Screenshot: Concern detail page showing rich text formatting]`

9. If the concern contains rich text formatting, verify it renders correctly:
   - **Bold text** appears bold
   - **Italic text** appears italic
   - **Headings (H2, H3)** appear in blue (#2c5aa0), larger than body text
   - **Bullet lists** and **numbered lists** are properly indented
   - **Blockquotes** appear with a blue left border and italic text
   - **Links** appear in blue and are clickable

**Part D: Navigate Back**

10. Click the **"&larr; Back to [Group Name]"** link at the top of the concern to return to the group management page.
    - Alternatively, use the browser's back button to return to the All Concerns page.

**Part E: Empty State (if applicable)**

11. If no concerns exist, the All Concerns page shows:
    - "No concerns posted yet."
    - "Be the first to share a civic issue with your community!"
    - A **"Go to Your Groups"** button (centered, blue)

### Expected Results

| Step | Expected Result |
|------|----------------|
| 3 | All Concerns page loads with count and concern cards |
| 4 | Each card shows title, scope badge, metadata, and preview |
| 8 | Full concern detail page with formatted rich text |
| 9 | All rich text formatting renders correctly |

### Success Criteria
- [ ] All Concerns page loads and shows correct concern count
- [ ] Concern cards display title, scope badge, author, group, date, and preview
- [ ] Preview text shows first 200 characters with HTML stripped
- [ ] Clicking a concern title opens the full detail view
- [ ] Rich text content renders with proper formatting (bold, lists, headings, etc.)
- [ ] Scope badges show correct colors (blue for Group, green for Network)
- [ ] Back navigation works correctly

### Troubleshooting

| Issue | Solution |
|-------|----------|
| "You do not have permission to view this concern" | Group-scoped concerns require group membership. Network-scoped concerns require being in the creator's recruit network. |
| Rich text appears as plain HTML tags | The concern was created before the rich text editor was enabled. This is expected for older concerns. |
| No concerns visible | Ensure concerns exist in the system. See Appendix A for creating test data. |

---

## Scenario 6: Network Tree Visualization - Access and Interact

### Purpose
Verify that users can access the network tree visualization, switch between text and graph views, and interact with the graphical representation of the recruitment network.

### Prerequisites
- [ ] Logged in as any authenticated user
- [ ] At least 2-3 users exist in the system with recruitment relationships

### Step-by-Step Instructions

**Part A: Navigate to the Tree Page**

1. From the **Dashboard**, scroll to the bottom of the action buttons.
2. Click the **"Tree"** button (a full-width blue button near the bottom of the list, after "Submit Voter Question").

   `[Screenshot: Dashboard with "Tree" button highlighted]`

3. The **Network Tree - Text View** page loads (`/admin/network`). Verify:
   - Blue header with "Call5 Democracy" and your email
   - Page label "Network Tree" in the top-right
   - **"Sign Out"** button in the header
   - Two tabs at the top of the content area

**Part B: Text View**

4. The page opens on the **Text View** tab by default. Verify the tab bar:
   - **"📋 Text View"** tab - currently active (white background, dark blue bottom border)
   - **"🌳 Graph View"** tab - inactive (gray background)

5. Below the tabs, a gray container displays the **tree structure** as an indented text list:
   - Each node shows: **[Name]** ([X] recruit(s))
   - Child nodes are indented to the right (25px per level) to show hierarchy
   - The root user (no recruiter) appears at the leftmost position
   - Users recruited by the root appear one indent level in
   - Their recruits appear two indent levels in, and so on

   `[Screenshot: Text View showing indented tree structure]`

6. Below the tree, a **"&larr; Back to Dashboard"** link returns to the dashboard.

**Part C: Graph View**

7. Click the **"🌳 Graph View"** tab.
8. The **Network Graph** page loads (`/admin/network-graph`). This page has a different layout:
   - A white header bar with "Call5 Democracy - Network Graph" on the left
   - Your email, a blue **"Back to Dashboard"** button, and a gray **"Sign Out"** button on the right

9. Below the header, verify the tab bar:
   - **"📋 Text View"** tab - inactive
   - **"🌳 Graph View"** tab - active (white background, dark blue bottom border)

10. Below the tabs:
    - Heading: **"Recruitment Network"**
    - Three control buttons on the right:
      - **"Fit to Screen"**
      - **"Toggle Physics"**
      - **"Export Image"**

11. The main area contains a **600px-tall interactive graph** rendered using vis.js. Verify:
    - **Nodes** appear as blue rectangular boxes with rounded corners
    - Each node displays: `[Name]` on the first line, `([X] recruits)` on the second line
    - **Arrows** (edges) point from recruiter to recruited users
    - The graph flows **left-to-right** (root users on the left, recruits to the right)
    - Node **sizes vary**: users with more recruits have larger boxes

    `[Screenshot: Graph View showing the visual network with nodes and arrows]`

**Part D: Interact with the Graph**

12. **Click and drag** a node to reposition it within the graph.
13. **Scroll** (mouse wheel) to zoom in and out of the graph.
14. **Click on a node** to view member details. An alert dialog appears showing:
    ```
    Member: [Name]
    ([X] recruits)
    Email: [user@email.com]
    ```
15. Click **"Fit to Screen"** to re-center and auto-scale the graph to show all nodes.
16. Click **"Toggle Physics"** to enable physics simulation (nodes will shift and settle; click again to disable).
17. Click **"Export Image"** to download a PNG image of the graph. The file saves as `call5-network-graph.png` with a white background.

**Part E: Legend / How to Use**

18. Below the graph, verify the **"How to Use"** legend section:
    - "🖱️ Click & Drag:" Move nodes around
    - "🔍 Scroll:" Zoom in/out
    - "👆 Click Node:" View member details
    - "📏 Box Size:" Larger = more recruits
    - "🎨 Box Color:" Shows group membership

**Part F: Switch Between Views**

19. Click the **"📋 Text View"** tab to return to the text view.
20. Verify the text tree is displayed again.
21. Click **"🌳 Graph View"** to return to the graph view.
22. Verify the graph reloads and displays correctly.

### Expected Results

| Step | Expected Result |
|------|----------------|
| 3 | Text View page loads with tab bar and indented tree |
| 8 | Graph View page loads with interactive vis.js graph |
| 11 | Nodes display as blue boxes with names and recruit counts |
| 14 | Clicking a node shows an alert with name, recruits, and email |
| 17 | PNG file downloads with white background |

### Success Criteria
- [ ] Text View shows all users in a properly indented tree hierarchy
- [ ] Graph View renders an interactive vis.js network visualization
- [ ] Graph flows left-to-right with arrows showing recruitment direction
- [ ] Node sizes reflect recruit counts (larger = more recruits)
- [ ] Clicking a node displays member name and email
- [ ] "Fit to Screen" re-centers the graph
- [ ] "Toggle Physics" toggles node simulation on/off
- [ ] "Export Image" downloads a PNG with white background
- [ ] Switching between Text and Graph tabs works without errors
- [ ] "Back to Dashboard" navigation works from both views

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Graph area is blank/empty | Wait a few seconds for the vis.js library to load from CDN. Check internet connection. |
| Nodes are overlapping | Click "Fit to Screen" to re-layout, or "Toggle Physics" to let nodes spread out. |
| Export Image is blank or transparent | Ensure you are not zoomed in too far. Click "Fit to Screen" first, then export. |
| Mobile: Graph is hard to interact with | The graph container is 400px on mobile. Use pinch-to-zoom and drag gestures. Navigation buttons appear automatically on touch devices. |

---

## Appendix A: Test Data Setup

### Required Test Accounts

For complete scenario coverage, the following test accounts should exist:

| Account | Auth Type | Recruited By | Has Recruits | Notes |
|---------|-----------|--------------|--------------|-------|
| Admin User | Google | None (root) | Yes | Has `is_admin=True` in database |
| Regular User 1 | Local | Admin User | Yes | Has at least 1 recruit |
| Regular User 2 | Google | Regular User 1 | No | New user for testing |
| New Test User | (to be created) | Any existing user | No | Use for signup scenarios |

### Creating Test Concerns

To test Scenario 5, at least one concern should exist:

1. Log in as any user who is a **member** of a group.
2. From the Dashboard, click **"Your Groups"**.
3. Click on a group name to go to the group management page.
4. Scroll to the **"Concerns"** section at the bottom of the group page.
5. Click the **"Post a Concern"** button.
6. On the **Post a Concern** page:
   - Enter a **title** (e.g., "Test Concern - Rich Text Features")
   - Use the **Quill rich text editor** toolbar to write a description with various formatting:
     - Add a **bold** word
     - Add an *italic* word
     - Create a bullet list
     - Create a numbered list
     - Add a heading (H2 or H3)
     - Add a blockquote
     - Add a link
   - Click **"Post Concern"**
7. The concern appears on the group page and in the All Concerns list.

### Creating Recruitment Relationships

To test Scenario 6 (Network Tree), ensure at least a 3-level recruitment chain:

1. Root user (no recruiter) recruits User A
2. User A recruits User B
3. User B recruits User C

This creates a tree: Root → A → B → C

### Invite Code Reference

Each user's invite code can be found on their Dashboard in the "Your Invite Link" section. The code is the 20-character string after `?ref=` in the URL.

---

## Appendix B: Common Troubleshooting

### General Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Page loads very slowly | Render free tier cold start | Wait 30-60 seconds. The service may need to wake up. Subsequent requests will be fast. |
| White page / 500 error | Server error | Refresh the page. If persistent, check the Render service status. |
| Session expired / logged out unexpectedly | Session timeout | Log in again. Sessions may expire after extended inactivity. |
| Page looks broken on mobile | CSS rendering issue | Try rotating your device. Ensure you're using a modern browser (Chrome, Safari, Firefox). |

### Authentication Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Google login loops back to landing page without logging in | OAuth callback error | Clear all cookies for the site. Try an incognito window. |
| "Invalid email or password" with correct credentials | Possible case sensitivity | Ensure email is entered exactly as registered. |
| Cannot sign in with Google after creating local account | Different auth types | If you registered with email/password, use the Login page, not Google sign-in (unless your email matches a Google account). |

### Concerns Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Post a Concern" button not visible | Not a group member | You must be a member of the group to post concerns. Join a group first. |
| Rich text toolbar not appearing | CDN load failure | Check internet connection. Quill.js loads from `cdn.quilljs.com`. |
| Concern description appears empty after posting | Editor empty on submit | Ensure you typed in the editor area (below the toolbar), not in the title field. |

### Browser Compatibility Notes

- **Chrome (recommended):** Full support for all features
- **Firefox:** Full support
- **Safari:** Google OAuth may require allowing cross-site tracking in Settings > Privacy
- **Edge:** Full support
- **Mobile browsers:** All features work. Graph view uses 400px container height on screens under 768px wide.

---

*Document Version: v0.4.07b | February 2026 | Call5 Democracy*
