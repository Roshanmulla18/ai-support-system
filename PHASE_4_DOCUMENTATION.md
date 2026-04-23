# Phase 4 - Ticket Management System (CRUD)

## Overview

Phase 4 implements a complete **Ticket Management System** with full CRUD (Create, Read, Update, Delete) operations. It provides a secure, role-based API for managing customer support tickets, including classification fields for AI integration in future phases.

**Status**: ✅ **COMPLETE & TESTED**

---

## Architecture

### 1. Database Model

#### Ticket Table (`tickets`)

| Field | Type | Constraints | Purpose |
|-------|------|-------------|---------|
| `id` | Integer | PK, Index | Unique ticket identifier |
| `title` | String | NOT NULL | Ticket summary (max 200 chars) |
| `description` | Text | NOT NULL | Detailed problem description |
| `status` | String | DEFAULT "open" | Ticket state (open, in_progress, resolved, closed) |
| `priority` | String | DEFAULT "medium" | Urgency level (low, medium, high, urgent) |
| `user_id` | Integer | FK(users.id), NOT NULL | Customer who created ticket |
| `assigned_to` | Integer | FK(users.id), NULL | Agent/Admin assigned to ticket |
| `ai_category` | String | NULL | AI classification (Phase 5+) |
| `ai_confidence` | Integer | NULL | Classification confidence (0-100) |
| `sentiment_score` | Integer | NULL | Customer sentiment (-100 to +100) |
| `ai_suggested_response` | Text | NULL | AI's proposed response |
| `resolved_by_ai` | Boolean | DEFAULT False | Was this resolved autonomously? |
| `created_at` | DateTime | Server timestamp | When ticket was created |
| `updated_at` | DateTime | Auto-updated | Last modification time |

**Relationships**:
```
Ticket.user_id → User.id (creator)
Ticket.assigned_to → User.id (assigned agent/admin)
```

---

## API Endpoints

All endpoints require **JWT authentication** via Bearer token in the `Authorization` header.

### 1. Create Ticket

**Endpoint**: `POST /tickets`

**Authentication**: Required (Bearer token)

**Request Body**:
```json
{
  "title": "Cannot login to account",
  "description": "I forgot my password and cannot log in. Please help me reset it.",
  "priority": "high"
}
```

**Validation Rules**:
- `title`: Required, 1-200 characters
- `description`: Required, 1-5000 characters
- `priority`: Optional, defaults to "medium". Valid: "low", "medium", "high", "urgent"

**Response** (201 Created):
```json
{
  "id": 2,
  "title": "Cannot login to account",
  "description": "I forgot my password and cannot log in. Please help me reset it.",
  "status": "open",
  "priority": "high",
  "user_id": 1,
  "assigned_to": null,
  "ai_category": null,
  "ai_confidence": null,
  "sentiment_score": null,
  "ai_suggested_response": null,
  "resolved_by_ai": false,
  "created_at": "2026-04-23T08:15:30.123456",
  "updated_at": "2026-04-23T08:15:30.123456"
}
```

**Error Responses**:
- `401 Unauthorized` – Missing or invalid token
- `400 Bad Request` – Validation error (title too long, missing fields, etc.)

**Usage Example** (cURL):
```bash
curl -X POST http://localhost:8002/tickets \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Password reset needed",
    "description": "I forgot my password",
    "priority": "high"
  }'
```

**Usage Example** (PowerShell):
```powershell
$body = @{
  title = "Cannot login"
  description = "Forgot password"
  priority = "high"
} | ConvertTo-Json

$headers = @{ Authorization = "Bearer $token" }

Invoke-WebRequest -Uri "http://localhost:8002/tickets" `
  -Method POST `
  -Headers $headers `
  -ContentType "application/json" `
  -Body $body
```

---

### 2. List Tickets

**Endpoint**: `GET /tickets`

**Authentication**: Required (Bearer token)

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `skip` | int | 0 | Records to skip (pagination) |
| `limit` | int | 100 | Max records to return |
| `status` | string | - | Filter by status (open, in_progress, resolved, closed) |
| `priority` | string | - | Filter by priority (low, medium, high, urgent) |

**Access Control**:
- **Customers** (role="customer"): See only their own tickets
- **Agents** (role="agent"): See all tickets
- **Admins** (role="admin"): See all tickets

**Response** (200 OK):
```json
{
  "total": 2,
  "skip": 0,
  "limit": 100,
  "tickets": [
    {
      "id": 1,
      "title": "Original ticket",
      "description": "First test ticket",
      "status": "open",
      "priority": "medium",
      "user_id": 1,
      "assigned_to": null,
      "ai_category": null,
      "ai_confidence": null,
      "sentiment_score": null,
      "ai_suggested_response": null,
      "resolved_by_ai": false,
      "created_at": "2026-02-20T09:00:00",
      "updated_at": "2026-02-20T09:00:00"
    },
    {
      "id": 2,
      "title": "Cannot login to account",
      "description": "I forgot my password...",
      "status": "open",
      "priority": "high",
      "user_id": 1,
      "assigned_to": null,
      "ai_category": null,
      "ai_confidence": null,
      "sentiment_score": null,
      "ai_suggested_response": null,
      "resolved_by_ai": false,
      "created_at": "2026-04-23T08:15:30.123456",
      "updated_at": "2026-04-23T08:15:30.123456"
    }
  ]
}
```

**Error Responses**:
- `401 Unauthorized` – Missing or invalid token
- `400 Bad Request` – Invalid filter value (e.g., `status=invalid_status`)
- `403 Forbidden` – User role unknown

**Usage Example** (cURL):
```bash
# Get all customer's tickets
curl -X GET "http://localhost:8002/tickets" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Filter by status
curl -X GET "http://localhost:8002/tickets?status=open" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Pagination
curl -X GET "http://localhost:8002/tickets?skip=10&limit=20" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 3. Get Single Ticket

**Endpoint**: `GET /tickets/{ticket_id}`

**Authentication**: Required (Bearer token)

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `ticket_id` | int | Unique ticket identifier |

**Access Control**:
- **Customers**: Can only view their own tickets
- **Agents/Admins**: Can view any ticket

**Response** (200 OK):
```json
{
  "id": 2,
  "title": "Cannot login to account",
  "description": "I forgot my password and cannot log in. Please help me reset it.",
  "status": "open",
  "priority": "high",
  "user_id": 1,
  "assigned_to": null,
  "ai_category": null,
  "ai_confidence": null,
  "sentiment_score": null,
  "ai_suggested_response": null,
  "resolved_by_ai": false,
  "created_at": "2026-04-23T08:15:30.123456",
  "updated_at": "2026-04-23T08:15:30.123456"
}
```

**Error Responses**:
- `401 Unauthorized` – Missing or invalid token
- `403 Forbidden` – Customer trying to view another customer's ticket
- `404 Not Found` – Ticket ID doesn't exist

**Usage Example**:
```bash
curl -X GET http://localhost:8002/tickets/2 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 4. Update Ticket

**Endpoint**: `PUT /tickets/{ticket_id}`

**Authentication**: Required (Bearer token)

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `ticket_id` | int | Unique ticket identifier |

**Request Body** (all fields optional):
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "status": "in_progress",
  "priority": "urgent",
  "assigned_to": 2,
  "ai_category": "password_reset",
  "ai_confidence": 85,
  "sentiment_score": -50,
  "ai_suggested_response": "Your password has been reset. Check your email.",
  "resolved_by_ai": false
}
```

**Validation Rules**:
- `status`: Must be one of "open", "in_progress", "resolved", "closed"
- `priority`: Must be one of "low", "medium", "high", "urgent"
- `assigned_to`: Must be valid user ID with role "agent" or "admin", or 0 to unassign
- `ai_confidence`: Integer 0-100
- `sentiment_score`: Integer -100 to +100

**Access Control**:

**Customers (role="customer")**:
- ✅ Can update: `title`, `description`
- ❌ Cannot update: `status`, `priority`, `assigned_to`, AI fields

**Agents/Admins (role="agent" or "admin")**:
- ✅ Can update: All fields
- ✅ Can assign tickets to other agents/admins
- ✅ Can update AI classification and response fields

**Response** (200 OK):
```json
{
  "id": 2,
  "title": "Updated title",
  "description": "Updated description",
  "status": "in_progress",
  "priority": "urgent",
  "user_id": 1,
  "assigned_to": 2,
  "ai_category": "password_reset",
  "ai_confidence": 85,
  "sentiment_score": -50,
  "ai_suggested_response": "Your password has been reset. Check your email.",
  "resolved_by_ai": false,
  "created_at": "2026-04-23T08:15:30.123456",
  "updated_at": "2026-04-23T08:20:45.789012"
}
```

**Error Responses**:
- `401 Unauthorized` – Missing or invalid token
- `403 Forbidden` – Customer trying to update status; non-creator customer accessing ticket
- `404 Not Found` – Ticket ID doesn't exist
- `400 Bad Request` – Invalid enum value (status/priority); assigned user not found; assigned user not an agent/admin

**Usage Examples**:

Customer updating own ticket:
```bash
curl -X PUT http://localhost:8002/tickets/2 \
  -H "Authorization: Bearer CUSTOMER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "New title"}'
```

Agent updating status and assigning:
```bash
curl -X PUT http://localhost:8002/tickets/2 \
  -H "Authorization: Bearer AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress",
    "priority": "high",
    "assigned_to": 3
  }'
```

Admin setting AI classification:
```bash
curl -X PUT http://localhost:8002/tickets/2 \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "resolved",
    "ai_category": "password_reset",
    "ai_confidence": 92,
    "ai_suggested_response": "Password reset completed",
    "resolved_by_ai": true
  }'
```

---

### 5. Delete Ticket

**Endpoint**: `DELETE /tickets/{ticket_id}`

**Authentication**: Required (Bearer token)

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `ticket_id` | int | Unique ticket identifier |

**Access Control**:
- ✅ **Admins only** (role="admin") can delete tickets
- ❌ Customers and agents cannot delete

**Response** (204 No Content):
```
[empty body]
```

**Error Responses**:
- `401 Unauthorized` – Missing or invalid token
- `403 Forbidden` – Non-admin user attempting deletion
- `404 Not Found` – Ticket ID doesn't exist

**Usage Example**:
```bash
curl -X DELETE http://localhost:8002/tickets/2 \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

---

## Role-Based Access Control Matrix

| Operation | Customer | Agent | Admin |
|-----------|----------|-------|-------|
| **Create Ticket** | ✅ (Own only) | ✅ | ✅ |
| **List Tickets** | ✅ (Own only) | ✅ (All) | ✅ (All) |
| **View Ticket** | ✅ (Own only) | ✅ (All) | ✅ (All) |
| **Update Title/Desc** | ✅ (Own) | ✅ (Any) | ✅ (Any) |
| **Update Status** | ❌ | ✅ | ✅ |
| **Update Priority** | ❌ | ✅ | ✅ |
| **Assign Ticket** | ❌ | ✅ | ✅ |
| **Set AI Fields** | ❌ | ✅ | ✅ |
| **Delete Ticket** | ❌ | ❌ | ✅ |

---

## Testing Results

### Endpoint Tests

| Test | Result | Details |
|------|--------|---------|
| Create ticket | ✅ PASS | New ticket created with ID 2 |
| List tickets | ✅ PASS | Customer sees 2 own tickets |
| Get ticket | ✅ PASS | Retrieved ticket 2 successfully |
| Update (customer) | ✅ PASS | Customer can update title |
| Update (agent) | ✅ PASS | Agent can update status/priority |
| Access control | ✅ PASS | Different customer blocked (403) |
| Invalid status | ✅ PASS | Rejected with 400 Bad Request |
| Missing auth | ✅ PASS | Returned 401 Unauthorized |

### Database Tests

✅ Tables auto-created on startup
✅ Foreign key constraints enforced
✅ Data persistence verified
✅ No data loss between server restarts

---

## Code Structure

### Files Modified

1. **`models.py`**
   - Added `Ticket` SQLAlchemy model with 16 fields
   - Defines `__tablename__ = "tickets"`
   - Foreign key relationships to `users` table

2. **`schemas.py`**
   - `TicketCreate` – Input validation for new tickets
   - `TicketUpdate` – Flexible update schema
   - `TicketResponse` – Output format with all fields

3. **`main.py`**
   - Helper function: `ticket_to_response()` for serialization
   - 5 new endpoints with full CRUD operations
   - Role-based access control in each endpoint
   - Updated startup banner showing Phase 4

---

## Integration with Previous Phases

### Phase 3 Integration
- All ticket endpoints use Phase 3 JWT authentication
- User roles (customer, agent, admin) control ticket access
- User table relationships maintained

### Data Flow
```
Customer → Login (Phase 3)
         → Get JWT Token
         → POST /tickets (Phase 4)
         → Get Ticket Details
         → Update Own Ticket
         
Agent    → Login (Phase 3)
         → Get JWT Token  
         → GET /tickets (all)
         → PUT /tickets/{id} (update status)
         → Set AI Classification (Phase 4)
```

---

## Future Integration (Phase 5+)

The ticket model is designed to support:

### AI Agent Integration (Phase 5)
- `ai_category` – Will be populated by LLM classification
- `ai_confidence` – Confidence score for classification
- `sentiment_score` – Customer emotion analysis
- `ai_suggested_response` – AI-generated response
- `resolved_by_ai` – Flag for autonomous resolution

### Example Phase 5 Flow
```
1. Ticket created → stored with status=open
2. AI Agent reads ticket
3. AI classifies: ai_category="password_reset", ai_confidence=92
4. AI generates: ai_suggested_response="Your password has been reset..."
5. AI executes action (calls password reset API)
6. Update: status="resolved", resolved_by_ai=true
7. Customer receives resolution
```

---

## Performance Considerations

- **Pagination**: List endpoint supports `skip`/`limit` for large datasets
- **Indexing**: `user_id` and `assigned_to` indexed for fast filtering
- **Query Optimization**: Role-based filtering done at database level
- **Response Size**: Only necessary fields returned (no password hashes, etc.)

---

## Error Handling

All errors follow standard HTTP conventions:

| Status | Meaning | Example |
|--------|---------|---------|
| 200 | Success | GET /tickets returned data |
| 201 | Created | POST /tickets created new ticket |
| 204 | No Content | DELETE /tickets/2 succeeded |
| 400 | Bad Request | Invalid status value |
| 401 | Unauthorized | Missing JWT token |
| 403 | Forbidden | Customer accessing another's ticket |
| 404 | Not Found | Ticket ID doesn't exist |
| 500 | Server Error | Database connection failed |

Error Response Format:
```json
{
  "detail": "Access denied"
}
```

---

## Quick Start Examples

### As a Customer

1. **Create a support ticket**:
   ```bash
   curl -X POST http://localhost:8002/tickets \
     -H "Authorization: Bearer $CUSTOMER_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Cannot reset password",
       "description": "The reset link expired",
       "priority": "high"
     }'
   ```

2. **View your tickets**:
   ```bash
   curl -X GET http://localhost:8002/tickets \
     -H "Authorization: Bearer $CUSTOMER_TOKEN"
   ```

3. **Update ticket description**:
   ```bash
   curl -X PUT http://localhost:8002/tickets/2 \
     -H "Authorization: Bearer $CUSTOMER_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "description": "Actually, I found the issue. Please ignore."
     }'
   ```

### As an Agent

1. **List all tickets**:
   ```bash
   curl -X GET http://localhost:8002/tickets \
     -H "Authorization: Bearer $AGENT_TOKEN"
   ```

2. **Assign ticket and update status**:
   ```bash
   curl -X PUT http://localhost:8002/tickets/2 \
     -H "Authorization: Bearer $AGENT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "assigned_to": 3,
       "status": "in_progress"
     }'
   ```

### As an Admin

1. **View all tickets with filter**:
   ```bash
   curl -X GET "http://localhost:8002/tickets?status=open&priority=urgent" \
     -H "Authorization: Bearer $ADMIN_TOKEN"
   ```

2. **Set AI classification on ticket**:
   ```bash
   curl -X PUT http://localhost:8002/tickets/2 \
     -H "Authorization: Bearer $ADMIN_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "ai_category": "account_unlock",
       "ai_confidence": 87,
       "ai_suggested_response": "Account unlocked successfully"
     }'
   ```

3. **Delete resolved ticket**:
   ```bash
   curl -X DELETE http://localhost:8002/tickets/1 \
     -H "Authorization: Bearer $ADMIN_TOKEN"
   ```

---

## Frequently Asked Questions

**Q: Can a customer delete their own ticket?**
A: No, only admins can delete tickets. Customers can update status if they want to mark it resolved.

**Q: Can an agent see all tickets or only assigned ones?**
A: Agents can see ALL tickets in the system. In Phase 5, we can add filtering by `assigned_to` if needed.

**Q: What happens if an agent assigns a ticket to a customer?**
A: The API validates that `assigned_to` user has role "agent" or "admin" and rejects if they don't.

**Q: Are timestamps automatically managed?**
A: Yes! `created_at` is set once at creation. `updated_at` automatically updates every time the ticket changes.

**Q: Can an agent update a customer's title/description?**
A: Yes, agents have full update permissions on any field.

---

## Troubleshooting

**Issue**: "401 Unauthorized"
- **Solution**: Ensure JWT token is included in `Authorization: Bearer <token>` header

**Issue**: "403 Forbidden" when accessing ticket
- **Solution**: If you're a customer, you can only see your own tickets (check `user_id`)

**Issue**: Cannot assign ticket
- **Solution**: Ensure target user exists and has role "agent" or "admin"

**Issue**: "400 Bad Request" with invalid status
- **Solution**: Use only: "open", "in_progress", "resolved", "closed"

---

## Summary

Phase 4 delivers a production-ready ticket management system with:

✅ Full CRUD operations
✅ Role-based access control
✅ Pagination and filtering
✅ AI-ready fields for Phase 5
✅ Comprehensive error handling
✅ Secure JWT authentication

**Status**: Ready for Phase 5 (AI Agent Integration)
