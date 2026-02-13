# Call5 Democracy v0.4.07b

**Rich Text Editor for Concerns**

February 11, 2026

---

## Overview

Add WYSIWYG (What You See Is What You Get) rich text editing to the Concerns feature, allowing users to format civic issues with bold, italics, bullet points, hyperlinks, and structured content. This makes Concerns more professional, easier to read, and better suited for detailed policy proposals with supporting documentation.

**Key Principle:** User-friendly formatting without requiring technical knowledge. Users get a toolbar with formatting buttons and see results immediately.

---

## Why Rich Text Matters for Civic Concerns

Plain text limitations hurt civic engagement:
- **No emphasis** - Can't highlight key points or urgent issues
- **No structure** - Long descriptions become walls of text
- **No links** - Can't cite sources, news articles, or supporting documents
- **No lists** - Proposals with action items are hard to follow
- **Unprofessional** - Plain text looks less credible

Rich text solves these:
- **Format for clarity** - Bold headers, bullet points, emphasis
- **Cite sources** - Link to news articles, government documents, research
- **Professional appearance** - Looks like serious policy proposals
- **Better engagement** - Easier to read = more people actually read it
- **Action-oriented** - Numbered lists for specific demands/proposals

---

## Editor Choice: Quill

**Selected Editor:** [Quill](https://quilljs.com/)

**Why Quill?**
- **Lightweight** - ~43KB minified, fast load times
- **Mobile-friendly** - Touch-optimized, works great on phones
- **Modern** - Clean design, good UX
- **Flexible** - Easy to customize toolbar
- **Active development** - Well-maintained, good documentation
- **MIT License** - Free for commercial use
- **Delta format** - Stores rich content as structured data (can convert to HTML)

**Alternatives Considered:**
- **TinyMCE** - More features but heavier (400KB+), complex mobile UX
- **CKEditor** - Very powerful but overkill for our needs
- **Trix** - Simpler but less flexible toolbar customization

---

## Features Included

### Toolbar Buttons

**Text Formatting:**
- Bold
- Italic
- Underline
- Strike-through

**Structure:**
- Heading 2 (for section titles)
- Heading 3 (for sub-sections)
- Bullet list
- Numbered list

**Content:**
- Hyperlink (with URL input dialog)
- Blockquote (for citing sources)

**NOT Included (to keep it simple):**
- Font selection (use default)
- Font size (use default + headings)
- Colors (maintain consistent design)
- Images (future enhancement)
- Tables (future enhancement)
- Code blocks (not needed for civic content)

### Mobile Optimization

- Touch-friendly toolbar buttons (larger tap targets)
- Toolbar stays accessible (sticky or scrolls into view)
- Link dialog works on mobile keyboards
- Copy/paste from mobile browsers

---

## Technical Implementation

### Frontend Changes

**CDN Includes (in `<head>`):**
```html
<!-- Quill CSS -->
<link href="https://cdn.quilljs.com/1.3.7/quill.snow.css" rel="stylesheet">

<!-- Quill JS -->
<script src="https://cdn.quilljs.com/1.3.7/quill.js"></script>
```

**Editor Initialization (in template):**
```html
<div id="editor-container"></div>

<script>
var quill = new Quill('#editor-container', {
  theme: 'snow',
  modules: {
    toolbar: [
      ['bold', 'italic', 'underline', 'strike'],
      [{ 'header': 2 }, { 'header': 3 }],
      [{ 'list': 'ordered'}, { 'list': 'bullet' }],
      ['link', 'blockquote'],
      ['clean']
    ]
  },
  placeholder: 'Describe the civic issue and your proposed solution...'
});
</script>
```

**Form Submission:**
```html
<form method="POST" onsubmit="return submitForm()">
  <input type="hidden" name="description" id="description-input">
  <!-- other form fields -->
  <button type="submit">Post Concern</button>
</form>

<script>
function submitForm() {
  // Get HTML from Quill and put in hidden input
  var html = quill.root.innerHTML;
  document.getElementById('description-input').value = html;
  return true;
}
</script>
```

### Backend Changes

**Storage:**
- Store HTML in `concerns.description` column (TEXT type, already exists)
- No schema changes needed

**Sanitization (CRITICAL for security):**
```python
from markupsafe import Markup
import bleach

ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 's',  # Basic formatting
    'h2', 'h3',                             # Headers
    'ul', 'ol', 'li',                       # Lists
    'a', 'blockquote'                       # Links and quotes
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'target', 'rel'],
    '*': []  # No attributes for other tags
}

def sanitize_html(html):
    """Clean user HTML to prevent XSS attacks"""
    # Remove dangerous tags and attributes
    clean = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )
    # Force external links to open in new tab with security
    clean = bleach.linkify(
        clean,
        callbacks=[lambda attrs, new=False: attrs.update({'target': '_blank', 'rel': 'noopener noreferrer'}) or attrs]
    )
    return clean
```

**Route Changes (`votereng.py`):**
```python
@app.route("/groups/<int:group_id>/concerns/create", methods=["POST"])
def create_concern(group_id):
    # ... existing auth/validation ...
    
    title = request.form.get("title")
    description_raw = request.form.get("description")
    
    # SANITIZE HTML BEFORE STORING
    description = sanitize_html(description_raw)
    
    concern = Concern(
        title=title,
        description=description,  # HTML stored here
        # ... rest of fields ...
    )
    # ... save to database ...
```

**Display (in templates):**
```html
<!-- Raw HTML would be escaped by Jinja2 by default -->
<!-- Use |safe filter to render HTML (ONLY after sanitization!) -->
<div class="concern-description">
    {{ concern.description|safe }}
</div>
```

### CSS Styling

**Rendered Content Styling:**
```css
/* Style the rendered HTML output */
.concern-description {
    line-height: 1.6;
    color: #333;
}

.concern-description h2 {
    font-size: 1.4em;
    font-weight: bold;
    margin-top: 1.2em;
    margin-bottom: 0.5em;
    color: #2c5aa0;
}

.concern-description h3 {
    font-size: 1.2em;
    font-weight: bold;
    margin-top: 1em;
    margin-bottom: 0.5em;
    color: #2c5aa0;
}

.concern-description ul, .concern-description ol {
    margin-left: 2em;
    margin-bottom: 1em;
}

.concern-description li {
    margin-bottom: 0.5em;
}

.concern-description a {
    color: #2c5aa0;
    text-decoration: underline;
}

.concern-description a:hover {
    color: #1e3a66;
}

.concern-description blockquote {
    border-left: 4px solid #2c5aa0;
    padding-left: 1em;
    margin-left: 0;
    font-style: italic;
    color: #555;
}

.concern-description strong {
    font-weight: bold;
}

.concern-description em {
    font-style: italic;
}
```

---

## Security Considerations

### XSS Prevention (Cross-Site Scripting)

**The Danger:**
Users could inject malicious JavaScript if HTML isn't sanitized:
```html
<script>alert('hacked!');</script>
<img src=x onerror="maliciousCode()">
```

**Our Protection:**
1. **Bleach Library** - Whitelist-based HTML sanitizer
2. **Allowed Tags Only** - Only safe formatting tags permitted
3. **Attribute Restrictions** - Only safe attributes (href for links)
4. **Link Security** - External links get `rel="noopener noreferrer"`
5. **Server-Side Only** - Sanitization happens in Python, can't be bypassed

**Requirements:**
```bash
pip install bleach --break-system-packages
```

**Update requirements.txt:**
```
bleach==6.1.0
```

### Content Security Policy

Consider adding CSP headers (future enhancement):
```python
@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "script-src 'self' cdn.quilljs.com"
    return response
```

---

## Where Rich Text Applies

### Concern Creation (`/groups/<id>/concerns/create`)
- Replace `<textarea>` with Quill editor
- Users compose concerns with formatting
- Hidden input captures HTML on submit

### Concern Viewing (`/concerns/<id>`)
- Display sanitized HTML with proper styling
- Links open in new tabs
- Formatted content renders correctly

### All Concerns Page (`/concerns/all`)
- **Preview only** (first 200 characters)
- Strip HTML tags for preview: `description[:200]`
- Full formatted version on detail page

### Group Concerns Section (`/groups/<id>`)
- **Preview only** (first 200 characters)
- Strip HTML for preview
- Full formatted version on detail page

**Why Plain Text Previews?**
- Keeps card layouts clean and predictable
- Prevents formatting from breaking card design
- Users click through for full formatted content
- Standard pattern (email previews, article cards, etc.)

---

## Implementation Steps

### Step 1: Install Dependencies
```bash
pip install bleach --break-system-packages
```

Update `requirements.txt`:
```
bleach==6.1.0
```

### Step 2: Add Sanitization Function
**File:** `votereng.py`

Add imports:
```python
import bleach
```

Add sanitization function (near top of file):
```python
ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'u', 's', 'h2', 'h3', 
                'ul', 'ol', 'li', 'a', 'blockquote']
ALLOWED_ATTRIBUTES = {'a': ['href', 'target', 'rel'], '*': []}

def sanitize_html(html):
    clean = bleach.clean(html, tags=ALLOWED_TAGS, 
                        attributes=ALLOWED_ATTRIBUTES, strip=True)
    clean = bleach.linkify(clean, callbacks=[
        lambda attrs, new=False: attrs.update({
            'target': '_blank', 
            'rel': 'noopener noreferrer'
        }) or attrs
    ])
    return clean
```

### Step 3: Update Concern Creation Route
**File:** `votereng.py`

Modify `/groups/<int:group_id>/concerns/create` POST handler:
```python
description_raw = request.form.get("description")
description = sanitize_html(description_raw)  # ADD THIS LINE
```

### Step 4: Update Concern Creation Template
**File:** `templates/concern_create.html`

Replace textarea with Quill:

**Current:**
```html
<textarea name="description" required></textarea>
```

**New:**
```html
<!-- Quill CDN -->
<link href="https://cdn.quilljs.com/1.3.7/quill.snow.css" rel="stylesheet">
<script src="https://cdn.quilljs.com/1.3.7/quill.js"></script>

<!-- Editor container -->
<div id="editor-container" style="height: 300px;"></div>
<input type="hidden" name="description" id="description-input">

<!-- Initialize editor -->
<script>
var quill = new Quill('#editor-container', {
  theme: 'snow',
  modules: {
    toolbar: [
      ['bold', 'italic', 'underline', 'strike'],
      [{ 'header': 2 }, { 'header': 3 }],
      [{ 'list': 'ordered'}, { 'list': 'bullet' }],
      ['link', 'blockquote'],
      ['clean']
    ]
  },
  placeholder: 'Describe the civic issue and your proposed solution...'
});

// Capture HTML on form submit
document.querySelector('form').onsubmit = function() {
  document.getElementById('description-input').value = quill.root.innerHTML;
  return true;
};
</script>
```

### Step 5: Update Concern View Template
**File:** `templates/concern_view.html`

Display formatted HTML:

**Current:**
```html
<p>{{ concern.description }}</p>
```

**New:**
```html
<div class="concern-description">
    {{ concern.description|safe }}
</div>

<style>
.concern-description {
    line-height: 1.6;
    color: #333;
}
.concern-description h2 {
    font-size: 1.4em;
    font-weight: bold;
    margin-top: 1.2em;
    margin-bottom: 0.5em;
    color: #2c5aa0;
}
/* ... rest of CSS from above ... */
</style>
```

### Step 6: Update Preview Displays
**Files:** `templates/concerns_all.html`, `templates/group_manage.html`

Strip HTML for previews:

**In Python (route):**
```python
# For each concern, create plain text preview
import re

def strip_html(html):
    return re.sub('<[^<]+?>', '', html)

# In route:
concerns_with_preview = []
for concern in concerns:
    preview = strip_html(concern.description)[:200]
    concerns_with_preview.append({
        'concern': concern,
        'preview': preview
    })
```

**Or in Jinja2 template:**
```html
<!-- Simple version: just truncate (HTML tags will show) -->
{{ concern.description[:200]|striptags }}...

<!-- Better version: strip then truncate -->
{{ concern.description|striptags|truncate(200) }}
```

### Step 7: Update Footer Versions
**Files:** Various templates

Update version string from v0.4.07a to v0.4.07b

### Step 8: Deploy to Render
1. Commit changes to GitHub
2. Push to main branch
3. Render auto-deploys
4. Verify on production

---

## Testing Plan

### Editor Functionality Tests

**Test 1: Basic Formatting**
- Create new concern
- Type text and apply bold, italic, underline
- Submit and view
- Verify formatting displays correctly

**Test 2: Headers**
- Use H2 and H3 headers in concern
- Submit and view
- Verify headers render with correct styling

**Test 3: Lists**
- Create bullet list
- Create numbered list
- Submit and view
- Verify lists display correctly

**Test 4: Hyperlinks**
- Add link to external site (e.g., news article)
- Submit and view
- Click link - should open in new tab
- Verify `rel="noopener noreferrer"` in HTML

**Test 5: Blockquotes**
- Add blockquote with source citation
- Submit and view
- Verify blockquote styling (left border, indented)

**Test 6: Mixed Formatting**
- Create concern with:
  - H2 header
  - Paragraph with **bold** and *italic*
  - Bullet list
  - External link
  - Blockquote
- Submit and view
- Verify all formatting preserved and styled

### Security Tests

**Test 7: XSS Prevention - Script Tag**
- Try to inject `<script>alert('XSS')</script>` in description
- Submit
- Verify script tag stripped (doesn't execute or display)

**Test 8: XSS Prevention - Event Handler**
- Try to inject `<img src=x onerror="alert('XSS')">`
- Submit
- Verify event handler stripped

**Test 9: XSS Prevention - JavaScript URL**
- Try to create link with `href="javascript:alert('XSS')"`
- Submit
- Verify malicious URL sanitized

**Test 10: Allowed Tags Only**
- Try to use `<table>`, `<div>`, `<span>` (not in whitelist)
- Submit
- Verify unsupported tags stripped but content preserved

### Preview Tests

**Test 11: All Concerns Preview**
- View `/concerns/all`
- Verify HTML tags don't show in preview
- Verify preview is plain text (200 chars)
- Click concern title
- Verify full formatted version displays

**Test 12: Group Concerns Preview**
- View group page
- Verify HTML tags don't show in concern cards
- Click concern
- Verify full formatted version displays

### Mobile Tests

**Test 13: Mobile Editor**
- Open concern creation on mobile device
- Verify toolbar accessible
- Tap formatting buttons
- Type with mobile keyboard
- Submit
- Verify formatting preserved

**Test 14: Mobile Viewing**
- View formatted concern on mobile
- Verify content readable
- Verify links tappable
- Verify no horizontal scrolling

### Edge Cases

**Test 15: Empty Formatting**
- Create concern with no formatting (plain text only)
- Submit
- Verify displays normally (no errors)

**Test 16: Very Long Content**
- Create concern with 2000+ words and heavy formatting
- Submit
- Verify page loads without issues
- Verify scrolling works

**Test 17: Special Characters**
- Use emojis, accented characters, symbols
- Apply formatting
- Submit
- Verify special characters preserved

---

## User Documentation

### Help Text for Users

**On Concern Creation Page:**
```
Formatting Tips:
• Use Bold for key points
• Add links to news articles or sources
• Use bullet points for proposals
• Keep it clear and professional
```

### Example Formatted Concern (for docs)

**Title:** Increase Funding for Community Gardens

**Description:**
```
## The Problem
Our neighborhood has only 2 community garden plots for 500+ families. 
According to a [recent study](https://example.com/study), community gardens:
• Reduce food insecurity
• Build community connections  
• Provide fresh produce access

## Our Proposal
We request $15,000 in funding to:
1. Expand the Oak Street garden by 50%
2. Add water infrastructure
3. Create 20 new garden plots

> "Community gardens are essential for food justice" - Local Food Bank Director

**Help us build a healthier neighborhood!**
```

---

## Design Decisions

### Why Quill Over TinyMCE?
- **Size:** Quill is 10x smaller (faster load)
- **Mobile:** Quill works great on touch devices
- **Modern:** Clean, minimal design fits Call5
- **Sufficient:** We don't need TinyMCE's advanced features

### Why Limited Toolbar?
- **Simplicity:** Too many options overwhelm users
- **Consistency:** Limited formatting = consistent design
- **Focus:** Users focus on content, not fonts/colors
- **Mobile:** Fewer buttons = usable on small screens

### Why No Images (Yet)?
- **Complexity:** Image upload requires file storage
- **Cost:** Image hosting (S3, etc.) adds expense
- **Focus:** Text-first keeps concerns scannable
- **Future:** Can add in v0.4.08+ with proper infrastructure

### Why Server-Side Sanitization?
- **Security:** Client-side can be bypassed
- **Guarantee:** Server always validates
- **Consistency:** One source of truth
- **Defense in Depth:** Multiple layers of protection

---

## Future Enhancements (v0.4.08+)

**Image Support:**
- Upload images to S3 or similar
- Embed in concerns
- Alt text for accessibility

**Video Embeds:**
- Support YouTube, Vimeo embeds
- Useful for protests, council meetings, etc.

**Tables:**
- Useful for budget proposals
- Comparison charts

**Mentions:**
- @mention other users
- Notify when mentioned

**Version History:**
- Track concern edits
- Show edit history
- "Last edited" timestamp

**Templates:**
- Pre-formatted templates for common concerns
- "Budget Request", "Policy Proposal", etc.

---

## Success Criteria

v0.4.07b is complete when:

✓ Quill editor loads on concern creation page  
✓ Toolbar with formatting buttons displays  
✓ Users can format text (bold, italic, etc.)  
✓ Users can add headers (H2, H3)  
✓ Users can create lists (bullet, numbered)  
✓ Users can add hyperlinks  
✓ Users can add blockquotes  
✓ Formatted concerns display correctly  
✓ HTML sanitization prevents XSS attacks  
✓ External links open in new tabs with security attributes  
✓ Previews show plain text (no HTML tags visible)  
✓ Mobile editor works on touch devices  
✓ Mobile formatted view is readable  
✓ bleach dependency added to requirements.txt  
✓ Version updated to v0.4.07b  
✓ Changes deployed to production (Render)

---

## Files to Modify

1. **`requirements.txt`** - Add bleach dependency
2. **`votereng.py`** - Add sanitize_html() function, modify POST route
3. **`templates/concern_create.html`** - Replace textarea with Quill editor
4. **`templates/concern_view.html`** - Display sanitized HTML with styling
5. **`templates/concerns_all.html`** - Strip HTML for previews
6. **`templates/group_manage.html`** - Strip HTML for previews, update footer

---

## Dependencies

**New Python Package:**
```
bleach==6.1.0
```

**CDN Resources (no install needed):**
- Quill CSS: https://cdn.quilljs.com/1.3.7/quill.snow.css
- Quill JS: https://cdn.quilljs.com/1.3.7/quill.js

---

**Deployment Target:** voter-engagement-app.onrender.com  
**Implementation Partner:** Claude Code  
**Version:** v0.4.07b  
**Build Date:** February 11, 2026  
**Platform:** Flask + PostgreSQL + Render + MailGun + Quill

---

_Call5 Democracy - Sustaining civic engagement beyond election day_
