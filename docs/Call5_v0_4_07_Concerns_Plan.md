# Call5 Democracy v0.4.07
## Concerns Feature - Group-Level Civic Issue Tracking

**February 10, 2026**

---

## Overview

Version 0.4.07 introduces the **Concerns** feature, enabling Call5 members to log civic issues within their groups and organize collective action. This transforms groups from passive membership lists into active organizing hubs, giving the network a concrete purpose beyond election-cycle Q&A.

**Core Innovation:** Concerns start group-scoped (safe space for discussion) but can be expanded network-wide by the creator (enabling exponential awareness spread through the recruit tree).

---

## Why Concerns Matter

The Concerns feature addresses a critical gap in current civic engagement platforms:

**Problem:** Most civic tech focuses on *consumption* (read news, ask candidates questions) rather than *organization* (identify issues, coordinate action).

**Solution:** Concerns give members a tool to:
- **Document civic issues** they care about (bills, policies, local problems)
- **Organize within trusted groups** (start with people they know)
- **Amplify through networks** (expand reach when comfortable)
- **Track engagement** (measure what matters to the community)

**Strategic Fit:** This feature activates the Groups infrastructure built in v0.3.1 Phase 2, giving groups actual utility beyond symbolic membership.

---

## Use Case: Alex and the Wyden Bill

**Scenario:** Alex (member of "54 Ave Group") learns that Senator Ron Wyden's bill (S.2723 - Epstein Financial Accountability Act, introduced September 2025) is being blocked by Senate Republicans. The bill requires suspicious activity reports on Jeffrey Epstein and associates.

**Action Flow:**
1. Alex visits 54 Ave Group page
2. Clicks "Post a Concern"
3. Fills form:
   - **Title:** "Support Senator Wyden's Epstein Transparency Bill"
   - **Description:** Explains bill details, current blockage, why it matters
4. Submits → Concern logged as group-scoped
5. All 54 Ave Group members receive email notification
6. After group discussion, Alex clicks "Share to Network" 
7. All 9 members in Tony's recruit network now see the concern

**Outcome:** A single member's local concern becomes network-wide awareness, leveraging Call5's exponential growth model.

---

## Conceptual Model

### Two-Tier Visibility

**Tier 1: Group-Scoped (Default)**
- Visible only to members of the specific group
- Safe space for initial discussion and refinement
- Creator controls whether to expand scope

**Tier 2: Network-Wide (Optional)**
- Visible to all members in the recruit network
- Only creator can promote concern to network-wide
- Enables exponential awareness spread

**Example:**
- Alex posts concern in "54 Ave Group" (3 members see it)
- Alex shares to network → All 9 network members see it
- Later: When network grows to 125 members, those 125 see it

### Relationships

**Concern ↔ Group:**
- Every concern belongs to exactly one group
- Group membership determines initial visibility
- Group context preserved even when shared network-wide

**Concern ↔ User:**
- Created by one user (creator has special permissions)
- Visible to users based on scope + membership rules

**Future:** Concern ↔ Comments (v0.4.2), Concern ↔ Actions (v0.4.3)

---

## Database Schema

### New Table: `concerns`

```sql
CREATE TABLE concerns (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    created_by_user_id INTEGER NOT NULL REFERENCES users(id),
    group_id INTEGER NOT NULL REFERENCES groups(id),
    scope VARCHAR(20) DEFAULT 'group' CHECK (scope IN ('group', 'network')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_concerns_group ON concerns(group_id);
CREATE INDEX idx_concerns_creator ON concerns(created_by_user_id);
CREATE INDEX idx_concerns_scope ON concerns(scope);
```

### Field Definitions

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | SERIAL | NO | Primary key |
| `title` | VARCHAR(200) | NO | Concern headline (e.g., "Support Wyden's Bill") |
| `description` | TEXT | NO | Full explanation with context, links, call to action |
| `created_by_user_id` | INTEGER | NO | Foreign key to users.id (concern creator) |
| `group_id` | INTEGER | NO | Foreign key to groups.id (home group) |
| `scope` | VARCHAR(20) | NO | 'group' (default) or 'network' |
| `created_at` | TIMESTAMP | NO | When concern was posted |
| `updated_at` | TIMESTAMP | NO | Last modification (for future edits feature) |

### Business Rules

**Visibility Rules:**
- **Group-scoped:** User must be member of concern's group to view
- **Network-scoped:** User must be in the recruit network (share a network ancestor) to view

**Creation Permissions:**
- Any member of a group can create concerns in that group
- No minimum recruit count required (unlike group creation)

**Scope Promotion:**
- Only the concern creator can change scope from 'group' to 'network'
- Once promoted to network, cannot be demoted back to group (prevents confusion)

**Email Notifications:**
- Group-scoped: Send to all group members except creator
- Network-scoped: Send to all network members except those already notified

---

## User Flows

### Flow 1: Creating a Group-Scoped Concern

**Precondition:** Alex is a member of "54 Ave Group"

1. Alex navigates to `/groups/1` (54 Ave Group page)
2. Sees "Post a Concern" button in the concerns section
3. Clicks button → navigates to `/groups/1/concerns/create`
4. Fills form:
   - **Title:** "Support Senator Wyden's Epstein Transparency Bill"
   - **Description:** (Multiline textarea with markdown support in future)
     ```
     Senator Ron Wyden introduced S.2723 in September 2025 requiring the 
     Secretary of State to produce suspicious activity reports on Jeffrey 
     Epstein and his associates.
     
     The bill is currently blocked by Senate Republicans. These financial 
     records are hard evidence with transaction dates, parties, amounts - 
     crucial for accountability.
     
     We should contact our senators to support this bill.
     ```
5. Submits form → `POST /groups/1/concerns/create`
6. Backend:
   - Creates concern record with `scope='group'`
   - Queries group members (Tony, Alex, David)
   - Sends email to Tony and David (not Alex, he's the creator)
7. Redirects to `/groups/1` → concern now visible in group's concern list
8. Alex sees "Share to Network" button (only visible to creator)

**Email Notification (Group-Scoped):**
```
Subject: New concern in 54 Ave Group: "Support Senator Wyden's Epstein Transparency Bill"

Alex Girouard posted a concern in 54 Ave Group:

"Senator Ron Wyden introduced S.2723 in September 2025 requiring the 
Secretary of State to produce suspicious activity reports on Jeffrey 
Epstein and his associates.

The bill is currently blocked by Senate Republicans..."

View full concern and discuss:
https://voter-engagement-app.onrender.com/groups/1

---
You're receiving this because you're a member of 54 Ave Group.
```

---

### Flow 2: Promoting Concern to Network-Wide

**Precondition:** Alex has posted a group-scoped concern, group members have discussed

1. Alex returns to `/groups/1` (54 Ave Group page)
2. Views his concern, sees "Share to Network" button
3. Clicks button → Modal confirmation:
   ```
   Share this concern with your entire Call5 network?
   
   This will notify all 9 members in your recruit network. This action 
   cannot be undone.
   
   [Cancel] [Share to Network]
   ```
4. Clicks "Share to Network" → `POST /concerns/<id>/promote`
5. Backend:
   - Updates concern: `scope='network'`
   - Queries all users in recruit network (find shared ancestor = Tony)
   - Excludes users already notified (Tony, David)
   - Sends email to remaining network members
6. Page refreshes → "Share to Network" button replaced with "Network-Wide" badge
7. Concern now visible to all network members (when they visit dashboard or group pages)

**Email Notification (Network Promotion):**
```
Subject: Network Concern: "Support Senator Wyden's Epstein Transparency Bill"

Alex Girouard shared a concern with the Call5 network:

"Senator Ron Wyden introduced S.2723 in September 2025 requiring the 
Secretary of State to produce suspicious activity reports on Jeffrey 
Epstein and his associates..."

View full concern:
https://voter-engagement-app.onrender.com/concerns/1

---
You're receiving this because you're part of the Call5 recruit network.
```

---

### Flow 3: Viewing Concerns as Group Member

**Precondition:** David is a member of "54 Ave Group"

1. David logs in, goes to dashboard
2. Sees notification: "1 new concern in 54 Ave Group"
3. Clicks group name → navigates to `/groups/1`
4. Sees concerns section with Alex's concern listed
5. Clicks concern title → navigates to `/concerns/1`
6. Views full concern details:
   - Title and full description
   - Creator name ("Posted by Alex Girouard")
   - Group context ("54 Ave Group")
   - Timestamp ("Posted 2 hours ago")
   - Scope badge ("Group" or "Network-Wide")
7. David does NOT see "Share to Network" button (only creator sees this)

---

### Flow 4: Viewing Network-Wide Concerns (Future: Dashboard Integration)

**Phase 1:** Concerns only visible through group pages

**Future (v0.4.2):**
1. User goes to dashboard
2. Sees "Network Concerns" section
3. Lists all network-wide concerns from recruit network
4. Grouped by originating group for context
5. Click to view full concern

---

## Implementation Steps

### Step 1: Database Setup

**Local Development:**
```sql
-- Execute in votereng_dev database
CREATE TABLE concerns (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    created_by_user_id INTEGER NOT NULL REFERENCES users(id),
    group_id INTEGER NOT NULL REFERENCES groups(id),
    scope VARCHAR(20) DEFAULT 'group' CHECK (scope IN ('group', 'network')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_concerns_group ON concerns(group_id);
CREATE INDEX idx_concerns_creator ON concerns(created_by_user_id);
CREATE INDEX idx_concerns_scope ON concerns(scope);
```

**Production Deployment:**
- Execute same SQL on Render PostgreSQL via pgAdmin
- Verify indexes created successfully

---

### Step 2: SQLAlchemy Model (votereng.py)

Add after `GroupMember` model:

```python
class Concern(db.Model):
    __tablename__ = 'concerns'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    scope = db.Column(db.String(20), default='group', nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    creator = db.relationship('User', backref='concerns_created')
    group = db.relationship('Group', backref='concerns')
    
    def __repr__(self):
        return f'<Concern {self.id}: {self.title[:30]}>'
```

---

### Step 3: Helper Function - Get Network Members

Add to votereng.py after existing helper functions:

```python
def get_network_members(user_id):
    """
    Get all users in the same recruit network (share a common ancestor).
    
    Algorithm:
    1. Find root ancestor (user with invited_by_user_id = NULL)
    2. Get all descendants of that root
    
    Returns: List of User objects
    """
    user = db.session.get(User, user_id)
    if not user:
        return []
    
    # Find root ancestor
    root = user
    while root.invited_by_user_id is not None:
        root = db.session.get(User, root.invited_by_user_id)
    
    # Get all descendants of root (BFS traversal)
    network = []
    queue = [root]
    visited = set()
    
    while queue:
        current = queue.pop(0)
        if current.id in visited:
            continue
        visited.add(current.id)
        network.append(current)
        
        # Add all direct recruits to queue
        for recruit in current.invitees:
            if recruit.id not in visited:
                queue.append(recruit)
    
    return network
```

---

### Step 4: Routes - Create Concern

**GET /groups/<id>/concerns/create** - Show creation form

```python
@app.route('/groups/<int:group_id>/concerns/create')
def create_concern_form(group_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))
    
    # Verify user is member of this group
    membership = GroupMember.query.filter_by(
        group_id=group_id,
        user_id=user_id
    ).first()
    
    if not membership:
        flash('You must be a member of this group to post concerns.')
        return redirect(url_for('groups_list'))
    
    group = db.session.get(Group, group_id)
    return render_template('concern_create.html', 
                          group=group,
                          user_name=session.get('user_name'))
```

**POST /groups/<id>/concerns/create** - Handle submission

```python
@app.route('/groups/<int:group_id>/concerns/create', methods=['POST'])
def create_concern(group_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))
    
    # Verify membership
    membership = GroupMember.query.filter_by(
        group_id=group_id,
        user_id=user_id
    ).first()
    
    if not membership:
        flash('You must be a member of this group to post concerns.')
        return redirect(url_for('groups_list'))
    
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    
    if not title or not description:
        flash('Title and description are required.')
        return redirect(url_for('create_concern_form', group_id=group_id))
    
    # Create concern
    concern = Concern(
        title=title,
        description=description,
        created_by_user_id=user_id,
        group_id=group_id,
        scope='group'
    )
    db.session.add(concern)
    db.session.commit()
    
    # Send email notifications to group members (except creator)
    group = db.session.get(Group, group_id)
    members = [m.user for m in group.members if m.user_id != user_id]
    
    for member in members:
        send_concern_notification(
            recipient_email=member.email,
            recipient_name=member.name,
            concern_title=title,
            creator_name=session.get('user_name'),
            group_name=group.name,
            concern_url=request.host_url.rstrip('/') + f'/concerns/{concern.id}',
            scope='group'
        )
    
    flash('Concern posted successfully.')
    return redirect(url_for('group_manage', group_id=group_id))
```

---

### Step 5: Routes - Promote Concern to Network

**POST /concerns/<id>/promote** - Expand scope to network

```python
@app.route('/concerns/<int:concern_id>/promote', methods=['POST'])
def promote_concern(concern_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))
    
    concern = db.session.get(Concern, concern_id)
    
    if not concern:
        flash('Concern not found.')
        return redirect(url_for('dashboard'))
    
    # Only creator can promote
    if concern.created_by_user_id != user_id:
        flash('Only the concern creator can share to network.')
        return redirect(url_for('view_concern', concern_id=concern_id))
    
    # Only group-scoped concerns can be promoted
    if concern.scope != 'group':
        flash('This concern is already network-wide.')
        return redirect(url_for('view_concern', concern_id=concern_id))
    
    # Update scope
    concern.scope = 'network'
    concern.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    
    # Get all network members
    network_members = get_network_members(user_id)
    
    # Get group members (already notified)
    group = concern.group
    group_member_ids = [m.user_id for m in group.members]
    
    # Send emails to network members not in the group
    for member in network_members:
        if member.id not in group_member_ids and member.id != user_id:
            send_concern_notification(
                recipient_email=member.email,
                recipient_name=member.name,
                concern_title=concern.title,
                creator_name=concern.creator.name,
                group_name=group.name,
                concern_url=request.host_url.rstrip('/') + f'/concerns/{concern_id}',
                scope='network'
            )
    
    flash('Concern shared with network.')
    return redirect(url_for('view_concern', concern_id=concern_id))
```

---

### Step 6: Routes - View Concern

**GET /concerns/<id>** - View full concern details

```python
@app.route('/concerns/<int:concern_id>')
def view_concern(concern_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))
    
    concern = db.session.get(Concern, concern_id)
    
    if not concern:
        flash('Concern not found.')
        return redirect(url_for('dashboard'))
    
    # Check visibility permissions
    user = db.session.get(User, user_id)
    
    if concern.scope == 'group':
        # Must be member of the group
        membership = GroupMember.query.filter_by(
            group_id=concern.group_id,
            user_id=user_id
        ).first()
        
        if not membership:
            flash('You do not have permission to view this concern.')
            return redirect(url_for('dashboard'))
    
    else:  # network scope
        # Must be in the same recruit network
        network_members = get_network_members(user_id)
        network_ids = [m.id for m in network_members]
        
        if concern.created_by_user_id not in network_ids:
            flash('You do not have permission to view this concern.')
            return redirect(url_for('dashboard'))
    
    # User is creator?
    is_creator = (concern.created_by_user_id == user_id)
    
    # Can promote? (creator + still group-scoped)
    can_promote = is_creator and concern.scope == 'group'
    
    return render_template('concern_view.html',
                          concern=concern,
                          is_creator=is_creator,
                          can_promote=can_promote,
                          user_name=session.get('user_name'))
```

---

### Step 7: Email Notification Function

Add to votereng.py after existing MailGun functions:

```python
def send_concern_notification(recipient_email, recipient_name, concern_title, 
                              creator_name, group_name, concern_url, scope):
    """
    Send email notification when a concern is posted or promoted.
    
    Args:
        scope: 'group' or 'network'
    """
    if scope == 'group':
        subject = f"New concern in {group_name}: \"{concern_title}\""
        body_text = f"""
{creator_name} posted a concern in {group_name}:

"{concern_title}"

View full concern and discuss:
{concern_url}

---
You're receiving this because you're a member of {group_name}.
"""
    else:  # network
        subject = f"Network Concern: \"{concern_title}\""
        body_text = f"""
{creator_name} shared a concern with the Call5 network:

"{concern_title}"

Originally posted in: {group_name}

View full concern:
{concern_url}

---
You're receiving this because you're part of the Call5 recruit network.
"""
    
    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f"Call5 Democracy <noreply@{MAILGUN_DOMAIN}>",
                "to": recipient_email,
                "subject": subject,
                "text": body_text
            }
        )
        
        if response.status_code == 200:
            print(f"Concern notification sent to {recipient_email}")
        else:
            print(f"Failed to send concern notification: {response.text}")
    
    except Exception as e:
        print(f"Error sending concern notification: {str(e)}")
```

---

### Step 8: Template - concern_create.html

Mobile-friendly form matching existing design:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Post a Concern - Call5 Democracy</title>
    <style>
        /* Copy base styles from dashboard.html */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            Alex-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            padding: 30px;
        }
        
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        h1 {
            color: #667eea;
            font-size: 24px;
        }
        
        .breadcrumb {
            color: #666;
            font-size: 14px;
            margin-bottom: 20px;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
            font-size: 14px;
        }
        
        input[type="text"],
        textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            font-family: inherit;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus,
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        textarea {
            min-height: 200px;
            resize: vertical;
        }
        
        .char-count {
            text-align: right;
            font-size: 12px;
            color: #999;
            margin-top: 5px;
        }
        
        .button-group {
            display: flex;
            gap: 15px;
            margin-top: 30px;
        }
        
        .btn {
            flex: 1;
            padding: 14px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn-secondary {
            background: #f0f0f0;
            color: #333;
        }
        
        .btn-secondary:hover {
            background: #e0e0e0;
        }
        
        .help-text {
            font-size: 13px;
            color: #666;
            margin-top: 5px;
            line-height: 1.5;
        }
        
        @media (Alex-width: 600px) {
            .container {
                padding: 20px;
            }
            
            .button-group {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📢 Post a Concern</h1>
        </div>
        
        <div class="breadcrumb">
            <a href="{{ url_for('dashboard') }}">Dashboard</a> → 
            <a href="{{ url_for('group_manage', group_id=group.id) }}">{{ group.name }}</a> → 
            Post Concern
        </div>
        
        <form method="POST" action="{{ url_for('create_concern', group_id=group.id) }}">
            <div class="form-group">
                <label for="title">Concern Title *</label>
                <input type="text" 
                       id="title" 
                       name="title" 
                       placeholder="E.g., Support Senator Wyden's Epstein Transparency Bill"
                       Alexlength="200"
                       required>
                <p class="help-text">A clear, concise headline (Alex 200 characters)</p>
            </div>
            
            <div class="form-group">
                <label for="description">Description *</label>
                <textarea id="description" 
                          name="description" 
                          placeholder="Explain the issue, why it matters, and what action you'd like the group to consider..."
                          required></textarea>
                <p class="help-text">
                    Provide context and details. You can include links, bill numbers, dates, etc.
                    This will be visible to all members of {{ group.name }}.
                </p>
            </div>
            
            <div class="button-group">
                <button type="button" 
                        class="btn btn-secondary" 
                        onclick="window.location.href='{{ url_for('group_manage', group_id=group.id) }}'">
                    Cancel
                </button>
                <button type="submit" class="btn btn-primary">
                    Post Concern
                </button>
            </div>
        </form>
    </div>
</body>
</html>
```

---

### Step 9: Template - concern_view.html

View concern with promotion button for creator:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ concern.title }} - Call5 Democracy</title>
    <style>
        /* Copy base styles from dashboard.html */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            Alex-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            padding: 30px;
        }
        
        .header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        .back-link {
            color: #667eea;
            text-decoration: none;
            font-size: 14px;
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }
        
        .concern-header {
            margin-bottom: 30px;
        }
        
        .concern-title {
            font-size: 28px;
            color: #333;
            margin-bottom: 15px;
            line-height: 1.3;
        }
        
        .concern-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            font-size: 14px;
            color: #666;
        }
        
        .meta-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .scope-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }
        
        .scope-group {
            background: #e3f2fd;
            color: #1976d2;
        }
        
        .scope-network {
            background: #e8f5e9;
            color: #388e3c;
        }
        
        .concern-body {
            margin: 30px 0;
            line-height: 1.8;
            color: #333;
            font-size: 16px;
            white-space: pre-wrap;
        }
        
        .action-section {
            margin-top: 40px;
            padding-top: 30px;
            border-top: 2px solid #f0f0f0;
        }
        
        .btn {
            display: inline-block;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }
        
        .modal.active {
            display: flex;
        }
        
        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 12px;
            Alex-width: 500px;
            width: 90%;
        }
        
        .modal-buttons {
            display: flex;
            gap: 15px;
            margin-top: 20px;
        }
        
        @media (Alex-width: 600px) {
            .container {
                padding: 20px;
            }
            
            .concern-title {
                font-size: 22px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <a href="{{ url_for('group_manage', group_id=concern.group.id) }}" class="back-link">
                ← Back to {{ concern.group.name }}
            </a>
        </div>
        
        <div class="concern-header">
            <h1 class="concern-title">{{ concern.title }}</h1>
            
            <div class="concern-meta">
                <div class="meta-item">
                    <span>👤</span>
                    <span>Posted by <strong>{{ concern.creator.name }}</strong></span>
                </div>
                
                <div class="meta-item">
                    <span>📅</span>
                    <span>{{ concern.created_at.strftime('%B %d, %Y at %I:%M %p') }}</span>
                </div>
                
                <div class="meta-item">
                    <span>🏠</span>
                    <span>{{ concern.group.name }}</span>
                </div>
                
                <div class="meta-item">
                    {% if concern.scope == 'group' %}
                        <span class="scope-badge scope-group">Group Only</span>
                    {% else %}
                        <span class="scope-badge scope-network">Network-Wide</span>
                    {% endif %}
                </div>
            </div>
        </div>
        
        <div class="concern-body">
{{ concern.description }}
        </div>
        
        {% if can_promote %}
        <div class="action-section">
            <p style="color: #666; margin-bottom: 15px;">
                This concern is currently visible only to {{ concern.group.name }} members.
                Share it with your entire Call5 network?
            </p>
            <button class="btn btn-primary" onclick="showPromoteModal()">
                📢 Share to Network
            </button>
        </div>
        {% endif %}
    </div>
    
    <!-- Promotion Confirmation Modal -->
    <div id="promoteModal" class="modal">
        <div class="modal-content">
            <h2 style="margin-bottom: 15px;">Share to Network?</h2>
            <p style="color: #666; line-height: 1.6;">
                This will notify all members in your Call5 recruit network. 
                This action cannot be undone.
            </p>
            <div class="modal-buttons">
                <button class="btn" style="background: #f0f0f0; color: #333;" onclick="hidePromoteModal()">
                    Cancel
                </button>
                <form method="POST" action="{{ url_for('promote_concern', concern_id=concern.id) }}" style="flex: 1;">
                    <button type="submit" class="btn btn-primary" style="width: 100%;">
                        Share to Network
                    </button>
                </form>
            </div>
        </div>
    </div>
    
    <script>
        function showPromoteModal() {
            document.getElementById('promoteModal').classList.add('active');
        }
        
        function hidePromoteModal() {
            document.getElementById('promoteModal').classList.remove('active');
        }
        
        // Close modal on outside click
        document.getElementById('promoteModal').addEventListener('click', function(e) {
            if (e.target === this) {
                hidePromoteModal();
            }
        });
    </script>
</body>
</html>
```

---

### Step 10: Update Group Management Page

Modify `templates/group_manage.html` to show concerns list:

Add after the members section:

```html
<!-- Concerns Section -->
<div class="section">
    <div class="section-header">
        <h2>📢 Group Concerns</h2>
        {% if is_member %}
        <a href="{{ url_for('create_concern_form', group_id=group.id) }}" class="btn btn-primary">
            Post a Concern
        </a>
        {% endif %}
    </div>
    
    {% if group.concerns %}
    <div class="concerns-list">
        {% for concern in group.concerns %}
        <div class="concern-card">
            <div class="concern-header">
                <h3>
                    <a href="{{ url_for('view_concern', concern_id=concern.id) }}">
                        {{ concern.title }}
                    </a>
                </h3>
                {% if concern.scope == 'network' %}
                <span class="scope-badge scope-network">Network-Wide</span>
                {% endif %}
            </div>
            <div class="concern-meta">
                <span>Posted by {{ concern.creator.name }}</span>
                <span>•</span>
                <span>{{ concern.created_at.strftime('%b %d, %Y') }}</span>
            </div>
            <div class="concern-preview">
                {{ concern.description[:200] }}{% if concern.description|length > 200 %}...{% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <p style="color: #999; text-align: center; padding: 30px;">
        No concerns posted yet. Be the first to raise an issue!
    </p>
    {% endif %}
</div>
```

Add CSS styles:

```css
.concerns-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.concern-card {
    border: 2px solid #f0f0f0;
    border-radius: 8px;
    padding: 20px;
    transition: all 0.3s;
}

.concern-card:hover {
    border-color: #667eea;
    box-shadow: 0 2px 10px rgba(102, 126, 234, 0.1);
}

.concern-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.concern-header h3 {
    margin: 0;
    font-size: 18px;
}

.concern-header h3 a {
    color: #333;
    text-decoration: none;
}

.concern-header h3 a:hover {
    color: #667eea;
}

.concern-meta {
    font-size: 13px;
    color: #999;
    margin-bottom: 12px;
}

.concern-preview {
    color: #666;
    line-height: 1.6;
}
```

---

## Testing Plan

### Test 1: Create Group-Scoped Concern

**Setup:** Alex logs in, navigates to 54 Ave Group

**Actions:**
1. Click "Post a Concern"
2. Fill title: "Support Senator Wyden's Epstein Transparency Bill"
3. Fill description with bill details
4. Submit

**Verify:**
- ✓ Concern appears in 54 Ave Group concerns list
- ✓ Concern visible to Tony and David (group members)
- ✓ Concern NOT visible to users outside group (e.g., Irene if she's in network)
- ✓ Email sent to Tony and David (not Alex)
- ✓ Email subject: "New concern in 54 Ave Group: ..."
- ✓ Concern shows "Group Only" badge
- ✓ Alex sees "Share to Network" button

---

### Test 2: Promote Concern to Network

**Setup:** Alex has posted group-scoped concern

**Actions:**
1. Alex views concern
2. Clicks "Share to Network"
3. Confirms in modal
4. Submits

**Verify:**
- ✓ Concern scope updated to 'network'
- ✓ "Share to Network" button disappears
- ✓ Badge changes to "Network-Wide"
- ✓ Email sent to all network members not in 54 Ave Group
- ✓ Email subject: "Network Concern: ..."
- ✓ Email mentions "Originally posted in: 54 Ave Group"

---

### Test 3: View Permissions - Group-Scoped

**Setup:** Concern is group-scoped in 54 Ave Group

**Test Group Member (David):**
- ✓ Can view concern from group page
- ✓ Cannot see "Share to Network" button
- ✓ Sees "Group Only" badge

**Test Non-Group Member (Irene, if in network):**
- ✓ Concern NOT visible in any view
- ✓ Direct URL access → "Permission denied" message

---

### Test 4: View Permissions - Network-Scoped

**Setup:** Concern promoted to network-wide

**Test Network Member (any user in recruit tree):**
- ✓ Can view concern
- ✓ Sees "Network-Wide" badge
- ✓ Sees originating group name

**Test Non-Network User (if exists):**
- ✓ Concern NOT visible
- ✓ Direct URL access → "Permission denied" message

---

### Test 5: Concern List Display

**Setup:** Multiple concerns in group (various states)

**Verify Group Page:**
- ✓ All concerns listed in reverse chronological order
- ✓ Network-wide concerns show badge
- ✓ Group-only concerns show no special badge
- ✓ Preview text limited to ~200 characters
- ✓ Creator names shown
- ✓ Dates formatted correctly

---

### Test 6: Email Notifications

**Test Group-Scoped Email:**
- ✓ Subject: "New concern in [Group]: [Title]"
- ✓ Body includes creator name
- ✓ Body includes concern title
- ✓ Body includes group name
- ✓ Body includes link to concern
- ✓ Footer: "You're receiving this because you're a member of [Group]"

**Test Network-Scoped Email:**
- ✓ Subject: "Network Concern: [Title]"
- ✓ Body includes creator name
- ✓ Body includes originating group
- ✓ Body includes link to concern
- ✓ Footer: "You're receiving this because you're part of the Call5 recruit network"

---

### Test 7: Mobile Responsiveness

**Test on Mobile Device:**
- ✓ Create concern form displays properly
- ✓ Text inputs and textarea are usable
- ✓ Buttons stack vertically on narrow screens
- ✓ Concern view page is readable
- ✓ Modal displays correctly
- ✓ Group concerns list doesn't break layout

---

### Test 8: Edge Cases

**Empty Group:**
- ✓ Group with no members except creator → no emails sent

**Creator Viewing Own Concern:**
- ✓ Sees "Share to Network" button (if group-scoped)
- ✓ Does NOT receive email notification

**Already Promoted:**
- ✓ Clicking promote again → error message
- ✓ Button not visible for network-scoped concerns

**Invalid Group ID:**
- ✓ Accessing /groups/999/concerns/create → error message

**Invalid Concern ID:**
- ✓ Accessing /concerns/999 → error message

---

## Success Metrics

Phase 1 is successful when:

✅ **Database:**
- `concerns` table created with all columns and indexes
- Can create concern records successfully
- Foreign keys enforce data integrity

✅ **Creation:**
- Any group member can create concerns
- Form validation works (required fields)
- Group-scoped concerns created by default

✅ **Viewing:**
- Group members can view group-scoped concerns
- Network members can view network-scoped concerns
- Non-members correctly denied access

✅ **Promotion:**
- Creator can promote group → network
- Promotion is one-way (no demotion)
- Non-creators cannot promote

✅ **Notifications:**
- Group members receive emails for new concerns
- Network members receive emails for promoted concerns
- Email content is clear and actionable

✅ **UI/UX:**
- Forms are mobile-friendly
- Design matches existing Call5 style
- Badge system clearly shows scope
- Navigation flows make sense

✅ **Production:**
- Deployed to Render
- Tested with real test users (Tony, Alex, David, TB Bryan)
- At least 1 concern created and promoted successfully

---

## Future Enhancements (v0.4.08+)

### Comments & Discussion (v0.4.08)
- Add `concern_comments` table
- Thread discussions under each concern
- Email notifications for new comments
- Mention system (@username)

### Actions & Tasks (v0.4.09)
- Add `concern_actions` table
- Link specific action items to concerns
- Track action completion status
- Assign actions to members

### Endorsements (v0.4.10)
- Add `concern_endorsements` table
- Members can endorse concerns
- Show endorsement count
- Sort by endorsements

### Rich Text Editor (v0.4.11)
- Upgrade description textarea to WYSIWYG editor
- Support markdown formatting
- Embed images and links
- Preview mode before posting

### Analytics Dashboard (v0.5)
- Concerns created over time
- Top concern topics (keyword extraction)
- Network propagation visualization
- Member engagement metrics

### Advanced Search & Filter (v0.5)
- Search concerns by keyword
- Filter by scope, group, date range
- Tag system for categorization
- Saved searches

---

## Technical Debt & Considerations

### Database Performance
- **Current:** Basic indexes on group_id, creator_id, scope
- **Future:** If concerns grow to thousands, consider:
  - Full-text search index on title + description
  - Composite indexes for common queries
  - Archival strategy for old concerns

### Email Scalability
- **Current:** Individual emails sent sequentially
- **Future:** If network grows to hundreds:
  - Batch email API calls
  - Queue-based processing
  - Rate limiting per MailGun tier

### Network Member Query
- **Current:** BFS traversal to find network members
- **Optimization:** Cache network membership in database
- **Trade-off:** Complexity vs. performance (current approach works fine for networks < 1000 members)

### Visibility Rules Complexity
- **Current:** Two-tier model (group vs. network)
- **Future:** May need more granular visibility:
  - Specific sub-networks
  - Region-based visibility
  - Issue-based topic groups

---

## Deployment Checklist

**Pre-Deployment:**
- [ ] Database migration tested locally
- [ ] All routes tested with test users
- [ ] Email notifications tested (MailGun sandbox)
- [ ] Mobile responsiveness verified
- [ ] Error handling tested (invalid IDs, permissions)

**Deployment:**
- [ ] Merge PR to main branch
- [ ] Render auto-deploys from GitHub
- [ ] Run database migration on production:
  ```sql
  -- Execute via pgAdmin on Render PostgreSQL
  CREATE TABLE concerns (...);
  CREATE INDEX ...;
  ```
- [ ] Verify table created: `SELECT * FROM concerns LIMIT 1;`

**Post-Deployment:**
- [ ] Test create concern flow with real account
- [ ] Test promotion flow
- [ ] Test email delivery (production MailGun)
- [ ] Test mobile UI on actual phone
- [ ] Monitor logs for errors
- [ ] Update version in footer to "v0.4.07"

**Rollback Plan (if issues):**
- Keep v0.4 branch live in Git
- Drop `concerns` table if major issues
- Revert to previous commit
- Redeploy via Render dashboard

---

## Stakeholder Communication

**For Beta Testers (Alex, David, TB Bryan):**
```
Subject: New Feature: Post Civic Concerns in Your Call5 Groups

Hey everyone,

We've just launched the Concerns feature! Now you can:

1. Post issues you care about to your group
2. Discuss with group members via email notifications
3. Promote concerns to the entire Call5 network when ready

Try it out:
1. Go to your group page (e.g., 54 Ave Group)
2. Click "Post a Concern"
3. Fill in the details
4. Submit and watch the emails fly!

Example: Alex can post about Senator Wyden's Epstein transparency bill,
discuss it with the 54 Ave Group, then share it with the full network
if the group thinks it's important.

This is our first step toward sustained civic engagement beyond just
asking candidates questions. Let me know what you think!

- Tony
```

**For Nextdoor Community:**
```
Subject: Call5 Democracy - New Feature for Community Organizing

Hi neighbors,

I'm excited to share a new feature in Call5 Democracy (the civic
engagement platform some of you tested):

🔔 Concerns Feature

You can now:
- Post civic issues to your group (e.g., local bills, policy changes)
- Collaborate with group members via email
- Amplify important issues to your entire network

Example: If you learn about a bill affecting our neighborhood, post it
to your 54 Ave Group. If it's important, share it with the broader Call5
network (currently 9 members, growing to 125+ soon).

This keeps us engaged between elections, not just during campaign season.

Try it at: https://voter-engagement-app.onrender.com

Feedback welcome!
- Tony
```

---

## Appendix: Database Query Reference

**Get all group-scoped concerns for a group:**
```sql
SELECT * FROM concerns 
WHERE group_id = 1 AND scope = 'group'
ORDER BY created_at DESC;
```

**Get all network-scoped concerns visible to a user:**
```sql
-- Find user's network root
WITH RECURSIVE network_tree AS (
    SELECT id, invited_by_user_id, 0 as level
    FROM users
    WHERE id = 1  -- Your user_id
    
    UNION ALL
    
    SELECT u.id, u.invited_by_user_id, nt.level + 1
    FROM users u
    JOIN network_tree nt ON u.id = nt.invited_by_user_id
    WHERE nt.invited_by_user_id IS NOT NULL
)
SELECT DISTINCT c.*
FROM concerns c
JOIN users u ON c.created_by_user_id = u.id
WHERE c.scope = 'network'
AND u.id IN (SELECT id FROM network_tree)
ORDER BY c.created_at DESC;
```

**Get concern count by group:**
```sql
SELECT g.name, COUNT(c.id) as concern_count
FROM groups g
LEFT JOIN concerns c ON c.group_id = g.id
GROUP BY g.id, g.name
ORDER BY concern_count DESC;
```

**Get concerns created in last 7 days:**
```sql
SELECT * FROM concerns
WHERE created_at > NOW() - INTERVAL '7 days'
ORDER BY created_at DESC;
```

---

## Appendix: MailGun Email Templates

**Group-Scoped Notification (Text):**
```
Subject: New concern in {{ group_name }}: "{{ concern_title }}"

{{ creator_name }} posted a concern in {{ group_name }}:

"{{ concern_title }}"

{{ concern_description_preview }}

View full concern and discuss:
{{ concern_url }}

---
You're receiving this because you're a member of {{ group_name }}.
To stop receiving these notifications, adjust your group settings.
```

**Network Promotion Notification (Text):**
```
Subject: Network Concern: "{{ concern_title }}"

{{ creator_name }} shared a concern with the Call5 network:

"{{ concern_title }}"

{{ concern_description_preview }}

Originally posted in: {{ group_name }}

View full concern:
{{ concern_url }}

---
You're receiving this because you're part of the Call5 recruit network.
To manage your network notifications, visit your dashboard.
```

**Future: HTML Email Templates**
- Rich formatting with gradients matching Call5 brand
- Inline images (Call5 logo)
- Action buttons ("View Concern", "Reply")
- Social sharing buttons (Nextdoor, Twitter, etc.)

---

## End of v0.4.07 Implementation Plan

**Document Version:** 1.0  
**Last Updated:** February 10, 2026  
**Author:** Tony Byorick  
**Implementation Partner:** Claude Code  

**Next Steps:**
1. Review this plan for accuracy and completeness
2. Hand off to Claude Code for implementation
3. Test locally with votereng_dev database
4. Deploy to Render production
5. Beta test with Alex, David, TB Bryan
6. Measure success: Track concern creation rate
7. Plan v0.4.08 based on user feedback
