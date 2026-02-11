# Call5 Democracy v0.4.07 Release Notes

**Release Date:** February 10, 2026
**Release Type:** Feature - Group-Level Civic Issue Tracking
**Status:** Deployed to Production
**Commit:** `110ebdd`

---

## Overview

Version 0.4.07 introduces the **Concerns** feature, enabling Call5 members to log civic issues within their groups and organize collective action. Concerns use a two-tier visibility model: they start group-scoped (safe space for discussion) and can be promoted to network-wide by the creator (enabling exponential awareness spread through the recruit tree).

This feature activates the Groups infrastructure built in earlier versions, giving groups actual utility beyond symbolic membership.

---

## What's New

### 1. Post Concerns to Groups

**Feature:** Any group member can post a civic concern to their group.

Members navigate to a group page and click "Post a Concern" to fill out a title and description. The concern is created as group-scoped by default, visible only to members of that group. Email notifications are sent to all group members (except the creator) via MailGun.

**User Flow:**
1. Navigate to group manage page (`/groups/<id>`)
2. Click "Post a Concern" button in the Group Concerns section
3. Fill in title (max 200 chars) and description
4. Submit → concern logged, group members emailed

---

### 2. View Concern Details

**Feature:** Full concern detail page with metadata and scope badge.

Each concern has a dedicated view page (`/concerns/<id>`) showing the title, full description, creator name, timestamp, originating group, and a scope badge ("Group Only" or "Network-Wide"). Visibility is enforced: group-scoped concerns require group membership, network-scoped concerns require network membership.

---

### 3. Share to Network (Promote Concern)

**Feature:** Concern creators can promote a group concern to network-wide visibility.

Only the creator sees the "Share to Network" button. Clicking it opens a confirmation modal. Once confirmed, the concern scope changes from `group` to `network`, and email notifications are sent to all recruit network members who are NOT already in the originating group (avoiding duplicate emails). Promotion is one-way and cannot be undone.

**User Flow:**
1. Creator views their group-scoped concern
2. Clicks "Share to Network" button
3. Confirmation modal: "This will notify all members in your Call5 recruit network. This action cannot be undone."
4. Confirms → scope updated, network members emailed
5. Button replaced with "Network-Wide" badge

---

### 4. Concerns Section on Group Page

**Feature:** Group manage page now displays a concerns list.

The group manage page (`/groups/<id>`) includes a "Group Concerns" section showing all concerns posted to that group in reverse chronological order. Each concern card shows title (clickable link), scope badge (if network-wide), creator name, date, and a 200-character description preview.

---

## Technical Changes

### Database

**New Table: `concerns`**

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL PK | Primary key |
| `title` | VARCHAR(200) | Concern headline |
| `description` | TEXT | Full explanation |
| `created_by_user_id` | INTEGER FK → users.id | Creator |
| `group_id` | INTEGER FK → groups.id | Home group |
| `scope` | VARCHAR(20) | `'group'` (default) or `'network'` |
| `created_at` | TIMESTAMP | When posted |
| `updated_at` | TIMESTAMP | Last modification |

Table auto-created via `db.create_all()` on app startup.

### Files Modified

**Backend (`votereng.py`):**
- Added `Concern` model (before `db.create_all()`)
- Added `get_network_members(user_id)` — BFS traversal to find all users in the same recruit tree
- Added `send_concern_notification()` — MailGun email for group and network notifications
- Added 4 routes:
  - `GET /groups/<id>/concerns/create` — show creation form
  - `POST /groups/<id>/concerns/create` — handle submission + email group members
  - `POST /concerns/<id>/promote` — change scope to network + email network members
  - `GET /concerns/<id>` — view concern with visibility enforcement
- Updated `group_manage` route to pass `is_member=True` to template

**New Templates:**
- `templates/concern_create.html` — form with title + description, breadcrumb navigation
- `templates/concern_view.html` — full concern detail with "Share to Network" modal

**Modified Templates:**
- `templates/group_manage.html` — added concerns section CSS + HTML, updated footer to v0.4.07

### Key Implementation Details

**MailGun pattern:** Uses existing codebase pattern with `os.getenv()` local vars:
```python
mailgun_api_key = os.getenv("MAILGUN_API_KEY")
mailgun_domain = os.getenv("MAILGUN_DOMAIN")
mailgun_base_url = os.getenv("MAILGUN_BASE_URL", "https://api.mailgun.net")
```

**Network traversal:** `get_network_members()` finds the root ancestor (user with `invited_by_user_id = NULL`), then BFS traversal to collect all descendants. Returns list of User objects.

**Email deduplication:** When promoting to network, group members (already notified) are excluded from the network email list.

**Visibility enforcement:**
- Group-scoped: requires `GroupMember` record for the requesting user
- Network-scoped: requires requesting user to be in the same recruit network as the concern creator

---

## Business Rules

1. **Any group member** can create concerns in that group
2. **Only the creator** can promote a concern from group to network
3. **Promotion is one-way** — cannot demote back to group
4. **Group-scoped email:** sent to all group members except creator
5. **Network-scoped email:** sent to all network members NOT already in the originating group
6. **Scope badge:** "Group Only" (blue) or "Network-Wide" (green)

---

## Design Decisions

- **Styling matches existing codebase:** Blue gradient theme (`#2c5aa0` / `#1e3a66`), consistent with dashboard and group pages
- **No emoji in buttons** (per codebase convention, spec had emoji which was removed)
- **Flash messages** used for success/error feedback (consistent with existing patterns)
- **Modal confirmation** for network promotion to prevent accidental mass emails

---

## Version History Context

| Version | Feature |
|---------|---------|
| v0.4.05 | Network Visualization (vis.js interactive graph) |
| v0.4.05a | Left-to-right layout, group labels/colors |
| v0.4.05b | White background fix for PNG export |
| v0.4.06 | Load Template, privacy headers, admin-only Admin button |
| v0.4.07 (broadcast) | Broadcast to All Members (super-admin email whitelist) |
| **v0.4.07 (concerns)** | **Group-Level Civic Issue Tracking (this release)** |

---

## Future Enhancements

- **v0.4.08:** Comments & Discussion (threaded comments under concerns)
- **v0.4.09:** Actions & Tasks (action items linked to concerns)
- **v0.4.10:** Endorsements (members can endorse concerns, sort by count)
- **v0.4.11:** Rich Text Editor (markdown/WYSIWYG for descriptions)
- **v0.5:** Dashboard integration (network-wide concerns visible on dashboard)

---

**Deployed By:** Tony Byorick
**Implementation:** Claude Code (Claude Opus 4.6)
**Deployment Target:** voter-engagement-app.onrender.com
**Environment:** Flask + PostgreSQL + Render + MailGun

---

_Call5 Democracy - Sustaining civic engagement beyond election day_

**Version:** 0.4.07
**Build Date:** February 10, 2026
**Platform:** Flask + PostgreSQL + Render
