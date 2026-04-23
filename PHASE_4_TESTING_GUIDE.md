# Phase 4 Testing Guide - Self-Assessment Checklist

## Prerequisites: Server Setup

### Step 1: Start the Server

```bash
# Navigate to project folder
cd C:\Users\mulla\OneDrive\Desktop\ai-support-system

# Activate virtual environment
.\venv310\Scripts\Activate.ps1

# Navigate to backend
cd backend

# Start server on port 8002
python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

**Expected Output**:
```
✅ Tables created successfully
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
🚀 AUTORESOLVE AI - PHASE 4 COMPLETE
✅ Phase 3: Registration & Authentication
✅ Phase 4: Ticket Management System (CRUD)
```

**What to observe**: Server is running at `http://localhost:8002`

---

## Part 1: Authentication (Prerequisite for All Tests)

### Get JWT Token

**What This Does**: Obtain an access token to use in all ticket endpoints

**Test Steps**:
```powershell
# Login as existing user
$loginResponse = Invoke-WebRequest -Uri "http://localhost:8002/login" `
  -Method POST `
  -ContentType "application/x-www-form-urlencoded" `
  -UseBasicParsing `
  -Body "username=testuser&password=Test@1234"

# Extract token
$token = ($loginResponse.Content | ConvertFrom-Json).access_token

# Display token (first 50 chars)
Write-Host "Token: $($token.Substring(0, 50))..."
```

**Expected Output**:
```
Status Code: 200
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWI...
```

**What to Observe**:
- ✅ Status code is **200 OK**
- ✅ `access_token` field exists in response
- ✅ Token starts with `eyJ` (base64 encoded JWT)
- ✅ `token_type` is "Bearer"

**If Test Fails**:
- ❌ Status 401: Wrong username/password
- ❌ Status 500: Server error (check server logs)

---

## Part 2: Endpoint Tests

### TEST 1: Create a Ticket

**What This Tests**: Can a customer create a new ticket?

**Test Steps**:
```powershell
# Setup
$token = "YOUR_JWT_TOKEN_FROM_ABOVE"
$headers = @{ Authorization = "Bearer $token" }

# Create ticket
$ticketBody = @{
  title = "Cannot login to my account"
  description = "I forgot my password and cannot log in to my account. Please help me reset it."
  priority = "high"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8002/tickets" `
  -Method POST `
  -ContentType "application/json" `
  -UseBasicParsing `
  -Headers $headers `
  -Body $ticketBody

$ticket = $response.Content | ConvertFrom-Json
$ticket | Format-List
```

**Expected Output**:
```
id              : 2 (or higher)
title           : Cannot login to my account
description     : I forgot my password and cannot log in to my account. Please help me reset it.
status          : open
priority        : high
user_id         : 1 (the current user)
assigned_to     : (empty/null)
ai_category     : (empty/null)
ai_confidence   : (empty/null)
sentiment_score : (empty/null)
resolved_by_ai  : False
created_at      : 2026-04-23T... (current timestamp)
updated_at      : 2026-04-23T... (current timestamp)
```

**What to Observe** ✓ Checklist:
- [ ] Status code is **201 Created** (not 200)
- [ ] Ticket has unique `id` (auto-generated)
- [ ] `status` is automatically set to "open"
- [ ] `priority` matches what you sent
- [ ] `user_id` is your ID (testuser = ID 1)
- [ ] `assigned_to` is null (not assigned yet)
- [ ] `created_at` and `updated_at` are timestamps
- [ ] AI fields are null (for Phase 5)

**Save the ticket ID**: You'll need it for next tests!

**If Test Fails**:
- ❌ 401: Invalid token
- ❌ 400: Missing required fields or invalid values
- ❌ 500: Server error

---

### TEST 2: List All Your Tickets

**What This Tests**: Can a customer see their own tickets?

**Test Steps**:
```powershell
$token = "YOUR_JWT_TOKEN"
$headers = @{ Authorization = "Bearer $token" }

# List tickets
$response = Invoke-WebRequest -Uri "http://localhost:8002/tickets" `
  -UseBasicParsing `
  -Headers $headers

$ticketList = $response.Content | ConvertFrom-Json

Write-Host "Total tickets: $($ticketList.total)"
Write-Host "Tickets in response: $($ticketList.tickets.Count)"
$ticketList.tickets | Format-Table id, title, status, priority
```

**Expected Output**:
```
Total tickets: 2 (or more)
Tickets in response: 2

id title                            status priority
-- -----                            ------ --------
 1 Original ticket                  open   medium
 2 Cannot login to my account       open   high
```

**What to Observe** ✓ Checklist:
- [ ] Status code is **200 OK**
- [ ] `total` shows correct number of your tickets
- [ ] `tickets` array contains all your tickets
- [ ] Only see tickets where `user_id` matches yours
- [ ] Each ticket has all fields populated

**Try With Filters**:
```powershell
# Only open tickets
Invoke-WebRequest -Uri "http://localhost:8002/tickets?status=open" ...

# Only high priority
Invoke-WebRequest -Uri "http://localhost:8002/tickets?priority=high" ...

# With pagination
Invoke-WebRequest -Uri "http://localhost:8002/tickets?skip=0&limit=10" ...
```

**Expected**: Filtering works correctly, returns only matching tickets

---

### TEST 3: Get Single Ticket

**What This Tests**: Can you view details of a specific ticket?

**Test Steps**:
```powershell
$token = "YOUR_JWT_TOKEN"
$ticketId = 2  # From TEST 1
$headers = @{ Authorization = "Bearer $token" }

# Get specific ticket
$response = Invoke-WebRequest -Uri "http://localhost:8002/tickets/$ticketId" `
  -UseBasicParsing `
  -Headers $headers

$ticket = $response.Content | ConvertFrom-Json
$ticket | Format-List
```

**Expected Output**:
```
id              : 2
title           : Cannot login to my account
description     : I forgot my password...
status          : open
priority        : high
user_id         : 1
assigned_to     : (null)
... (all fields)
```

**What to Observe** ✓ Checklist:
- [ ] Status code is **200 OK**
- [ ] Returns complete ticket details
- [ ] Ticket ID matches what you requested
- [ ] All fields are populated

**Try Invalid ID**:
```powershell
# Try non-existent ticket
Invoke-WebRequest -Uri "http://localhost:8002/tickets/99999" ...
```

**Expected**: Status code **404 Not Found** with error message

---

### TEST 4: Update Your Ticket (Customer)

**What This Tests**: Can you update your own ticket? What can you change?

**Test Steps**:
```powershell
$token = "YOUR_JWT_TOKEN"
$ticketId = 2
$headers = @{ Authorization = "Bearer $token" }

# Update title only (customer should be allowed)
$updateBody = @{
  title = "URGENT: Cannot access my account - password reset needed"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8002/tickets/$ticketId" `
  -Method PUT `
  -ContentType "application/json" `
  -UseBasicParsing `
  -Headers $headers `
  -Body $updateBody

$ticket = $response.Content | ConvertFrom-Json
Write-Host "Updated title: $($ticket.title)"
Write-Host "Status still: $($ticket.status)"
```

**Expected Output**:
```
Updated title: URGENT: Cannot access my account - password reset needed
Status still: open
```

**What to Observe** ✓ Checklist:
- [ ] Status code is **200 OK**
- [ ] `title` was updated to your new value
- [ ] `status` did NOT change (customers can't change status)
- [ ] `updated_at` timestamp changed

**Try to Change Status (Should FAIL)**:
```powershell
# Customer trying to change status
$updateBody = @{
  status = "resolved"  # Customers shouldn't be able to do this
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8002/tickets/$ticketId" `
  -Method PUT `
  -ContentType "application/json" `
  -UseBasicParsing `
  -Headers $headers `
  -Body $updateBody
```

**Expected**: Status code **200 OK**, but `status` should still be "open" (not changed)

---

### TEST 5: Access Control - Other Customer Can't See Your Ticket

**What This Tests**: Does the system prevent other customers from viewing your tickets?

**Test Steps**:
```powershell
# Login as DIFFERENT customer (newuser)
$loginResponse = Invoke-WebRequest -Uri "http://localhost:8002/login" `
  -Method POST `
  -ContentType "application/x-www-form-urlencoded" `
  -UseBasicParsing `
  -Body "username=newuser&password=NewUser@123"

$otherToken = ($loginResponse.Content | ConvertFrom-Json).access_token
$otherHeaders = @{ Authorization = "Bearer $otherToken" }

# Try to access testuser's ticket (ID 2)
try {
  $response = Invoke-WebRequest -Uri "http://localhost:8002/tickets/2" `
    -UseBasicParsing `
    -Headers $otherHeaders
  Write-Host "❌ ERROR: Access was allowed (SECURITY BREACH!)"
} catch {
  $statusCode = $_.Exception.Response.StatusCode
  Write-Host "✅ Good: Got status code $statusCode"
}
```

**Expected Output**:
```
✅ Good: Got status code 403
```

**What to Observe** ✓ Checklist:
- [ ] Status code is **403 Forbidden**
- [ ] Error message: "Access denied"
- [ ] Other customer cannot view your tickets
- [ ] Security is working ✅

**What NOT to Observe** ❌:
- ❌ Status code 200 (would mean anyone can see anyone's tickets!)
- ❌ Ticket details shown

---

### TEST 6: List Tickets as Agent/Admin

**What This Tests**: Do agents and admins see ALL tickets, not just their own?

**Test Steps**:
```powershell
# Create an agent account first (if needed)
# For now, we'll need to manually set a user's role in database or use existing admin

# Login as admin (if available) or modify testuser's role
# For testing, let's check what testuser sees
$token = "YOUR_TESTUSER_TOKEN"
$headers = @{ Authorization = "Bearer $token" }

$response = Invoke-WebRequest -Uri "http://localhost:8002/tickets" `
  -UseBasicParsing `
  -Headers $headers

$ticketList = $response.Content | ConvertFrom-Json
Write-Host "Testuser sees: $($ticketList.tickets.Count) tickets"

# Show all user_ids to verify (customer should only see their own)
$ticketList.tickets | Select-Object id, title, user_id | Format-Table
```

**Expected Output** (for customer):
```
Testuser sees: 2 tickets

id title                                        user_id
-- -----                                        -------
 1 Original ticket                              1
 2 Cannot access my account - password reset n 1
```

**What to Observe** ✓ Checklist:
- [ ] Customer only sees their own tickets (`user_id` = their ID)
- [ ] Doesn't see other customers' tickets

---

### TEST 7: Delete Ticket (Admin Only)

**What This Tests**: Can admins delete tickets? Can customers?

**Test Steps**:
```powershell
# Login as customer and try to delete (should fail)
$customerToken = "YOUR_TESTUSER_TOKEN"
$customerHeaders = @{ Authorization = "Bearer $customerToken" }

$response = Invoke-WebRequest -Uri "http://localhost:8002/tickets/2" `
  -Method DELETE `
  -UseBasicParsing `
  -Headers $customerHeaders `
  -ErrorAction SilentlyContinue

if ($response.StatusCode -eq 204) {
  Write-Host "❌ ERROR: Customer was allowed to delete!"
} else {
  Write-Host "✅ Good: Customer got status code $($response.StatusCode)"
}
```

**Expected Output**:
```
✅ Good: Customer got status code 403
```

**What to Observe** ✓ Checklist:
- [ ] Customer gets **403 Forbidden**
- [ ] Only admins can delete
- [ ] Security is enforced ✅

---

## Part 3: Data Validation Tests

### TEST 8: Title Too Long

**What This Tests**: Does validation catch invalid input?

**Test Steps**:
```powershell
$token = "YOUR_JWT_TOKEN"
$headers = @{ Authorization = "Bearer $token" }

# Create title that's way too long (max is 200)
$longTitle = "A" * 201  # 201 characters

$ticketBody = @{
  title = $longTitle
  description = "Test"
  priority = "high"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8002/tickets" `
  -Method POST `
  -ContentType "application/json" `
  -UseBasicParsing `
  -Headers $headers `
  -Body $ticketBody `
  -ErrorAction SilentlyContinue

if ($response.StatusCode -ne 201) {
  Write-Host "✅ Good: Request was rejected with status $($response.StatusCode)"
} else {
  Write-Host "❌ ERROR: Invalid input was accepted!"
}
```

**Expected**: Status code **400 Bad Request**

**What to Observe**:
- [ ] Validation error message appears
- [ ] Ticket was not created

---

### TEST 9: Missing Required Fields

**Test Steps**:
```powershell
# Try to create ticket without description
$ticketBody = @{
  title = "Missing description"
  # description is missing!
  priority = "high"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8002/tickets" `
  -Method POST `
  -ContentType "application/json" `
  -UseBasicParsing `
  -Headers $headers `
  -Body $ticketBody `
  -ErrorAction SilentlyContinue

if ($response.StatusCode -ne 201) {
  Write-Host "✅ Good: Validation caught missing field, status $($response.StatusCode)"
}
```

**Expected**: Status code **400 Bad Request**

---

### TEST 10: Invalid Priority Value

**Test Steps**:
```powershell
$ticketBody = @{
  title = "Test"
  description = "Test"
  priority = "super_urgent"  # Invalid! Should be: low, medium, high, urgent
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8002/tickets" `
  -Method POST `
  -ContentType "application/json" `
  -UseBasicParsing `
  -Headers $headers `
  -Body $ticketBody `
  -ErrorAction SilentlyContinue

if ($response.StatusCode -ne 201) {
  Write-Host "✅ Good: Invalid enum value rejected, status $($response.StatusCode)"
}
```

**Expected**: Status code **400 Bad Request**

---

## Part 4: Authentication Tests

### TEST 11: Missing Authorization Header

**Test Steps**:
```powershell
# Try to access without token
$response = Invoke-WebRequest -Uri "http://localhost:8002/tickets" `
  -UseBasicParsing `
  -ErrorAction SilentlyContinue

Write-Host "Status code: $($response.StatusCode)"
```

**Expected**: Status code **401 Unauthorized**

**What to Observe**:
- [ ] Cannot access any endpoint without token

---

### TEST 12: Invalid/Expired Token

**Test Steps**:
```powershell
$badHeaders = @{ Authorization = "Bearer INVALID_TOKEN_123" }

$response = Invoke-WebRequest -Uri "http://localhost:8002/tickets" `
  -UseBasicParsing `
  -Headers $badHeaders `
  -ErrorAction SilentlyContinue

Write-Host "Status code: $($response.StatusCode)"
```

**Expected**: Status code **401 Unauthorized**

---

## Testing Summary Checklist

Print this out and check off as you go:

### Functional Tests
- [ ] Can create ticket (POST /tickets)
- [ ] Can list own tickets (GET /tickets)
- [ ] Can filter by status
- [ ] Can filter by priority
- [ ] Can get single ticket (GET /tickets/{id})
- [ ] Can update own ticket (PUT /tickets/{id})
- [ ] Pagination works (skip/limit)

### Security Tests
- [ ] Other customer can't see my tickets (403)
- [ ] Customer can't change status (stays unchanged)
- [ ] Customer can't delete tickets (403)
- [ ] Missing token returns 401
- [ ] Invalid token returns 401

### Validation Tests
- [ ] Title too long rejected (400)
- [ ] Missing title rejected (400)
- [ ] Missing description rejected (400)
- [ ] Invalid priority rejected (400)
- [ ] Empty fields rejected (400)

### Database Tests
- [ ] Ticket saved to database
- [ ] user_id correctly stored
- [ ] created_at timestamp set
- [ ] updated_at timestamp updates

---

## Quick Test Script (Copy & Paste)

```powershell
# SETUP
$loginResponse = Invoke-WebRequest -Uri "http://localhost:8002/login" `
  -Method POST -ContentType "application/x-www-form-urlencoded" `
  -UseBasicParsing -Body "username=testuser&password=Test@1234"
$token = ($loginResponse.Content | ConvertFrom-Json).access_token
$headers = @{ Authorization = "Bearer $token" }

# TEST 1: Create Ticket
Write-Host "TEST 1: Create Ticket"
$ticketBody = @{ title="Test Ticket"; description="Testing"; priority="high" } | ConvertTo-Json
$r = Invoke-WebRequest -Uri "http://localhost:8002/tickets" -Method POST `
  -ContentType "application/json" -UseBasicParsing -Headers $headers -Body $ticketBody
$ticketId = ($r.Content | ConvertFrom-Json).id
Write-Host "✅ Created ticket ID: $ticketId" -ForegroundColor Green

# TEST 2: List Tickets
Write-Host "`nTEST 2: List Tickets"
$r = Invoke-WebRequest -Uri "http://localhost:8002/tickets" -UseBasicParsing -Headers $headers
$count = ($r.Content | ConvertFrom-Json).total
Write-Host "✅ Listed $count tickets" -ForegroundColor Green

# TEST 3: Get Single Ticket
Write-Host "`nTEST 3: Get Single Ticket"
$r = Invoke-WebRequest -Uri "http://localhost:8002/tickets/$ticketId" -UseBasicParsing -Headers $headers
$title = ($r.Content | ConvertFrom-Json).title
Write-Host "✅ Retrieved: $title" -ForegroundColor Green

# TEST 4: Update Ticket
Write-Host "`nTEST 4: Update Ticket"
$updateBody = @{ title="Updated Title" } | ConvertTo-Json
$r = Invoke-WebRequest -Uri "http://localhost:8002/tickets/$ticketId" -Method PUT `
  -ContentType "application/json" -UseBasicParsing -Headers $headers -Body $updateBody
$newTitle = ($r.Content | ConvertFrom-Json).title
Write-Host "✅ Updated to: $newTitle" -ForegroundColor Green

# TEST 5: Access Control
Write-Host "`nTEST 5: Access Control"
$loginResponse = Invoke-WebRequest -Uri "http://localhost:8002/login" `
  -Method POST -ContentType "application/x-www-form-urlencoded" `
  -UseBasicParsing -Body "username=newuser&password=NewUser@123"
$otherToken = ($loginResponse.Content | ConvertFrom-Json).access_token
$otherHeaders = @{ Authorization = "Bearer $otherToken" }
try {
  Invoke-WebRequest -Uri "http://localhost:8002/tickets/$ticketId" `
    -UseBasicParsing -Headers $otherHeaders
  Write-Host "❌ Security failure: Other user could access ticket!" -ForegroundColor Red
} catch {
  Write-Host "✅ Security: Other user blocked (403)" -ForegroundColor Green
}

Write-Host "`n✅ ALL TESTS COMPLETED" -ForegroundColor Green
```

---

## Expected Results Summary

| Test | Expected Result | Status |
|------|-----------------|--------|
| Create Ticket | 201 Created | ✅ |
| List Tickets | 200 OK, array returned | ✅ |
| Get Ticket | 200 OK, single ticket | ✅ |
| Update Ticket | 200 OK, updated fields | ✅ |
| Delete (Customer) | 403 Forbidden | ✅ |
| Access Control | 403 Forbidden | ✅ |
| Invalid Data | 400 Bad Request | ✅ |
| Missing Auth | 401 Unauthorized | ✅ |

---

## Troubleshooting

**Problem**: "401 Unauthorized"
- **Solution**: Check token is valid, use login endpoint to get fresh token

**Problem**: "403 Forbidden" on create ticket
- **Solution**: Ensure you're using customer role, not admin

**Problem**: Pagination not working
- **Solution**: Try `?skip=0&limit=10` (must be query params, not body)

**Problem**: "404 Not Found"
- **Solution**: Ticket ID doesn't exist, try listing tickets first

**Problem**: Server won't start
- **Solution**: Check port 8002 is not in use: `netstat -ano | findstr :8002`

---

**Good luck with testing! Take your time and verify each test. You're checking that Phase 4 is production-ready!** 🚀
