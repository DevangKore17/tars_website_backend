Requirements for the backend

1. Reply Instantly (Don't Keep Them Waiting)
The Goal: The moment an email arrives, we need to say "Got it!" (HTTP 202 Accepted) before we actually process or route the email.
Why: If we take too long figuring out where the email goes, the provider will think the request failed and will keep blasting us with the same email over and over.

2. Inspect the Package (Data Validation)
The Goal: Use Pydantic to strictly define what an incoming email should look like (e.g., it must have a sender, a recipient, and a body).
Why: Sometimes the provider sends weird, broken, or missing data. If the package doesn't meet our strict rules, we reject it immediately so it doesn't crash our app further down the line.

3. Do the Heavy Lifting in the Background (asynchronous )
The Goal: The main FastAPI endpoint acts like a receptionist—it just takes the package, gives a receipt, and hands it off. The actual work of reading the rules and forwarding the email needs to happen in a background task.
Why: This keeps the main app incredibly fast and responsive, allowing us to handle a large volume of incoming emails without freezing up.
