# Call5 Democracy v0.4 - User Guide & Testing Instructions

## Welcome to Call5 Democracy

Call5 Democracy is a civic engagement platform that grows through personal networks. Each member recruits others using their unique invite link, creating an expanding "call-5" network of engaged citizens who organize around civic issues in their communities.

This guide provides step-by-step instructions for using the platform. It is organized by your role.

## How to Use This Guide

**Are you NEW to Call5?**
You received an invite link from someone and are joining for the first time.
> Jump to [Part 2: For New Members (Invitees)](#21-what-to-expect)

**Are you ALREADY a Call5 member?**
You have an account and want to recruit new members, manage your network, or explore platform features.
> See [Part 1: For Existing Members (Invitors)](#part-1-for-existing-members-invitors)

## Table of Contents

**Part 1: For Existing Members (Invitors)**
- [1.1 How to Get Your Invite Link](#11-how-to-get-your-invite-link)
- [1.2 How to Share Your Invite Link](#12-how-to-share-your-invite-link)
- [1.3 How to Verify Your Recruits](#13-how-to-verify-your-recruits)
- [1.4 Messaging Your Recruits](#14-messaging-your-recruits)
- [1.5 Creating and Managing Groups](#15-creating-and-managing-groups)
- [1.6 Viewing and Posting Concerns](#16-viewing-and-posting-concerns)
- [1.7 Viewing Your Network Tree](#17-viewing-your-network-tree)

**Part 2: For New Members (Invitees)**
- [2.1 What to Expect](#21-what-to-expect)
- [2.2 Signing Up with Google (Option A)](#22-signing-up-with-google-option-a)
- [2.3 Signing Up with Email and Password (Option B)](#23-signing-up-with-email-and-password-option-b)
- [2.4 Your First Time on the Dashboard](#24-your-first-time-on-the-dashboard)
- [2.5 Logging In on Future Visits (Google)](#25-logging-in-on-future-visits-google)
- [2.6 Logging In on Future Visits (Email/Password)](#26-logging-in-on-future-visits-emailpassword)
- [2.7 Exploring Concerns](#27-exploring-concerns)
- [2.8 Viewing Your Network Tree](#28-viewing-your-network-tree)

**Appendices**
- [Appendix A: Test Data Setup (For Admins)](#appendix-a-test-data-setup-for-admins)
- [Appendix B: Common Troubleshooting](#appendix-b-common-troubleshooting)

---

## Application Information

- **Application URL:** `https://voter-engagement-app.onrender.com/`
- **Version:** v0.4.07b
- **Supported Browsers:** Chrome (recommended), Firefox, Safari, Edge
- **Mobile:** All pages are mobile-friendly and work on phone and tablet browsers

---

# Part 1: For Existing Members (Invitors)

**This section is for you if:**
- You already have a Call5 account
- You want to recruit new members to grow the network
- You want to manage your groups and concerns
- You want to explore the network tree

---

## 1.1 How to Get Your Invite Link

Your invite link is a unique URL that connects new members to you when they sign up. Every person who uses your link becomes part of your recruit network.

1. Log in to Call5 at `https://voter-engagement-app.onrender.com/`
2. From the landing page, click the **"Dashboard"** button in the blue header bar.
3. On the Dashboard, locate the **"Your Invite Link"** section. It is below the stats card that shows your recruit count.
4. Your invite link appears in a read-only text field. It looks like this:
   ```
   https://voter-engagement-app.onrender.com/?ref=XXXXXXXXXXXXXXXXXXXX
   ```
5. Click the blue **"Copy"** button next to the link. The button text briefly changes to **"Copied!"** to confirm the link is on your clipboard.

   `[Screenshot: Dashboard showing the "Your Invite Link" section with Copy button]`

> **Tip:** Your invite code is the 20-character string after `?ref=`. This code is unique to you and never changes.

---

## 1.2 How to Share Your Invite Link

Once you have your invite link copied, send it to people you want to recruit. Here are effective ways to share it:

- **Nextdoor private message** - Great for reaching neighbors directly
- **Email** - Include a brief personal message explaining what Call5 is
- **Text message / SMS** - Quick and easy for people you know
- **Social media DM** (Twitter, Bluesky, Mastodon) - For your broader network

**Using the Share Page:**

For more sharing options, click the **"Share Your Invite Link"** button on your Dashboard. The Share page (`/share`) provides:

- Your invite link with a **"Copy"** button
- An **email invitation form** where you enter a recipient's email and optional personal message. Click **"Send Invitation"** to send directly from Call5.
- Pre-written **copy-and-paste messages** for five platforms:
  - Nextdoor, Twitter, Bluesky, Mastodon, and Email
  - Each message includes your invite link and is ready to copy

   `[Screenshot: Share page showing platform cards with pre-written messages]`

**What to tell people:**

When sharing your link, a brief explanation helps. For example:
> "I'm using Call5 Democracy to stay informed and organize around local civic issues. Join my network using this link: [your invite link]"

---

## 1.3 How to Verify Your Recruits

After someone signs up using your invite link, you can confirm they joined:

1. Go to your **Dashboard**.
2. Check the **stats card** at the top. The large blue number shows your total **People Recruited**. This count increases each time someone signs up with your link.
3. For a detailed view, click the **"Tree"** button near the bottom of the Dashboard to see your full recruitment network.

### What if my recruit count didn't go up?
- The new member must complete their signup (including email verification if they used email/password).
- Refresh your Dashboard page to see the updated count.
- If the person navigated directly to the signup page without first loading your invite link, the recruitment relationship won't be established. They need to click your link first, then sign up.

---

## 1.4 Messaging Your Recruits

Call5 includes a built-in messaging system for communicating with your recruiter and your recruits.

**From the Dashboard, you have these messaging buttons:**

- **"Message Your Recruiter"** - Send a message to the person who recruited you. (Grayed out with "(No Recruiter)" if you are a root user with no recruiter.)
- **"Message Your Recruits"** - Send a message to people you recruited. (Grayed out with "(No Recruits)" if you haven't recruited anyone yet.)
- **"Messages"** - View your inbox with all sent and received messages.

> **Note:** You can only message people in your direct recruitment chain (your recruiter and your recruits). This keeps conversations focused and relevant.

---

## 1.5 Creating and Managing Groups

Groups let you organize your recruits around specific topics or activities.

**Creating a Group:**
1. From the Dashboard, click **"Create Group"**. (This button is grayed out with "(Recruit first)" until you have at least one recruit.)
2. Fill in the group details and submit.

**Managing Groups:**
1. From the Dashboard, click **"Your Groups"** to see all groups you belong to or lead.
2. Click on a group name to go to its management page, where you can view members, post concerns, and manage the group.

---

## 1.6 Viewing and Posting Concerns

Concerns are civic issues that members share with their groups and the broader network.

**Viewing All Concerns:**
1. From the Dashboard, click **"View All Concerns"** (located after "Your Groups" in the button list).
2. The All Concerns page shows every concern across the platform, sorted newest first.
3. Each concern card displays:
   - **Title** (clickable to view full details)
   - **Scope badge:** "Group Only" (blue) or "Network-Wide" (green)
   - **Metadata:** Author name, group name, and date
   - **Preview:** First 200 characters of the description
4. Click any title to read the full concern with rich text formatting.

**Posting a New Concern:**
1. Go to a group page (Dashboard > **"Your Groups"** > click a group name).
2. Scroll to the **"Concerns"** section at the bottom.
3. Click **"Post a Concern"**.
4. On the Post a Concern page:
   - Enter a **title** (max 200 characters)
   - Write a **description** using the rich text editor toolbar (bold, italic, headings, lists, links, blockquotes)
   - Click **"Post Concern"**
5. The concern is initially visible only to group members (scope: "Group Only").

**Promoting a Concern to the Network:**

If you created a group-scoped concern and want to share it more broadly:
1. Open the concern by clicking its title.
2. If you are the creator and the concern is still "Group Only," you will see a **"Share to Network"** button at the bottom.
3. Click it, then confirm in the modal dialog.
4. The concern becomes "Network-Wide" and all members in your recruit network are notified by email.
5. This action cannot be undone.

---

## 1.7 Viewing Your Network Tree

The network tree shows the full recruitment hierarchy, so you can see how your network is growing.

1. From the Dashboard, click the **"Tree"** button (near the bottom of the action buttons).
2. The **Text View** loads by default, showing an indented list:
   - Each line shows: **Name** (X recruits)
   - Indentation shows who recruited whom (deeper indent = recruited by the person above)
3. Click the **"🌳 Graph View"** tab for an interactive visual map:
   - Blue boxes represent members, with arrows showing who recruited whom
   - Larger boxes = more recruits
   - The graph flows left-to-right (founders on the left, newest recruits on the right)
4. **Interact with the graph:**
   - Click and drag nodes to reposition them
   - Scroll to zoom in/out
   - Click a node to see the member's name and email
5. **Control buttons** (above the graph):
   - **"Fit to Screen"** - Re-centers the view
   - **"Toggle Physics"** - Enables/disables node animation
   - **"Export Image"** - Downloads the graph as a PNG file

   `[Screenshot: Graph View showing the recruitment network visualization]`

---

# Part 2: For New Members (Invitees)

**This section is for you if:**
- You received an invite link from someone
- You are signing up for Call5 for the first time
- You want to understand how to use the platform

**Before you start:** You should have received an invite link that looks like this:
```
https://voter-engagement-app.onrender.com/?ref=XXXXXXXXXXXXXXXXXXXX
```

If you don't have this link yet, ask the person who invited you to send it to you. The link is important because it connects your new account to the person who invited you.

---

## 2.1 What to Expect

Here's what happens when you join Call5:

1. You click the invite link you received
2. You create an account (using Google or email/password - your choice)
3. You land on your personal Dashboard
4. You get your own invite link to recruit others
5. You can explore concerns, view the network tree, and participate in groups

The signup process takes about 2 minutes. You'll need either a Google account or a valid email address.

---

## 2.2 Signing Up with Google (Option A)

This is the fastest way to join. You'll use your existing Google account - no new password to remember.

### What You Need
- The invite link you received
- A Google account (Gmail, Google Workspace, etc.)

### Steps

1. Click the invite link you received, or paste it into your browser's address bar and press Enter.
2. A page titled **"Voter Engagement Response Form"** loads. This is the Call5 landing page.
3. In the blue header area, look for the white **"Sign in with Google"** button. It has the familiar four-color Google "G" logo next to the text.

   `[Screenshot: Landing page showing the "Sign in with Google" button]`

4. Click **"Sign in with Google"**.
5. Google's account selection screen appears. Choose the Google account you want to use for Call5.
6. If this is your first time, Google may ask you to approve Call5 Democracy's access. Click **"Allow"** or **"Continue"**.
7. You are redirected back to the Call5 landing page. Your email now appears in the blue header area, along with two new buttons: **"Dashboard"** and **"Sign Out"**.

   `[Screenshot: Landing page after successful Google sign-in showing email and Dashboard button]`

8. Click the **"Dashboard"** button to go to your personal Dashboard.
9. Your Dashboard loads. You should see:
   - **"Welcome, [Your Name]!"** at the top (your Google account name)
   - **"Recruited by: [Name]"** below the welcome line (the name of the person who sent you the invite link)
   - A stats card showing **"0"** People Recruited (this will grow as you invite others)
   - **"Your Invite Link"** section with your own unique link for recruiting others

   `[Screenshot: New member's Dashboard showing welcome message and recruiter attribution]`

That's it! Your account is created and ready to use. Continue to [Section 2.4](#24-your-first-time-on-the-dashboard) to learn about your Dashboard.

### Troubleshooting

| Issue | Solution |
|-------|----------|
| The Google sign-in button does nothing when I click it | Pop-ups may be blocked. Check your browser's pop-up blocker settings and allow pop-ups for this site. |
| I see an error page after approving Google access | Clear your browser cookies and try again. Open the invite link in a fresh browser tab. |
| My Dashboard doesn't show "Recruited by" anyone | Make sure you opened the **invite link** first (the URL with `?ref=...`), then signed in. If you navigated to the site directly without the invite link, the connection to your inviter won't be made. Ask your inviter to send the link again, sign out, then click the link and sign in again. |
| I already have a Call5 account from before | No problem! Clicking "Sign in with Google" will log you into your existing account. Your existing recruiter relationship is preserved. |

---

## 2.3 Signing Up with Email and Password (Option B)

If you prefer not to use Google, you can create an account with your email address and a password.

### What You Need
- The invite link you received
- A valid email address you can access (for verification)
- A password that meets the requirements (see below)

### Steps

**Creating Your Account:**

1. Click the invite link you received, or paste it into your browser's address bar and press Enter.
2. The Call5 landing page loads.
3. In the blue header area, click the **"Sign up with Email"** button. It's a semi-transparent button below the Google sign-in option, separated by an "or" divider.

   `[Screenshot: Landing page with "Sign up with Email" button highlighted]`

4. The **Sign Up** page loads. You'll see a form with the heading **"Sign Up with Email"** and the subtitle "Join Call5 to engage with your civic community."
5. Fill in the form:

   | Field | What to Enter |
   |-------|--------------|
   | **Full Name** | Your first and last name |
   | **Email Address** | A valid email you can check right away |
   | **Password** | A password (see requirements below) |
   | **Confirm Password** | Type the same password again |

6. **Password requirements** (shown below the password field):
   - At least **8 characters** long
   - Must include at least one **uppercase letter** (A-Z)
   - Must include at least one **lowercase letter** (a-z)
   - Must include at least one **number** (0-9)

   Example of a valid password: `MyPassword1`

7. Click the blue **"Create Account"** button.

   `[Screenshot: Signup form filled in with all fields]`

**Verifying Your Email:**

8. You'll see a green banner message:
   > "Account created! Please check your email to verify your account."
9. Check your email inbox for a verification message from Call5 Democracy. (Check your spam/junk folder if you don't see it within a few minutes.)
10. Click the **verification link** in the email to confirm your address.

**Logging In for the First Time:**

11. After clicking the verification link, go to: `https://voter-engagement-app.onrender.com/login`
12. On the **Log In** page, enter your **Email Address** and **Password**.
13. Click the blue **"Log In"** button.
14. A green banner appears: **"Welcome back, [Your Name]!"**
15. You are taken to your **Dashboard**. Verify you see:
    - **"Welcome, [Your Name]!"**
    - **"Recruited by: [Name]"** (the person who sent you the invite link)
    - Stats showing **"0"** People Recruited
    - Your own unique invite link

   `[Screenshot: Dashboard after first email/password login]`

Your account is set up! Continue to [Section 2.4](#24-your-first-time-on-the-dashboard) to learn about your Dashboard.

### Troubleshooting

| Issue | Solution |
|-------|----------|
| I see a red error: **"All fields are required"** | Make sure every field is filled in before clicking "Create Account." |
| I see a red error: **"Passwords do not match"** | Re-type both the Password and Confirm Password fields carefully. They must be identical. |
| I see a red error about password requirements | Your password needs at least 8 characters, one uppercase letter, one lowercase letter, and one number. Try a stronger password. |
| I see: **"Email already registered. Please log in."** | You already have an account with this email. Go to the Login page and sign in instead. |
| I never received the verification email | Check your spam/junk folder. Wait up to 5 minutes. If it still doesn't arrive, go to the login page and look for a "resend verification" option. |
| I see: **"Please verify your email before logging in"** | You need to click the verification link in the email you received during signup. Check your inbox (and spam folder). |
| My Dashboard doesn't show "Recruited by" anyone | Make sure you clicked the **invite link** (the URL with `?ref=...`) before signing up. The invite code is captured when you first load that page. |

---

## 2.4 Your First Time on the Dashboard

Your Dashboard is your home base on Call5. Here's what you'll find:

`[Screenshot: Full Dashboard with all sections labeled]`

### Header
- Your **name** is displayed in the blue header
- **"Sign Out"** button (top right area)
- Page label "Dashboard" in the top-right corner

### Welcome Section
- **"Welcome, [Your Name]!"**
- **"Recruited by: [Name]"** - shows who invited you to Call5

### Stats Card
- A large blue number showing how many **People Recruited** you have
- As a new member, this starts at **0** and grows as people sign up using your invite link

### Your Invite Link
- A text field with your unique invite link
- Click the blue **"Copy"** button to copy it to your clipboard
- Share this link with others to recruit them (they'll be connected to you in the network)

### Action Buttons
Your Dashboard has a vertical list of blue buttons. Here's what each one does:

| Button | What It Does |
|--------|-------------|
| **Share Your Invite Link** | Opens a page with your invite link, an email form, and pre-written messages for social media |
| **Message Your Recruiter** | Send a message to the person who invited you |
| **Message Your Recruits** | Send a message to people you've recruited (available after your first recruit) |
| **Messages** | View your message inbox |
| **Create Group** | Start a new group (available after your first recruit) |
| **Your Groups** | View groups you belong to or lead |
| **View All Concerns** | Browse civic issues posted by the community |
| **Submit Voter Question** | Ask a question to an AI candidate personality |
| **Tree** | View the recruitment network as a text list or interactive graph |

> **Note:** Some buttons appear grayed out when you first join. For example, **"Message Your Recruits"** shows "(No Recruits)" and **"Create Group"** shows "(Recruit first)" until you've recruited at least one person. They'll become active as your network grows.

---

## 2.5 Logging In on Future Visits (Google)

When you come back to Call5 after signing out or closing your browser:

1. Go to `https://voter-engagement-app.onrender.com/`
2. Click the white **"Sign in with Google"** button in the blue header.
3. Select your Google account (if you have multiple, pick the one you used to sign up).
4. You'll land back on the landing page with your email displayed in the header.
5. Click **"Dashboard"** to go to your Dashboard.

That's it! Google handles the authentication, so there's no password to remember.

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Google sign-in loops back without logging me in | Clear your browser cookies for the Call5 site and try again. Or try an incognito/private window. |
| I don't see the "Dashboard" button after signing in | Look for your email address in the blue header area. The "Dashboard" button should be right next to it. If you don't see your email, the sign-in didn't complete. Try again. |

---

## 2.6 Logging In on Future Visits (Email/Password)

When you come back to Call5 after signing out or closing your browser:

1. Go to `https://voter-engagement-app.onrender.com/`
2. Click the **"Log in"** link in the blue header (text reads: "Already have an account? **Log in**").
3. The Login page loads with two fields:
   - **Email Address** (placeholder: "you@example.com")
   - **Password** (placeholder: "Your password")
4. Enter your email and password, then click the blue **"Log In"** button.
5. A green banner shows: **"Welcome back, [Your Name]!"**
6. You're taken to your Dashboard.

### If You Forgot Your Password
- On the Login page, click the **"Forgot password?"** link (blue text, right-aligned below the password field).
- Follow the instructions to reset your password via email.

### Troubleshooting

| Issue | Solution |
|-------|----------|
| **"Invalid email or password"** | Double-check your email and password for typos. Email is case-sensitive. |
| **"Account locked for X minutes"** | After 5 incorrect password attempts, your account locks for 30 minutes for security. Wait and try again. |
| **"Please verify your email before logging in"** | You need to click the verification link from the email you received when you first signed up. Check your inbox and spam folder. |
| I forgot which email I used | Try each email you might have used. If you signed up with Google, use the Google sign-in button instead. |

---

## 2.7 Exploring Concerns

Concerns are civic issues that Call5 members share with the community. You can browse and read concerns posted by other members.

1. From your Dashboard, click the **"View All Concerns"** button.
2. The **All Concerns** page loads, showing:
   - Heading: **"All Concerns"**
   - Subheading: "Civic issues from across the Call5 community"
   - A count of total concerns (e.g., "3 total concerns")

3. Each concern appears as a card with:
   - **Title** (click to read the full concern)
   - **Scope badge** on the right:
     - **"Group Only"** (blue badge) - visible to group members
     - **"Network-Wide"** (green badge) - visible to the broader network
   - **Metadata:** "Posted by [Name] - [Group Name] - [Date]"
   - **Preview:** First 200 characters of the description

   `[Screenshot: All Concerns page showing concern cards with badges]`

4. Click a **concern title** to open it and read the full text.
5. The concern detail page shows:
   - The full **title** as a large heading
   - **Author**, **date and time**, **group name**, and **scope badge**
   - The complete **description** with rich text formatting (bold, italic, headings, lists, links, blockquotes)

   `[Screenshot: A concern detail page with rich text formatting]`

6. To go back, click **"&larr; Back to [Group Name]"** at the top of the page, or use your browser's back button.

> **Note:** If you see a message saying "You do not have permission to view this concern," it means the concern is group-scoped and you're not a member of that group. Network-wide concerns are visible to everyone in the creator's recruit network.

---

## 2.8 Viewing Your Network Tree

The network tree shows how Call5 members are connected through recruitment. Even as a new member, you can see the full network.

1. From your Dashboard, click the **"Tree"** button (near the bottom of the action buttons).
2. The **Text View** loads first, showing a simple indented list:
   - Each line shows a member's **name** and their **recruit count**
   - Deeper indentation means that person was recruited by the person above them
   - You should be able to find your own name in the tree, indented under the person who invited you

   `[Screenshot: Text View of the network tree]`

3. To see a visual map, click the **"🌳 Graph View"** tab at the top.
4. An interactive graph appears:
   - **Blue boxes** represent members (larger boxes = more recruits)
   - **Arrows** point from recruiters to their recruits
   - The graph flows **left to right** (founders on the left, newest members on the right)

   `[Screenshot: Graph View showing the visual network]`

5. **How to interact with the graph:**
   - **Click and drag** a box to move it around
   - **Scroll** (mouse wheel) to zoom in or out
   - **Click on a box** to see the member's name and email
   - On mobile: use pinch-to-zoom and drag gestures

6. **Buttons above the graph:**
   - **"Fit to Screen"** - Resets the view to show all members
   - **"Toggle Physics"** - Makes nodes bounce and settle (click again to stop)
   - **"Export Image"** - Downloads the graph as a picture file (PNG)

7. Below the graph, a **"How to Use"** legend explains all the interactions.

8. To go back, click **"Back to Dashboard"** (blue button in the header on Graph View, or a link below the tree on Text View).

> **Tip:** As you recruit people, you'll see your part of the tree grow. Check back to watch your network expand!

---

# Appendices

---

## Appendix A: Test Data Setup (For Admins)

This section is for platform administrators setting up test data. Regular users can skip this.

### Creating Test Concerns

To ensure the Concerns feature has content for new users to explore:

1. Log in as a user who is a **member** of a group.
2. From the Dashboard, click **"Your Groups"**.
3. Click on a group name to open its management page.
4. Scroll to the **"Concerns"** section at the bottom.
5. Click **"Post a Concern"**.
6. On the Post a Concern page:
   - Enter a **title** (e.g., "Support Local Transit Improvements")
   - Use the **rich text editor** toolbar to format the description:
     - Add **bold** and *italic* text
     - Create bullet and numbered lists
     - Add headings (H2 or H3)
     - Add blockquotes and links
   - Click **"Post Concern"**
7. The concern appears in the group and on the All Concerns page.

### Ensuring Recruitment Chains

For the Network Tree to be meaningful, ensure at least a 3-level recruitment chain exists:

1. Root user (the original account, no recruiter) recruits User A
2. User A recruits User B
3. User B recruits User C

This creates a visible tree: Root > A > B > C

### Invite Code Reference

Each user's invite code can be found on their Dashboard in the "Your Invite Link" section. The code is the 20-character string after `?ref=` in the URL.

---

## Appendix B: Common Troubleshooting

### General Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| The page takes a long time to load | The server may be waking up from a sleep state | Wait 30-60 seconds and refresh. Subsequent pages will load quickly. |
| I see a white page or error | A temporary server issue | Refresh the page. If it persists, try again in a few minutes. |
| I got logged out unexpectedly | Session expired | Log in again. Sessions may expire after extended inactivity. |
| The page looks broken on my phone | Display rendering issue | Try rotating your phone. Make sure you're using an up-to-date browser (Chrome, Safari, or Firefox). |

### Sign-In Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Google sign-in keeps looping without logging me in | OAuth session error | Clear all cookies for the site, or try in an incognito/private window. |
| "Invalid email or password" but I'm sure my credentials are right | Possible typo or case mismatch | Re-type your email carefully. If you signed up with Google, use the Google button instead of email/password. |
| "Account locked for X minutes" | Too many failed login attempts | Wait for the lockout period to end (30 minutes), then try again with the correct password. |

### Concerns Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| I can't see the "Post a Concern" button | You're not a member of the group | You need to be a group member to post. Ask the group leader to add you. |
| The rich text toolbar doesn't appear | The toolbar library didn't load | Check your internet connection and refresh the page. |
| My concern description appears empty after posting | You may have typed outside the editor area | Make sure you click inside the white editor area (below the toolbar) before typing. |

### Browser Notes

- **Chrome** is recommended for the best experience
- **Safari** users: If Google sign-in doesn't work, go to Safari > Settings > Privacy and uncheck "Prevent cross-site tracking"
- **Mobile browsers:** All features work. The graph view adjusts to a smaller size on phone screens.

---

*Document Version: v0.4.07b | February 2026 | Call5 Democracy*
