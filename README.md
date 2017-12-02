# MiniBank
MiniBank system

This system requires Domain Driven Design, REST, CQRS and Event Sourcing. Also, there needs to be a Database involved.

## Considerations

This project is being developed in Python so I can focus on learning the theory behind the system requirements separately from the implementation. This is possible because I already know Python, so there is no extra difficulty being imposed by the programming language.

Database is a simple stack of JSON objects representing the events needed to rebuild application state. Implementation in PostgreSQL

There will be a simple web interface to interact with the system, from the point of view of a sysadmin.
