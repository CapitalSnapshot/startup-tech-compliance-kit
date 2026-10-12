# Runbooks

Short, numbered, copy-and-run. Each one states who may start it, what must be true first, the steps, how to know it worked, and how to undo it. Write the time next to each step as you run it; that record is your evidence.

- [`restore-test.md`](restore-test.md): prove your backups work and measure recovery time
- [`cutover.md`](cutover.md): move live traffic from an old system to a new one
- [`rollback.md`](rollback.md): go back to the old system
- [`incident-response.md`](incident-response.md): the first hour of an incident, by role (controller or processor), and who to tell
- [`tabletop-incident-notification.md`](tabletop-incident-notification.md): a rehearsal that separates contractual from statutory notification deadlines
- [`rebuild-from-nothing.md`](rebuild-from-nothing.md): prove you can recreate production from the repository and the secrets manager
