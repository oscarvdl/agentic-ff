# Decision Record: Split Orders and Billing into Separate Contexts

## Status
Accepted

## Context
Order capture and invoicing changed together for two years because they
shared a model. Tax rules changed on a regulator's timetable, order flow
changed on the product team's, and every tax change required regression
testing the checkout path.

## Decision
Orders owns the lifecycle of an order: lines, quantities, fulfilment
state. Billing owns money: VAT rates, invoice totals, payment terms.
Orders never computes a tax amount. It publishes an order, and Billing
prices it.

## Consequences
The contexts version independently and a tax change no longer touches
checkout. The cost is an integration boundary where there used to be a
method call, and a VAT rate table with exactly one home.

## Alternatives Considered
A shared kernel holding the money types, with both contexts depending on
it. Rejected because the rate table is the thing that changes, and a
shared kernel would have put the change back in both contexts at once.

## Related
Superseded ADR-0004, the single-model order design.
