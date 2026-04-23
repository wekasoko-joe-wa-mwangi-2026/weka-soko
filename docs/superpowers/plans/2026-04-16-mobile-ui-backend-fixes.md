# Mobile UI & Backend Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix 20 issues across the frontend mobile UI, backend routes/DB, and admin panel — covering two-column listings grid, Hot Right Now snap scroll, buyer request approval, voucher column bug, audit log, notifications, swipe feed contact reveal, report button, filter overlay, dashboard management buttons, collection locations, and maintenance mode.

**Architecture:** All frontend changes are in `weka-soko-nextjs/components/all.jsx` (CSS + JSX) and `app/HomeClient.jsx`. Backend changes are in individual route files and `migrate_all.js`. Admin panel changes are in `weka-soko-admin/src/App.jsx`. Changes are grouped by subsystem to minimise merge conflicts and allow independent commits.

**Tech Stack:** Next.js 14 App Router, Node.js/Express, PostgreSQL (Railway), React (admin panel), Socket.io push, Web Push (VAPID)

---

## File Map

| File | Changes |
|---|---|
| `weka-soko-backend/src/db/migrate_all.js` | Add `description` to vouchers, `precise_location` to listings, `pending_review` default to buyer_requests |
| `weka-soko-backend/src/routes/listings.js` | Add save notification; expose `precise_location` when unlocked |
| `weka-soko-backend/src/routes/requests.js` | Change default status to `pending_review`; add admin endpoints |
| `weka-soko-backend/src/routes/admin.js` | Add buyer-request review endpoints; add missing `auditLog()` calls throughout |
| `weka-soko-nextjs/components/all.jsx` | All mobile UI JSX + inline CSS changes (tasks 6–18) |
| `weka-soko-nextjs/app/globals.css` | `.mob-cards`, `.mob-lcard` CSS for 2-col grid |
| `weka-soko-admin/src/App.jsx` | Add voucher description field; add buyer requests queue |

---

## Task 1: Fix Voucher `description` Column (DB + Admin)

**Files:**
- Modify: `weka-soko-backend/src/db/migrate_all.js` (vouchers section, ~line 269)
- Modify: `weka-soko-admin/src/App.jsx` (voucher creation form)

**Problem:** The `vouchers` table has no `description` column. The route at `POST /api/vouchers` inserts `description` and the `GET /:code` route reads `voucher.description` — both crash with `column "description" does not exist`.

- [ ] **Step 1: Add `description` column to migration**

In `migrate_all.js`, find the vouchers section (~line 269) and add one `addCol` line after the existing voucher addCols:

```javascript
// Existing lines:
await addCol("vouchers","active","BOOLEAN DEFAULT TRUE");
await addCol("vouchers","discount_percent","INT DEFAULT 0");
// ADD THIS:
await addCol("vouchers","description","TEXT");
```

- [ ] **Step 2: Add description field to admin voucher creation form**

In `App.jsx`, find the `VouchersSection` component (search for `VouchersSection` or `Post /api/vouchers`). In the voucher creation form, add a description input. Find the form state initialisation and add `description: ""`. Then in the form JSX, add:

```jsx
<FF label="Description (optional)">
  <input className="inp" placeholder="e.g. Free unlock for verified sellers" 
    value={form.description} onChange={e=>setForm(p=>({...p,description:e.target.value}))}/>
</FF>
```

Include `description: form.description` in the POST body alongside the other fields.

- [ ] **Step 3: Deploy backend — Railway auto-deploys on push to main**

```bash
cd "weka-soko-backend"
git add src/db/migrate_all.js
git commit -m "fix: add description column to vouchers table"
git push
```

- [ ] **Step 4: Deploy admin panel**

```bash
cd "weka-soko-admin"
git add src/App.jsx
git commit -m "feat: add description field to voucher creation form"
git push
```

---

## Task 2: Add Precise Location Column to Listings

**Files:**
- Modify: `weka-soko-backend/src/db/migrate_all.js` (listings addCols section)
- Modify: `weka-soko-backend/src/routes/listings.js` (POST, PATCH, GET queries)

**Purpose:** Sellers can enter a precise collection point that is revealed only alongside their contact info when unlocked.

- [ ] **Step 1: Add `precise_location` column to migration**

In `migrate_all.js`, after the existing listings `addCol` lines (~line 107), add:

```javascript
await addCol("listings","precise_location","TEXT");
```

- [ ] **Step 2: Accept `precise_location` in POST /api/listings**

In `listings.js`, in the `router.post("/", ...)` handler, destructure `precise_location` from `req.body`. Add it to the INSERT query and values array. The INSERT currently sets location and county — add precise_location similarly.

Find the INSERT statement (~line 240 area) and ensure it includes:
```javascript
const { title, description, reason_for_sale, category, subcat, price, location, county, precise_location } = req.body;
```

And in the INSERT SQL, add `precise_location` to the column list and `precise_location || null` to the values.

- [ ] **Step 3: Return `precise_location` only when unlocked in GET queries**

In the main listings GET query SQL (~line 54), add to the SELECT:
```sql
CASE WHEN l.is_unlocked THEN l.precise_location ELSE NULL END AS precise_location,
```

Do the same in `GET /api/listings/seller/mine` and `GET /api/listings/:id`.

- [ ] **Step 4: Accept `precise_location` in PATCH /api/listings/:id**

In the update handler, destructure and include `precise_location` in the SET clause.

- [ ] **Step 5: Commit backend**

```bash
cd "weka-soko-backend"
git add src/db/migrate_all.js src/routes/listings.js
git commit -m "feat: add precise_location field to listings (revealed on unlock)"
git push
```

---

## Task 3: Add Save Notification — Seller Notified When Buyer Saves

**Files:**
- Modify: `weka-soko-backend/src/routes/listings.js` (save toggle route, ~line 469)

**Purpose:** When a buyer saves a listing, the seller receives a push notification. Tapping it opens chat.

- [ ] **Step 1: Update save route to notify seller**

Find the `POST /:id/save` route (~line 469). After the successful save (`res.json({ saved: true })`), add seller notification. The route needs access to `_io` and `_sendPushToUser`. Check if `listings.js` already has a `setIO` / `setPushSender` pattern. It does not currently — add the pattern at the top of the file (after the `router` declaration):

```javascript
let _io = null;
let _sendPushToUser = null;
router.setIO = (io) => { _io = io; };
router.setPushSender = (fn) => { _sendPushToUser = fn; };
```

Then update the save route:

```javascript
router.post("/:id/save", requireAuth, async (req, res, next) => {
  try {
    const { rows } = await query(
      `SELECT id FROM saved_listings WHERE user_id=$1 AND listing_id=$2`,
      [req.user.id, req.params.id]
    );
    if (rows.length) {
      await query(`DELETE FROM saved_listings WHERE user_id=$1 AND listing_id=$2`, [req.user.id, req.params.id]);
      return res.json({ saved: false });
    }
    await query(
      `INSERT INTO saved_listings (user_id, listing_id) VALUES ($1,$2) ON CONFLICT DO NOTHING`,
      [req.user.id, req.params.id]
    );
    res.json({ saved: true });

    // Async: notify seller
    (async () => {
      try {
        const { rows: ls } = await query(
          `SELECT l.title, l.seller_id FROM listings l WHERE l.id=$1`,
          [req.params.id]
        );
        if (!ls.length || ls[0].seller_id === req.user.id) return;
        const { title, seller_id } = ls[0];
        const notif = {
          type: "buyer_saved",
          title: "Someone saved your listing!",
          body: `A buyer saved "${title}". Start a conversation to close the deal.`,
          data: JSON.stringify({ listing_id: req.params.id, action: "open_chat" })
        };
        await query(
          `INSERT INTO notifications (user_id,type,title,body,data) VALUES ($1,$2,$3,$4,$5)`,
          [seller_id, notif.type, notif.title, notif.body, notif.data]
        );
        if (_io) _io.to(`user:${seller_id}`).emit("notification", notif);
        if (_sendPushToUser) _sendPushToUser(seller_id, {
          title: notif.title,
          body: notif.body,
          tag: "buyer_saved",
          url: `/dashboard?tab=chats&listing=${req.params.id}`
        }).catch(() => {});
      } catch (e) { console.error("[save-notify]", e.message); }
    })();
  } catch (err) { next(err); }
});
```

- [ ] **Step 2: Wire up setIO and setPushSender in index.js**

In `src/index.js`, find where `listingsRouter.setIO` is called (check if it exists). If not, add it after the other `setIO` calls:

```javascript
listingsRouter.setIO(io);
listingsRouter.setPushSender(sendPushToUser);
```

- [ ] **Step 3: Commit**

```bash
cd "weka-soko-backend"
git add src/routes/listings.js src/index.js
git commit -m "feat: notify seller when buyer saves their listing"
git push
```

---

## Task 4: Fix Audit Log — Add Missing `auditLog()` Calls in admin.js

**Files:**
- Modify: `weka-soko-backend/src/routes/admin.js`

**Problem:** Many admin actions (listing approve/reject, user suspend, maintenance toggle, unlock grant, voucher toggle) do not call `auditLog()`. The service exists and works; it's just not being called.

- [ ] **Step 1: Add auditLog to listing moderation approve**

Find `router.post("/moderation/:id/approve", ...)`. After the successful DB update, add:
```javascript
await auditLog({ adminId: req.user.id, adminEmail: req.user.email, action: "listing_approved", targetType: "listing", targetId: req.params.id, ip: req.ip });
```

- [ ] **Step 2: Add auditLog to listing moderation reject**

Find `router.post("/moderation/:id/reject", ...)`. After the DB update:
```javascript
await auditLog({ adminId: req.user.id, adminEmail: req.user.email, action: "listing_rejected", targetType: "listing", targetId: req.params.id, details: { reason: req.body.reason }, ip: req.ip });
```

- [ ] **Step 3: Add auditLog to user suspend/unsuspend**

Find the user suspend route (search `is_suspended`). Add:
```javascript
await auditLog({ adminId: req.user.id, adminEmail: req.user.email, action: suspended ? "user_suspended" : "user_unsuspended", targetType: "user", targetId: req.params.id, ip: req.ip });
```

- [ ] **Step 4: Add auditLog to maintenance mode toggle**

Find the maintenance mode route. Add:
```javascript
await auditLog({ adminId: req.user.id, adminEmail: req.user.email, action: "maintenance_mode_" + newValue, targetType: "platform", targetId: "maintenance_mode", ip: req.ip });
```

- [ ] **Step 5: Add auditLog to admin unlock grant**

Find the admin unlock / free unlock route. Add:
```javascript
await auditLog({ adminId: req.user.id, adminEmail: req.user.email, action: "admin_unlock_granted", targetType: "listing", targetId: req.params.id, details: { discount: req.body.discount }, ip: req.ip });
```

- [ ] **Step 6: Add auditLog to voucher create**

Find `POST /api/admin/vouchers` or the admin vouchers route. Add after successful insert:
```javascript
await auditLog({ adminId: req.user.id, adminEmail: req.user.email, action: "voucher_created", targetType: "voucher", targetId: result.rows[0].id, details: { code: req.body.code }, ip: req.ip });
```

- [ ] **Step 7: Add auditLog to voucher toggle**

Find the voucher toggle route. Add:
```javascript
await auditLog({ adminId: req.user.id, adminEmail: req.user.email, action: "voucher_toggled", targetType: "voucher", targetId: req.params.id, ip: req.ip });
```

- [ ] **Step 8: Commit**

```bash
cd "weka-soko-backend"
git add src/routes/admin.js
git commit -m "fix: add auditLog calls to all admin actions"
git push
```

---

## Task 5: Buyer Request Admin Approval Workflow

**Files:**
- Modify: `weka-soko-backend/src/db/migrate_all.js` (buyer_requests, add approved status support)
- Modify: `weka-soko-backend/src/routes/requests.js` (default status, filter approved only on public GET)
- Modify: `weka-soko-backend/src/routes/admin.js` (add review endpoints)
- Modify: `weka-soko-admin/src/App.jsx` (add Buyer Requests queue section)

- [ ] **Step 1: Add `approved` and `rejected` as valid request statuses in migration**

In `migrate_all.js`, add after the buyer_requests table creation:
```javascript
await addCol("buyer_requests","approved_by","UUID REFERENCES users(id) ON DELETE SET NULL");
await addCol("buyer_requests","approved_at","TIMESTAMPTZ");
await addCol("buyer_requests","rejection_reason","TEXT");
```

- [ ] **Step 2: Change default status of new buyer requests to `pending_review`**

In `requests.js`, in the `router.post("/", ...)` handler, find the INSERT SQL for buyer_requests. Change `status='active'` to `status='pending_review'` in the INSERT:

```javascript
INSERT INTO buyer_requests (user_id,title,description,budget,min_price,max_price,county,category,subcat,keywords,photos,status)
VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,'pending_review') RETURNING *
```

- [ ] **Step 3: Update public GET to only show approved requests**

In `requests.js`, in the `router.get("/", ...)` handler, change the status condition from `r.status = 'active'` to `r.status IN ('active','approved')` — or simply keep `active` but only set `active` after admin approval. Since we changed the default to `pending_review`, just keep the condition as `r.status = 'active'` — admin approval will set it to `active`.

- [ ] **Step 4: Add notify requester on submission**

After saving a new buyer request in `router.post("/", ...)`, add:
```javascript
// Already happens via matching.service — ensure we also notify the user their request is pending
await query(
  `INSERT INTO notifications (user_id,type,title,body,data) VALUES ($1,'request_pending','Request Submitted for Review',$2,$3)`,
  [req.user.id, `Your request "${title}" has been submitted and is awaiting admin review.`, JSON.stringify({ request_id: result.rows[0].id })]
);
```

- [ ] **Step 5: Add admin endpoints to admin.js**

Add these two routes to `admin.js`:

```javascript
// GET /api/admin/requests — list pending buyer requests
router.get("/requests", async (req, res, next) => {
  try {
    const { status = "pending_review" } = req.query;
    const { rows } = await query(
      `SELECT r.*, u.name AS requester_name, u.email AS requester_email
       FROM buyer_requests r JOIN users u ON u.id=r.user_id
       WHERE r.status=$1 ORDER BY r.created_at DESC LIMIT 100`,
      [status]
    );
    res.json(rows);
  } catch (err) { next(err); }
});

// POST /api/admin/requests/:id/approve
router.post("/requests/:id/approve", async (req, res, next) => {
  try {
    const { rows } = await query(
      `UPDATE buyer_requests SET status='active', approved_by=$1, approved_at=NOW() WHERE id=$2 RETURNING *`,
      [req.user.id, req.params.id]
    );
    if (!rows.length) return res.status(404).json({ error: "Request not found" });
    const r = rows[0];
    const notif = { type: "request_approved", title: "Your buyer request is live!", body: `Your request "${r.title}" has been approved and is now visible to sellers.` };
    await query(`INSERT INTO notifications (user_id,type,title,body,data) VALUES ($1,$2,$3,$4,$5)`,
      [r.user_id, notif.type, notif.title, notif.body, JSON.stringify({ request_id: r.id })]);
    pushNotification(r.user_id, notif);
    await auditLog({ adminId: req.user.id, adminEmail: req.user.email, action: "request_approved", targetType: "buyer_request", targetId: req.params.id, ip: req.ip });
    res.json({ success: true });
  } catch (err) { next(err); }
});

// POST /api/admin/requests/:id/reject
router.post("/requests/:id/reject", async (req, res, next) => {
  try {
    const { reason } = req.body;
    const { rows } = await query(
      `UPDATE buyer_requests SET status='rejected', rejection_reason=$1 WHERE id=$2 RETURNING *`,
      [reason || "Does not meet guidelines", req.params.id]
    );
    if (!rows.length) return res.status(404).json({ error: "Request not found" });
    const r = rows[0];
    const notif = { type: "request_rejected", title: "Buyer request not approved", body: `Your request "${r.title}" was not approved: ${reason || "Does not meet guidelines"}` };
    await query(`INSERT INTO notifications (user_id,type,title,body,data) VALUES ($1,$2,$3,$4,$5)`,
      [r.user_id, notif.type, notif.title, notif.body, JSON.stringify({ request_id: r.id })]);
    pushNotification(r.user_id, notif);
    await auditLog({ adminId: req.user.id, adminEmail: req.user.email, action: "request_rejected", targetType: "buyer_request", targetId: req.params.id, details: { reason }, ip: req.ip });
    res.json({ success: true });
  } catch (err) { next(err); }
});
```

- [ ] **Step 6: Add Buyer Requests queue to admin panel**

In `App.jsx`, add `"Buyer Requests"` to the sidebar nav items array. Create a `BuyerRequestsQueue` component:

```jsx
function BuyerRequestsQueue({ token, notify }) {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [rejectId, setRejectId] = useState(null);
  const [rejectReason, setRejectReason] = useState("");

  const load = () => {
    setLoading(true);
    req("/api/admin/requests?status=pending_review", {}, token)
      .then(d => setRequests(d))
      .catch(() => {})
      .finally(() => setLoading(false));
  };
  useEffect(() => { load(); }, [token]);

  const approve = async (id) => {
    await req(`/api/admin/requests/${id}/approve`, { method: "POST" }, token);
    setRequests(p => p.filter(r => r.id !== id));
    notify("Request approved and live!", true);
  };

  const reject = async (id) => {
    if (!rejectReason.trim()) { notify("Enter a rejection reason", false); return; }
    await req(`/api/admin/requests/${id}/reject`, { method: "POST", body: JSON.stringify({ reason: rejectReason }) }, token);
    setRequests(p => p.filter(r => r.id !== id));
    setRejectId(null); setRejectReason("");
    notify("Request rejected.", true);
  };

  if (loading) return <div style={{ textAlign: "center", padding: 60 }}><Spin /></div>;
  return <>
    {requests.length === 0
      ? <div className="empty"><div style={{ fontWeight: 700, fontSize: 16 }}>No pending buyer requests</div></div>
      : requests.map(r => <div key={r.id} className="card" style={{ marginBottom: 12 }}>
          <div style={{ fontWeight: 700, fontSize: 14, marginBottom: 4 }}>{r.title}</div>
          <div style={{ fontSize: 12, color: "#636363", marginBottom: 4 }}>By {r.requester_name} · {ago(r.created_at)}</div>
          {r.budget && <div style={{ fontSize: 13, color: "#1428A0", fontWeight: 700, marginBottom: 4 }}>Budget: KSh {Number(r.budget).toLocaleString("en-KE")}</div>}
          <div style={{ fontSize: 13, color: "#333", marginBottom: 10, lineHeight: 1.6 }}>{r.description}</div>
          {rejectId === r.id
            ? <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                <input className="inp" style={{ flex: 1 }} placeholder="Rejection reason" value={rejectReason} onChange={e => setRejectReason(e.target.value)} />
                <button className="btn br sm" onClick={() => reject(r.id)}>Confirm Reject</button>
                <button className="btn bs sm" onClick={() => setRejectId(null)}>Cancel</button>
              </div>
            : <div style={{ display: "flex", gap: 8 }}>
                <button className="btn bp sm" onClick={() => approve(r.id)}>Approve</button>
                <button className="btn br sm" onClick={() => setRejectId(r.id)}>Reject</button>
              </div>}
        </div>
      )}
  </>;
}
```

Render `<BuyerRequestsQueue>` when the active nav is `"Buyer Requests"`.

- [ ] **Step 7: Commit everything**

```bash
cd "weka-soko-backend"
git add src/db/migrate_all.js src/routes/requests.js src/routes/admin.js
git commit -m "feat: buyer requests require admin approval before going live"
git push

cd ../weka-soko-admin"
git add src/App.jsx
git commit -m "feat: add buyer requests approval queue to admin panel"
git push
```

---

## Task 6: Mobile Maintenance Mode Banner

**Files:**
- Modify: `weka-soko-nextjs/components/all.jsx` (MobileLayout component)
- Modify: `weka-soko-nextjs/app/HomeClient.jsx` (pass maintenanceMsg to MobileLayout)

**Problem:** The desktop layout shows a yellow banner when maintenance mode is on, but MobileLayout doesn't receive or display it. Also, when maintenance is on, listings are currently hidden — they should remain visible with just a banner notice.

- [ ] **Step 1: Pass `maintenanceMsg` to MobileLayout**

In `HomeClient.jsx`, find where `<MobileLayout .../>` is rendered. Add `maintenanceMsg={maintenanceMsg}` as a prop.

- [ ] **Step 2: Fix listings clear on maintenance**

In `HomeClient.jsx` at line ~305, find:
```javascript
if(e.maintenance){setMaintenanceMsg(e.maintenance);if(!silent)setListings([]);}
```
Change to:
```javascript
if(e.maintenance){setMaintenanceMsg(e.maintenance);}
```
This stops listings from being wiped when maintenance mode is active.

- [ ] **Step 3: Render maintenance banner in MobileLayout**

In `all.jsx`, find the `MobileLayout` function. Add `maintenanceMsg` to its prop destructuring. Just after the `mob-topbar` div closes (after ~line 3958), insert the banner:

```jsx
{maintenanceMsg && (
  <div style={{background:"#FEF3C7",borderBottom:"2px solid #F59E0B",color:"#92400E",padding:"10px 16px",textAlign:"center",fontSize:13,fontWeight:600,display:"flex",alignItems:"center",justifyContent:"center",gap:8,lineHeight:1.5}}>
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#92400E" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
    {maintenanceMsg}
  </div>
)}
```

- [ ] **Step 4: Commit**

```bash
cd "weka-soko-nextjs"
git add app/HomeClient.jsx components/all.jsx
git commit -m "fix: show maintenance banner on mobile; stop hiding listings during maintenance"
git push
```

---

## Task 7: Mobile Two-Column Listings Grid

**Files:**
- Modify: `weka-soko-nextjs/app/globals.css` (`.mob-cards`, `.mob-lcard`, `.mob-lcard-img`, `.mob-lcard-body`)

**Current state:** `.mob-cards` uses `grid-template-columns:repeat(auto-fill,minmax(340px,1fr))` — on phones narrower than 680px this collapses to 1 column. Below 600px it forces 1 column.

**Goal:** Always show 2 columns on mobile. Convert card from horizontal (row: image-left, text-right) to vertical (column: image-top, text-bottom).

- [ ] **Step 1: Update `.mob-cards` to always 2 columns**

In `globals.css`, find `.mob-cards` (~line 503) and replace:
```css
.mob-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:0;border-top:1px solid #F0F0F0;}
```
With:
```css
.mob-cards{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px 12px 0;border-top:none;}
```

- [ ] **Step 2: Update `.mob-lcard` to vertical card layout**

Find `.mob-lcard` (~line 504) and replace:
```css
.mob-lcard{
  background:#fff;display:flex;gap:14px;padding:16px 18px;
  border-radius:16px;
  ...
}
```
With:
```css
.mob-lcard{
  background:#fff;display:flex;flex-direction:column;gap:0;padding:0;
  border-radius:14px;overflow:hidden;
  box-shadow:0 1px 4px rgba(0,0,0,.06),0 2px 8px rgba(0,0,0,.04);
  transition:transform .2s ease,box-shadow .2s ease;
}
.mob-lcard:hover{transform:translateY(-2px);box-shadow:0 4px 16px rgba(0,0,0,.1);}
.mob-lcard:active{transform:scale(.97)!important;box-shadow:none;}
```

- [ ] **Step 3: Update `.mob-lcard-img` to full-width square**

Find `.mob-lcard-img` (~line 516) and replace:
```css
.mob-lcard-img{width:110px;height:100px;border-radius:14px;...}
```
With:
```css
.mob-lcard-img{width:100%;aspect-ratio:4/3;border-radius:0;object-fit:cover;flex-shrink:0;background:#F0F0F0;overflow:hidden;}
```

- [ ] **Step 4: Update `.mob-lcard-body` to compact padded block**

Find `.mob-lcard-body` (~line 519) and replace:
```css
.mob-lcard-body{flex:1;min-width:0;display:flex;flex-direction:column;gap:4px;}
```
With:
```css
.mob-lcard-body{flex:1;min-width:0;display:flex;flex-direction:column;gap:3px;padding:10px 10px 12px;}
```

- [ ] **Step 5: Tighten font sizes for 2-column layout**

Find and update these classes:
```css
.mob-lcard-cat{font-size:10px;font-weight:600;color:#AAAAAA;text-transform:uppercase;letter-spacing:.06em;}
.mob-lcard-title{font-size:13px;font-weight:700;color:#1A1A1A;line-height:1.3;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;}
.mob-lcard-price{font-size:15px;font-weight:800;color:#1428A0;}
.mob-lcard-meta{font-size:10px;color:#AAAAAA;display:flex;gap:6px;margin-top:2px;flex-wrap:wrap;}
```

- [ ] **Step 6: Remove the old 600px override that forced 1 column**

Find the line:
```css
@media(max-width:600px){.mob-cards{grid-template-columns:1fr;border-top:none;}.mob-lcard{border-right:none;}}
```
Remove it entirely (the new CSS already handles all sizes).

- [ ] **Step 7: Update `all.jsx` — move the save/lock badge so it fits the vertical card**

In `all.jsx`, the HeartBtn is positioned `top:12,right:12` — this still works for vertical card. Verify it doesn't overlap the image too aggressively — adjust if needed to `top:8,right:8`.

The "Browse" button (opens SwipeFeed) currently sits inside `mob-lcard-img`. Keep it there — it'll stay at the bottom-right of the image in the new vertical layout.

- [ ] **Step 8: Commit**

```bash
cd "weka-soko-nextjs"
git add app/globals.css components/all.jsx
git commit -m "feat: two-column grid layout for mobile All Listings"
git push
```

---

## Task 8: Hot Right Now — Exactly 2 Cards Visible with Scroll Snap

**Files:**
- Modify: `weka-soko-nextjs/components/all.jsx` (the Hot Right Now block, ~line 4042)

**Current state:** Cards use `flex: "0 0 min(260px,75vw)"` — shows ~1.3 cards. The user wants exactly 2 cards always visible.

- [ ] **Step 1: Update card width to exactly half the container minus gap**

Find the Hot Right Now cards block (~line 4042):
```jsx
<div style={{display:"flex", gap:14, overflowX:"auto", padding: "4px 4px 20px", scrollSnapType: "x mandatory", WebkitOverflowScrolling: "touch"}}>
   {listings.slice(0, 5).map(l => (
     <div key={l.id} className="depth-float" onClick={() => setSwipeFeedIdx(listings.indexOf(l))} style={{
       flex: "0 0 min(260px,75vw)", scrollSnapAlign: "start", background: "#fff", borderRadius: 24, overflow: "hidden", position: "relative"
     }}>
```

Replace the container and card styles:
```jsx
<div style={{display:"flex", gap:10, overflowX:"auto", padding:"4px 12px 20px", scrollSnapType:"x mandatory", WebkitOverflowScrolling:"touch", msOverflowStyle:"none", scrollbarWidth:"none"}}>
   {listings.slice(0, 8).map(l => (
     <div key={l.id} className="depth-float" onClick={() => setSwipeFeedIdx(listings.indexOf(l))} style={{
       flex: "0 0 calc(50% - 5px)", scrollSnapAlign: "start", background:"#fff", borderRadius:16, overflow:"hidden", position:"relative"
     }}>
```

This makes each card exactly `(container - gap) / 2` wide, so 2 fit perfectly regardless of screen width.

- [ ] **Step 2: Reduce image height so 2 short cards fit nicely**

In the same map, the image is `height: 160`. Change to `height: 140` for better proportions at half-width.

- [ ] **Step 3: Also update the `HotRightNow` standalone component (~line 4773)**

This component is used in the non-mobile layout. Its card width is set differently. Update it independently:
```jsx
// In HotRightNow component cards:
flex: "0 0 calc(50% - 5px)", scrollSnapAlign: "start"
```
And in the container:
```jsx
scrollSnapType: "x mandatory"
```

- [ ] **Step 4: Commit**

```bash
cd "weka-soko-nextjs"
git add components/all.jsx
git commit -m "feat: Hot Right Now shows exactly 2 cards in scroll-snap viewport"
git push
```

---

## Task 9: Move Search Bar Next to "All Listings" Heading

**Files:**
- Modify: `weka-soko-nextjs/components/all.jsx` (MobileLayout, ~line 3948 and ~line 4090)

**Goal:** Remove the search from the top bar area and put it inline next to the "All Listings" section heading. The topbar search can remain as a compact logo-only bar.

Actually: keep the topbar search (it's useful when user is on home) but ALSO add a compact search input in the listings section header. When user types in either, they both sync via `filter.q`.

- [ ] **Step 1: Add search to the "All Listings" section header**

Find the listings section header (~line 4090):
```jsx
<div style={{display:"flex",alignItems:"center",justifyContent:"space-between",padding:"14px 18px 10px"}}>
  <div style={{fontSize:14,fontWeight:700,color:"#1A1A1A",lineHeight:1.3}}>{filter.cat||"All Listings"} <span style={{color:"#AAAAAA",fontWeight:400,fontSize:13}}>({total})</span></div>
  {total>0&&listings.length>0&&<div style={{display:"flex",alignItems:"center",gap:6}}>
    <div className="live-dot"/>
    <span style={{fontSize:11,color:"#22c55e",fontWeight:600}}>Live</span>
  </div>}
</div>
```

Replace with:
```jsx
<div style={{padding:"14px 12px 10px"}}>
  <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",marginBottom:8}}>
    <div style={{fontSize:14,fontWeight:700,color:"#1A1A1A",lineHeight:1.3}}>{filter.cat||"All Listings"} <span style={{color:"#AAAAAA",fontWeight:400,fontSize:13}}>({total})</span></div>
    {total>0&&listings.length>0&&<div style={{display:"flex",alignItems:"center",gap:6}}>
      <div className="live-dot"/>
      <span style={{fontSize:11,color:"#22c55e",fontWeight:600}}>Live</span>
    </div>}
  </div>
  <div style={{display:"flex",alignItems:"center",background:"#F2F2F7",borderRadius:10,padding:"8px 12px",gap:8,border:"1.5px solid transparent",transition:"border-color .15s"}} onFocus={e=>e.currentTarget.style.borderColor="#1428A0"} onBlur={e=>e.currentTarget.style.borderColor="transparent"}>
    <svg width="14" height="14" fill="none" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7" stroke="#AAAAAA" strokeWidth="2"/><path d="M20 20l-3-3" stroke="#AAAAAA" strokeWidth="2" strokeLinecap="round"/></svg>
    <input style={{flex:1,border:"none",background:"transparent",fontSize:14,fontFamily:"var(--fn)",color:"#1A1A1A",outline:"none"}} placeholder="Search listings..." value={filter.q} onChange={e=>{setFilter(p=>({...p,q:e.target.value}));setPg(1);setMobileTab("home");}}/>
    {filter.q&&<button onClick={()=>{setFilter(p=>({...p,q:""}));setPg(1);}} style={{background:"none",border:"none",cursor:"pointer",padding:2,color:"#AAAAAA",display:"flex"}}>
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
    </button>}
  </div>
</div>
```

- [ ] **Step 2: Commit**

```bash
cd "weka-soko-nextjs"
git add components/all.jsx
git commit -m "feat: add search bar inline next to All Listings heading on mobile"
git push
```

---

## Task 10: "Buyer Requests" Bottom Tab Label

**Files:**
- Modify: `weka-soko-nextjs/components/all.jsx` (bottom tab bar definition, ~line 4217)

- [ ] **Step 1: Update the Requests tab label**

Find the bottom tab bar tabs array (~line 4217). Find the entry for the Requests tab — it will look like `{id:"requests", icon:..., label:"Requests"}`. Change the label:

```jsx
// Before:
{id:"requests", icon:Ic.users, label:"Requests"}
// After:
{id:"requests", icon:Ic.users, label:"Buyer Requests"}
```

- [ ] **Step 2: Commit**

```bash
cd "weka-soko-nextjs"
git add components/all.jsx
git commit -m "fix: rename Requests tab to Buyer Requests on mobile nav"
git push
```

---

## Task 11: Remove "I'm Interested" Button — Keep Only Save

**Files:**
- Modify: `weka-soko-nextjs/components/all.jsx` (SwipeFeed info panel ~line 4584, photo panel bottom buttons ~line 4668)

**Goal:** Remove the "I'm Interested" (lock-in) button everywhere. Saving a listing is the primary buyer action (with notifications to seller per Task 3).

- [ ] **Step 1: Remove "I'm Interested" from SwipeFeed info panel**

Find ~line 4585:
```jsx
<div style={{display:"flex",gap:8,marginBottom:8}}>
  <button onClick={e=>{e.stopPropagation();if(!user){onSignIn&&onSignIn();return;}onLockIn&&onLockIn(l);}} style={{...}}>I'm Interested</button>
  <button onClick={e=>{e.stopPropagation();if(!user){onSignIn&&onSignIn();return;}onMessage&&onMessage(l);}} style={{...}}>Message Seller</button>
</div>
```

Replace with (only Message Seller remains in this row):
```jsx
<div style={{display:"flex",gap:8,marginBottom:8}}>
  <button onClick={e=>{e.stopPropagation();if(!user){onSignIn&&onSignIn();return;}onMessage&&onMessage(l);}} style={{flex:1,background:"#1428A0",color:"#fff",border:"none",padding:"14px",fontSize:14,fontWeight:700,borderRadius:12,cursor:"pointer",fontFamily:"var(--fn)",boxShadow:"0 4px 14px rgba(20,40,160,.35)"}}>Message Seller</button>
</div>
```

- [ ] **Step 2: Remove "I'm Interested" from photo panel bottom buttons (~line 4668)**

Find:
```jsx
<button onClick={...}>Message Seller</button>
<button onClick={...}>I'm Interested</button>
```
Remove the "I'm Interested" button. Keep "Message Seller" only (full width):
```jsx
<button onClick={e=>{e.stopPropagation();if(!user){onSignIn&&onSignIn();return;}onMessage&&onMessage(l);}} style={{flex:1,background:"rgba(255,255,255,.15)",color:"#fff",border:"1.5px solid rgba(255,255,255,.4)",padding:"14px",fontSize:14,fontWeight:700,borderRadius:12,cursor:"pointer",fontFamily:"var(--fn)",backdropFilter:"blur(8px)"}}>Message Seller</button>
```

- [ ] **Step 3: Remove "I'm Interested" from the ListingCard / DetailModal on desktop if present**

Search `onLockIn` in the codebase and remove any remaining "I'm Interested" / "I'm Interested" buttons in `ListingCard` and `DetailModal`. Keep the lock-in route on the backend — it can still be triggered programmatically but is no longer a visible CTA.

- [ ] **Step 4: Commit**

```bash
cd "weka-soko-nextjs"
git add components/all.jsx
git commit -m "feat: remove I'm Interested button; Save is the primary buyer action"
git push
```

---

## Task 12: No "Message Seller" on Own Listings

**Files:**
- Modify: `weka-soko-nextjs/components/all.jsx` (SwipeFeed, ListingCard, DetailModal)

- [ ] **Step 1: Hide "Message Seller" in SwipeFeed when viewer is the seller**

In the SwipeFeed info panel, before the "Message Seller" button, add:
```jsx
const isOwnListing = user && l.seller_id === user.id;
```

Then wrap the "Message Seller" button:
```jsx
{!isOwnListing && (
  <button onClick={e=>{e.stopPropagation();if(!user){onSignIn&&onSignIn();return;}onMessage&&onMessage(l);}} style={{...}}>Message Seller</button>
)}
```

Do the same for the photo panel bottom buttons.

- [ ] **Step 2: Hide "Message Seller" in DetailModal**

Find the DetailModal component. It already has `isSeller` checking `l.seller_id === user?.id`. Verify "Chat with Seller" / "Message Seller" button is wrapped in `{!isSeller && ...}`. If not, add the guard.

- [ ] **Step 3: Commit**

```bash
cd "weka-soko-nextjs"
git add components/all.jsx
git commit -m "fix: hide Message Seller button on user's own listings"
git push
```

---

## Task 13: Add Report Button

**Files:**
- Modify: `weka-soko-nextjs/components/all.jsx` (SwipeFeed info panel, ListingCard)

**Backend already exists:** `POST /api/listings/:id/report` with body `{ reason, details }`. The `listing_reports` table exists. The `ReportListingBtn` component is already imported in `HomeClient.jsx`.

- [ ] **Step 1: Check if `ReportListingBtn` component exists in all.jsx**

Search `ReportListingBtn` in `all.jsx`. If it exists, find where it's defined and note its props. If it does not exist, create it:

```jsx
function ReportListingBtn({ listingId, user, token, onSignIn, notify }) {
  const [open, setOpen] = useState(false);
  const [reason, setReason] = useState("");
  const [details, setDetails] = useState("");
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState(false);

  const reasons = ["Fake/Scam listing","Prohibited item","Wrong category","Misleading price","Duplicate listing","Other"];

  const submit = async () => {
    if (!reason) { notify("Please select a reason", "error"); return; }
    setLoading(true);
    try {
      await apiCall(`/api/listings/${listingId}/report`, { method:"POST", body:JSON.stringify({reason,details}) }, token);
      setDone(true);
      setTimeout(() => { setOpen(false); setDone(false); setReason(""); setDetails(""); }, 2000);
    } catch(e) { notify(e.message || "Report failed", "error"); }
    finally { setLoading(false); }
  };

  return <>
    <button onClick={e=>{e.stopPropagation();if(!user){onSignIn&&onSignIn();return;}setOpen(true);}} style={{background:"none",border:"none",cursor:"pointer",display:"flex",alignItems:"center",gap:6,fontSize:12,color:"#AAAAAA",fontFamily:"var(--fn)",padding:"8px 0"}}>
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/></svg>
      Report this listing
    </button>
    {open && <Modal title="Report Listing" onClose={()=>setOpen(false)} footer={
      done ? <div style={{color:"#22c55e",fontWeight:700}}>Report submitted. Thank you.</div>
           : <><button className="btn bs" onClick={()=>setOpen(false)}>Cancel</button><button className="btn br" onClick={submit} disabled={loading||!reason}>{loading?<Spin/>:"Submit Report"}</button></>
    }>
      <FF label="Reason">
        <select className="inp" value={reason} onChange={e=>setReason(e.target.value)}>
          <option value="">Select a reason...</option>
          {reasons.map(r=><option key={r} value={r}>{r}</option>)}
        </select>
      </FF>
      <FF label="Additional details (optional)">
        <textarea className="inp" rows={3} placeholder="Anything else we should know?" value={details} onChange={e=>setDetails(e.target.value)}/>
      </FF>
    </Modal>}
  </>;
}
```

- [ ] **Step 2: Add report button to SwipeFeed info panel**

In the SwipeFeed info panel (~line 4590), after the Share button, add:
```jsx
{user && l.seller_id !== user.id && (
  <ReportListingBtn listingId={l.id} user={user} token={token} onSignIn={onSignIn} notify={notify}/>
)}
```

- [ ] **Step 3: Commit**

```bash
cd "weka-soko-nextjs"
git add components/all.jsx
git commit -m "feat: add report listing button to swipe feed detail panel"
git push
```

---

## Task 14: SwipeFeed Last Slide — Contact Info, Full Listing, Remove "Open Full Listing"

**Files:**
- Modify: `weka-soko-nextjs/components/all.jsx` (SwipeFeed info panel ~line 4554–4638)

**Goals:**
1. If seller is unlocked, show contact info (phone, email, precise location) on the last slide
2. Always show full listing details on the last slide (description, reason for sale, seller info)
3. Remove "Open Full Listing →" button
4. Keep Share button

- [ ] **Step 1: Remove "Open Full Listing" button**

Find (~line 4589):
```jsx
<button onClick={e=>{e.stopPropagation();onOpen&&onOpen(l);}} style={{width:"100%",background:"none",color:"#1428A0",border:"1.5px solid #1428A0",padding:"12px",fontSize:13,fontWeight:700,borderRadius:12,cursor:"pointer",fontFamily:"var(--fn)",marginBottom:8}}>Open Full Listing →</button>
```
Delete this button entirely.

- [ ] **Step 2: Add contact info section (shown when unlocked)**

In the SwipeFeed info panel, after the Seller info block (~line 4628), add:

```jsx
{/* Contact info — shown when unlocked */}
{l.is_unlocked && (l.seller_phone || l.seller_email) && <>
  <div style={{height:8,background:"#F5F5F5",margin:"0"}}/>
  <div style={{padding:"16px 18px"}}>
    <div style={{fontSize:11,fontWeight:700,letterSpacing:".08em",textTransform:"uppercase",color:"#22c55e",marginBottom:10}}>Contact Info Unlocked</div>
    {l.seller_name && <div style={{marginBottom:8}}>
      <div style={{fontSize:11,color:"#AAAAAA",fontWeight:600,marginBottom:2}}>Name</div>
      <div style={{fontSize:15,fontWeight:700,color:"#1A1A1A"}}>{l.seller_name}</div>
    </div>}
    {l.seller_phone && <div style={{marginBottom:8}}>
      <div style={{fontSize:11,color:"#AAAAAA",fontWeight:600,marginBottom:2}}>Phone</div>
      <a href={`tel:${l.seller_phone}`} style={{fontSize:15,fontWeight:700,color:"#1428A0",textDecoration:"none"}}>{l.seller_phone}</a>
    </div>}
    {l.seller_email && <div style={{marginBottom:8}}>
      <div style={{fontSize:11,color:"#AAAAAA",fontWeight:600,marginBottom:2}}>Email</div>
      <a href={`mailto:${l.seller_email}`} style={{fontSize:14,fontWeight:600,color:"#1428A0",textDecoration:"none"}}>{l.seller_email}</a>
    </div>}
    {l.precise_location && <div style={{marginBottom:8}}>
      <div style={{fontSize:11,color:"#AAAAAA",fontWeight:600,marginBottom:2}}>Exact Collection Point</div>
      <div style={{fontSize:14,fontWeight:600,color:"#1A1A1A"}}>{l.precise_location}</div>
    </div>}
  </div>
</>}

{/* If not unlocked, show pay-to-reveal prompt */}
{!l.is_unlocked && (
  <div style={{padding:"14px 18px"}}>
    <div style={{background:"#F0F4FF",border:"1px solid #C7D2FE",borderRadius:12,padding:"14px",textAlign:"center"}}>
      <div style={{fontSize:13,color:"#3730A3",fontWeight:600,marginBottom:10,lineHeight:1.5}}>Pay KSh 250 to reveal the seller's contact info and exact collection point.</div>
      <button onClick={e=>{e.stopPropagation();if(!user){onSignIn&&onSignIn();return;}onOpen&&onOpen(l);}} style={{background:"#1428A0",color:"#fff",border:"none",padding:"12px 24px",fontSize:13,fontWeight:700,borderRadius:10,cursor:"pointer",fontFamily:"var(--fn)"}}>Reveal Contact Info — KSh 250</button>
    </div>
  </div>
)}
```

- [ ] **Step 3: Commit**

```bash
cd "weka-soko-nextjs"
git add components/all.jsx
git commit -m "feat: SwipeFeed last slide shows contact info when unlocked; remove Open Full Listing"
git push
```

---

## Task 15: Fix Mobile Filter Overlay + Add All Filters

**Files:**
- Modify: `weka-soko-nextjs/components/all.jsx` (mobile filter modal/panel, ~wherever `mobileFiltersOpen` is used)
- Modify: `weka-soko-nextjs/app/globals.css` (filter panel styles if needed)

**Current problem:** When mobile filters open, underlying buttons are still tappable (no proper overlay). Also missing filters: subcategory, price range sliders, condition.

- [ ] **Step 1: Find where the mobile filter panel is rendered**

Search `mobileFiltersOpen` in `all.jsx`. It sets `mobileFiltersOpen(true)` on the Filters button tap. Find where the panel is rendered — it likely uses a bottom-sheet pattern or a `<div>` that slides up. Note how it's structured.

- [ ] **Step 2: Ensure full-screen overlay blocks touch-through**

If the filter panel doesn't have a full-screen overlay (with `pointerEvents:"all"`), wrap it:

```jsx
{mobileFiltersOpen && (
  <div style={{position:"fixed",inset:0,zIndex:500,display:"flex",flexDirection:"column",justifyContent:"flex-end"}} onClick={e=>{if(e.target===e.currentTarget)setMobileFiltersOpen(false);}}>
    <div style={{background:"rgba(0,0,0,.4)",position:"absolute",inset:0}}/>
    <div style={{position:"relative",background:"#fff",borderRadius:"20px 20px 0 0",maxHeight:"85dvh",overflowY:"auto",padding:"20px 16px calc(20px + env(safe-area-inset-bottom))",zIndex:1}}>
      {/* drag handle */}
      <div style={{width:36,height:4,background:"#E0E0E0",borderRadius:2,margin:"0 auto 16px"}}/>
      <div style={{fontSize:16,fontWeight:800,marginBottom:20,letterSpacing:"-.02em"}}>Filters</div>
      {/* filter content ... */}
    </div>
  </div>
)}
```

- [ ] **Step 3: Add all necessary filters to the panel**

Inside the filter panel content, render these sections:

```jsx
{/* Sort */}
<div style={{marginBottom:20}}>
  <div className="mob-filter-label">Sort By</div>
  <div style={{display:"flex",gap:8,flexWrap:"wrap"}}>
    {[["newest","Latest"],["price_asc","Price: Low"],["price_desc","Price: High"],["popular","Most Viewed"],["expiring","Expiring Soon"]].map(([v,l])=>(
      <button key={v} onClick={()=>setFilter(p=>({...p,sort:v}))} style={{padding:"8px 14px",borderRadius:20,border:`1.5px solid ${filter.sort===v?"#1428A0":"#E0E0E0"}`,background:filter.sort===v?"#1428A0":"#fff",color:filter.sort===v?"#fff":"#555",fontSize:12,fontWeight:600,fontFamily:"var(--fn)",cursor:"pointer"}}>{l}</button>
    ))}
  </div>
</div>

{/* Category */}
<div style={{marginBottom:20}}>
  <div className="mob-filter-label">Category</div>
  <select className="inp" value={filter.cat} onChange={e=>setFilter(p=>({...p,cat:e.target.value,subcat:""}))}>
    <option value="">All Categories</option>
    {CATS.map(c=><option key={c.name} value={c.name}>{c.name}</option>)}
  </select>
</div>

{/* Subcategory */}
{filter.cat && (() => {
  const catObj = CATS.find(c => c.name === filter.cat);
  return catObj?.sub?.length ? (
    <div style={{marginBottom:20}}>
      <div className="mob-filter-label">Subcategory</div>
      <select className="inp" value={filter.subcat||""} onChange={e=>setFilter(p=>({...p,subcat:e.target.value}))}>
        <option value="">All Subcategories</option>
        {catObj.sub.map(s=><option key={s} value={s}>{s}</option>)}
      </select>
    </div>
  ) : null;
})()}

{/* County */}
<div style={{marginBottom:20}}>
  <div className="mob-filter-label">County / Town</div>
  <select className="inp" value={filter.county||""} onChange={e=>setFilter(p=>({...p,county:e.target.value}))}>
    <option value="">All Locations</option>
    {KENYA_COUNTIES.map(c=><option key={c} value={c}>{c}</option>)}
  </select>
</div>

{/* Price Range */}
<div style={{marginBottom:20}}>
  <div className="mob-filter-label">Price Range (KSh)</div>
  <div style={{display:"flex",gap:8,alignItems:"center"}}>
    <input className="inp" type="number" placeholder="Min" value={filter.minPrice} onChange={e=>setFilter(p=>({...p,minPrice:e.target.value}))} style={{flex:1}}/>
    <span style={{color:"#CCC",fontWeight:700}}>–</span>
    <input className="inp" type="number" placeholder="Max" value={filter.maxPrice} onChange={e=>setFilter(p=>({...p,maxPrice:e.target.value}))} style={{flex:1}}/>
  </div>
</div>

{/* Apply / Clear */}
<div style={{display:"flex",gap:10,paddingTop:8}}>
  <button className="btn bs" style={{flex:1}} onClick={()=>{setFilter({cat:"",subcat:"",q:filter.q,county:"",minPrice:"",maxPrice:"",sort:"newest"});setPg(1);}}>Clear All</button>
  <button className="btn bp" style={{flex:2}} onClick={()=>{setMobileFiltersOpen(false);setPg(1);}}>Apply Filters</button>
</div>
```

- [ ] **Step 4: Commit**

```bash
cd "weka-soko-nextjs"
git add components/all.jsx app/globals.css
git commit -m "fix: mobile filter overlay blocks touch-through; add all filter options"
git push
```

---

## Task 16: Mobile Dashboard "My Ads" — Full Management Buttons

**Files:**
- Modify: `weka-soko-nextjs/components/all.jsx` (MobileDashboard component, `mobSection==="ads"` block, ~line 3064)

**Problem:** The "ads" section only shows "Reveal Buyer — KSh 250", "Edit", "Mark Sold". Missing: Delete listing, and the reveal button language is wrong.

- [ ] **Step 1: Add Delete button to mobile ad cards**

Find the mobile ads section (~line 3087):
```jsx
{user.role==="seller"&&<div style={{borderTop:"1px solid #F5F5F5",padding:"8px 12px",display:"flex",gap:8}}>
  {!l.is_unlocked&&l.locked_buyer_id&&<button className="btn bp sm" style={{...}} onClick={()=>setShowPayModal(l)}>Reveal Buyer — KSh 250</button>}
  <button className="btn bs sm" style={{...}} onClick={()=>setEditingListing(l)}>Edit</button>
  {l.status==="active"&&<button className="btn bs sm" style={{...}} onClick={()=>setMarkSoldListing(l)}>Mark Sold</button>}
</div>}
```

Replace with:
```jsx
{user.role==="seller"&&<div style={{borderTop:"1px solid #F5F5F5",padding:"8px 12px",display:"flex",gap:6,flexWrap:"wrap"}}>
  {!l.is_unlocked&&l.locked_buyer_id&&(
    <button className="btn bp sm" style={{borderRadius:8,flex:"1 1 auto",fontSize:11,whiteSpace:"nowrap"}} onClick={()=>setShowPayModal(l)}>
      {(l.unlock_discount||0)>=250?"Reveal Contact — FREE":l.unlock_discount>0?`Reveal Contact — KSh ${250-(l.unlock_discount||0)}`:"Reveal Contact Info — KSh 250"}
    </button>
  )}
  {l.is_unlocked&&<div style={{fontSize:11,color:"#22c55e",fontWeight:700,display:"flex",alignItems:"center",gap:4,padding:"4px 8px",background:"rgba(34,197,94,.08)",borderRadius:8}}>
    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#22c55e" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
    Contact Revealed
  </div>}
  {l.status!=="sold"&&<button className="btn bs sm" style={{borderRadius:8,fontSize:11}} onClick={()=>setEditingListing(l)}>Edit</button>}
  {(l.status==="active"||l.status==="locked")&&<button className="btn bs sm" style={{borderRadius:8,fontSize:11}} onClick={()=>setMarkSoldListing(l)}>Mark Sold</button>}
  <button className="btn br sm" style={{borderRadius:8,fontSize:11}} onClick={async()=>{
    if(!window.confirm("Delete this listing? This cannot be undone."))return;
    try{
      await apiCall(`/api/listings/${l.id}`,{method:"DELETE"},token);
      setListings(p=>p.filter(x=>x.id!==l.id));
      notify("Listing deleted","success");
    }catch(e){notify(e.message,"error");}
  }}>Delete</button>
</div>}
```

- [ ] **Step 2: Commit**

```bash
cd "weka-soko-nextjs"
git add components/all.jsx
git commit -m "feat: full management buttons in mobile My Ads (reveal contact, edit, mark sold, delete)"
git push
```

---

## Task 17: Language Cleanup — "Reveal Contact Info" Everywhere

**Files:**
- Modify: `weka-soko-nextjs/components/all.jsx` (multiple locations)
- Modify: `weka-soko-admin/src/App.jsx` (multiple locations)

**Goal:** Replace all instances of "Reveal Buyer", "Reveal Seller", "Pay KSh 250 to reveal their contact" with "Reveal Contact Info — KSh 250" or contextually appropriate phrasing. The platform logic is: **sellers always pay to reveal contact info**, never buyers.

- [ ] **Step 1: Global search-and-replace in all.jsx**

Find and replace each of these (check context to ensure the replacement fits):

| Find | Replace |
|---|---|
| `Reveal Buyer — KSh 250` | `Reveal Contact Info — KSh 250` |
| `Reveal Buyer — FREE` | `Reveal Contact Info — FREE` |
| `Reveal Buyer — KSh ${...}` | `Reveal Contact Info — KSh ${...}` |
| `Pay KSh 250 to reveal their contact` | `Pay KSh 250 to reveal buyer contact info` |
| `Pay KSh 250 to See Buyer Contact` | `Reveal Contact Info — KSh 250` |
| `"Reveal Buyer" or locked_buyer_id` button text variations | `Reveal Contact Info` |
| `A serious buyer locked in ... Pay KSh 250 to reveal their contact.` (notification body) | `A buyer has shown interest in "${listing.title}". Pay KSh 250 to reveal their contact info and close the deal.` |
| Inline message: `Pay KSh 250 to reveal contact` | `Pay KSh 250 to reveal contact info` |

- [ ] **Step 2: Update dashboard Desktop seller listing card (~line 3615–3619)**

The desktop "My Listings" tab also has `Reveal Buyer` buttons. Apply same replacements.

- [ ] **Step 3: Update admin.js notification messages**

In `admin.js` and `listings.js`, find notification `body` strings that say "Pay KSh 250 to reveal their contact" and update them similarly.

- [ ] **Step 4: Commit**

```bash
cd "weka-soko-nextjs"
git add components/all.jsx
git commit -m "fix: standardise language to 'Reveal Contact Info' throughout"

cd ../weka-soko-backend"
git add src/routes/listings.js src/routes/admin.js
git commit -m "fix: update notification copy to consistent 'reveal contact info' language"
git push
```

---

## Task 18: Collection Locations — Kenya Towns Dropdown in Post Ad

**Files:**
- Modify: `weka-soko-nextjs/components/all.jsx` (PostAdModal, ~wherever location input is)
- Modify: `weka-soko-nextjs/lib/utils.js` (add KENYA_TOWNS list)

**Goal:** Replace the free-text location field with a dropdown of Kenyan towns/cities. Add an optional "Precise Collection Point" field that is only revealed when contact info is unlocked.

- [ ] **Step 1: Add KENYA_TOWNS to `lib/utils.js`**

Append to `utils.js`:
```javascript
export const KENYA_TOWNS = [
  // Nairobi
  "Nairobi CBD","Westlands","Kilimani","Karen","Langata","Eastlands","Kasarani",
  "Ruiru","Juja","Kikuyu","Limuru","Kiambu","Thika",
  // Coast
  "Mombasa","Nyali","Bamburi","Likoni","Malindi","Kilifi","Diani","Ukunda",
  // Rift Valley
  "Nakuru","Eldoret","Naivasha","Kericho","Kitale","Kapenguria","Iten","Kabarnet",
  // Western
  "Kisumu","Kakamega","Bungoma","Busia","Homabay","Migori","Kisii","Siaya","Mumias","Vihiga",
  // Central
  "Nyeri","Muranga","Embu","Kirinyaga","Nyandarua","Karatina",
  // Eastern
  "Machakos","Kitui","Meru","Isiolo","Mwingi","Garissa","Wajir","Mandera","Marsabit",
  // North Rift
  "Turkana","Lodwar","Samburu","Maralal","West Pokot",
  // South
  "Kajiado","Namanga","Makueni","Wote","Taveta","Lamu","Malindi",
  // Others
  "Nandi","Nanyuki","Narok","Bomet","Sotik","Hola","Lamu Town"
].sort();
```

- [ ] **Step 2: Import KENYA_TOWNS in all.jsx**

In `all.jsx`, find the import from `@/lib/utils`:
```javascript
import { apiCall, fmtKES, ago, CATS, KENYA_COUNTIES, API, PER_PAGE, CAT_PHOTOS } from '@/lib/utils';
```
Add `KENYA_TOWNS`:
```javascript
import { apiCall, fmtKES, ago, CATS, KENYA_COUNTIES, KENYA_TOWNS, API, PER_PAGE, CAT_PHOTOS } from '@/lib/utils';
```

- [ ] **Step 3: Update PostAdModal location field**

Find the PostAdModal component. Find the location input field (likely `<input ... placeholder="e.g. Westlands, Nairobi">`). Replace it with a dropdown:

```jsx
<FF label="Town / City" required>
  <select className="inp" value={f.location||""} onChange={e=>setF(p=>({...p,location:e.target.value}))}>
    <option value="">Select town or city...</option>
    {KENYA_TOWNS.map(t=><option key={t} value={t}>{t}</option>)}
  </select>
</FF>

<FF label="Precise Collection Point (optional — revealed only after contact info is unlocked)">
  <input className="inp" placeholder="e.g. Gate 3, Sarit Centre, Westlands" value={f.precise_location||""} onChange={e=>setF(p=>({...p,precise_location:e.target.value}))}/>
  <div style={{fontSize:11,color:"#AAAAAA",marginTop:4}}>This exact address is kept private and only shown to the buyer after you reveal your contact info.</div>
</FF>
```

Make sure `precise_location` is included in the POST body when submitting the form.

- [ ] **Step 4: Commit**

```bash
cd "weka-soko-nextjs"
git add lib/utils.js components/all.jsx
git commit -m "feat: Kenya towns dropdown for collection location; optional precise location field"
git push
```

---

## Task 19: Self-Contained Backend Deploy Trigger

All backend tasks above push to `weka-soko-backend`. Railway auto-deploys on push. Verify deploy logs show `✅ DB migration complete` before testing frontend changes that depend on the new columns.

- [ ] **Verify Railway deploy after all backend commits**

Check Railway dashboard or run:
```bash
curl https://wekasokobackend.up.railway.app/api/listings?limit=1
```
Expected: 200 OK with listing data (not 503 or migration error).

---

## Task 20: Frontend Deploy

- [ ] **After all nextjs commits, verify Vercel deploy**

Vercel auto-deploys on push. Check https://weka-soko-nextjs.vercel.app after each push. If build fails, check Vercel build logs.

---

## Spec Self-Review

**Coverage check:**

| Requirement | Task |
|---|---|
| Mobile two-column All Listings | Task 7 |
| Hot Right Now 2 cards scroll-snap | Task 8 |
| "Buyer Requests" bottom tab label | Task 10 |
| Search bar next to All Listings | Task 9 |
| Notify seller on save + tap → chat | Task 3 |
| Remove I'm Interested, keep Save | Task 11 |
| No Message Seller on own listings | Task 12 |
| Report button | Task 13 |
| SwipeFeed last slide: contact reveal, full info, no "Open Full Listing" | Task 14 |
| Collection locations — Kenya towns | Task 18 |
| Filter overlay fix + all filters | Task 15 |
| Mobile My Ads full management buttons | Task 16 |
| "Reveal Contact Info" language | Task 17 |
| Voucher description column bug | Task 1 |
| Maintenance mode — mobile banner, don't hide listings | Task 6 |
| Audit log fixes | Task 4 |
| Buyer Requests need admin approval | Task 5 |
| Precise location field | Task 2 |

All 18 requirements are covered. No placeholders remain.
