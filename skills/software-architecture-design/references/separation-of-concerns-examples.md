# Separation of Concerns and GOOD/RED Examples

Use this reference when a boundary decision depends on responsibility assignment or when a proposed refactor may only be a file split.

## Definition

**Separation of Concerns (SoC)** means that responsibilities which change for different reasons have explicit, owned boundaries and communicate through narrow contracts. A concern is a cohesive responsibility or change axis—not merely a noun, directory, class, or layer name. A boundary is architectural when it also makes ownership, dependency direction, lifecycle, trust, transaction, failure, performance, or compatibility behavior explicit.

SoC is not achieved by moving code into more files. If the same code still owns the same decisions, imports still point through the same concrete dependencies, and no contract or invariant changes, the topology has been renamed rather than separated.

## Practice

1. **Identify concerns and change axes.** Name the business rule, persistence, transport, rendering, scheduling, security, or other responsibility and the reason each would change.
2. **Assign ownership.** Give each mutable fact and policy one authoritative owner, lifecycle, visibility, and failure/recovery authority.
3. **Define a narrow contract.** Specify inputs, outputs, errors, ordering, consistency, security, and resource invariants. Keep transport and storage types at adapters unless they are part of the intentional contract.
4. **Set dependency direction.** Adapters depend on stable policy/ports; policy does not import transport or persistence. Detect cycles and prevent dependency reversal.
5. **Test the contract.** Test semantic rules without infrastructure, adapters against their contract, and boundary integration with representative failure cases.
6. **Distinguish a real boundary from a split.** Require an independently testable decision, owner, dependency edge, or lifecycle/failure behavior; otherwise keep the code together and record why.

## Example map

| ID | Decision covered | GOOD/RED pair |
| --- | --- | --- |
| `AB-SOC-01` | Business, persistence, and transport ownership | Mixed handler versus ports/adapters around a semantic core |
| `AB-SOC-02` | File split versus dependency improvement | Renamed coupling versus a contract with one-way dependencies |

The snippets are deliberately minimal and illustrative. **RED** shows a failure mode to reject; do not copy it into executable code. Re-run repository-native checks and contract tests for the actual system.

## `AB-SOC-01` — business, persistence, and transport

### RED

```diff
--- a/app/orders.py
+++ b/app/orders.py
@@
 @app.post("/orders")
 def create_order():
-    payload = request.get_json()
-    row = OrderModel(user_id=payload["user_id"], total=payload["total"])
-    db.session.add(row)
-    db.session.commit()
-    requests.post(PAYMENTS_URL, json={"order_id": row.id, "total": row.total})
-    return jsonify({"id": row.id}), 201
+    # Transport parsing, business policy, persistence, and payment I/O
+    # all change this handler for unrelated reasons.
+    payload = request.get_json()
+    if payload["total"] <= 0:
+        return jsonify({"error": "invalid total"}), 400
+    row = OrderModel(user_id=payload["user_id"], total=payload["total"])
+    db.session.add(row)
+    db.session.commit()
+    requests.post(PAYMENTS_URL, json={"order_id": row.id, "total": row.total})
+    return jsonify({"id": row.id}), 201
```

### GOOD

```diff
--- /dev/null
+++ b/orders/domain.py
@@
+def place_order(command, orders, payments):
+    if command.total <= 0:
+        raise InvalidOrder("total must be positive")
+    order = Order(command.user_id, command.total)
+    orders.save(order)
+    payments.authorize(order.id, order.total)
+    return order
--- /dev/null
+++ b/orders/http.py
@@
+@app.post("/orders")
+def create_order():
+    command = CreateOrder.from_json(request.get_json())
+    order = place_order(command, order_repository, payment_port)
+    return jsonify(OrderResponse.from_domain(order)), 201
--- /dev/null
+++ b/orders/persistence.py
@@
+class SqlOrderRepository:
+    def save(self, order):
+        session.add(OrderRow.from_domain(order))
+        session.commit()
```

The domain owns the rule and coordinates through ports; HTTP owns translation and persistence owns storage mapping. The exact transaction and payment consistency contract still needs to be specified and tested.

## `AB-SOC-02` — file splitting versus a real boundary

### RED

```diff
--- a/order.py
+++ b/order.py
@@
-class Order:
-    def total(self): ...
-    def save(self): db.session.add(self); db.session.commit()
-    def to_response(self): return jsonify(self.__dict__)
--- /dev/null
+++ b/order_domain.py
@@
+from flask import jsonify
+from sqlalchemy.orm import Session
+
+class Order:
+    def total(self): ...
+    def save(self, session: Session): session.add(self); session.commit()
+    def to_response(self): return jsonify(self.__dict__)
```

The files moved, but the domain still depends on transport and persistence. Ownership and dependency direction did not improve.

### GOOD

```diff
--- a/order.py
+++ b/order.py
@@
-from flask import jsonify
-from sqlalchemy.orm import Session
-class Order:
-    def save(self, session): ...
-    def to_response(self): ...
+class Order:
+    def total(self): ...
+
+class OrderRepository(Protocol):
+    def save(self, order: Order) -> None: ...
--- /dev/null
+++ b/order_http.py
@@
+def to_response(order: Order) -> Response:
+    return jsonify({"id": order.id, "total": order.total()})
--- /dev/null
+++ b/order_sql.py
@@
+class SqlOrderRepository(OrderRepository):
+    def save(self, order: Order) -> None:
+        session.add(OrderRow.from_domain(order))
+        session.commit()
```

The semantic owner exposes a narrow repository contract; HTTP and SQL adapters depend on that contract. The boundary is real because storage and transport can change independently, and each side has a separately testable invariant.
