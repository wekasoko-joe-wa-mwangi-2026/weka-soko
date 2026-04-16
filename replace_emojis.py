#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Replace emoji characters in JSX files with inline SVG icons."""

import sys

# ── SVG BUILDERS ──────────────────────────────────────────────────────────────
# Returns JSX-compatible SVG strings (using {{}} for JSX style object syntax)

def s_check(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><polyline points="20 6 9 17 4 12"/></svg>'

def s_x(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>'

def s_warn(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'

def s_party(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'

def s_fire(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M12 2c0 0-5 4-5 9a5 5 0 0 0 10 0c0-5-5-9-5-9z"/><path d="M12 12c0 0-2 1.5-2 3a2 2 0 0 0 4 0c0-1.5-2-3-2-3z"/></svg>'

def s_lock(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>'

def s_unlock(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/></svg>'

def s_creditcard(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>'

def s_ban(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/></svg>'

def s_email(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>'

def s_star_filled(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" strokeWidth="1" style={{{{display:"inline",verticalAlign:"middle"}}}}><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'

def s_box(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>'

def s_cart(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>'

def s_tag(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>'

def s_bag(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>'

def s_inbox(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>'

def s_flag(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/></svg>'

def s_pin(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'

def s_eye(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>'

def s_bell(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>'

def s_phone(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>'

def s_user(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'

def s_chat(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'

def s_shield(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'

def s_trophy(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><polyline points="8 21 12 17 16 21"/><line x1="12" y1="17" x2="12" y2="11"/><path d="M7 4H4a2 2 0 0 0-2 2v1a5 5 0 0 0 5 5"/><path d="M17 4h3a2 2 0 0 1 2 2v1a5 5 0 0 1-5 5"/><rect x="7" y="2" width="10" height="10" rx="1"/></svg>'

def s_door(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>'

def s_trash(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>'

def s_edit(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>'

def s_gift(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><polyline points="20 12 20 22 4 22 4 12"/><rect x="2" y="7" width="20" height="5"/><line x1="12" y1="22" x2="12" y2="7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/></svg>'

def s_search(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'

def s_doc(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'

def s_heart(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>'

def s_globe(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{{{display:"inline",verticalAlign:"middle"}}}}><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>'

def s_clock(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'

def s_cal(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'

def s_dollar(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>'

def s_lightning(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'

def s_info(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>'

def s_refresh(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>'

def s_handshake(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'

def s_settings(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>'

# ── REPLACEMENT RULES ──────────────────────────────────────────────────────────
# Ordered by most specific/context first; use exact emoji characters as keys.
# Each value is a callable or string giving the JSX SVG replacement.

# Emojis and their context-appropriate replacements
# Format: list of (emoji_char, replacement_string) pairs
# For emojis used at specific sizes in certain contexts, we do context-aware replacements

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_len = len(content)

    # ── CONTEXT-SPECIFIC REPLACEMENTS (order matters) ──────────────────────────

    # Notification type icons in the object literal (large block replacements)
    # Line 2594 / 2930 in all.jsx — emoji icon map for notification types
    content = content.replace(
        '{new_message:"\U0001f4ac",buyer_locked_in:"\U0001f525",escrow_released:"\U0001f4b0",payment_confirmed:"\u2705",warning:"\u26a0\ufe0f",admin_edit:"\U0001f6e0",suspension:"\U0001f6ab",seller_pitch:"\U0001f4ec",pitch_accepted:"\u2705",request_match:"\U0001f6d2",listing_match:"\U0001f3f7\ufe0f",listing_approved:"\u2705"}',
        '{new_message:"chat",buyer_locked_in:"fire",escrow_released:"money",payment_confirmed:"check",warning:"warn",admin_edit:"settings",suspension:"ban",seller_pitch:"inbox",pitch_accepted:"check",request_match:"cart",listing_match:"tag",listing_approved:"check"}'
    )

    # ── FACE EMOJIS (rating labels in LeaveReviewBtn) ─────────────────────────
    content = content.replace(
        '["","\U0001f61e Poor","\U0001f610 Fair","\U0001f642 Good","\U0001f60a Very Good","\U0001f929 Excellent"]',
        '["","Poor","Fair","Good","Very Good","Excellent"]'
    )

    # ── SPECIFIC STRING REPLACEMENTS (with context) ───────────────────────────

    # "🎉 " welcome messages
    content = content.replace('! \U0001f389 Check your email', '! Check your email')
    content = content.replace('! \U0001f389"', '!"')
    content = content.replace('"Welcome back, "+parsed.name.split(" ")[0]+"! \U0001f389"', '"Welcome back, "+parsed.name.split(" ")[0]+"!"')
    content = content.replace('`Welcome to Weka Soko, ${data.user.name?.split(" ")[0]||""}! \U0001f389 Check your email', '`Welcome to Weka Soko, ${data.user.name?.split(" ")[0]||""}! Check your email')
    content = content.replace('`Welcome back, ${data.user.name?.split(" ")[0]||""}! \U0001f389`', '`Welcome back, ${data.user.name?.split(" ")[0]||""}!`')

    # Notification messages with emojis in strings
    content = content.replace('"Your ad is now live on Weka Soko! "', '"Your ad is now live on Weka Soko! "')
    content = content.replace('notify("\U0001f389 Your ad is now live', 'notify("Your ad is now live')
    content = content.replace('"Email verified! Welcome to Weka Soko.","success"', '"Email verified! Welcome to Weka Soko.","success"')
    content = content.replace('notify("\u2705 Email verified! Welcome to Weka Soko."', 'notify("Email verified! Welcome to Weka Soko."')
    content = content.replace('notify("\u2705 Email verified! You can now sign in."', 'notify("Email verified! You can now sign in."')

    # Suspension notice
    content = content.replace('notify("\u26d4 Your account has been suspended. You will be logged out.","error")', 'notify("Your account has been suspended. You will be logged out.","error")')
    content = content.replace('notify("\U0001f6ab Your account has been suspended. Check your email.","error")', 'notify("Your account has been suspended. Check your email.","error")')

    # Admin edit info message
    content = content.replace('notify("\u2139\ufe0f Admin has updated your listing: "', 'notify("Admin has updated your listing: "')
    content = content.replace('notify("Admin has updated your listing: "+(n.body||""),"info")', 'notify("Admin has updated your listing: "+(n.body||""),"info")')

    # Lock-in / payment success messages
    content = content.replace('notify("\U0001f525 Locked in! The seller has been notified.","success")', 'notify("Locked in! The seller has been notified.","success")')
    content = content.replace('notify("\U0001f553 Contact details revealed!","success")', 'notify("Contact details revealed!","success")')
    content = content.replace('notify("\U0001f513 Contact details revealed!","success")', 'notify("Contact details revealed!","success")')
    content = content.replace('notify("\U0001f513 Buyer contact revealed!","success")', 'notify("Buyer contact revealed!","success")')
    content = content.replace('notify("\U0001f510 Escrow activated!","success")', 'notify("Escrow activated!","success")')
    content = content.replace('notify("\U0001f513 Buyer contact unlocked!","success")', 'notify("Buyer contact unlocked!","success")')

    # HomeClient PayModal notify calls
    content = content.replace('notify("\U0001f513 Contact details revealed!","success")', 'notify("Contact details revealed!","success")')
    content = content.replace('notify("\U0001f513 Buyer contact revealed!","success")', 'notify("Buyer contact revealed!","success")')
    content = content.replace('notify("\U0001f510 Escrow activated!","success")', 'notify("Escrow activated!","success")')
    content = content.replace('"\U0001f513 Contact details revealed!"', '"Contact details revealed!"')
    content = content.replace('"\U0001f513 Buyer contact revealed!"', '"Buyer contact revealed!"')
    content = content.replace('"\U0001f510 Escrow activated!"', '"Escrow activated!"')
    content = content.replace('"\U0001f513 Buyer contact unlocked!"', '"Buyer contact unlocked!"')

    # PostAdModal notifications
    content = content.replace('notify("\u23f3 Ad submitted! It\'s under review', 'notify("Ad submitted! It\'s under review')
    content = content.replace('notify("\u23f3 Ad under review', 'notify("Ad under review')

    # Mark sold modal
    content = content.replace('"\U0001f389 Marked as sold via Weka Soko!"', '"Marked as sold via Weka Soko!"')
    content = content.replace('"\u2705 Marked as sold outside platform."', '"Marked as sold outside platform."')

    # Contact info detection error
    content = content.replace('notify(`\u274c Contact info detected', 'notify(`Contact info detected')

    # Profile update
    content = content.replace('notify("\u2705 Profile updated!","success")', 'notify("Profile updated!","success")')

    # Password changed
    content = content.replace('notify("\u2705 Password changed successfully!","success")', 'notify("Password changed successfully!","success")')

    # Verification email
    content = content.replace('notify("\u2705 Verification email sent! Check your inbox.","success")', 'notify("Verification email sent! Check your inbox.","success")')

    # Review submitted
    content = content.replace('notify("\u2b50 Review submitted!","success")', 'notify("Review submitted!","success")')

    # Request posted
    content = content.replace('notify("\u2705 Request posted! Sellers will be notified.","success")', 'notify("Request posted! Sellers will be notified.","success")')

    # Contact revealed in PitchesTab
    content = content.replace('notify(`\u2705 Contact revealed!', 'notify(`Contact revealed!')

    # Resubmit
    content = content.replace('notify("\u23f3 Resubmitted","success")', 'notify("Resubmitted","success")')

    # Remove contact info warning
    content = content.replace('notify("\u26a0\ufe0f Remove contact info from flagged fields","warning")', 'notify("Remove contact info from flagged fields","warning")')

    # Unlock free
    content = content.replace('notify("\U0001f513 Unlocked!","success")', 'notify("Unlocked!","success")')

    # Buyer reveal
    content = content.replace('notify("\U0001f513 Buyer contact revealed!","success")', 'notify("Buyer contact revealed!","success")')

    # ── TEXT CONTENT / JSX REPLACEMENTS ──────────────────────────────────────

    # "✓" checkmarks in text spans (these are Unicode ✓ 0x2713)
    content = content.replace('<span style={{color:"#1428A0",fontWeight:800,fontSize:16}}>\u2713</span>Free to post', '<span style={{color:"#1428A0",fontWeight:800,fontSize:16}}>\u2713</span>Free to post')
    # Keep ✓ text symbols that are already clean text chars
    # The ✓ in "SOLD ✓" is decorative text – keep as-is (it's a simple symbol not emoji)
    # 0x2713 is standard check character, not a unicode emoji, keep as text

    # Kenya flag emoji in hero text
    content = content.replace('\U0001f1f0\U0001f1ea Kenya\'s Resell Platform', 'Kenya\'s Resell Platform')
    content = content.replace('\U0001f1f0\U0001f1ea Kenya\'s Resell Platform', 'Kenya\'s Resell Platform')

    # Trust bar check marks (these ✓ chars in the trust bar can stay as text)

    # Hero "How It Works" section - icons in array
    content = content.replace(
        '[["\\U0001f4dd","Post for Free","No upfront cost. Photos, description, location \u2014 done in 2 minutes."],\n            ["\\U0001f4ac","Chat Safely","Anonymous, moderated chat. Contact info hidden until unlock."],\n            ["\\U0001f525","Buyer Locks In","Serious buyers click \'I\'m Interested\'. You get notified instantly."],\n            ["\\U0001f4b3","Pay KSh 250","Seller pays once to see buyer contact. Till 5673935. Non-refundable."],\n            ["\\U0001f510","Safe Escrow","Optional 7.5% escrow. Funds held until you confirm delivery."],\n            ["\\U0001f3c6","Deal Done","Leave a review. Build your seller reputation on the platform."]]',
        '[["doc","Post for Free","No upfront cost. Photos, description, location \u2014 done in 2 minutes."],["chat","Chat Safely","Anonymous, moderated chat. Contact info hidden until unlock."],["fire","Buyer Locks In","Serious buyers click \'I\'m Interested\'. You get notified instantly."],["card","Pay KSh 250","Seller pays once to see buyer contact. Till 5673935. Non-refundable."],["lock","Safe Escrow","Optional 7.5% escrow. Funds held until you confirm delivery."],["trophy","Deal Done","Leave a review. Build your seller reputation on the platform."]]'
    )

    # "Buyers Want" sidebar heading
    content = content.replace('\U0001f6d2 Buyers Want', 'Buyers Want')

    # "What Buyers Want" heading
    content = content.replace('\U0001f6d2 What Buyers Want', 'What Buyers Want')

    # Listings empty state search icon
    content = content.replace('<div style={{fontSize:56,marginBottom:16,opacity:.15}}>\U0001f50d</div>', '<div style={{fontSize:56,marginBottom:16,opacity:.15,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_search(48) + '</div>')

    # Pay modal reveal buttons
    content = content.replace('"\U0001f513 Reveal"', '"Reveal"')
    content = content.replace('"\U0001f513 Reveal Buyer \u2014 KSh 250"', '"Reveal Buyer \u2014 KSh 250"')
    content = content.replace('"\U0001f513 Pay KSh 250 to See Buyer Contact"', '"Pay KSh 250 to See Buyer Contact"')

    # Action Required heading
    content = content.replace('\U0001f525 Action Required \u2014 Buyers Waiting', 'Action Required \u2014 Buyers Waiting')

    # "Buyers Waiting" mobile card heading
    content = content.replace('\U0001f525 {stats.buyersWaiting}', '{stats.buyersWaiting}')

    # Chat Threads heading
    content = content.replace('\U0001f4ac Chat Threads', 'Chat Threads')

    # Notifications heading
    content = content.replace('\U0001f514 All Notifications', 'All Notifications')

    # Interests heading
    content = content.replace('\U0001f525 Listings You\'re Interested In', 'Listings You\'re Interested In')

    # Empty states
    content = content.replace('<div style={{fontSize:48,marginBottom:12,opacity:.2}}>\U0001f525</div>', '<div style={{fontSize:48,marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_fire(40) + '</div>')

    # ── LARGE DISPLAY EMOJIS (used as decorative icons, wrapped in divs) ───────

    # 📦 Box/Package — used as placeholder image icon
    content = content.replace('<span style={{fontSize:44,opacity:.15}}>\U0001f4e6</span>', '<span style={{opacity:.15}}>' + s_box(44) + '</span>')
    content = content.replace('<span style={{fontSize:80,opacity:.15}}>\U0001f4e6</span>', '<span style={{opacity:.15}}>' + s_box(80) + '</span>')
    content = content.replace('<div style={{fontSize:48,marginBottom:12,opacity:.2}}>\U0001f4e6</div>', '<div style={{marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_box(48) + '</div>')
    content = content.replace('<div style={{fontSize:40,marginBottom:12,opacity:.2}}>\U0001f4e6</div>', '<div style={{marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_box(40) + '</div>')
    content = content.replace('<div style={{fontSize:40,marginBottom:12,opacity:.2}}>\U0001f4e6</div>', '<div style={{marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_box(40) + '</div>')
    content = content.replace('<span style={{fontSize:40,position:"absolute",top:"50%",left:"50%",transform:"translate(-50%,-50%)",opacity:.15}}>\U0001f4e6</span>', '<span style={{position:"absolute",top:"50%",left:"50%",transform:"translate(-50%,-50%)",opacity:.15}}>' + s_box(40) + '</span>')
    content = content.replace('<div style={{width:"100%",height:"100%",display:"flex",alignItems:"center",justifyContent:"center",fontSize:20,opacity:.3}}>\U0001f4e6</div>', '<div style={{width:"100%",height:"100%",display:"flex",alignItems:"center",justifyContent:"center",opacity:.3}}>' + s_box(20) + '</div>')
    content = content.replace('<div style={{width:"100%",height:"100%",display:"flex",alignItems:"center",justifyContent:"center",fontSize:24,opacity:.3}}>\U0001f4e6</div>', '<div style={{width:"100%",height:"100%",display:"flex",alignItems:"center",justifyContent:"center",opacity:.3}}>' + s_box(24) + '</div>')
    content = content.replace('<div style={{width:"100%",height:"100%",display:"flex",alignItems:"center",justifyContent:"center",fontSize:28,opacity:.15}}>\U0001f4e6</div>', '<div style={{width:"100%",height:"100%",display:"flex",alignItems:"center",justifyContent:"center",opacity:.15}}>' + s_box(28) + '</div>')
    content = content.replace('<div style={{display:"flex",alignItems:"center",justifyContent:"center",height:"100%",fontSize:36,opacity:.15}}>\U0001f4e6</div>', '<div style={{display:"flex",alignItems:"center",justifyContent:"center",height:"100%",opacity:.15}}>' + s_box(36) + '</div>')
    content = content.replace('<div style={{display:"flex",alignItems:"center",justifyContent:"center",height:"100%",fontSize:40,opacity:.15}}>\U0001f4e6</div>', '<div style={{display:"flex",alignItems:"center",justifyContent:"center",height:"100%",opacity:.15}}>' + s_box(40) + '</div>')

    # 🛒 Cart
    content = content.replace('<div style={{fontSize:28,marginBottom:8,opacity:.3}}>\U0001f6d2</div>', '<div style={{marginBottom:8,opacity:.3,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_cart(28) + '</div>')
    content = content.replace('<div style={{fontSize:40,marginBottom:12,opacity:.3}}>\U0001f6d2</div>', '<div style={{marginBottom:12,opacity:.3,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_cart(40) + '</div>')
    content = content.replace('<div style={{fontSize:44,marginBottom:12,opacity:.2}}>\U0001f6d2</div>', '<div style={{marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_cart(44) + '</div>')
    content = content.replace('<div style={{fontSize:40,marginBottom:12,opacity:.2}}>\U0001f6d2</div>', '<div style={{marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_cart(40) + '</div>')
    content = content.replace('<div style={{fontSize:40,marginBottom:12,opacity:.2}}>\U0001f6d2</div>', '<div style={{marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_cart(40) + '</div>')

    # 📬 Inbox
    content = content.replace('<div style={{fontSize:40,marginBottom:12,opacity:.2}}>\U0001f4ec</div>', '<div style={{marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_inbox(40) + '</div>')
    content = content.replace('<div style={{fontSize:32,marginBottom:8,opacity:.3}}>\U0001f4ec</div>', '<div style={{marginBottom:8,opacity:.3,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_inbox(32) + '</div>')

    # ✅ large check
    content = content.replace('<div style={{fontSize:56,marginBottom:16,opacity:.15}}>\u2705</div>', '<div style={{marginBottom:16,opacity:.15,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_check(56) + '</div>')
    content = content.replace('<div style={{fontSize:48}}>\u2705</div>', '<div style={{display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_check(48) + '</div>')

    # ⭐ large star
    content = content.replace('<div style={{fontSize:48}}>\u2b50</div>', '<div style={{display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_star_filled(48) + '</div>')

    # 🔥 large fire in interests
    content = content.replace('<div style={{fontSize:48,marginBottom:12,opacity:.2}}>\U0001f525</div>', '<div style={{marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_fire(48) + '</div>')

    # 🔔 large bell
    content = content.replace('<div style={{fontSize:48,marginBottom:12,opacity:.2}}>\U0001f514</div>', '<div style={{marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_bell(48) + '</div>')
    content = content.replace('<div style={{fontSize:48,marginBottom:12,opacity:.2}}>\U0001f514</div>', '<div style={{marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_bell(48) + '</div>')

    # 📱 phone (PWA banner)
    content = content.replace('<span style={{fontSize:28}}>\U0001f4f1</span>', '<span>' + s_phone(28) + '</span>')

    # 📧 email (verification banner)
    content = content.replace('<span style={{fontSize:20}}>\U0001f4e7</span>', '<span>' + s_email(20) + '</span>')

    # ⚠️ Warning verification section
    content = content.replace('<span style={{fontSize:28,flexShrink:0}}>\u26a0\ufe0f</span>', '<span style={{flexShrink:0}}>' + s_warn(28) + '</span>')

    # 🔒 Lock (seller section)
    content = content.replace('<span style={{fontSize:30}}>\U0001f512</span>', '<span>' + s_lock(30) + '</span>')

    # 🔓 Unlock (revealed contact)
    content = content.replace('<span style={{fontSize:18}}>\U0001f513</span>', '<span>' + s_unlock(18) + '</span>')

    # 👤 User
    content = content.replace('<span style={{fontSize:16}}>\U0001f464</span>', '<span>' + s_user(16) + '</span>')

    # 📞 Phone
    content = content.replace('<span style={{fontSize:16}}>\U0001f4de</span>', '<span>' + s_phone(16) + '</span>')

    # ✉️ Email
    content = content.replace('<span style={{fontSize:16}}>\u2709\ufe0f</span>', '<span>' + s_email(16) + '</span>')

    # 🔍 Search in detail modal zoom hint
    content = content.replace('>\U0001f50d Click to enlarge<', '>Click to enlarge<')

    # 🏷️ tag in MarkSoldModal
    content = content.replace('<div style={{fontSize:48, marginBottom:12}}>\U0001f3f7\ufe0f</div>', '<div style={{marginBottom:12,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_tag(48) + '</div>')

    # 🛒 in MarkSoldModal buttons
    content = content.replace('<div style={{fontSize:22}}>\U0001f6d2</div>', '<div style={{display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_cart(22) + '</div>')

    # 🤝 Handshake in MarkSoldModal
    content = content.replace('<div style={{fontSize:22}}>\U0001f91d</div>', '<div style={{display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_handshake(22) + '</div>')

    # 🔥 in buyer waiting card (large)
    content = content.replace('<span style={{fontSize:32}}>\U0001f525</span>', '<span>' + s_fire(32) + '</span>')

    # 🚪 door sign out
    content = content.replace('<span style={{fontSize:20}}>\U0001f6aa</span>', '<span>' + s_door(20) + '</span>')

    # 🗑 trash delete account
    content = content.replace('<span style={{fontSize:20}}>\U0001f5d1</span>', '<span>' + s_trash(20) + '</span>')

    # Review pending star in list
    content = content.replace('<span style={{fontSize:24}}>\u2b50</span>', '<span>' + s_star_filled(24) + '</span>')

    # ─── In-line emoji → SVG for button text, labels, spans ──────────────────

    # Report reasons array
    content = content.replace('{value:"scam",label:"\U0001f6a8 Scam / Fraud"}', '{value:"scam",label:"Scam / Fraud"}')
    content = content.replace('{value:"fake_item",label:"\U0001f3ad Fake or misleading item"}', '{value:"fake_item",label:"Fake or misleading item"}')
    content = content.replace('{value:"wrong_price",label:"\U0001f4b0 Wrong price"}', '{value:"wrong_price",label:"Wrong price"}')
    content = content.replace('{value:"offensive",label:"\U0001f6ab Offensive content"}', '{value:"offensive",label:"Offensive content"}')
    content = content.replace('{value:"spam",label:"\U0001f4e7 Spam"}', '{value:"spam",label:"Spam"}')
    content = content.replace('{value:"wrong_category",label:"\U0001f4c2 Wrong category"}', '{value:"wrong_category",label:"Wrong category"}')
    content = content.replace('{value:"already_sold",label:"\u2705 Item already sold"}', '{value:"already_sold",label:"Item already sold"}')
    content = content.replace('{value:"other",label:"\u2753 Other"}', '{value:"other",label:"Other"}')

    # ReportListingBtn button text
    content = content.replace('>\U0001f6a9 Report<', '>Report<')
    # Modal title for report
    content = content.replace('>\U0001f6a9 Report this listing<', '>Report this listing<')
    # Report done large icon
    content = content.replace('<div style={{fontSize:48}}>\u2705</div>', '<div style={{display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_check(48) + '</div>')

    # LeaveReviewBtn labels
    content = content.replace('"\u2b50 Review Buyer"', '"Review Buyer"')
    content = content.replace('"\u2b50 Review Seller"', '"Review Seller"')
    # Submit review button star
    content = content.replace('"Submit \u2b50"', '"Submit Review"')
    content = content.replace('"Submit Review \u2b50"', '"Submit Review"')
    # Review leave label
    content = content.replace('>\u2b50 Leave a Review (', '>Leave a Review (')
    # Pending reviews star
    # (already covered above)

    # Profile section Edit button
    content = content.replace('>\u270f\ufe0f Edit<', '>Edit<')
    content = content.replace('>\u270f\ufe0f<', '>' + s_edit(14) + '<')

    # Dashboard status badges for listings
    content = content.replace('"pending_review"?"\u23f3 Review"', '"pending_review"?"Review"')
    content = content.replace('"rejected"?"\u274c Rejected"', '"rejected"?"Rejected"')
    content = content.replace('"pending_review"?"\u23f3 Under Review"', '"pending_review"?"Under Review"')
    content = content.replace('"needs_changes"?"\u270f\ufe0f Needs Changes"', '"needs_changes"?"Needs Changes"')
    content = content.replace('"rejected"?"\u274c Rejected"', '"rejected"?"Rejected"')

    # Role switcher button text
    content = content.replace('{target==="seller"?"\U0001f3f7":"\U0001f6cd"} Switch to', 'Switch to')
    content = content.replace('{target==="seller"?"\U0001f3f7\ufe0f":"\U0001f6cd\ufe0f"} Switch to', 'Switch to')

    # Sign out / delete in dashboard settings
    content = content.replace('>\U0001f6aa Sign Out<', '>Sign Out<')
    content = content.replace('>\U0001f5d1 Delete My Account<', '>Delete My Account<')

    # Role badge in profile
    content = content.replace('{user.role==="seller"?"\U0001f3f7 Seller":"\U0001f6cd Buyer"}', '{user.role==="seller"?"Seller":"Buyer"}')
    content = content.replace('{user.role==="seller"?"\U0001f3f7 SELLER":"\U0001f6cd BUYER"}', '{user.role==="seller"?"SELLER":"BUYER"}')
    content = content.replace('{user.role==="seller"?"\U0001f3f7 Seller":"\U0001f6cd\ufe0f Buyer"}', '{user.role==="seller"?"Seller":"Buyer"}')
    content = content.replace('{user.role==="seller"?"\U0001f3f7\ufe0f":"\U0001f6cd\ufe0f"}', '{user.role==="seller"?"Seller":"Buyer"}')

    # Reviewer role badge
    content = content.replace('{r.reviewer_role==="buyer"?"\U0001f6cd Buyer":"\U0001f3f7 Seller"}', '{r.reviewer_role==="buyer"?"Buyer":"Seller"}')

    # Sold channel badges in SoldSection
    content = content.replace('{l.sold_channel==="platform"?"\U0001f6d2 Via WekaSoko":"\U0001f91d Elsewhere"}', '{l.sold_channel==="platform"?"Via WekaSoko":"Elsewhere"}')

    # Calendar/date icons in SoldSection
    content = content.replace('>\U0001f4c5 Listed<', '>' + s_cal(12) + ' Listed<')
    content = content.replace('>\u2705 Sold<', '>Sold<')
    content = content.replace('>\u23f1 Time to sell<', '>Time to sell<')

    # ⭐ in pending reviews pending star (24px, already done above)
    # ★ unicode star in rating - those are 0x2605/0x2606, already text chars, keep as-is

    # Quick action icons in MobileDashboard (array literals with emoji)
    content = content.replace('{icon:"\U0001f4e6",label:"My Ads"', '{icon:"box",label:"My Ads"')
    content = content.replace('{icon:"\U0001f525",label:"Buyers"', '{icon:"fire",label:"Buyers"')
    content = content.replace('{icon:"\U0001f3c6",label:"Sold Items"', '{icon:"trophy",label:"Sold Items"')
    content = content.replace('{icon:"\U0001f6d2",label:"Requests"', '{icon:"cart",label:"Requests"')
    content = content.replace('{icon:"\u2764\ufe0f",label:"Saved"', '{icon:"heart",label:"Saved"')
    content = content.replace('{icon:"\U0001f6d2",label:"Requests"', '{icon:"cart",label:"Requests"')
    content = content.replace('{icon:"\U0001f4ac",label:"Messages"', '{icon:"chat",label:"Messages"')
    content = content.replace('{icon:"\U0001f514",label:"Alerts"', '{icon:"bell",label:"Alerts"')

    # Render quick action icons
    content = content.replace('<div style={{fontSize:26,marginBottom:8}}>{a.icon}</div>', '<div style={{marginBottom:8,display:"flex",alignItems:"center"}}>{a.icon==="box"?' + s_box(26) + ':a.icon==="fire"?' + s_fire(26) + ':a.icon==="trophy"?' + s_trophy(26) + ':a.icon==="cart"?' + s_cart(26) + ':a.icon==="heart"?' + s_heart(26) + ':a.icon==="chat"?' + s_chat(26) + ':a.icon==="bell"?' + s_bell(26) + ':null}</div>')

    # Dashboard stats icons in overview grid
    content = content.replace('{icon:"\U0001f4e6",label:"Total Ads"', '{icon:"box",label:"Total Ads"')
    content = content.replace('{icon:"\u2705",label:"Active"', '{icon:"check",label:"Active"')
    content = content.replace('{icon:"\U0001f3c6",label:"Sold"', '{icon:"trophy",label:"Sold"')
    content = content.replace('{icon:"\U0001f441",label:"Total Views"', '{icon:"eye",label:"Total Views"')
    content = content.replace('{icon:"\U0001f525",label:"Buyers Waiting"', '{icon:"fire",label:"Buyers Waiting"')
    content = content.replace('{icon:"\U0001f4ac",label:"Unread Msgs"', '{icon:"chat",label:"Unread Msgs"')
    content = content.replace('{icon:"\U0001f514",label:"Unread"', '{icon:"bell",label:"Unread"')

    # Render dashboard overview icons
    content = content.replace('<div style={{fontSize:24,marginBottom:8}}>{s.icon}</div>', '<div style={{marginBottom:8,display:"flex",alignItems:"center"}}>{s.icon==="box"?' + s_box(24) + ':s.icon==="check"?' + s_check(24) + ':s.icon==="trophy"?' + s_trophy(24) + ':s.icon==="eye"?' + s_eye(24) + ':s.icon==="fire"?' + s_fire(24) + ':s.icon==="chat"?' + s_chat(24) + ':s.icon==="bell"?' + s_bell(24) + ':null}</div>')

    # Listing view count / interest count inline
    content = content.replace('>\U0001f441 {l.view_count||0} views<', '>' + s_eye(12) + ' {l.view_count||0} views<')
    content = content.replace('>\U0001f525 {l.interest_count||0} interested<', '>' + s_fire(12) + ' {l.interest_count||0} interested<')
    content = content.replace('>\U0001f441 {l.view_count||0}<', '>' + s_eye(12) + ' {l.view_count||0}<')
    content = content.replace('>\U0001f525 {l.interest_count||0}<', '>' + s_fire(12) + ' {l.interest_count||0}<')
    # ListingCard location/view/interest row
    content = content.replace('>📍 {l.location}</span>', '>' + s_pin(11) + ' {l.location}</span>')
    content = content.replace('>👁 {l.view_count||0}</span>', '>' + s_eye(11) + ' {l.view_count||0}</span>')
    content = content.replace('>\U0001f4cd {l.location}</span>', '>' + s_pin(11) + ' {l.location}</span>')
    content = content.replace('>\U0001f441 {l.view_count||0}</span>', '>' + s_eye(11) + ' {l.view_count||0}</span>')

    # Sold section location/county
    content = content.replace('>\U0001f4cd {l.county||l.location||"Kenya"}<', '>' + s_pin(11) + ' {l.county||l.location||"Kenya"}<')

    # Locked buyer interested banner
    content = content.replace('>\U0001f525 Buyer Interested<', '>Buyer Interested<')

    # Detail modal badges
    content = content.replace('"\u23f3 Under Review"', '"Under Review"')
    content = content.replace('"\u270f\ufe0f Needs Changes"', '"Needs Changes"')
    content = content.replace('"\u274c Rejected"', '"Rejected"')

    # Detail modal location
    content = content.replace('>\U0001f4cd {l.location}', '>' + s_pin(12) + ' {l.location}')

    # Detail modal view/interest/time
    content = content.replace('>\U0001f441 {l.view_count||0} views<', '>' + s_eye(12) + ' {l.view_count||0} views<')
    content = content.replace('>\U0001f525 {l.interest_count||0} interested<', '>' + s_fire(12) + ' {l.interest_count||0} interested<')
    content = content.replace('>\U0001f552 {ago(l.created_at)}<', '>' + s_clock(12) + ' {ago(l.created_at)}<')
    content = content.replace('>\u23f0 {timeLeft(l.expires_at)}<', '>' + s_clock(12) + ' {timeLeft(l.expires_at)}<')

    # Stay safe tip
    content = content.replace('>\U0001f6e1\ufe0f Stay Safe on Weka Soko<', '>' + s_shield(14) + ' Stay Safe on Weka Soko<')
    content = content.replace('• \U0001f6a9 <strong>Something feel off?</strong>', '• <strong>Something feel off?</strong>')

    # Escrow info
    content = content.replace('>\U0001f510 <strong>Safe Escrow:</strong>', '>' + s_lock(14) + ' <strong>Safe Escrow:</strong>')

    # Response rate
    content = content.replace('>\u26a1 {Math.round(l.response_rate)}%', '>' + s_lightning(11) + ' {Math.round(l.response_rate)}%')

    # Chat button text
    content = content.replace('>\U0001f4ac Chat with Seller<', '>Chat with Seller<')
    content = content.replace('>\U0001f4ac View Messages<', '>View Messages<')

    # Detail modal footer buttons
    content = content.replace('>\U0001f525 I\'m Interested \u2014 Lock In<', '>I\'m Interested \u2014 Lock In<')
    content = content.replace('>\U0001f510 Buy with Escrow<', '>Buy with Escrow<')
    content = content.replace('>\U0001f513 Pay KSh 250 to See Buyer Contact<', '>Pay KSh 250 to See Buyer Contact<')

    # Linked request banner cart icon
    content = content.replace('<span style={{fontSize:20}}>\U0001f6d2</span>', '<span>' + s_cart(20) + '</span>')

    # Post ad alert
    content = content.replace('>\u2705 Posting is free.', '>Posting is free.')

    # Field error warning
    content = content.replace('>\u26a0\ufe0f {fieldErrors.description}<', '>' + s_warn(11) + ' {fieldErrors.description}<')

    # Pay choice pay now/later icons (in selection cards)
    content = content.replace('>\U0001f4b3 Pay KSh 250 Now<', '>Pay KSh 250 Now<')
    content = content.replace('>\u23f0 Post Anonymously (Pay Later)<', '>Post Anonymously (Pay Later)<')
    content = content.replace('{payChoice==="now"?"\U0001f4b3":"\u23f0"}', '{payChoice==="now"?"pay-now":"pay-later"}')
    content = content.replace('<span style={{fontSize:18}}>{payChoice==="now"?"\U0001f4b3":"\u23f0"}</span>', '<span>' + s_creditcard(18) + '</span>')

    # Save changes button
    content = content.replace('"Save Changes \u2705"', '"Save Changes"')

    # PostAdModal description warning
    content = content.replace('"⚠️ Remove contact info from flagged fields","warning"', '"Remove contact info from flagged fields","warning"')

    # Pay later / review notification
    content = content.replace('notify("\u23f3 Ad submitted! It\'s under review', 'notify("Ad submitted! It\'s under review')

    # "I Have This" button (📬)
    content = content.replace('>\U0001f4ec I Have This<', '>I Have This<')

    # WhatBuyersWant compact empty state
    content = content.replace('<div style={{fontSize:28,marginBottom:8,opacity:.3}}>\U0001f6d2</div>', '<div style={{marginBottom:8,opacity:.3,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_cart(28) + '</div>')

    # WhatBuyersWant county tag
    content = content.replace('>\U0001f4cd {r.county}<', '>' + s_pin(11) + ' {r.county}<')

    # Dashboard listing row inline stats
    content = content.replace('}>👁 {l.view_count||0} · 🔥 {l.interest_count||0}</div>', '}>' + s_eye(12) + ' {l.view_count||0} · ' + s_fire(12) + ' {l.interest_count||0}</div>')
    content = content.replace('">{l.view_count||0} views · \U0001f525 {l.interest_count||0} interested</div>', '">' + s_eye(11) + ' {l.view_count||0} views · ' + s_fire(11) + ' {l.interest_count||0} interested</div>')

    # Listings ad listing moderation note
    content = content.replace('>\u274c {l.moderation_note}<', '>Rejected: {l.moderation_note}<')
    content = content.replace('>\u23f3 Awaiting review<', '>Awaiting review<')

    # Listing status badge in ads tab
    content = content.replace('"pending_review"?"\u23f3 Review":', '"pending_review"?"Review":')

    # Free unlock button
    content = content.replace('>\U0001f381 Free<', '>Free<')

    # Sold button
    content = content.replace('>\u2705 Sold<', '>Sold<')

    # Edit pencil button in ads tab
    content = content.replace('>\u270f\ufe0f<', '>' + s_edit(14) + '<')

    # Resubmit refresh
    content = content.replace('>\u21ba<', '>' + s_refresh(14) + '<')

    # Delete X
    content = content.replace('>\u2715<', '>x<')

    # 🔓 Reveal buyer buttons in various places
    content = content.replace('>\U0001f513 Reveal Buyer \u2014 KSh 250<', '>Reveal Buyer \u2014 KSh 250<')
    content = content.replace('>\U0001f513 {l.linked_request_id?"Reveal Buyer":"Unlock"} \u2014 KSh 250<', '>{l.linked_request_id?"Reveal Buyer":"Unlock"} \u2014 KSh 250<')
    content = content.replace('>\U0001f513 Accept \u2014 Pay KSh 250<', '>Accept \u2014 Pay KSh 250<')

    # PostRequestModal title
    content = content.replace('title="\U0001f6d2 Post a Buyer Request"', 'title="Post a Buyer Request"')

    # View count in listing detail
    content = content.replace('>\U0001f441 {l.view_count||0} views<', '>' + s_eye(12) + ' {l.view_count||0} views<')

    # Mobile listing card location
    content = content.replace('>{l.location&&<span>📍 {l.location}</span>}', '>{l.location&&<span>' + s_pin(11) + ' {l.location}</span>}')
    content = content.replace('>{l.location&&<span>\U0001f4cd {l.location}</span>}', '>{l.location&&<span>' + s_pin(11) + ' {l.location}</span>}')

    # MobileLayout hero banner Kenya flag text
    content = content.replace('>\U0001f1f0\U0001f1ea Kenya\'s Resell Platform<', '>Kenya\'s Resell Platform<')

    # Mobile listing empty
    content = content.replace('<div style={{fontSize:40,marginBottom:12,opacity:.3}}>\U0001f50d</div>', '<div style={{marginBottom:12,opacity:.3,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_search(40) + '</div>')

    # Mobile requests empty
    content = content.replace('<div style={{fontSize:44,marginBottom:12,opacity:.2}}>\U0001f6d2</div>', '<div style={{marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_cart(44) + '</div>')

    # Mobile county request tag
    content = content.replace('>\U0001f4cd {r.county}<', '>' + s_pin(11) + ' {r.county}<')

    # "I have This" mobile button
    content = content.replace('>\U0001f4ec I Have This\n                        <', '>I Have This\n                        <')

    # Mobile layout clear filter
    content = content.replace('>Clear ✕<', '>Clear<')

    # Password show/hide eye icons
    content = content.replace('>{showCurrent?"\U0001f648":"\U0001f441"}<', '>{showCurrent?' + s_eyeoff(16) + ':' + s_eye(16) + '}<')
    content = content.replace('>{showNew?"\U0001f648":"\U0001f441"}<', '>{showNew?' + s_eyeoff(16) + ':' + s_eye(16) + '}<')

    # Verification section email send button
    content = content.replace('"\U0001f4e7 Send Verification Email"', '"Send Verification Email"')

    # ── HomeClient.jsx specific ────────────────────────────────────────────────

    # notify welcome back
    content = content.replace('notify("Welcome back, "+parsed.name.split(" ")[0]+"! \U0001f389","success")', 'notify("Welcome back, "+parsed.name.split(" ")[0]+"!","success")')

    # Email verified notifications
    content = content.replace('notify("\u2705 Email verified! Welcome to Weka Soko.","success")', 'notify("Email verified! Welcome to Weka Soko.","success")')
    content = content.replace('notify("\u2705 Email verified! You can now sign in.","success")', 'notify("Email verified! You can now sign in.","success")')

    # listing_approved notification
    content = content.replace('notify("\U0001f389 Your ad is now live on Weka Soko! "+(n.body||""),"success")', 'notify("Your ad is now live on Weka Soko! "+(n.body||""),"success")')

    # Suspension notification
    content = content.replace('notify("\u26d4 Your account has been suspended. You will be logged out.","error")', 'notify("Your account has been suspended. You will be logged out.","error")')

    # admin_edit notification
    content = content.replace('notify("\u2139\ufe0f Admin has updated your listing: "+(n.body||""),"info")', 'notify("Admin has updated your listing: "+(n.body||""),"info")')

    # handleLockIn
    content = content.replace('notify("\U0001f525 Locked in! The seller has been notified.","success")', 'notify("Locked in! The seller has been notified.","success")')

    # PayModal success notifications in HomeClient
    content = content.replace('notify("\U0001f513 Contact details revealed!","success")', 'notify("Contact details revealed!","success")')
    content = content.replace('notify(modal.payType==="unlock"?"\U0001f513 Buyer contact revealed!":"\U0001f510 Escrow activated!","success")', 'notify(modal.payType==="unlock"?"Buyer contact revealed!":"Escrow activated!","success")')
    content = content.replace('notify("\U0001f513 Buyer contact unlocked!","success")', 'notify("Buyer contact unlocked!","success")')

    # Hero section checkmarks (these ✓ chars 0x2713 are already plain text)
    # Trust bar checkmarks
    content = content.replace('<span style={{color:"#1428A0",fontWeight:800,fontSize:16}}>✓</span>Free to post', '<span style={{color:"#1428A0",fontWeight:800,fontSize:16}}>' + s_check(16) + '</span>Free to post')
    content = content.replace('<span style={{color:"#1428A0",fontWeight:800,fontSize:16}}>✓</span>Anonymous chat', '<span style={{color:"#1428A0",fontWeight:800,fontSize:16}}>' + s_check(16) + '</span>Anonymous chat')
    content = content.replace('<span style={{color:"#1428A0",fontWeight:800,fontSize:16}}>✓</span>M-Pesa escrow', '<span style={{color:"#1428A0",fontWeight:800,fontSize:16}}>' + s_check(16) + '</span>M-Pesa escrow')
    content = content.replace('<span style={{color:"#fff",fontSize:16,fontWeight:800}}>✓</span>', '<span style={{color:"#fff",fontSize:16,fontWeight:800}}>' + s_check(16) + '</span>')

    # "How It Works" section icon rendering
    content = content.replace('<div style={{fontSize:28,marginBottom:14}}>{icon}</div>', '<div style={{marginBottom:14,display:"flex",alignItems:"center"}}>{icon==="doc"?' + s_doc(28) + ':icon==="chat"?' + s_chat(28) + ':icon==="fire"?' + s_fire(28) + ':icon==="card"?' + s_creditcard(28) + ':icon==="lock"?' + s_lock(28) + ':icon==="trophy"?' + s_trophy(28) + ':null}</div>')

    # "Buyers Want" sidebar section heading
    content = content.replace('<div style={{fontSize:16,fontWeight:700,color:"#1A1A1A",marginBottom:12}}>\U0001f6d2 Buyers Want</div>', '<div style={{fontSize:16,fontWeight:700,color:"#1A1A1A",marginBottom:12}}>' + s_cart(16) + ' Buyers Want</div>')

    # Homepage clear filter button
    content = content.replace('>\u2715 Clear All Filters<', '>Clear All Filters<')

    # Sort select options
    content = content.replace('"Price: Low \u2192 High"', '"Price: Low to High"')
    content = content.replace('"Price: High \u2192 Low"', '"Price: High to Low"')

    # Grid/List view toggle buttons
    content = content.replace('>\u229e<', '>Grid<')
    content = content.replace('>\u2630<', '>List<')

    # Mobile sort buttons
    content = content.replace('"Price \u2191"', '"Price: Low"')
    content = content.replace('"Price \u2193"', '"Price: High"')
    content = content.replace('"Price \u2191":s==="price_desc"?"Price \u2193"', '"Price: Low":s==="price_desc"?"Price: High"')

    # Mobile sort in filter drawer
    content = content.replace('["price_asc","Price \u2191"]', '["price_asc","Price: Low"]')
    content = content.replace('["price_desc","Price \u2193"]', '["price_desc","Price: High"]')

    # Back arrow in sold page
    content = content.replace('>\u2190 Back to Marketplace<', '>Back to Marketplace<')

    # Dashboard "Back to Home" button
    content = content.replace('>\u2190 Back to Home<', '>Back to Home<')

    # Pagination arrows
    content = content.replace('>\u2190 Prev<', '>Prev<')
    content = content.replace('>Next \u2192<', '>Next<')
    content = content.replace('>\u2190 Back to Marketplace<', '>Back to Marketplace<')

    # View all arrow
    content = content.replace('>View all \u2192<', '>View all<')
    content = content.replace('"View all →"', '"View all"')
    content = content.replace('"Post Request \u2192"', '"Post Request"')
    content = content.replace('"Post Your First Ad \u2192"', '"Post Your First Ad"')
    content = content.replace('"Browse Listings \u2192"', '"Browse Listings"')

    # Lightbox arrows
    content = content.replace('"leftArrow":"\u2190"', '"leftArrow":"<"')
    content = content.replace('"rightArrow":"\u2192"', '"rightArrow":">"')

    # Up arrow in send button
    content = content.replace('"Send \u2191"', '"Send"')

    # Auth modal resend
    content = content.replace('>\u2713 Email resent! Check your inbox.<', '>Email resent! Check your inbox.<')
    content = content.replace('>\u2705 Email sent! Click the link in your inbox to activate your account.<', '>Email sent! Click the link in your inbox to activate your account.<')

    # Profile section verified badge
    content = content.replace('>\u2713 Verified<', '>Verified<')
    content = content.replace('>\u26a0 Unverified<', '>Unverified<')

    # Password match check
    content = content.replace('"\u2713 Passwords match"', '"Passwords match"')
    content = content.replace('"\u2717 Passwords do not match"', '"Passwords do not match"')

    # Role switch success
    content = content.replace('notify(`Switched to ${target} account \u2713`,"success")', 'notify(`Switched to ${target} account`,"success")')

    # WhatBuyersWant heading h2
    content = content.replace('>\U0001f6d2 What Buyers Want<', '>What Buyers Want<')

    # Mobile requests section heading
    content = content.replace('>\U0001f6d2 What Buyers Want<', '>What Buyers Want<')

    # Mobile trust strip check marks
    content = content.replace('[["✓","Free to post"],["✓","Anonymous chat"],["✓","M-Pesa escrow"]]', '[["check","Free to post"],["check","Anonymous chat"],["check","M-Pesa escrow"]]')
    content = content.replace('<span key={txt}><span style={{color:"#1428A0",fontWeight:800}}>{icon}</span>{txt}</span>', '<span key={txt}><span style={{color:"#1428A0",fontWeight:800}}>{icon==="check"?' + s_check(14) + ':icon}</span>{txt}</span>')

    # Filter clear button
    content = content.replace('>✕ Clear<', '>Clear<')
    content = content.replace('>✕ Clear filters<', '>Clear filters<')
    content = content.replace('>✕ Clear All Filters<', '>Clear All Filters<')

    # Dismiss PWA banner
    content = content.replace('>✕<', '>Close<')

    # Mobile filter close X
    content = content.replace('button style={{background:"#F5F5F5",border:"none",borderRadius:"50%",width:32,height:32,cursor:"pointer",fontSize:16,display:"flex",alignItems:"center",justifyContent:"center"}}>✕</button>', 'button style={{background:"#F5F5F5",border:"none",borderRadius:"50%",width:32,height:32,cursor:"pointer",fontSize:16,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_x(16) + '</button>')

    # User delete request X buttons
    content = content.replace('style={{background:"none",border:"none",cursor:"pointer",color:"#AEAEB2",fontSize:14,padding:"0 2px",flexShrink:0}}>✕</button>', 'style={{background:"none",border:"none",cursor:"pointer",color:"#AEAEB2",fontSize:14,padding:"0 2px",flexShrink:0}}>' + s_x(14) + '</button>')
    content = content.replace('style={{background:"none",border:"none",cursor:"pointer",color:"#CCCCCC",fontSize:14,padding:"0 2px",flexShrink:0}}>✕</button>', 'style={{background:"none",border:"none",cursor:"pointer",color:"#CCCCCC",fontSize:14,padding:"0 2px",flexShrink:0}}>' + s_x(14) + '</button>')
    content = content.replace('style={{background:"none",border:"none",cursor:"pointer",color:"#CCC",fontSize:16,padding:"0 2px",flexShrink:0,lineHeight:1}}>✕</button>', 'style={{background:"none",border:"none",cursor:"pointer",color:"#CCC",fontSize:16,padding:"0 2px",flexShrink:0,lineHeight:1}}>' + s_x(14) + '</button>')
    content = content.replace('style={{background:"none",border:"none",cursor:"pointer",color:"#AEAEB2",fontSize:14,padding:"0 2px",flexShrink:0,lineHeight:1}}>✕</button>', 'style={{background:"none",border:"none",cursor:"pointer",color:"#AEAEB2",fontSize:14,padding:"0 2px",flexShrink:0,lineHeight:1}}>' + s_x(14) + '</button>')

    # Pay choice cancel X
    content = content.replace('style={{background:"none",border:"none",cursor:"pointer",color:"#AAAAAA",fontSize:18}}>✕</button>', 'style={{background:"none",border:"none",cursor:"pointer",color:"#AAAAAA"}}>' + s_x(16) + '</button>')

    # Existing photo remove button x
    content = content.replace('>×</button>', '>' + s_x(11) + '</button>')

    # Dashboard listing delete X button
    content = content.replace('className="btn br2 sm" onClick={()=>deleteListing(l.id)}>✕</button>', 'className="btn br2 sm" onClick={()=>deleteListing(l.id)}>' + s_x(14) + '</button>')

    # Pitch declined text
    content = content.replace('>\u2715 Declined<', '>Declined<')

    # SOLD badge check
    # "SOLD ✓" — keep the ✓ as text, it's used in CSS badge, not emoji

    # MobileLayout close filter button
    content = content.replace('style={{background:"#F5F5F5",border:"none",borderRadius:"50%",width:32,height:32,cursor:"pointer",fontSize:16,display:"flex",alignItems:"center",justifyContent:"center"}}>✕</button>', 'style={{background:"#F5F5F5",border:"none",borderRadius:"50%",width:32,height:32,cursor:"pointer",display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_x(16) + '</button>')

    # Mobile clear filter ✕
    content = content.replace('>Clear ✕<', '>Clear<')

    # "Post Request →" button
    content = content.replace('"Post Request →"', '"Post Request"')

    # "Post Your First Ad →"
    content = content.replace('"Post Your First Ad →"', '"Post Your First Ad"')

    return content

def s_eyeoff(sz=16):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>'

# Note: s_eyeoff needs to be defined at module level before process_file uses it
# Re-run with fixed order

# Actually, let's just do the replacements directly in the main function

def do_all_replacements(content):
    """Apply all emoji replacements to content."""
    return process_file_content(content)

def process_file_content(content):
    """All replacements. Returns updated content."""
    c = content

    # eyeoff helper
    def eyeoff(sz=16):
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>'

    # Now call process_file and patch the eyeoff
    result = process_file_str(c, eyeoff)
    return result

def process_file_str(c, eyeoff_fn):
    """Main replacement logic."""

    # ── Notification type map (emoji → text key) ─────────────────────────────
    c = c.replace(
        '{new_message:"\U0001f4ac",buyer_locked_in:"\U0001f525",escrow_released:"\U0001f4b0",payment_confirmed:"\u2705",warning:"\u26a0\ufe0f",admin_edit:"\U0001f6e0",suspension:"\U0001f6ab",seller_pitch:"\U0001f4ec",pitch_accepted:"\u2705",request_match:"\U0001f6d2",listing_match:"\U0001f3f7\ufe0f",listing_approved:"\u2705"}',
        '{new_message:"chat",buyer_locked_in:"fire",escrow_released:"money",payment_confirmed:"check",warning:"warn",admin_edit:"settings",suspension:"ban",seller_pitch:"inbox",pitch_accepted:"check",request_match:"cart",listing_match:"tag",listing_approved:"check"}'
    )

    # Notification icon rendering (in notification list items)
    c = c.replace(
        '<span style={{fontSize:22,flexShrink:0}}>\n                  {({new_message:"chat"',
        '<span style={{flexShrink:0,display:"flex",alignItems:"center"}}>\n                  {({new_message:' + s_chat(22)
    )

    # ── Face emojis in rating labels ──────────────────────────────────────────
    c = c.replace(
        '["","\U0001f61e Poor","\U0001f610 Fair","\U0001f642 Good","\U0001f60a Very Good","\U0001f929 Excellent"]',
        '["","Poor","Fair","Good","Very Good","Excellent"]'
    )

    # ── Notification/toast message strings ────────────────────────────────────
    for old, new in [
        ('notify(`Welcome to Weka Soko, ${data.user.name?.split(" ")[0]||""}! \U0001f389 Check your email',
         'notify(`Welcome to Weka Soko, ${data.user.name?.split(" ")[0]||""}! Check your email'),
        ('notify(`Welcome back, ${data.user.name?.split(" ")[0]||""}! \U0001f389`,"success")',
         'notify(`Welcome back, ${data.user.name?.split(" ")[0]||""}!`,"success")'),
        ('"Welcome back, "+parsed.name.split(" ")[0]+"! \U0001f389","success"',
         '"Welcome back, "+parsed.name.split(" ")[0]+"!","success"'),
        ('notify("\U0001f389 Your ad is now live on Weka Soko! "+(n.body||""),"success")',
         'notify("Your ad is now live on Weka Soko! "+(n.body||""),"success")'),
        ('notify("\u2705 Email verified! Welcome to Weka Soko.","success")',
         'notify("Email verified! Welcome to Weka Soko.","success")'),
        ('notify("\u2705 Email verified! You can now sign in.","success")',
         'notify("Email verified! You can now sign in.","success")'),
        ('notify("\u26d4 Your account has been suspended. You will be logged out.","error")',
         'notify("Your account has been suspended. You will be logged out.","error")'),
        ('notify("\U0001f6ab Your account has been suspended. Check your email.","error")',
         'notify("Your account has been suspended. Check your email.","error")'),
        ('notify("\u2139\ufe0f Admin has updated your listing: "+(n.body||""),"info")',
         'notify("Admin has updated your listing: "+(n.body||""),"info")'),
        ('notify("\U0001f525 Locked in! The seller has been notified.","success")',
         'notify("Locked in! The seller has been notified.","success")'),
        ('notify("\U0001f513 Contact details revealed!","success")',
         'notify("Contact details revealed!","success")'),
        ('notify("\U0001f513 Buyer contact revealed!","success")',
         'notify("Buyer contact revealed!","success")'),
        ('notify("\U0001f510 Escrow activated!","success")',
         'notify("Escrow activated!","success")'),
        ('notify("\U0001f513 Buyer contact unlocked!","success")',
         'notify("Buyer contact unlocked!","success")'),
        ('notify(modal.payType==="unlock"?"\U0001f513 Buyer contact revealed!":"\U0001f510 Escrow activated!","success")',
         'notify(modal.payType==="unlock"?"Buyer contact revealed!":"Escrow activated!","success")'),
        ('notify("\U0001f513 Buyer contact revealed!","success")',
         'notify("Buyer contact revealed!","success")'),
        ('notify("\U0001f510 Escrow activated!","success")',
         'notify("Escrow activated!","success")'),
        ('notify("\U0001f513 Unlocked!","success")',
         'notify("Unlocked!","success")'),
        ('notify("\u23f3 Ad submitted! It\'s under review \u2014 you\'ll be notified once it goes live.","info")',
         'notify("Ad submitted! It\'s under review \u2014 you\'ll be notified once it goes live.","info")'),
        ('notify("\u23f3 Ad under review \u2014 you\'ll be notified when it\'s live. Buyer contact will be revealed on approval.","info")',
         'notify("Ad under review \u2014 you\'ll be notified when it\'s live. Buyer contact will be revealed on approval.","info")'),
        ('notify("\u23f3 Ad submitted for review. Pay KSh 250 from your dashboard to reveal buyer contact once live.","info")',
         'notify("Ad submitted for review. Pay KSh 250 from your dashboard to reveal buyer contact once live.","info")'),
        ('notify(`\u274c Contact info detected \u2014 ${err.violations',
         'notify(`Contact info detected \u2014 ${err.violations'),
        ('notify("\u26a0\ufe0f Remove contact info from flagged fields","warning")',
         'notify("Remove contact info from flagged fields","warning")'),
        ('notify("\u2705 Profile updated!","success")',
         'notify("Profile updated!","success")'),
        ('notify("\u2705 Password changed successfully!","success")',
         'notify("Password changed successfully!","success")'),
        ('notify("\u2705 Verification email sent! Check your inbox.","success")',
         'notify("Verification email sent! Check your inbox.","success")'),
        ('notify("\u2b50 Review submitted!","success")',
         'notify("Review submitted!","success")'),
        ('notify("\u2705 Request posted! Sellers will be notified.","success")',
         'notify("Request posted! Sellers will be notified.","success")'),
        ('notify(`\u2705 Contact revealed! ${res.seller_contact',
         'notify(`Contact revealed! ${res.seller_contact'),
        ('notify("\u23f3 Resubmitted","success")',
         'notify("Resubmitted","success")'),
        ('notify("\U0001f513 Buyer contact revealed!","success")',
         'notify("Buyer contact revealed!","success")'),
    ]:
        c = c.replace(old, new)

    # ── Notification message in chatmodal (string content) ───────────────────
    c = c.replace(
        'body: systemMessage || `\u26a0\ufe0f Message blocked: ${reason}. Contact info must stay hidden until KSh 250 unlock is paid.`',
        'body: systemMessage || `Message blocked: ${reason}. Contact info must stay hidden until KSh 250 unlock is paid.`'
    )
    c = c.replace(
        'notify("\U0001f6ab Your account has been suspended. Check your email.","error")',
        'notify("Your account has been suspended. Check your email.","error")'
    )
    c = c.replace(
        'notify(`\u26a0\ufe0f Message blocked (${violationCount}/3 violations)`, "warning")',
        'notify(`Message blocked (${violationCount}/3 violations)`, "warning")'
    )

    # ── Mark sold modal ───────────────────────────────────────────────────────
    c = c.replace(
        '? "\U0001f389 Marked as sold via Weka Soko!"\n          : "\u2705 Marked as sold outside platform."',
        '? "Marked as sold via Weka Soko!"\n          : "Marked as sold outside platform."'
    )

    # ── Report reasons ────────────────────────────────────────────────────────
    for old, new in [
        ('{value:"scam",label:"\U0001f6a8 Scam / Fraud"}', '{value:"scam",label:"Scam / Fraud"}'),
        ('{value:"fake_item",label:"\U0001f3ad Fake or misleading item"}', '{value:"fake_item",label:"Fake or misleading item"}'),
        ('{value:"wrong_price",label:"\U0001f4b0 Wrong price"}', '{value:"wrong_price",label:"Wrong price"}'),
        ('{value:"offensive",label:"\U0001f6ab Offensive content"}', '{value:"offensive",label:"Offensive content"}'),
        ('{value:"spam",label:"\U0001f4e7 Spam"}', '{value:"spam",label:"Spam"}'),
        ('{value:"wrong_category",label:"\U0001f4c2 Wrong category"}', '{value:"wrong_category",label:"Wrong category"}'),
        ('{value:"already_sold",label:"\u2705 Item already sold"}', '{value:"already_sold",label:"Item already sold"}'),
        ('{value:"other",label:"\u2753 Other"}', '{value:"other",label:"Other"}'),
    ]:
        c = c.replace(old, new)

    # ── Button/label text replacements ───────────────────────────────────────
    for old, new in [
        # Report button
        ('>\U0001f6a9 Report<', '>Report<'),
        ('>\U0001f6a9 Report this listing<', '>Report this listing<'),
        # Review labels
        ('"\u2b50 Review Buyer"', '"Review Buyer"'),
        ('"\u2b50 Review Seller"', '"Review Seller"'),
        ('"Submit \u2b50"', '"Submit Review"'),
        ('"Submit Review \u2b50"', '"Submit Review"'),
        # Edit button
        ('>\u270f\ufe0f Edit<', '>Edit<'),
        # Profile verified/unverified badges
        ('>\u2713 Verified<', '>Verified<'),
        ('>\u26a0 Unverified<', '>Unverified<'),
        # Password match
        ('"\u2713 Passwords match"', '"Passwords match"'),
        ('"\u2717 Passwords do not match"', '"Passwords do not match"'),
        # Role switch
        ('notify(`Switched to ${target} account \u2713`,"success")', 'notify(`Switched to ${target} account`,"success")'),
        # Sign out / delete
        ('>\U0001f6aa Sign Out<', '>Sign Out<'),
        ('>\U0001f5d1 Delete My Account<', '>Delete My Account<'),
        # Role badges
        ('{user.role==="seller"?"\U0001f3f7 Seller":"\U0001f6cd Buyer"}', '{user.role==="seller"?"Seller":"Buyer"}'),
        ('{user.role==="seller"?"\U0001f3f7 SELLER":"\U0001f6cd BUYER"}', '{user.role==="seller"?"SELLER":"BUYER"}'),
        ('{r.reviewer_role==="buyer"?"\U0001f6cd Buyer":"\U0001f3f7 Seller"}', '{r.reviewer_role==="buyer"?"Buyer":"Seller"}'),
        # RoleSwitcher button text
        ('{target==="seller"?"\U0001f3f7":"\U0001f6cd"} Switch to', 'Switch to'),
        # Sold channel
        ('{l.sold_channel==="platform"?"\U0001f6d2 Via WekaSoko":"\U0001f91d Elsewhere"}', '{l.sold_channel==="platform"?"Via WekaSoko":"Elsewhere"}'),
        # Status badges
        ('"pending_review"?"\u23f3 Review":', '"pending_review"?"Review":'),
        ('"rejected"?"\u274c Rejected":', '"rejected"?"Rejected":'),
        ('"pending_review"?"\u23f3 Under Review":', '"pending_review"?"Under Review":'),
        ('"needs_changes"?"\u270f\ufe0f Needs Changes":', '"needs_changes"?"Needs Changes":'),
        # Reveal/unlock buttons
        ('>\U0001f513 Reveal"', '>Reveal"'),
        ('>\U0001f513 Reveal<', '>Reveal<'),
        ('"\U0001f513 Reveal"', '"Reveal"'),
        ('"\U0001f513 Reveal Buyer \u2014 KSh 250"', '"Reveal Buyer \u2014 KSh 250"'),
        ('"\U0001f513 Pay KSh 250 to See Buyer Contact"', '"Pay KSh 250 to See Buyer Contact"'),
        ('">\U0001f513 Reveal Buyer \u2014 KSh 250<', '"Reveal Buyer \u2014 KSh 250<'),
        ('>\U0001f513 Reveal Buyer \u2014 KSh 250<', '>Reveal Buyer \u2014 KSh 250<'),
        ('>{l.linked_request_id?"Reveal Buyer":"Unlock"} \u2014 KSh 250<', '>{l.linked_request_id?"Reveal Buyer":"Unlock"} \u2014 KSh 250<'),
        ('>\U0001f513 {l.linked_request_id?"Reveal Buyer":"Unlock"} \u2014 KSh 250<', '>{l.linked_request_id?"Reveal Buyer":"Unlock"} \u2014 KSh 250<'),
        ('>\U0001f513 Accept \u2014 Pay KSh 250<', '>Accept \u2014 Pay KSh 250<'),
        # Chat buttons
        ('>\U0001f4ac Chat with Seller<', '>Chat with Seller<'),
        ('>\U0001f4ac View Messages<', '>View Messages<'),
        # Interest/lock in buttons
        ('>\U0001f525 I\'m Interested \u2014 Lock In<', '>I\'m Interested \u2014 Lock In<'),
        ('>\U0001f510 Buy with Escrow<', '>Buy with Escrow<'),
        ('>\U0001f513 Pay KSh 250 to See Buyer Contact<', '>Pay KSh 250 to See Buyer Contact<'),
        # Free unlock
        ('>\U0001f381 Free<', '>Free<'),
        # Sold button
        ('>\u2705 Sold<', '>Sold<'),
        # PostAd alerts
        ('>\u2705 Posting is free.', '>Posting is free.'),
        ('"Save Changes \u2705"', '"Save Changes"'),
        # PostRequest modal title
        ('title="\U0001f6d2 Post a Buyer Request"', 'title="Post a Buyer Request"'),
        # "I Have This" button
        ('>\U0001f4ec I Have This<', '>I Have This<'),
        # WhatBuyersWant h2
        ('>\U0001f6d2 What Buyers Want<', '>What Buyers Want<'),
        # Mobile requests heading
        ('>\U0001f6d2 What Buyers Want<', '>What Buyers Want<'),
        # Action required heading
        ('\U0001f525 Action Required \u2014 Buyers Waiting', 'Action Required \u2014 Buyers Waiting'),
        # Chat threads heading
        ('>\U0001f4ac Chat Threads<', '>Chat Threads<'),
        # Notifications heading
        ('>\U0001f514 All Notifications<', '>All Notifications<'),
        # Interests tab heading
        ('>\U0001f525 Listings You\'re Interested In (', '>Listings You\'re Interested In ('),
        # MarkSold modal title
        ('title="\u2705 Mark as Sold"', 'title="Mark as Sold"'),
        # Review section heading
        ('>\u2b50 Leave a Review (', '>Leave a Review ('),
        # Auth resend text
        ('>\u2713 Email resent! Check your inbox.<', '>Email resent! Check your inbox.<'),
        ('>\u2705 Email sent! Click the link in your inbox to activate your account.<', '>Email sent! Click the link in your inbox to activate your account.<'),
        # Send verification email
        ('"\U0001f4e7 Send Verification Email"', '"Send Verification Email"'),
        # Contact revealed
        ('">\u2705 Contact revealed \u2014 {l.seller_name', '">Contact revealed \u2014 {l.seller_name'),
        ('>\u2705 Contact revealed \u2014 {l.seller_name', '>Contact revealed \u2014 {l.seller_name'),
        # Lock hidden
        ('"\U0001f512 Contact hidden"', '"Contact hidden"'),
        ('">\U0001f512 Contact hidden"', '"Contact hidden"'),
        # Zoom hint
        ('>\U0001f50d Click to enlarge<', '>Click to enlarge<'),
        # Kenya flag in hero
        ('\U0001f1f0\U0001f1ea Kenya\'s Resell Platform', 'Kenya\'s Resell Platform'),
        # Mobile hero banner flag
        ('>\U0001f1f0\U0001f1ea Kenya\'s Resell Platform<', '>Kenya\'s Resell Platform<'),
        # View all arrow
        ('"View all →"', '"View all"'),
        ('"Post Request →"', '"Post Request"'),
        ('"Post Your First Ad →"', '"Post Your First Ad"'),
        # Back arrows in buttons
        ('>← Back to Marketplace<', '>Back to Marketplace<'),
        ('>← Back to Home<', '>Back to Home<'),
        ('>← Prev<', '>Prev<'),
        ('>Next →<', '>Next<'),
        # Pitch declined
        ('>\u2715 Declined<', '>Declined<'),
        # Mobile requests county tag
        ('>\U0001f4cd {r.county}<', '>' + s_pin(11) + ' {r.county}<'),
        # Buyers Want sidebar heading
        ('\U0001f6d2 Buyers Want', 'Buyers Want'),
        # Sort options in select dropdown
        ('"Price: Low → High"', '"Price: Low to High"'),
        ('"Price: High → Low"', '"Price: High to Low"'),
        # Mobile sort
        ('"Price ↑"', '"Price: Low"'),
        ('"Price ↓"', '"Price: High"'),
        # Mobile filter price sort options
        ('["price_asc","Price ↑"]', '["price_asc","Price: Low"]'),
        ('["price_desc","Price ↓"]', '["price_desc","Price: High"]'),
        # Grid/list toggle
        ('>⊞<', '>Grid<'),
        ('>☰<', '>List<'),
        # Clear filter
        ('>✕ Clear All Filters<', '>Clear All Filters<'),
        ('>✕ Clear<', '>Clear<'),
        ('>Clear ✕<', '>Clear<'),
        ('>✕ Clear filters<', '>Clear filters<'),
        # PWA dismiss
        ('>✕<', '>Close<'),
        # Lightbox arrows (text)
        ('← Prev', 'Prev'),
        ('Next →', 'Next'),
        # Contact hidden chat button
        ('>\U0001f512 Contact hidden<', '>Contact hidden<'),
        # Lock contact hidden display
        ('"\U0001f512 Contact hidden"', '"Contact hidden"'),
        # Filter clear
        ('>\u2715 Clear<', '>Clear<'),
    ]:
        c = c.replace(old, new)

    # ── PAY CHOICE CARDS ──────────────────────────────────────────────────────
    c = c.replace(
        '>\U0001f4b3 Pay KSh 250 Now<',
        '>Pay KSh 250 Now<'
    )
    c = c.replace(
        '>\u23f0 Post Anonymously (Pay Later)<',
        '>Post Anonymously (Pay Later)<'
    )
    # Pay choice icon span
    c = c.replace(
        '<span style={{fontSize:18}}>{payChoice==="now"?"\U0001f4b3":"\u23f0"}</span>',
        '<span>' + s_creditcard(18) + '</span>'
    )

    # ── Field error warning ───────────────────────────────────────────────────
    c = c.replace(
        '>\u26a0\ufe0f {fieldErrors.description}<',
        '>' + s_warn(11) + ' {fieldErrors.description}<'
    )

    # ── Response rate lightning ───────────────────────────────────────────────
    c = c.replace(
        '>\u26a1 {Math.round(l.response_rate)}%',
        '>' + s_lightning(11) + ' {Math.round(l.response_rate)}%'
    )

    # ── Inline location pins ──────────────────────────────────────────────────
    for emoji, replacement in [
        ('\U0001f4cd {l.location}', s_pin(11) + ' {l.location}'),
        ('\U0001f4cd {l.county||l.location||"Kenya"}', s_pin(11) + ' {l.county||l.location||"Kenya"}'),
        ('📍 {l.location}', s_pin(11) + ' {l.location}'),
        ('\U0001f4cd {r.county}', s_pin(11) + ' {r.county}'),
        ('📍 {r.county}', s_pin(11) + ' {r.county}'),
    ]:
        c = c.replace(emoji, replacement)

    # ── Inline view / interest counts ────────────────────────────────────────
    c = c.replace('\U0001f441 {l.view_count||0} views', s_eye(12) + ' {l.view_count||0} views')
    c = c.replace('\U0001f525 {l.interest_count||0} interested', s_fire(12) + ' {l.interest_count||0} interested')
    c = c.replace('\U0001f441 {l.view_count||0}', s_eye(12) + ' {l.view_count||0}')
    c = c.replace('\U0001f525 {l.interest_count||0}', s_fire(12) + ' {l.interest_count||0}')
    c = c.replace('👁 {l.view_count||0} views', s_eye(12) + ' {l.view_count||0} views')
    c = c.replace('🔥 {l.interest_count||0} interested', s_fire(12) + ' {l.interest_count||0} interested')
    c = c.replace('👁 {l.view_count||0}', s_eye(11) + ' {l.view_count||0}')
    c = c.replace('🔥 {l.interest_count||0}', s_fire(11) + ' {l.interest_count||0}')

    # ── Sold overlay check ────────────────────────────────────────────────────
    # "SOLD ✓" keep as-is (text check, not emoji)

    # ── Buyer interested banner ───────────────────────────────────────────────
    c = c.replace('>\U0001f525 Buyer Interested<', '>Buyer Interested<')

    # ── Shield: Stay safe tip ─────────────────────────────────────────────────
    c = c.replace('>\U0001f6e1\ufe0f Stay Safe on Weka Soko<', '>' + s_shield(14) + ' Stay Safe on Weka Soko<')
    c = c.replace('• \U0001f6a9 <strong>Something feel off?</strong>', '• <strong>Something feel off?</strong>')

    # ── Escrow info ───────────────────────────────────────────────────────────
    c = c.replace('>\U0001f510 <strong>Safe Escrow:</strong>', '>' + s_lock(14) + ' <strong>Safe Escrow:</strong>')

    # ── LARGE DECORATIVE ICONS ────────────────────────────────────────────────
    # 📦 Box (various sizes)
    box_repls = [
        ('<span style={{fontSize:44,opacity:.15}}>\U0001f4e6</span>', '<span style={{opacity:.15}}>' + s_box(44) + '</span>'),
        ('<span style={{fontSize:80,opacity:.15}}>\U0001f4e6</span>', '<span style={{opacity:.15}}>' + s_box(80) + '</span>'),
        ('<div style={{fontSize:48,marginBottom:12,opacity:.2}}>\U0001f4e6</div>', '<div style={{marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_box(48) + '</div>'),
        ('<div style={{fontSize:40,marginBottom:12,opacity:.2}}>\U0001f4e6</div>', '<div style={{marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_box(40) + '</div>'),
        ('<span style={{fontSize:40,position:"absolute",top:"50%",left:"50%",transform:"translate(-50%,-50%)",opacity:.15}}>\U0001f4e6</span>', '<span style={{position:"absolute",top:"50%",left:"50%",transform:"translate(-50%,-50%)",opacity:.15}}>' + s_box(40) + '</span>'),
        ('<div style={{width:"100%",height:"100%",display:"flex",alignItems:"center",justifyContent:"center",fontSize:20,opacity:.3}}>\U0001f4e6</div>', '<div style={{width:"100%",height:"100%",display:"flex",alignItems:"center",justifyContent:"center",opacity:.3}}>' + s_box(20) + '</div>'),
        ('<div style={{width:"100%",height:"100%",display:"flex",alignItems:"center",justifyContent:"center",fontSize:24,opacity:.3}}>\U0001f4e6</div>', '<div style={{width:"100%",height:"100%",display:"flex",alignItems:"center",justifyContent:"center",opacity:.3}}>' + s_box(24) + '</div>'),
        ('<div style={{width:"100%",height:"100%",display:"flex",alignItems:"center",justifyContent:"center",fontSize:28,opacity:.15}}>\U0001f4e6</div>', '<div style={{width:"100%",height:"100%",display:"flex",alignItems:"center",justifyContent:"center",opacity:.15}}>' + s_box(28) + '</div>'),
        ('<div style={{display:"flex",alignItems:"center",justifyContent:"center",height:"100%",fontSize:36,opacity:.15}}>\U0001f4e6</div>', '<div style={{display:"flex",alignItems:"center",justifyContent:"center",height:"100%",opacity:.15}}>' + s_box(36) + '</div>'),
        ('<div style={{display:"flex",alignItems:"center",justifyContent:"center",height:"100%",fontSize:40,opacity:.15}}>\U0001f4e6</div>', '<div style={{display:"flex",alignItems:"center",justifyContent:"center",height:"100%",opacity:.15}}>' + s_box(40) + '</div>'),
        ('<div style={{fontSize:48,marginBottom:12,opacity:.2}}>\U0001f4e6</div>', '<div style={{marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_box(48) + '</div>'),
    ]
    for old, new in box_repls:
        c = c.replace(old, new)

    # 🛒 Cart (various sizes)
    cart_repls = [
        ('<div style={{fontSize:28,marginBottom:8,opacity:.3}}>\U0001f6d2</div>', '<div style={{marginBottom:8,opacity:.3,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_cart(28) + '</div>'),
        ('<div style={{fontSize:40,marginBottom:12,opacity:.3}}>\U0001f6d2</div>', '<div style={{marginBottom:12,opacity:.3,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_cart(40) + '</div>'),
        ('<div style={{fontSize:44,marginBottom:12,opacity:.2}}>\U0001f6d2</div>', '<div style={{marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_cart(44) + '</div>'),
        ('<div style={{fontSize:40,marginBottom:12,opacity:.2}}>\U0001f6d2</div>', '<div style={{marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_cart(40) + '</div>'),
        ('<span style={{fontSize:20}}>\U0001f6d2</span>', '<span>' + s_cart(20) + '</span>'),
        ('<div style={{fontSize:22}}>\U0001f6d2</div>', '<div style={{display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_cart(22) + '</div>'),
    ]
    for old, new in cart_repls:
        c = c.replace(old, new)

    # 📬 Inbox
    inbox_repls = [
        ('<div style={{fontSize:40,marginBottom:12,opacity:.2}}>\U0001f4ec</div>', '<div style={{marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_inbox(40) + '</div>'),
        ('<div style={{fontSize:32,marginBottom:8,opacity:.3}}>\U0001f4ec</div>', '<div style={{marginBottom:8,opacity:.3,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_inbox(32) + '</div>'),
    ]
    for old, new in inbox_repls:
        c = c.replace(old, new)

    # ✅ large check
    c = c.replace('<div style={{fontSize:56,marginBottom:16,opacity:.15}}>\u2705</div>', '<div style={{marginBottom:16,opacity:.15,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_check(56) + '</div>')
    c = c.replace('<div style={{fontSize:48}}>\u2705</div>', '<div style={{display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_check(48) + '</div>')

    # ⭐ large star
    c = c.replace('<div style={{fontSize:48}}>\u2b50</div>', '<div style={{display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_star_filled(48) + '</div>')

    # ⭐ pending review star (24px)
    c = c.replace('<span style={{fontSize:24}}>\u2b50</span>', '<span>' + s_star_filled(24) + '</span>')

    # 🔥 large fire
    for old, new in [
        ('<div style={{fontSize:48,marginBottom:12,opacity:.2}}>\U0001f525</div>', '<div style={{marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_fire(48) + '</div>'),
        ('<div style={{fontSize:40,marginBottom:12,opacity:.2}}>\U0001f525</div>', '<div style={{marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_fire(40) + '</div>'),
        ('<span style={{fontSize:32}}>\U0001f525</span>', '<span>' + s_fire(32) + '</span>'),
    ]:
        c = c.replace(old, new)

    # 🔔 large bell
    for old, new in [
        ('<div style={{fontSize:48,marginBottom:12,opacity:.2}}>\U0001f514</div>', '<div style={{marginBottom:12,opacity:.2,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_bell(48) + '</div>'),
    ]:
        c = c.replace(old, new)

    # 📱 Phone (PWA banner)
    c = c.replace('<span style={{fontSize:28}}>\U0001f4f1</span>', '<span>' + s_phone(28) + '</span>')

    # 📧 Email (verification banner)
    c = c.replace('<span style={{fontSize:20}}>\U0001f4e7</span>', '<span>' + s_email(20) + '</span>')

    # ⚠️ Warning (verification section)
    c = c.replace('<span style={{fontSize:28,flexShrink:0}}>\u26a0\ufe0f</span>', '<span style={{flexShrink:0}}>' + s_warn(28) + '</span>')

    # 🔒 Lock (seller section)
    c = c.replace('<span style={{fontSize:30}}>\U0001f512</span>', '<span>' + s_lock(30) + '</span>')

    # 🔓 Unlock (revealed)
    c = c.replace('<span style={{fontSize:18}}>\U0001f513</span>', '<span>' + s_unlock(18) + '</span>')

    # 👤 User
    c = c.replace('<span style={{fontSize:16}}>\U0001f464</span>', '<span>' + s_user(16) + '</span>')

    # 📞 Phone
    c = c.replace('<span style={{fontSize:16}}>\U0001f4de</span>', '<span>' + s_phone(16) + '</span>')

    # ✉️ Email
    c = c.replace('<span style={{fontSize:16}}>\u2709\ufe0f</span>', '<span>' + s_email(16) + '</span>')

    # 🏷️ Tag (MarkSoldModal)
    c = c.replace('<div style={{fontSize:48, marginBottom:12}}>\U0001f3f7\ufe0f</div>', '<div style={{marginBottom:12,display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_tag(48) + '</div>')

    # 🤝 Handshake (MarkSoldModal)
    c = c.replace('<div style={{fontSize:22}}>\U0001f91d</div>', '<div style={{display:"flex",alignItems:"center",justifyContent:"center"}}>' + s_handshake(22) + '</div>')

    # 🚪 Door (sign out)
    c = c.replace('<span style={{fontSize:20}}>\U0001f6aa</span>', '<span>' + s_door(20) + '</span>')

    # 🗑 Trash (delete account)
    c = c.replace('<span style={{fontSize:20}}>\U0001f5d1</span>', '<span>' + s_trash(20) + '</span>')

    # ── Quick action icons (MobileDashboard) ──────────────────────────────────
    c = c.replace('{icon:"\U0001f4e6",label:"My Ads"', '{icon:"box",label:"My Ads"')
    c = c.replace('{icon:"\U0001f525",label:"Buyers"', '{icon:"fire",label:"Buyers"')
    c = c.replace('{icon:"\U0001f3c6",label:"Sold Items"', '{icon:"trophy",label:"Sold Items"')
    c = c.replace('{icon:"\U0001f6d2",label:"Requests",sub:`${myRequests.length} active`,action:()=>setMobSection("requests")}', '{icon:"cart",label:"Requests",sub:`${myRequests.length} active`,action:()=>setMobSection("requests")}')
    c = c.replace('{icon:"\u2764\ufe0f",label:"Saved"', '{icon:"heart",label:"Saved"')
    c = c.replace('{icon:"\U0001f6d2",label:"Requests",sub:`${myRequests.length} active`,action:()=>setMobSection("requests")},', '{icon:"cart",label:"Requests",sub:`${myRequests.length} active`,action:()=>setMobSection("requests")},')
    c = c.replace('{icon:"\U0001f4ac",label:"Messages"', '{icon:"chat",label:"Messages"')
    c = c.replace('{icon:"\U0001f514",label:"Alerts"', '{icon:"bell",label:"Alerts"')

    # Render quick actions icon div
    c = c.replace(
        '<div style={{fontSize:26,marginBottom:8}}>{a.icon}</div>',
        '<div style={{marginBottom:8,display:"flex",alignItems:"center",justifyContent:"center"}}>'
        '{a.icon==="box"?' + s_box(26) + ':'
        'a.icon==="fire"?' + s_fire(26) + ':'
        'a.icon==="trophy"?' + s_trophy(26) + ':'
        'a.icon==="cart"?' + s_cart(26) + ':'
        'a.icon==="heart"?' + s_heart(26) + ':'
        'a.icon==="chat"?' + s_chat(26) + ':'
        'a.icon==="bell"?' + s_bell(26) + ':null}'
        '</div>'
    )

    # ── Dashboard overview stat icons ─────────────────────────────────────────
    c = c.replace('{icon:"\U0001f4e6",label:"Total Ads"', '{icon:"box",label:"Total Ads"')
    c = c.replace('{icon:"\u2705",label:"Active"', '{icon:"check",label:"Active"')
    c = c.replace('{icon:"\U0001f3c6",label:"Sold"', '{icon:"trophy",label:"Sold"')
    c = c.replace('{icon:"\U0001f441",label:"Total Views"', '{icon:"eye",label:"Total Views"')
    c = c.replace('{icon:"\U0001f525",label:"Buyers Waiting"', '{icon:"fire",label:"Buyers Waiting"')
    c = c.replace('{icon:"\U0001f4ac",label:"Unread Msgs"', '{icon:"chat",label:"Unread Msgs"')
    c = c.replace('{icon:"\U0001f514",label:"Unread"', '{icon:"bell",label:"Unread"')

    # Render overview icons
    c = c.replace(
        '<div style={{fontSize:24,marginBottom:8}}>{s.icon}</div>',
        '<div style={{marginBottom:8,display:"flex",alignItems:"center"}}>'
        '{s.icon==="box"?' + s_box(24) + ':'
        's.icon==="check"?' + s_check(24) + ':'
        's.icon==="trophy"?' + s_trophy(24) + ':'
        's.icon==="eye"?' + s_eye(24) + ':'
        's.icon==="fire"?' + s_fire(24) + ':'
        's.icon==="chat"?' + s_chat(24) + ':'
        's.icon==="bell"?' + s_bell(24) + ':null}'
        '</div>'
    )

    # ── "How It Works" section ────────────────────────────────────────────────
    c = c.replace(
        '[["📝","Post for Free","No upfront cost. Photos, description, location — done in 2 minutes."],\n            ["💬","Chat Safely","Anonymous, moderated chat. Contact info hidden until unlock."],\n            ["🔥","Buyer Locks In","Serious buyers click \'I\'m Interested\'. You get notified instantly."],\n            ["💳","Pay KSh 250","Seller pays once to see buyer contact. Till 5673935. Non-refundable."],\n            ["🔐","Safe Escrow","Optional 7.5% escrow. Funds held until you confirm delivery."],\n            ["🏆","Deal Done","Leave a review. Build your seller reputation on the platform."]]',
        '[["doc","Post for Free","No upfront cost. Photos, description, location — done in 2 minutes."],\n            ["chat","Chat Safely","Anonymous, moderated chat. Contact info hidden until unlock."],\n            ["fire","Buyer Locks In","Serious buyers click \'I\'m Interested\'. You get notified instantly."],\n            ["card","Pay KSh 250","Seller pays once to see buyer contact. Till 5673935. Non-refundable."],\n            ["lock","Safe Escrow","Optional 7.5% escrow. Funds held until you confirm delivery."],\n            ["trophy","Deal Done","Leave a review. Build your seller reputation on the platform."]]'
    )
    # Render How It Works icons
    c = c.replace(
        '<div style={{fontSize:28,marginBottom:14}}>{icon}</div>',
        '<div style={{marginBottom:14,display:"flex",alignItems:"center"}}>'
        '{icon==="doc"?' + s_doc(28) + ':'
        'icon==="chat"?' + s_chat(28) + ':'
        'icon==="fire"?' + s_fire(28) + ':'
        'icon==="card"?' + s_creditcard(28) + ':'
        'icon==="lock"?' + s_lock(28) + ':'
        'icon==="trophy"?' + s_trophy(28) + ':null}'
        '</div>'
    )

    # ── Calendar/date icons in SoldSection ────────────────────────────────────
    c = c.replace('>\U0001f4c5 Listed<', '>' + s_cal(12) + ' Listed<')
    c = c.replace('>\u2705 Sold<', '>Sold<')
    c = c.replace('>\u23f1 Time to sell<', '>Time to sell<')

    # ── Trust bar checkmarks (HomeClient) ─────────────────────────────────────
    c = c.replace(
        '<span style={{color:"#1428A0",fontWeight:800,fontSize:16}}>✓</span>Free to post',
        '<span style={{color:"#1428A0",fontWeight:800,fontSize:16}}>' + s_check(14) + '</span>Free to post'
    )
    c = c.replace(
        '<span style={{color:"#1428A0",fontWeight:800,fontSize:16}}>✓</span>Anonymous chat',
        '<span style={{color:"#1428A0",fontWeight:800,fontSize:16}}>' + s_check(14) + '</span>Anonymous chat'
    )
    c = c.replace(
        '<span style={{color:"#1428A0",fontWeight:800,fontSize:16}}>✓</span>M-Pesa escrow',
        '<span style={{color:"#1428A0",fontWeight:800,fontSize:16}}>' + s_check(14) + '</span>M-Pesa escrow'
    )
    c = c.replace(
        '<span style={{color:"#fff",fontSize:16,fontWeight:800}}>✓</span>',
        '<span style={{color:"#fff",display:"inline-flex",alignItems:"center"}}>' + s_check(14) + '</span>'
    )

    # ── Mobile trust strip ────────────────────────────────────────────────────
    c = c.replace(
        '[["✓","Free to post"],["✓","Anonymous chat"],["✓","M-Pesa escrow"]]',
        '[["check","Free to post"],["check","Anonymous chat"],["check","M-Pesa escrow"]]'
    )
    c = c.replace(
        '<span key={txt}><span style={{color:"#1428A0",fontWeight:800}}>{icon}</span>{txt}</span>',
        '<span key={txt}><span style={{color:"#1428A0",display:"inline-flex",alignItems:"center"}}>{icon==="check"?' + s_check(14) + ':icon}</span>{txt}</span>'
    )

    # ── Password show/hide buttons ────────────────────────────────────────────
    c = c.replace(
        '>{showCurrent?"\U0001f648":"\U0001f441"}<',
        '>{showCurrent?' + eyeoff_fn(16) + ':' + s_eye(16) + '}<'
    )
    c = c.replace(
        '>{showNew?"\U0001f648":"\U0001f441"}<',
        '>{showNew?' + eyeoff_fn(16) + ':' + s_eye(16) + '}<'
    )

    # ── Pagination / nav arrows in pager component ────────────────────────────
    # Pager: ← and → arrows kept as text (they are HTML chars not emojis)

    # ── Remove remaining bare emoji chars ─────────────────────────────────────
    # After all context-aware replacements, sweep for any remaining
    # emoji chars with generic replacements

    # 🔥 fire remaining
    c = c.replace('\U0001f525', s_fire(16))
    # 🛒 cart remaining
    c = c.replace('\U0001f6d2', s_cart(16))
    # 📦 box remaining
    c = c.replace('\U0001f4e6', s_box(16))
    # ✅ check remaining
    c = c.replace('\u2705', s_check(16))
    # ⚠️ warning remaining
    c = c.replace('\u26a0\ufe0f', s_warn(16))
    c = c.replace('\u26a0', s_warn(16))
    # ❌ x remaining
    c = c.replace('\u274c', s_x(16))
    # 💬 chat remaining
    c = c.replace('\U0001f4ac', s_chat(16))
    # 🔒 lock remaining
    c = c.replace('\U0001f512', s_lock(16))
    # 🔓 unlock remaining
    c = c.replace('\U0001f513', s_unlock(16))
    # ⭐ star remaining
    c = c.replace('\u2b50', s_star_filled(16))
    # ★ and ☆ — keep these as text (used for rating display strings)
    # 🏷 tag remaining
    c = c.replace('\U0001f3f7\ufe0f', s_tag(16))
    c = c.replace('\U0001f3f7', s_tag(16))
    # 🛍 bag remaining
    c = c.replace('\U0001f6cd\ufe0f', s_bag(16))
    c = c.replace('\U0001f6cd', s_bag(16))
    # 📬 inbox remaining
    c = c.replace('\U0001f4ec', s_inbox(16))
    # 🔔 bell remaining
    c = c.replace('\U0001f514', s_bell(16))
    # 📍 pin remaining
    c = c.replace('\U0001f4cd', s_pin(16))
    c = c.replace('📍', s_pin(11))
    # 👁 eye remaining
    c = c.replace('\U0001f441', s_eye(16))
    c = c.replace('👁', s_eye(11))
    # 🎉 party remaining
    c = c.replace('\U0001f389', s_party(16))
    # 🏆 trophy remaining
    c = c.replace('\U0001f3c6', s_trophy(16))
    # 💳 credit card remaining
    c = c.replace('\U0001f4b3', s_creditcard(16))
    # 📧 email remaining
    c = c.replace('\U0001f4e7', s_email(16))
    # 📞 phone remaining
    c = c.replace('\U0001f4de', s_phone(16))
    # 👤 user remaining
    c = c.replace('\U0001f464', s_user(16))
    # 🔓 unlock remaining (already done above)
    # 🛡 shield remaining
    c = c.replace('\U0001f6e1\ufe0f', s_shield(16))
    c = c.replace('\U0001f6e1', s_shield(16))
    # 🚫 ban remaining
    c = c.replace('\U0001f6ab', s_ban(16))
    # ⛔ ban remaining
    c = c.replace('\u26d4', s_ban(16))
    # 🔑 key → lock
    c = c.replace('\U0001f511', s_lock(16))
    # 🚨 siren → flag
    c = c.replace('\U0001f6a8', s_flag(16))
    # 🎭 theater → tag
    c = c.replace('\U0001f3ad', s_tag(16))
    # 💰 money → dollar
    c = c.replace('\U0001f4b0', s_dollar(16))
    # 📂 folder → doc
    c = c.replace('\U0001f4c2', s_doc(16))
    # ❓ question → info
    c = c.replace('\u2753', s_info(16))
    # ⚡ lightning remaining
    c = c.replace('\u26a1', s_lightning(16))
    # ⏰/⏱/⏳ clock remaining
    c = c.replace('\u23f0', s_clock(16))
    c = c.replace('\u23f1', s_clock(16))
    c = c.replace('\u23f3', s_clock(16))
    # 🗓️ calendar remaining
    c = c.replace('\U0001f4c5', s_cal(16))
    # 🚪 door remaining
    c = c.replace('\U0001f6aa', s_door(16))
    # 🗑 trash remaining
    c = c.replace('\U0001f5d1\ufe0f', s_trash(16))
    c = c.replace('\U0001f5d1', s_trash(16))
    # ✏️ pencil remaining
    c = c.replace('\u270f\ufe0f', s_edit(16))
    c = c.replace('\u270f', s_edit(16))
    # 🔍 search remaining
    c = c.replace('\U0001f50d', s_search(16))
    # ↺ refresh remaining
    c = c.replace('\u21ba', s_refresh(16))
    # ✕ × x remaining (small button chars - not emojis but clean up)
    # ✓ checkmark remaining (not emoji, keep)
    # ✗ remaining
    c = c.replace('\u2717', s_x(16))
    # ✕ remaining (0x2715)
    c = c.replace('\u2715', s_x(14))
    # ↑ up arrow
    c = c.replace('\u2191', '')
    # ↓ down arrow
    c = c.replace('\u2193', '')
    # → right arrow (in buttons text we already replaced, remaining are in options)
    # Keep → in option text for sort (already replaced above)
    # 🤝 handshake remaining
    c = c.replace('\U0001f91d', s_handshake(16))
    # 🎁 gift remaining
    c = c.replace('\U0001f381', s_gift(16))
    # 🛠 settings remaining
    c = c.replace('\U0001f6e0\ufe0f', s_settings(16))
    c = c.replace('\U0001f6e0', s_settings(16))
    # 🙈 eye-off remaining
    c = c.replace('\U0001f648', eyeoff_fn(16))
    # 🏷️ tag (already done)
    # 📝 doc remaining
    c = c.replace('\U0001f4dd', s_doc(16))
    # 🇰🇪 Kenya flag remaining
    c = c.replace('\U0001f1f0\U0001f1ea', s_globe(16))
    # ℹ️ info remaining
    c = c.replace('\u2139\ufe0f', s_info(16))
    c = c.replace('\u2139', s_info(16))
    # 🔩 wrench/settings
    c = c.replace('\U0001f529', s_settings(16))

    return c


# ── MAIN ──────────────────────────────────────────────────────────────────────
import re

def has_emojis(content):
    """Check if file still has emoji characters."""
    emoji_pattern = re.compile(
        u'[\U0001F600-\U0001F64F'
        u'\U0001F300-\U0001F5FF'
        u'\U0001F680-\U0001F6FF'
        u'\U0001F1E0-\U0001F1FF'
        u'\U00002702-\U000027B0'
        u'\U0001F900-\U0001F9FF'
        u'\U0001FA00-\U0001FA6F'
        u'\U0001FA70-\U0001FAFF'
        u'\u2764'
        u'\u2753'
        u'\u274c'
        u'\u26d4'
        u'\u2b50'
        u']', flags=re.UNICODE)
    return bool(emoji_pattern.search(content))

if __name__ == "__main__":
    files = [
        r"C:\Users\USER\Documents\Weka Soko\weka-soko-nextjs\components\all.jsx",
        r"C:\Users\USER\Documents\Weka Soko\weka-soko-nextjs\app\HomeClient.jsx",
    ]

    for filepath in files:
        print(f"Processing: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Apply all replacements
        def eyeoff_16(sz=16):
            return f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{{{display:"inline",verticalAlign:"middle"}}}}><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>'

        updated = process_file_str(content, eyeoff_16)

        remaining = has_emojis(updated)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated)

        print(f"  Done. Emojis remaining: {remaining}")
        if updated != original:
            print(f"  File was modified.")
        else:
            print(f"  WARNING: No changes made!")

print("All done!")
