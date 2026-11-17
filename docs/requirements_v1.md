# Requirements from Customer Feedback

_Generated with prompt version `v1`. Priorities are computed from feedback evidence; story text is drafted by an LLM and should be reviewed by a BA._

## Theme ranking

| Rank | Theme | Mentions | High-urgency | Avg rating | Score | Priority |
|---|---|---|---|---|---|---|
| 1 | delivery_delay | 5.0 | 4.0 | 1.2 | 14.0 | high |
| 2 | app_bug | 6.0 | 2.0 | 1.8 | 14.0 | high |
| 3 | payment_issue | 2.0 | 2.0 | 1.5 | 6.0 | high |
| 4 | pricing | 3.0 | 0.0 | 3.0 | 6.0 | medium |

## User stories

### REQ-01: Improved Delivery Tracking and Estimation
- **Theme:** delivery_delay
- **Priority:** high
- **Source feedback IDs:** 1, 12, 15, 23, 30

**User story:** As a customer, I want to receive accurate delivery estimates and tracking information so that I can plan my day accordingly and avoid delays.

**Acceptance criteria:**
1. Delivery estimates are accurate within 10 minutes
2. Real-time tracking of order status
3. Notification system for delivery delays
4. Support chat is always available and responsive
5. Driver is held accountable for incorrect deliveries

**Assumptions:**
- Customer has a stable internet connection
- Driver has access to GPS and real-time traffic updates
- Support team is available during business hours

**Open questions:**
- How will the system handle delivery delays due to traffic or road closures?
- Can the system provide a reason for the delay?
- How will the driver be incentivized to provide accurate delivery estimates and tracking information?

### REQ-02: Fix App Bugs
- **Theme:** app_bug
- **Priority:** high
- **Source feedback IDs:** 4, 8, 10, 18, 24, 27

**User story:** As a user, I want to be able to apply promo codes, search for products, update my delivery address, complete payments, receive relevant notifications, and log in successfully, so I can have a seamless shopping experience.

**Acceptance criteria:**
1. App should not crash when applying promo codes
2. Search functionality should return relevant results
3. User should be able to update delivery address successfully
4. App should not freeze during payment
5. Notifications should be relevant and not spammy
6. Login should work successfully after the latest update

**Assumptions:**
- User has a stable internet connection
- User has a valid promo code
- User has a valid login credentials

**Open questions:**
- How many promo codes should be available for users to apply?
- What is the optimal search query length for relevant results?
- What is the ideal frequency for notifications?
- What is the maximum allowed number of failed login attempts before account lockout?

### REQ-03: Payment Issue Refund and Deduction
- **Theme:** payment_issue
- **Priority:** high
- **Source feedback IDs:** 3, 14

**User story:** As a customer, I want to be able to request a refund for a duplicate charge and have my payment failed transaction reversed, so that I can avoid financial loss.

**Acceptance criteria:**
1. The system allows customers to request a refund for a duplicate charge.
2. The system reverses the payment failed transaction and credits the customer's account.
3. The system notifies the customer of the refund and transaction reversal within 24 hours.
4. The system provides a clear explanation of the refund and transaction reversal process.
5. The system ensures that the refund and transaction reversal are processed within 3 business days.
6. The system provides a secure and reliable payment processing system.
7. The system allows customers to track the status of their refund and transaction reversal requests.
8. The system provides a clear and concise error message when a payment failed transaction is detected.
9. The system provides a clear and concise error message when a duplicate charge is detected.
10. The system ensures that the customer's account is updated to reflect the refund and transaction reversal.
11. The system provides a clear and concise explanation of the refund and transaction reversal process to the customer's support team.

**Assumptions:**
- The customer has a valid payment method on file.
- The customer has a valid email address on file.
- The system has the necessary permissions to process refunds and transaction reversals.
- The system has the necessary permissions to update customer accounts.

**Open questions:**
- How will the system handle cases where the customer's payment method is invalid?
- How will the system handle cases where the customer's account is overdrawn?
- What is the process for escalating a refund or transaction reversal request to a support team?
- How will the system communicate with the customer regarding the status of their refund and transaction reversal request?

### REQ-04: Optimize Pricing for Daily Use
- **Theme:** pricing
- **Priority:** medium
- **Source feedback IDs:** 5, 9, 21

**User story:** As a daily user of the service, I want to be able to order food without excessive delivery fees, so that I can continue to use the service without breaking the bank.

**Acceptance criteria:**
1. Delivery fees should not exceed 10% of the total order value
2. Portion sizes should be adjusted to maintain a consistent price point
3. All fees should be clearly displayed at checkout, including service fee, delivery fee, and tax

**Assumptions:**
- Customers will continue to order daily
- Service will continue to operate with the same pricing structure

**Open questions:**
- How will the service handle price increases for certain menu items?
- Will there be any promotions or discounts to offset the increased fees?
