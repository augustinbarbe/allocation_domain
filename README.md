# DDD event-driven

Boiler plate for Domain driven and event driven service
Inspired by the amazing Architecture Patterns with Python

- Domain centric with uow and repository pattern
- Event driven (internal event loop and external message bus)
- Dependency injection for external connector (among those : orm, object storage, authorization server)

## Developpement

```bash
git clone git@github.com:augustinbarbe/ddd_architecture.git
cd ddd_architecture/
```

Run the application stack for local development ( support hot reload):
Requires docker

```bash
make run
```

Delete the stack (including database)

```bash
make clean
```

Run unit tests

```
make test
```
