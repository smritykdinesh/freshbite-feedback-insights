# Requirements from Customer Feedback

_Generated with prompt version `v2`. Priorities are computed from feedback evidence; story text is drafted by an LLM and should be reviewed by a BA._

## Theme ranking

| Rank | Theme | Mentions | High-urgency | Avg rating | Score | Priority |
|---|---|---|---|---|---|---|
| 1 | app_bug | 6.0 | 2.0 | 1.8 | 14.0 | high |
| 2 | delivery_delay | 5.0 | 4.0 | 1.2 | 14.0 | high |
| 3 | payment_issue | 2.0 | 2.0 | 1.5 | 6.0 | high |
| 4 | pricing | 3.0 | 0.0 | 3.0 | 6.0 | medium |

## User stories

### REQ-01: Stable Promo Code Checkout and Navigation
- **Theme:** app_bug
- **Priority:** high
- **Source feedback IDs:** 4, 8, 10, 18, 24, 27

**User story:** As a returning customer, I want promo codes to apply without errors and search results to be accurate so that I can complete my order smoothly.

**Acceptance criteria:**
1. Given a valid promo code, when the customer applies it at checkout, then the discount is shown before payment.
2. Given a valid search query, when the customer submits it, then relevant results are displayed.
3. Given a valid promo code, when the customer completes payment, then the charged amount matches the discounted total.
4. Given a valid search query, when the customer clicks on a result, then the corresponding order details are displayed.

**Assumptions:**
- Promo codes are single-use per order.

**Open questions:**
- Can promo codes be combined with loyalty rewards?

### REQ-02: Reliable Delivery Time Estimation
- **Theme:** delivery_delay
- **Priority:** high
- **Source feedback IDs:** 1, 12, 15, 23, 30

**User story:** As a customer, I want the delivery time estimate to be accurate and reflect the actual delivery time so that I can plan my day accordingly.

**Acceptance criteria:**
1. Given a delivery estimate of 30 minutes, when the customer receives a notification of delivery, then the delivery time is within 15 minutes of the estimated time.
2. Given a delivery estimate of 1 hour, when the customer receives a notification of delivery, then the delivery time is within 30 minutes of the estimated time.
3. Given a delivery estimate of 2 hours, when the customer receives a notification of delivery, then the delivery time is within 1 hour of the estimated time.
4. Given a delivery estimate, when the customer reports a delay, then the support team investigates and provides a revised delivery time estimate.
5. Given a delivery estimate, when the customer reports a missed delivery, then the support team sends a notification with a revised delivery time estimate and a new estimated delivery time.

**Assumptions:**
- Delivery drivers are aware of their estimated delivery time and can provide updates to the app.

**Open questions:**
- What is the maximum acceptable delay for delivery estimates?
- Can delivery drivers provide real-time updates on their location?
- How will missed deliveries be handled in terms of refunds or replacements?

### REQ-03: Error handling for payment failures
- **Theme:** payment_issue
- **Priority:** high
- **Source feedback IDs:** 3, 14

**User story:** As a customer, I want the app to notify me of payment failures and offer a refund when I've been charged twice for the same order so that I can resolve the issue quickly.

**Acceptance criteria:**
1. Given a payment fails, when the customer is notified, then an option to dispute the charge is presented.
2. Given a payment failure, when the customer disputes the charge, then a refund is processed within 24 hours.
3. Given a duplicate charge, when the customer contacts support, then a refund is issued immediately.

**Assumptions:**
- Payment failures are typically due to insufficient funds or expired payment methods.

**Open questions:**
- What is the maximum timeframe for processing a refund after a payment failure?

### REQ-04: Transparent pricing with clear fees
- **Theme:** pricing
- **Priority:** medium
- **Source feedback IDs:** 5, 9, 21

**User story:** As a frequent user, I want the total cost of my order to include all applicable fees upfront so that I can budget accurately and avoid surprises.

**Acceptance criteria:**
1. Given a menu item, when the customer views their order summary, then all applicable fees (delivery, service, tax) are clearly displayed.
2. Given a menu item, when the customer completes checkout, then the total cost (including fees) is displayed before final payment.
3. Given a menu item, when the customer reviews their order history, then the total cost (including fees) for each order is visible.
4. Given a menu item, when the customer requests a refund, then the refund amount (after fees) is processed correctly.

**Assumptions:**
- Menu items have a fixed price and no additional charges.

**Open questions:**
- Are there any discounts or promotions that could affect the total cost?
