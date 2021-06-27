# Allocation service

Boiler plate for Domain driven and event driven service
Inspired by the work from Architecture Patterns with Python (https://www.oreilly.com/library/view/architecture-patterns-with/9781492052197/)

- Domain centric with uow and repository pattern
- Event driven (internal event loop and external message bus)
- Dependency injection for external connector (among those : orm, object storage, authorization server)
- Production grade API (pagination, JWT authentication, RESTful)

## Developpement

```bash
git clone git@github.com:augustinbarbe/allocation_domain.git
cd allocation_domain/
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

Run tests

```
make test
```

## Domain requirements :

- A pool is a combination of a Resource and a quantity
- The service allocates resource requests on Pools
- A request is allocated to a pool of the corresponding resource if it has enough quantity
- Pools can be added. If a pool has a new resource, the resource must be added to the inventory
- Pools quantity can be changed. If a pool has its quantity decreased, already allocated resources shall be deallocated

## Entrypoints :

There are two entrypoints to interact with the service :

- A rest API to request resources and create new pools
- A pubsub consumer which listen for pool quantity modifications events
