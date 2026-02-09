# Call5 Democracy v0.4.06 Release Notes

**Release Date:** February 9, 2026
**Release Type:** UX & Security Improvements
**Status:** Ready for Deployment

---

## Overview

Version 0.4.06 introduces user experience enhancements and security improvements focused on streamlining the invitation workflow and protecting user privacy. This release refines the share page interaction model and implements role-based UI controls for administrative functions.

---

## What's New

### 1. One-Click Email Template Loading

**Feature:** Load Template button on Share page

Users can now load the email invitation template directly into the personal message field with a single click, eliminating the need for manual copy-paste operations.

**Benefits:**
- Reduces friction in the invitation workflow
- Improves mobile user experience (no clipboard gymnastics)
- Maintains full editing capability after template load
- Provides clear visual feedback ("✓ Loaded" confirmation)

**User Impact:** Faster, smoother invitation sending process

---

### 2. Privacy-Enhanced Headers

**Feature:** Display user names instead of email addresses in page headers

Dashboard and Share pages now display the user's name in the authentication section rather than their email address.

**Benefits:**
- Reduces privacy exposure when sharing screen or looking over shoulder
- Cleaner, more personal interface
- User still sees their identity clearly confirmed

**User Impact:** Better privacy protection without sacrificing usability

---

### 3. Role-Based Admin Access Control

**Feature:** Admin button conditionally rendered based on user role

The Admin button on the dashboard now only appears for users with admin privileges (`is_admin=True` in database). The Tree button remains visible to all authenticated users.

**Benefits:**
- Cleaner interface for regular users
- Prevents confusion about unavailable features
- Implements proper UI-level authorization
- Complements existing backend security checks

**User Impact:**
- **Admins:** No change - full access maintained
- **Regular users:** Simplified dashboard, Admin button hidden; Tree remains accessible

---

## Technical Changes

### Files Modified

**Frontend:**
- `templates/share.html` - Added Load Template button and JavaScript handler
- `templates/dashboard.html` - Implemented admin conditional, name display

**Backend:**
- `votereng.py` - Enhanced dashboard and share routes with template variables

### Code Additions

**New CSS Classes:**
- `.load-template-btn` - Styled button for template loading
- `.load-template-btn.loaded` - Success state styling
- Mobile responsive breakpoints for template button

**New JavaScript Functions:**
- `loadEmailTemplate()` - Handles template loading and user feedback

**New Template Variables:**
- `is_admin` - Boolean flag for admin privilege checks
- `user_name` - User's display name for headers

### Database Schema

**No database changes required** - Uses existing `is_admin` column in `users` table

---

## Security Improvements

1. **Authorization Enforcement:** Admin UI button hidden from unauthorized users
2. **Privacy Protection:** Email addresses removed from page headers
3. **Principle of Least Privilege:** Users only see admin functions they can access

**Note:** Backend authorization checks remain in place as primary security mechanism

---

## Mobile Responsiveness

All new features are fully mobile-responsive:
- Load Template button stacks vertically on screens < 480px
- Button expands to full width on mobile for easy tapping
- All styling adapts to small screens without horizontal scrolling

---

## Testing Checklist

### Functional Testing
- [x] Load template button appears on share page
- [x] Template loads correctly (subject line and opening paragraph removed)
- [x] Visual feedback ("✓ Loaded") displays for 2 seconds
- [x] Loaded template is editable
- [x] Cursor positioned at end of loaded text

### Security Testing
- [x] Admin button visible for admin users
- [x] Admin button hidden for non-admin users
- [x] Tree button visible to all authenticated users
- [x] Backend routes still enforce authorization

### Privacy Testing
- [x] Dashboard shows user name, not email
- [x] Share page shows user name, not email
- [x] Admin page still shows emails (appropriate for admin context)

### Mobile Testing
- [x] Load template button responsive on mobile
- [x] All pages render correctly on small screens
- [x] Touch targets appropriately sized

---

## Deployment Notes

### Pre-Deployment Checklist

1. **Backup database** (PostgreSQL on Render)
2. **Test on local environment** with both admin and non-admin accounts
3. **Review Git commit** for completeness
4. **Verify no hardcoded credentials** in modified files

### Deployment Steps

1. Push changes to GitHub repository
2. Render auto-deploys from main branch
3. Monitor deployment logs for errors
4. Test production environment:
   - Log in as admin → verify Admin button visible
   - Log in as regular user → verify Admin button hidden, Tree still visible
   - Test share page template loading
   - Verify mobile responsiveness

### Rollback Plan

If issues arise:
1. Revert Git commit: `git revert HEAD`
2. Push to main branch
3. Render auto-deploys previous version
4. Database unaffected (no schema changes)

---

## Known Issues

**None identified** - This release contains isolated UI/UX improvements with no known breaking changes.

---

## Browser Compatibility

Tested and verified on:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (iOS and macOS)
- Mobile browsers (iOS Safari, Chrome Mobile)

**Minimum Requirements:**
- JavaScript enabled
- CSS3 support
- Clipboard API support (graceful degradation for older browsers)

---

## Version History Context

**Previous Version:** v0.4.05 - Network Visualization (Interactive tree graph with vis.js)

**Current Version:** v0.4.06 - UX & Security Improvements

**Next Planned:** v0.4.07+ (TBD based on user feedback)

---

## Metrics to Monitor Post-Release

1. **Invitation Engagement:**
   - % of users who use Load Template button
   - Time spent on share page (should decrease)
   - Email invitation send rate

2. **User Feedback:**
   - Questions about admin access (should decrease)
   - Privacy-related concerns (should decrease)

3. **Technical Metrics:**
   - JavaScript errors (should remain zero)
   - Mobile vs desktop usage patterns
   - Page load times (should be unaffected)

---

## Credits

**Development:** Claude Code implementation
**Design & Specification:** Tony Byorick, Claude AI
**Testing:** Call5 Development Team
**User Feedback:** Nextdoor Responsible AI group, early beta testers

---

## Support & Feedback

**Issues:** Report via GitHub Issues or contact tony.byorick@gmail.com
**Feature Requests:** Nextdoor Responsible AI group discussions
**Documentation:** See `/docs` folder for updated UI documentation

---

## Stakeholder Summary

**For Non-Technical Stakeholders:**

This release makes two important improvements:

1. **Easier Invitations:** Users can now share Call5 Democracy with friends in one click instead of copying and pasting text
2. **Better Privacy:** Email addresses are no longer displayed on screen, and admin controls are only shown to authorized people

**Impact:** Smoother user experience, better privacy protection, cleaner interface

**Risk Level:** Low - These are interface improvements only, no database changes

---

**Release Approved By:** Tony Byorick
**Deployment Target:** voter-engagement-app.onrender.com
**Environment:** Production (PostgreSQL, MailGun, OpenAI GPT-4o-mini)

---

_Call5 Democracy - Sustaining civic engagement beyond election day_

**Version:** 0.4.06
**Build Date:** February 9, 2026
**Platform:** Flask + PostgreSQL + Render
