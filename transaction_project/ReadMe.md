Real-Time Transaction Monitoring API Documentation
===============================================

Introduction:
--------------
This API implements a real-time transaction monitoring system using Django. It evaluates various policies to trigger alerts or actions when certain conditions are met in transaction data.

URL Endpoints:
---------------
1. `POST /api/transactions/create/`
   Purpose: Creates a new transaction based on user input.
   Input:
   - user: User's identifier.
   - amount: Transaction amount.
   - chosen_tier: Chosen tier number (1 or 2).
   Actions:
   - Validates if the user is flagged.
   - Checks if the transaction amount is within allowed limits.
   - Verifies if the chosen tier is valid and within its limits.
   - Ensures that no multiple transactions occur within a minute.
   - Records the transaction in the database.
   - Evaluates policies and triggers email alerts if needed.
   Returns:
   - HTTP 200 if successful, or an error message if validation fails.

2. `POST /api/policies/check/`
   Purpose: Triggers policy evaluation for unprocessed transactions.
   Input: None
   Actions:
   - Fetches unprocessed transactions.
   - For each transaction, evaluates policies and takes actions.
   Returns: None

Models:
-------
1. Transaction:
   - Fields: user (CharField), amount (DecimalField), chosen_tier_number (IntegerField),
             timestamp (DateTimeField), flagged (BooleanField), processed (BooleanField)
   - Purpose: Represents a transaction record in the database.
   - Connections: Connected to URL endpoint `/api/transactions/create/` for transaction creation.

Scheduler:
----------
- A background scheduler is used to perform policy evaluation at regular intervals.
- The scheduler is set to run the `scheduled_policy_evaluation` function every 30 minutes.
- This function fetches unprocessed transactions and evaluates policies for each transaction.

Functions and Logic:
---------------------
1. `scheduled_policy_evaluation()`:
   - Purpose: Evaluates policies for unprocessed transactions at regular intervals.
   - Fetches unprocessed transactions.
   - Calls `process_single_transaction()` for each transaction.

2. `policy_evaluation(transaction)`:
   - Purpose: Evaluates policies for a given transaction and triggers actions.
   - Checks if transaction amount is below the tier limit and sends notifications.

3. `send_notification_email(user, amount, chosen_tier_number)`:
   - Purpose: Sends email notifications for transaction alerts.
   - Creates and sends an email to notify about a transaction.

4. `process_transaction(request)`:
   - Purpose: Handles incoming transaction creation requests.
   - Validates user's flagged status, transaction amount, tier choice, and frequency.
   - Records the transaction, triggers policy evaluation, and returns appropriate response.

5. `process_single_transaction(transaction)`:
   - Purpose: Handles policy evaluation and processing for a single transaction.
   - Calls `policy_evaluation(transaction)` and marks the transaction as processed.

6. `is_user_flagged(user)`:
   - Purpose: Checks if a user is flagged by querying the database.

7. `has_recent_transaction(user)`:
   - Purpose: Checks if a user has made recent transactions within the last minute.

Connection Between Endpoints, Views, and Model:
-----------------------------------------------
- The `Transaction` model represents transaction records in the database.
- The `/api/transactions/create/` endpoint is connected to the `process_transaction` view.
- The view validates input, creates transaction records, and triggers policy evaluation.
- The scheduler regularly triggers the `scheduled_policy_evaluation` function.
