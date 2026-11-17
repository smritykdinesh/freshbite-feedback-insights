# Sample business requirements document

## Problem

Customers report that search results sometimes fail to open, interrupting their ability to find information.

## User story

As a customer, I want search results to open reliably, so that I can reach the information I need without repeating my search.

## Acceptance criteria

- Given a search returns a result, when the customer selects it, then the corresponding item opens.
- Given an item cannot be opened, when the failure occurs, then the customer sees a clear message and a useful next step.
- Given search behavior changes, when reliability is monitored, then failures can be measured by result and error type.

## Open questions

- Which result types and platforms are affected?
- What is the current failure rate and target recovery time?
- Should failed results offer retry, alternate results, or both?
