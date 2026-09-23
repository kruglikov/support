[PHP Design Patterns & Web Application Architecture](https://softwarepatternslexicon.com/php/)
<table_of_contents color="gray"/>
# OOP
- **Abstraction -** Hiding the complex implementation details and showing only the essential features of an object. It reduces complexity by allowing you to ignore irrelevant details.
- **Encapsulation **- The bundling of data (attributes) and the methods (functions) that operate on that data into a single unit (a class). It also involves restricting direct access to some of an object's components, which is often called "information hiding.”
- **Inheritance -** A mechanism where a new class (child class) is based on an existing class (parent class). The child class inherits the attributes and methods of the parent class and can add its own. It promotes code reusability and establishes an "is-a" relationship.  (descendant, ancestor)
- **Polymorphism -** A mechanism that allows code to interact with objects of different types through a single, uniform interface.
### Types of p**olymorphism**
- <span color="red">Compile-time Polymorphism (Static Binding) \\ Run-time Polymorphism (Dynamic Binding)</span>
- <span color="red">type polymorphism, adhoc polymirphism, interfaces</span>
### Types of Relations:
#### <span color="red">Inheritance vs Composition vs Aggregation vs Association</span>
<details>
<summary>**Inheritance (“is-a” relationship)**</summary>
	- **Definition**: A class (child/subclass) inherits attributes and methods from another class (parent/superclass).
	- **Direction**: Unidirectional (parent ← child).
	- **Lifetime**: Tied to the object’s type, not runtime connections.
	- **Example**: `Dog` inherits from `Animal`.
	python
	```plain text
class Animal:
    def breathe(self):
        print("breathing")

class Dog(Animal):   # Dog is an Animal
    def bark(self):
        print("bark")

d = Dog()
d.breathe()   # inherited method
d.bark()      # own method
	```
	**UML**:
	text
	```plain text
    Animal
      ↑
      |
     Dog
	```
</details>
<details>
<summary>**Association (“uses-a” / “knows-a” relationship)**</summary>
	- **Definition**: A relationship where objects of one class know about objects of another class. It can be **unidirectional** or **bidirectional**.
	- **Direction**: Defined (A → B) or bidirectional.
	- **Lifetime**: Independent lifetimes.
	- **Example**: A `Doctor` knows a `Patient` (and vice versa).
	python
	```plain text
class Doctor:
    def __init__(self, name):
        self.name = name
        self.patients = []

    def add_patient(self, patient):
        self.patients.append(patient)

class Patient:
    def __init__(self, name):
        self.name = name
        self.doctors = []

    def add_doctor(self, doctor):
        self.doctors.append(doctor)

doc = Doctor("House")
pat = Patient("John")
doc.add_patient(pat)   # association
pat.add_doctor(doc)    # optional bidirectional
	```
	**UML**:
	text
	```plain text
Doctor ----------> Patient   (simple association)
or bidirectional:
Doctor <--------> Patient
	```
</details>
<details>
<summary>**Aggregation (“has-a” but weak relationship)**</summary>
	- **Definition**: A specialized form of association where one class **contains** another, but the contained object can exist independently.
	- **Direction**: Usually unidirectional from container to contained.
	- **Lifetime**: Independent — if the container is destroyed, the contained objects can still exist.
	- **Example**: A `Department` has `Professor`s. Professors can exist without the department (they could move to another).
	python
	```plain text
class Professor:
    def __init__(self, name):
        self.name = name

class Department:
    def __init__(self, name):
        self.name = name
        self.professors = []

    def add_professor(self, prof):
        self.professors.append(prof)

# Professors created independently
p1 = Professor("Smith")
p2 = Professor("Jones")

dept = Department("CS")
dept.add_professor(p1)   # aggregation
dept.add_professor(p2)

# Even if dept is deleted, prof objects remain
del dept
print(p1.name)   # still exists
	```
	**UML** (hollow diamond):
	text
	```plain text
Department <>--------> Professor
(aggregation)
	```
</details>
<details>
<summary>**Composition (“ows” but strong relationship)**</summary>
	- **Definition**: A stronger form of aggregation where the **contained object’s lifetime is tied to the container** — it cannot exist independently.
	- **Direction**: From container to contained.
	- **Lifetime**: Contained objects are created and destroyed with the container.
	- **Example**: A `House` has `Room`s. If the house is destroyed, the rooms cease to exist.
	python
	```plain text
class Room:
    def __init__(self, name):
        self.name = name

class House:
    def __init__(self, address):
        self.address = address
        # rooms created inside the house
        self.rooms = [Room("kitchen"), Room("bedroom")]

    # no separate method to add external rooms
    # rooms are part of the house

house = House("123 Main St")
# rooms are only accessible through house
print(house.rooms[0].name)   # kitchen

# when house is destroyed, rooms are gone too
del house
# rooms cannot exist outside house
	```
	**UML** (filled diamond):
	text
	```plain text
House ♦--------> Room
(composition)
	```
</details>
<details>
<summary>**Comparison Table**</summary>
	<table header-row="true">
<tr>
<td>**Feature**</td>
<td>**Inheritance**</td>
<td>**Association**</td>
<td>**Aggregation**</td>
<td>**Composition**</td>
</tr>
<tr>
<td>Relationship</td>
<td>is-a</td>
<td>uses-a / knows-a</td>
<td>has-a (weak)</td>
<td>has-a (strong)</td>
</tr>
<tr>
<td>Direction</td>
<td>Parent ← Child</td>
<td>Defined or bidirectional</td>
<td>Container → Contained</td>
<td>Container → Contained</td>
</tr>
<tr>
<td>Lifetime</td>
<td>Compile-time / class hierarchy</td>
<td>Independent</td>
<td>Independent (shared)</td>
<td>Tied together</td>
</tr>
<tr>
<td>Ownership</td>
<td>No</td>
<td>No</td>
<td>No</td>
<td>Yes</td>
</tr>
<tr>
<td>UML</td>
<td>Triangle arrow</td>
<td>Simple line</td>
<td>Hollow diamond</td>
<td>Filled diamond</td>
</tr>
<tr>
<td>Example</td>
<td>Car is-a Vehicle</td>
<td>Doctor knows Patient</td>
<td>Department has Professors</td>
<td>House has Rooms</td>
</tr>
	</table>
</details>
# Patterns & Principles
[https://en.wikipedia.org/wiki/Category:Programming_principles](https://en.wikipedia.org/wiki/Category:Programming_principles)
## IoC {toggle="true"}
	IoC is a **design** principle where the control of object creation and dependencies is handed over to a container or framework, instead of the objects controlling it themselves.
	Hollywood principle: "Don't call us, we'll call you."
## Composition over Inheritance
<details>
<summary>Favor object composition over class inheritance.<br>Prefer wiring objects together from small, swappable parts rather than locking behaviour into rigid class hierarchies.</summary>
	![](https://prod-files-secure.s3.us-west-2.amazonaws.com/8a3cc761-c117-4f8e-9775-0208e44a3977/5629020b-e15e-40e7-9ad2-3f89cb45190b/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB46664SI2WYZ%2F20260910%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260910T110301Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjELn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIAjqgNaQzJ%2FyyM%2BB5tW%2FvKO7sYA1n6IzhhTjuLOnrNReAiEA37TbBTshCfMKT%2Fk5gfwgqOJdE9r6vKAxQPtCu2S7k4QqiAQIgv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDFMLfMXScSwh94NlpircAyOJ6q%2BoYUgyc%2BlK2MWl9QhwEo3MzdRqtKCR8Zmd9av8Y8S48cM6fwR%2F%2B9eiheZCYcOpQMnlsnAE62iJfUGADZCPf8Z8QYvZhtoywtWaMbo8SJDysaz%2F5tTXEx%2FWHFqFWyLolEdE6984Hr4y6d2PdA07ZD2QB3Q2VzAosYUukkEZOiRznk5mG8eB4tzzBrhmDm1ZSE3NokEo5a2vEBwrwdo2akKynU45hJkXscp%2FpIiTpU1WKek0nvryD1zZ7o545Zzvk9Yl%2FmeQiPKuuh1Ho2xdQRHTwEE%2BHOIqekCOgts8AYQ5XjKGb0l95Zs0vfDkZpbbcUYevLaqC99KgKnp%2FiXLhfnqYds40z%2BrpjziLV3HruO5HesWrOR3cM6lsUAwOhVbKXQqxVb7HA9pzZ%2BWIN0fqcAICD9kxgWMvIiWO6bwU02gt5%2FGDSBLFIVhu7wSTU3N6qaoGu6qR2e0m6%2FRq%2FIp6EUiH2oVw6nfPY9HbwzygYedke6aYwNCYZT8Ut8Yky9pWmWzCS3RQ2iyETFTpQhXkn6IT1mKfE%2FbIG6REzfuTadbPx2F565BXMrqyRCh16aGuwDvlDYst3tSdQgestT7TWvaPDYDe99ntPvI4rgPnrtsS%2FP%2BW9nN%2BVKwMNvjidUGOqUBh3Feb%2F15C37T0UAcxOpe8TWYlK8dUAnmoqVQa5vPCydV1RzXamWAZVXyFJMxk6hrEoRYbfm46HvDopXyx6yvbb5XzsGHspUTrfsFDxJWhxhekfVJHR4cUMEg2yke5Twe2fEBVGrKOhE71HoSO1EHpdlSuF5sCPHf9IeTDEpGv8yPABS5tWNWhaLp8juS4xS9Jm2MfUGqg5Emmjj1OYujOPP%2FQoLs&X-Amz-Signature=fe944fd7bbb5279198b9a80718ede8f11c21b671589c9bc146578a4a12082a48&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
	A few things worth emphasising beyond the cards:
	**The "gorilla-banana problem"** (coined by Joe Armstrong, creator of Erlang) is one of the most visceral descriptions of inheritance's cost: you wanted a banana, but because `Banana` inherits from `Tree` which inherits from `Forest`, you got the entire jungle too. Every field, every dependency, every side-effect in the ancestor chain comes along for the ride whether you want it or not.
	**The Liskov Substitution Principle (LSP)** is what makes inheritance semantically correct or incorrect — not just syntactically. If you can't substitute a subclass wherever the parent is expected without changing observable behaviour, the hierarchy is broken by design. The classic example: a `Square` that overrides `Rectangle.setWidth` to also set height violates LSP silently. Callers that depend on width and height being independent will get wrong results.
	**Composition is not free of tradeoffs.** The delegation boilerplate is real, and in a language without delegation sugar (like Kotlin's `by` keyword or Go's embedded structs), a wide interface means a lot of one-liner forwarding methods. Some teams use code generation or dynamic proxies to avoid this; others accept the verbosity as a fair trade for the flexibility.
	**The practical rule of thumb** most experienced engineers converge on: start with composition, and only reach for inheritance when you genuinely need the type identity — when the hierarchy *is* the semantics, not just a code-sharing convenience.
</details>
## **SOLID**
- **Single Responsibility Principle **(SRP)** **A class should have only <span underline="true">one reason to change</span>, meaning it should have only one responsibility.
- **Open/Closed Principle **(OCP)** **Software entities (like classes) should be open for <span underline="true">extension</span> but closed for modification. You should be able to add new functionality without changing existing code.
- **Liskov Substitution Principle **(LSP)** **Objects of a <span underline="true">superclass</span> should be replaceable with objects of its <span underline="true">subclasses</span> without breaking the application. In other words, a subclass should fulfill the "is-a" relationship in behavior, not just in name.
	<details>
	<summary>**LSP “Weaken Preconditions” Rule:  **A subclass is allowed to *weaken* (but not strengthen) the preconditions of a method it overrides.</summary>
		**Why?** If a subclass *strengthened* preconditions, then code that works perfectly with the superclass might fail when using the subclass, violating substitutability.
	</details>
	<details>
	<summary>**LSP "Strengthen Postconditions" Rule**: A subclass is allowed to **strengthen** (but not weaken) the postconditions of a method it overrides.</summary>
		**Why?** If a subclass *weakened* postconditions, then code that relies on the guarantees of the superclass might fail when using the subclass, violating substitutability.
	</details>
- **Interface Segregation Principle **(ISP)** **Clients should not be forced to depend on interfaces they do not use. It's better to have many small, specific interfaces than one large, "god" interface.
- **Dependency Inversion Principle **(DIP)** **Depend on abstractions (e.g., interfaces), not on concrete implementations. High-level modules should not depend on low-level modules; both should depend on abstractions.
## **Abstraction Principle**
<details>
<summary>Software components should expose only essential features and behaviors while hiding unnecessary implementation details. </summary>
	### **Why This Principle is Crucial**
	### **1. Managing Complexity**
	Software systems can have millions of lines of code. Without abstraction, no human could comprehend or maintain them.
	**Example:** Consider a web request:
	text
	```plain text
HTTP Request → Load Balancer → Web Server → Application Code → Database → Cache → External API → Response
	```
	Abstraction lets a developer work on the application code without understanding TCP/IP, DNS resolution, database indexing algorithms, or CPU cache optimization.
	### **2. Enabling Mental Models**
	Good abstractions create intuitive mental models that match the problem domain.
	java
	```plain text
// Good abstraction - matches mental model of bankingBankAccount account = bank.getAccount("12345");
account.deposit(1000.00);
account.transferTo(otherAccount, 500.00);

// vs. poor abstraction that exposes implementationDatabaseRecord record = database.select("accounts", "id=12345");
double newBalance = record.getDouble("balance") + 1000.00;
database.update("accounts", "balance", newBalance, "id=12345");
	```
	### **Key Mechanisms for Implementing Abstraction**
	### **1. Functions/Methods**
	The most basic form of abstraction - hiding algorithmic complexity.
	python
	```plain text
# Simple interfacedef send_notification(user, message):
# Hidden complexity: validation, formatting,# service selection, retry logic, error handlingif not is_valid_user(user):
        raise InvalidUserError()

    formatted_message = format_message(message)
    service = select_notification_service(user)

    try:
        service.send(user.contact_info, formatted_message)
        log_success(user, message)
    except ServiceError as e:
        handle_retry(user, message, service)
	```
	### **2. Classes and Modules**
	Bundling related functionality and hiding internal state.
	java
	```plain text
public class DocumentProcessor {
// Simple public APIpublic ProcessingResult processDocument(String filePath) {
        validateFile(filePath);
        Document document = parseDocument(filePath);
        applyBusinessRules(document);
        return generateResult(document);
    }

// Hidden implementation detailsprivate void validateFile(String path) {
// Complex file validation logic}

    private Document parseDocument(String path) {
// Complex parsing logic for different formats}

    private void applyBusinessRules(Document doc) {
// Complex domain-specific rules}
}
	```
	### **3. Layers of Abstraction**
	Building systems with multiple levels of abstraction, each building on the one below.
	text
	```plain text
┌─────────────────────────────────┐
│    Business Logic Layer         │ ← High-level domain concepts
│  (Orders, Customers, Payments)  │
└─────────────────────────────────┘
┌─────────────────────────────────┐
│     Service Layer              │ ← Business transactions & workflows
│ (OrderProcessing, UserManagement)│
└─────────────────────────────────┘
┌─────────────────────────────────┐
│    Data Access Layer           │ ← Database interactions
│   (Repositories, ORM)          │
└─────────────────────────────────┘
┌─────────────────────────────────┐
│    Infrastructure Layer        │ ← Technical concerns
│   (HTTP, Database, Caching)    │
└─────────────────────────────────┘
	```
	### **Characteristics of Good Abstractions**
	### **1. Simple Interface, Complex Implementation**
	java
	```plain text
// Good: Simple interfacepublic class PaymentGateway {
    public PaymentResult charge(CreditCard card, Money amount) {
// Complex implementation hidden:// - Tokenization// - API communication// - Error handling// - Retry logic// - Fraud detection// - Logging}
}

// Usage is trivialPaymentResult result = gateway.charge(creditCard, amount);
	```
	### **2. Domain-Aligned**
	Good abstractions speak the language of the domain, not the language of implementation.
	java
	```plain text
// Good - speaks business language
loanApplication.approve();
investmentPortfolio.rebalance();

// Poor - exposes technical concerns
database.updateStatus(applicationId, "APPROVED");
calculator.recalculateWeights(portfolioId);
	```
	### **3. Consistent and Predictable**
	java
	```plain text
// Consistent abstraction pattern
fileSystem.create(path);
fileSystem.read(path);
fileSystem.delete(path);

database.insert(record);
database.query(criteria);
database.delete(id);

// Same mental model applies across different components
	```
	### **Common Pitfalls and Anti-Patterns**
	### **1. Leaky Abstractions**
	When implementation details "leak" through the interface.
	java
	```plain text
// Leaky abstraction - exposes file system concernspublic class ConfigLoader {
// Users have to think about file encoding and pathspublic Properties loadConfig(String filePath, String encoding)
        throws FileNotFoundException, UnsupportedEncodingException {
// ...}
}

// Better abstraction - hides file system detailspublic class ConfigLoader {
// Simple interface, handles complexity internallypublic AppConfig loadConfig() {
// Determines path, encoding, handles exceptions internally}
}
	```
	### **2. Over-Abstraction**
	Creating unnecessary abstraction layers for simple logic.
	```java
// Over-abstracted - too many layers for simple operationData
AccessObjectFactory.getInstance()
    .getUserDAO()
    .createQueryBuilder()
    .where("id").equals(userId)
    .execute()
    .getSingleResult();

// Simpler approach
userRepository.findById(userId);
	```
	### **3. Wrong Abstraction Level**
	Abstracting at the wrong conceptual level.
	```java
// Wrong level - too technical
public class SQLQueryBuilder {
    public void addWhereClause(String column, String operator, Object value);
    public void addJoin(String table, String onClause);
}

// Better - domain-oriented
public class ProductSearch {
    public void filterByCategory(Category category);
    public void filterByPriceRange(Money min, Money max);
}
	```
	### **Conclusion**
	The Abstraction Principle is not just a technical guideline—it's a **philosophy of managing complexity** through thoughtful design. By creating simple interfaces that hide complex implementations, we:
	- **Reduce cognitive load** for developers
	- **Enable parallel work** across teams
	- **Create maintainable systems** that can evolve over time
	- **Build reliable software** through well-defined boundaries
	Mastering abstraction means understanding what to hide, what to expose, and at what level of detail—a skill that separates good software designers from great ones.
</details>
## Information Hiding Principle (IHP)
<details>
<summary>“Minimize the amount of information that each module needs to know about the others.”</summary>
	The Information Hiding Principle isn't just for object-oriented programming; it's a universal design philosophy that scales across all levels of software abstraction, from a single variable to an entire distributed system.
	Here’s how it's applied at various levels, from the smallest to the largest scale.
	### **1. Variable/Data Structure Level**
	At this most granular level, information hiding is about controlling access to data.
	- **Mechanism:** Access modifiers (`private`, `protected`), getter/setter methods.
	- **What is Hidden:** The internal representation and state of data.
	- **Example:**
		- Instead of using a public `int age` field, you make it `private` and provide a `public setAge(int age)` method. This method can **hide the validation logic** inside it, preventing the object from ever entering an invalid state (e.g., `if (age > 0 && age < 150)`).
		- You might start storing a `birthDate` internally for more accuracy, but still expose a `getAge()` method that calculates the age on the fly. The outside world doesn't know or care that the internal representation changed.
	**Benefit:** Ensures data integrity and allows you to change the data type or validation rules without impacting the rest of the codebase.
	---
	### **2. Procedure/Function Level**
	A function is the original module. Its implementation is hidden behind its signature.
	- **Mechanism:** Function definitions.
	- **What is Hidden:** The algorithm and logic steps used to achieve the function's goal.
	- **Example:**
		python
		```plain text
def calculate_tax(income):
# The caller doesn't need to know the specific tax brackets,# deduction formulas, or rounding rules.# This logic could change without affecting any callers.
    brackets = [...]
    deductions = [...]
# ... complex calculation ...return final_tax_amount
		```
	- **Benefit:** You can optimize the algorithm (e.g., for speed or memory) or fix a bug in the calculation without changing any code that calls `calculate_tax`.
	---
	### **3. Class/Module Level**
	This is the most classic and well-known application of the principle in Object-Oriented Programming.
	- **Mechanism:** Classes, Interfaces, and Access Modifiers.
	- **What is Hidden:** The internal state (fields) and the implementation of methods. The class exposes a public API.
	- **Example:** The `BankAccount` class from the previous discussion is a perfect example. The `balance` and the logging mechanism (`logTransaction`) are hidden. Only the `deposit`, `withdraw`, and `getBalance` methods are public.
	- **Benefit:** Promotes loose coupling between classes. The `Main` class doesn't depend on how `BankAccount` stores its balance, only on its public contract.
	---
	### **4. Component/Library Level**
	At this level, we hide the functionality of a collection of related classes and modules.
	- **Mechanism:** Public API of a library (e.g., `.jar` file, `.dll`, npm package). The internal classes within the library are often not exposed.
	- **What is Hidden:** All the internal classes, modules, and their complex interactions that make the library work.
	- **Example:**
		- A **Date/Time library** (like Java's `java.time` or Python's `datetime`). You use the `LocalDateTime` class without knowing about the hidden `TemporalAdjusters` or `Chronology` classes that do the heavy lifting.
		- An **HTTP Client library** hides the details of socket management, connection pooling, SSL handshakes, and protocol parsing. You just call `httpClient.get(url)`.
	- **Benefit:** Drastically reduces complexity for the consumer. Allows library developers to make sweeping internal changes and release new versions without breaking existing applications, as long as the public API remains stable.
	---
	### **5. Architectural Layer Level**
	In a layered architecture (e.g., Presentation -\> Business Logic -\> Data Access), information hiding is enforced between the layers.
	- **Mechanism:** Defined interfaces between layers.
	- **What is Hidden:** The implementation details of an entire layer.
	- **Example:** In a typical web app:
		- **Presentation Layer (UI):** Hides how it renders views (e.g., using React vs. vanilla JS).
		- **Business Logic Layer:** Hides the complex rules and workflows. The UI just calls a method like `placeOrder(cart)`.
		- **Data Access Layer (DAL):** Hides the specifics of the database technology (SQL vs. NoSQL), the schema, and the query language. The business layer calls `userRepository.findByEmail(email)` without knowing if it's a SQL query or a MongoDB find operation.
	- **Benefit:** Allows you to swap out entire technological stacks for one layer without affecting the others. You could change your database from MySQL to PostgreSQL by only modifying the DAL.
	---
	### **6. Service Level (Microservices & APIs)**
	This is information hiding at the highest level of application design, crucial for microservices and Service-Oriented Architecture (SOA).
	- **Mechanism:** Well-defined API contracts (REST, gRPC, GraphQL).
	- **What is Hidden:** **Everything** about the service: its programming language, its database, its internal architecture, and its business logic.
	- **Example:**
		- A **"User Service"** exposes a REST endpoint `GET /users/{id}`. The consumer (e.g., a front-end or another service) gets a JSON user object back.
		- **What's Hidden:** The fact that the User Service is written in Java, uses a PostgreSQL database, has a cache in Redis, and that the `getUser` method calls three different internal classes and a legacy system. The consumer only sees the HTTP endpoint and the JSON response format.
	- **Benefit:** This is the foundation of independent, scalable, and evolvable systems. Teams can develop, deploy, and scale their services independently. The "Payment Service" can be completely rewritten in Go without the "Order Service" even noticing.
	### **Summary Table**
	<table header-row="true">
<tr>
<td>**Level**</td>
<td>**What is Hidden**</td>
<td>**Mechanism**</td>
<td>**Key Benefit**</td>
</tr>
<tr>
<td>**Variable**</td>
<td>Data representation & validation</td>
<td>Getters/Setters</td>
<td>Data Integrity, Flexibility to Change</td>
</tr>
<tr>
<td>**Function**</td>
<td>Algorithm & logic steps</td>
<td>Function Definition</td>
<td>Algorithm Optimization</td>
</tr>
<tr>
<td>**Class**</td>
<td>Internal state & method implementation</td>
<td>Classes, `private`/`public`</td>
<td>Loose Coupling, Maintainability</td>
</tr>
<tr>
<td>**Component**</td>
<td>Internal modules & complex interactions</td>
<td>Library API</td>
<td>Reduced Consumer Complexity</td>
</tr>
<tr>
<td>**Architectural Layer**</td>
<td>Technology & implementation of a whole layer</td>
<td>Layer Interfaces</td>
<td>Technology Independence</td>
</tr>
<tr>
<td>**Service**</td>
<td>Everything: language, database, logic</td>
<td>API Contracts (REST/gRPC)</td>
<td>Independent Development & Scalability</td>
</tr>
	</table>
	The overarching theme is that at
</details>
## **Principle of Least Knowledge(PLK) & **Law of Demeter(LoD)
<details>
<summary>**Law of Demeter (LoD)**, also known as the . The law is famously simplified as "use only **one dot**".</summary>
	### **🤔 What is the Law of Demeter?**
	At its core, the Law of Demeter is a design guideline that promotes **loose coupling** in software. It states that a software unit (like an object or class) should only communicate with its immediate "friends" and not with "strangers". The principle is often summarized with the phrase, "**Only talk to your immediate friends**".
	In practice, the law suggests that a method `M` of an object `A` should only call methods belonging to:
	- The object `A` itself.
	- Objects passed as arguments to `M`.
	- Any objects that `A` creates or instantiates.
	- `A`'s direct component objects (e.g., objects stored in its instance variables).
	The law is famously simplified as "use only **one dot**". For example, `person.getWallet().getMoney()` would be discouraged because `getWallet()` returns a stranger (`Wallet`) whose `getMoney()` method is being called. Instead, the preferred design is `person.pay()`, delegating the responsibility to `person`.
	### **📜 A Brief History: The Demeter Project**
	The principle was proposed by Ian Holland in **1987** at **Northeastern University** in Boston. It originated from the **Demeter Project**, an adaptive and aspect-oriented programming research project.
	The project was named after **Demeter**, the Greek goddess of agriculture. This name was chosen to symbolize a "bottom-up" philosophy of "growing" software organically, rather than "building" it rigidly from the top down.
	The principle gained widespread recognition after being featured in the classic software development book, *The Pragmatic Programmer*.
	### **✨ Why Follow This Principle? Key Benefits**
	Following the Law of Demeter brings several advantages to software design:
	- **Improved Maintainability and Adaptability**: Because objects are less dependent on the internal structure of others, you can change a class without affecting classes that depend on it.
	- **Reduced Software Defects**: Research has shown that lower coupling (aided by the Law of Demeter) can correlate with a lower probability of software bugs.
	- **Enhanced Readability and Understandability**: Code that follows this rule is generally easier to follow because it reduces complex chains of method calls.
	- **Increased Reusability**: Loosely coupled classes are easier to reuse in different contexts.
	### **⚠️ Potential Drawbacks and Criticisms**
	The principle is a guideline, not a strict law, and can be over-applied, leading to issues:
	- **"Wrapper" Overload**: Strict application may lead to many small "wrapper" or "delegation" methods that do nothing but pass a call along. This increases system complexity, which contradicts the goal of simplifying the design.
	- **Performance Overhead**: The extra delegation can introduce additional time and space overhead, though it's often negligible.
	- **Trade-off with Functionality**: Correctly applying the rule can sometimes lead to wider class interfaces to support delegated behaviors, which can be seen as a drawback.
	The Law of Demeter is best used as a **code smell** or heuristic to identify problematic coupling, rather than as a rigid rule to enforce at all costs.
	### **🔧 How to Apply It: Practical Examples and Patterns**
	The Law of Demeter is often implemented in practice using well-known design patterns:
	- **Don't Chain Methods**: Instead of writing code like `order.customer.address.city()`, you should ask yourself if `order` can just provide `order.getCustomerCity()`.
	- **Create Delegation Methods**: If object `A` needs data from a deep part of object `B`, rather than exposing `B`'s internal structure, you give `B` a new method that handles the request.
	- **Use Facade Pattern**: A `Facade` provides a simplified interface to a complex subsystem. Client code talks only to the facade, which then manages the more complex interactions internally.
	- **Use Mediator Pattern**: A `Mediator` acts as a central hub that manages communications between different objects, preventing them from needing to know about each other directly.
	### **💎 Summary**
	The Law of Demeter is a foundational principle in object-oriented design that champions loose coupling and information hiding. While strict adherence can sometimes lead to extra boilerplate code, it remains a valuable guide for building maintainable, robust, and understandable software systems.
	If you're interested, I can illustrate the difference between code that violates the Law of Demeter and code that follows it with a concrete example.
</details>
### **IHP vs PLK vs LoD** {toggle="true"}
	<details>
	<summary>Three related principles. They operate at different levels of abstraction. IHP ⊃ PLK ⊃ LoD</summary>
		![](https://prod-files-secure.s3.us-west-2.amazonaws.com/8a3cc761-c117-4f8e-9775-0208e44a3977/d1f4d341-187a-4268-9d1f-7db8f9771513/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB46664SI2WYZ%2F20260910%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260910T110301Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjELn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIAjqgNaQzJ%2FyyM%2BB5tW%2FvKO7sYA1n6IzhhTjuLOnrNReAiEA37TbBTshCfMKT%2Fk5gfwgqOJdE9r6vKAxQPtCu2S7k4QqiAQIgv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDFMLfMXScSwh94NlpircAyOJ6q%2BoYUgyc%2BlK2MWl9QhwEo3MzdRqtKCR8Zmd9av8Y8S48cM6fwR%2F%2B9eiheZCYcOpQMnlsnAE62iJfUGADZCPf8Z8QYvZhtoywtWaMbo8SJDysaz%2F5tTXEx%2FWHFqFWyLolEdE6984Hr4y6d2PdA07ZD2QB3Q2VzAosYUukkEZOiRznk5mG8eB4tzzBrhmDm1ZSE3NokEo5a2vEBwrwdo2akKynU45hJkXscp%2FpIiTpU1WKek0nvryD1zZ7o545Zzvk9Yl%2FmeQiPKuuh1Ho2xdQRHTwEE%2BHOIqekCOgts8AYQ5XjKGb0l95Zs0vfDkZpbbcUYevLaqC99KgKnp%2FiXLhfnqYds40z%2BrpjziLV3HruO5HesWrOR3cM6lsUAwOhVbKXQqxVb7HA9pzZ%2BWIN0fqcAICD9kxgWMvIiWO6bwU02gt5%2FGDSBLFIVhu7wSTU3N6qaoGu6qR2e0m6%2FRq%2FIp6EUiH2oVw6nfPY9HbwzygYedke6aYwNCYZT8Ut8Yky9pWmWzCS3RQ2iyETFTpQhXkn6IT1mKfE%2FbIG6REzfuTadbPx2F565BXMrqyRCh16aGuwDvlDYst3tSdQgestT7TWvaPDYDe99ntPvI4rgPnrtsS%2FP%2BW9nN%2BVKwMNvjidUGOqUBh3Feb%2F15C37T0UAcxOpe8TWYlK8dUAnmoqVQa5vPCydV1RzXamWAZVXyFJMxk6hrEoRYbfm46HvDopXyx6yvbb5XzsGHspUTrfsFDxJWhxhekfVJHR4cUMEg2yke5Twe2fEBVGrKOhE71HoSO1EHpdlSuF5sCPHf9IeTDEpGv8yPABS5tWNWhaLp8juS4xS9Jm2MfUGqg5Emmjj1OYujOPP%2FQoLs&X-Amz-Signature=cd551456d8dfc5a1fecd9051e480cb1f72d649c8176b203d3a3efb30867e82ce&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
	</details>
## **Principle of least surprise** (POLS)
<details>
<summary>**Principle of least astonishment** (**POLA**), also known as **principle of least surprise** (**POLS**)</summary>
	> A software component (be it a function, class, API, or UI) should behave in such a way that its actions and outputs are what most developers would naturally expect, minimizing "astonishing" or surprising behavior.
	When a developer uses your code, they come with a set of pre-existing assumptions based on their knowledge of the language, common conventions, and the component's name. POLA dictates that your code should align with these assumptions as closely as possible.
	---
	### **Why is POLA Important?**
	Violating POLA leads to several significant problems:
	1. **Increased Cognitive Load:** Developers spend extra mental energy trying to understand and remember the "quirks" of your system instead of solving business problems.
	2. **More Bugs:** Surprising behavior is a fertile ground for bugs. A developer who misunderstands what a function does will use it incorrectly.
	3. **Reduced Productivity:** Time is wasted debugging unexpected outcomes, reading source code to decipher behavior, or consulting documentation for what should be intuitive.
	4. **Poor Maintainability:** Code that astonishes is hard to reason about, making it difficult and risky to modify later.
	---
	### **POLA in Practice: Examples and Anti-Patterns**
	Let's look at concrete examples across different levels of a codebase.
	### **1. Function and Method Design**
	This is where POLA is most frequently applied.
	- **Good (POLA-compliant):**
		- A function named `getUserById(id)` returns a `User` object or `null`/`None` if not found. This is unsurprising.
		- A method `save()` on a `Document` object persists the document to a database. The developer expects this.
	- **Astonishing (POLA-violating):**
		- **Side Effects in Getters:** A method named `getTotal()` that also recalculates and updates the internal state of the object. A "getter" is expected to be a pure accessor without side effects.
		```java
// Astonishing!
public double getTotal() {
    this.total = calculateTotal();// Recalculates and mutates statereturn this.total;
}
		```
		- **Misleading Names:** A function named `validateOrder(order)` that, as a side effect, also saves the validated order to the database. The name suggests it only performs validation.
		- **Non-Standard Return Values:** A function `processData()` that returns `true` on failure and `false` on success, inverting the common convention.
	### **2. API Design (Libraries and Frameworks)**
	APIs should feel intuitive and consistent.
	- **Good (POLA-compliant):**
		- In a collection class, `list.add(item)` adds an item to the end of the list. `list.insert(index, item)` inserts it at a specific position.
		- A `sort()` method sorts the collection in ascending order by default, as this is the most common expectation.
	- **Astonishing (POLA-violating):**
		- **Inconsistent Conventions:** A library where most methods use camelCase but a few use snake_case for no apparent reason.
		- **Unexpected Defaults:** A configuration setting named `sslEnabled` that defaults to `false`, forcing the developer to explicitly enable security, which is a surprising and insecure default.
		- **"Magic" Behavior:** A framework that silently changes the behavior of a base class based on the name of a method (e.g., methods starting with `on` are automatically registered as event listeners without any declaration). While powerful, this can be astonishing to debug.
	### **3. Language and Syntax Design**
	Even programming language designers must follow POLA.
	- **Good (POLA-compliant):**
		- In Python, the `+` operator concatenates strings and adds numbers. This matches mathematical and intuitive concepts.
		- In Java, the `.equals()` method checks for value equality, while `==` checks for reference equality. Once learned, this is consistent.
	- **Astonishing (POLA-violating):**
		- **JavaScript's ****`==`**** vs ****`===`****:** The loose equality operator (`==`) performs type coercion, leading to surprising results like `[] == false` evaluating to `true`. This is a classic violation of POLA that forces developers to always use `===`.
		- **PHP's ****`in_array`**** Behavior:** The function `in_array(0, ['a', 'b'])` returns `true` because the string `'a'` is loosely compared to the integer `0`, and in PHP, `'a' == 0` is `true`. This is highly astonishing.
	### **4. Configuration and Environment**
	- **Good (POLA-compliant):**
		- A `DEBUG` environment variable where `DEBUG=true` enables debug mode and `DEBUG=false` disables it.
		- A configuration file where settings are hierarchically organized, mirroring the structure of the application.
	- **Astonishing (POLA-violating):**
		- A `DISABLE_LOGGING` variable where you must set it to `false` to *enable* logging. This is a double negative and is mentally taxing.
		- A system where the order of configuration files being loaded is undefined or counter-intuitive, leading to settings being overridden in surprising ways.
	---
	### **How to Achieve POLA in Your Code**
	1. **Follow Naming Conventions:** Use clear, descriptive, and conventional names. A function named `calculateTotal()` should only calculate, not calculate and save.
	2. **Adhere to Conventions:** Respect the established conventions of your language and ecosystem (e.g., getters should be side-effect free, methods starting with `is` should return a boolean).
	3. **Minimize Surprising Side Effects:** A function should do one thing, and its primary effect should be obvious from its name. Avoid "hidden" operations.
	4. **Provide Sensible Defaults:** Default configurations should be safe, secure, and match the most common use case.
	5. **Embrace Consistency:** Be consistent within your own codebase. If you handle errors in a specific way in one module, do the same in all others.
	6. **Design Predictable APIs:** When designing an API, think from the perspective of a developer who is seeing it for the first time. Would they be able to guess how to use it?
	7. **Write Clear Documentation:** For cases where you must deviate from the norm (for performance or a valid technical reason), document the behavior clearly and prominently.
	### **The Relationship with Other Principles**
	POLA is deeply connected to other software principles:
	- **Single Responsibility Principle (SRP):** A function with a single responsibility is less likely to have surprising side effects.
	- **Don't Repeat Yourself (DRY):** Inconsistent behavior often arises from duplicated, slightly modified code.
	- **KISS (Keep It Simple, Stupid):** Simple designs are inherently less astonishing.
	### **Conclusion**
	The Principle of Least Astonishment is fundamentally about **empathy for the developer**—who could be your future self, a teammate, or an open-source user. It's a guiding philosophy that prioritizes clarity, consistency, and predictability over cleverness or unconventional shortcuts. By designing systems that act the way developers expect them to, you create software that is not only more pleasant to work with but also more robust, maintainable, and less prone to errors.
</details>
## **GRASP Patterns**
- **General Responsibility Assignment Software Patterns (GRASP)**
	- **Information Expert** - Assign the responsibility for a task to the class that owns all the necessary data for it.
	- **Creator** - Class B should create instances of class A if one of the following conditions holds: B contains A, B aggregates A, B uses A, or B initializes data for A.
	- **Controller** - The first object after the UI that receives a user request. It should coordinate the execution of an operation but not do all the work itself.
	- **Low Coupling** - Strive for minimal interaction between classes. Changes in one class should minimally affect others.
	- **High Cohesion** - Elements within a class (methods, fields) should be closely related and form a single, well-defined whole.
	- **Polymorphism** - Use polymorphism to handle alternative behaviors based on type.
	- **Pure Fabrication** - Create an artificial class, unrelated to the problem domain, to house behavior that is illogical to place in existing domain classes. This abstracts a certain service behavior (e.g., saving an object to a database) away from the domain object.
	- **Indirection** - Assign the responsibility to an intermediate object to mediate between other components or services, so they are not directly coupled.
	- **Protected Variations** - Identify points of predicted variation or instability and assign responsibilities to create a stable interface around them.
## **Inversion of Control (IoC) & Dependency Injection** {toggle="true"}
	**IoC is a design principle** that inverts the flow of control in a program. Instead of your code calling frameworks or libraries, the framework calls your code.
	**Analogy:** Think of a *Hollywood principle* - "Don't call us, we'll call you."
	- **Traditional Control Flow:** Your code controls the program execution
	- **Inverted Control Flow:** The framework controls the program execution and calls your code when needed
	**Without IoC**
	```php
// Your code is in control
class UserController {
    public function store() {
        $user = new User();
        $user->save(); // You decide when to save
        $this->sendWelcomeEmail(); // You decide when to send email
    }
}
	```
	**With IoC**
	```php
// Framework is in control
class UserController {
    public function store(Request $request) { // Laravel calls this method when route is hit
				// You don't control when this runs
	  }
}
	```
	**IoC is the umbrella concept** - Dependency Injection is one way to achieve it.
	### Patterns that implement the Inversion of Control principle
	<table header-row="true">
<tr>
<td>**Pattern**</td>
<td>**Control Inversion Aspect**</td>
<td>**Primary Use Case**</td>
</tr>
<tr>
<td>**Dependency Injection**</td>
<td>Object construction and wiring</td>
<td>Application composition, testing</td>
</tr>
<tr>
<td>**Service Locator**</td>
<td>Dependency lookup</td>
<td>Legacy systems, gradual refactoring</td>
</tr>
<tr>
<td>**Factory Pattern**</td>
<td>Object creation logic</td>
<td>Complex object creation, pooling</td>
</tr>
<tr>
<td>**Template Method**</td>
<td>Algorithm steps</td>
<td>Framework design, code reuse</td>
</tr>
<tr>
<td>**Strategy Pattern**</td>
<td>Algorithm selection</td>
<td>Runtime behavior changes</td>
</tr>
<tr>
<td>**Observer Pattern**</td>
<td>Event notification</td>
<td>UI frameworks, reactive systems</td>
</tr>
<tr>
<td>**Callback Pattern**</td>
<td>Asynchronous response handling</td>
<td>I/O operations, APIs</td>
</tr>
	</table>
	### **Why DI Became Dominant**
	While all these patterns implement IoC, Dependency Injection became the most popular because:
	1. **Explicit dependencies** - All dependencies are visible in the constructor/setters
	2. **Testability** - Easy to mock dependencies for unit testing
	3. **Composition root** - All wiring happens in one place
	4. **Framework support** - Excellent tooling (Spring, Guice, Dagger, etc.)
	5. **No hidden dependencies** - Unlike Service Locator, which can hide what a class needs
	<empty-block/>
**Tell, Don't Ask Principle**
## Coupling Dimensions
## <span color="red">GoF (Design) patterns</span>
- **Creational**
	<details>
	<summary>**Singleton** - Class has only one instance</summary>
		<empty-block/>
	</details>
	<details>
	<summary>**Factory method** (Simple Factory) - Parent abstract class has a `create()` method and descendants implement it.</summary>
		<empty-block/>
	</details>
	- Abstract factory - Factory method, но с большим кличеством cerate() методов, которые создают связанные обьекты.
	- **Prototype** -  имеет метод clone() для клонивроания
	- Builder & Director - создавать конфигурации обьектов из различных наборов 
- **Structural**
	- Adapter - *Позволяет объектам с несовместимыми интерфейсами работать вместе.*
	- Facade - *Предоставляет простой интерфейс к сложной системе классов, библиотеке или фреймворку.*
	- **Decorator** (Wrapper) - * Позволяет динамически добавлять объектам новую функциональность, оборачивая их в полезные «обёртки».*
	- Proxy - *Позволяет подставлять вместо реальных объектов специальные объекты-заменители. Эти объекты перехватывают вызовы к оригинальному объекту, позволяя сделать что-то до или после передачи вызова оригиналу.*
	- Bridge (Driver) -  аналог драйвера, чтобы не плодить классы принтера для каждого отдельного модели принтера
		<details>
		<summary> </summary>
			```php
// АБСТРАКЦИЯ - полный интерфейс того, что умеет делать принтер
public interface PrinterDriver {
    // Основные операции
    void print(String documentContent, int copies);
    void cancelPrint();
    void scan(String source, String format);
    void copy(int copies, boolean isDuplex);
    
    // Настройки и статус
    String getStatus();
    int getInkLevel(); // Уровень чернил/тонера
    int getPaperCount(); // Количество бумаги
    void setPrintQuality(Quality quality); // Качество печати
    void setPaperSize(PaperSize size); // Размер бумаги
    
    // Обслуживание
    void cleanHeads(); // Прочистка головок
    void alignCartridges(); // Выравнивание картриджей
    void calibrate(); // Калибровка
    
    // Информация
    String getModelName();
    String getSerialNumber();
}

// Вспомогательные enum'ы для настроек
enum Quality { DRAFT, NORMAL, HIGH, PHOTO }
enum PaperSize { A4, A5, LETTER, LEGAL }
			```
			```php
public class HPLaserJetDriver implements PrinterDriver {
    private Quality currentQuality = Quality.NORMAL;
    private PaperSize currentPaperSize = PaperSize.A4;
    
    @Override
    public void print(String documentContent, int copies) {
        // Специфичная для лазерных принтеров HP логика
        convertToPCL(documentContent); // Конвертация в язык PCL
        heatFuserUnit(); // Нагрев термоэлемента
        feedPaper(); // Подача бумаги
        applyToner(); // Нанесение тонера
        fuseToner(); // Закрепление тонера нагреванием
        
        System.out.println("Печатаем " + copies + " копий на HP LaserJet");
        System.out.println("Качество: " + currentQuality + ", Бумага: " + currentPaperSize);
    }
    
    @Override
    public void scan(String source, String format) {
        // У этого принтера нет сканера!
        throw new UnsupportedOperationException("HP LaserJet не поддерживает сканирование");
    }
    
    @Override
    public void copy(int copies, boolean isDuplex) {
        // Нет встроенного копира
        throw new UnsupportedOperationException("HP LaserJet не поддерживает копирование");
    }
    
    @Override
    public int getInkLevel() {
        // Для лазерного принтера - уровень тонера
        checkTonerSensor(); // Опрос датчика тонера
        return 85; // Возвращаем 85%
    }
    
    @Override
    public void cleanHeads() {
        // Для лазерника это не актуально
        System.out.println("Очистка не требуется для лазерных принтеров");
    }
    
    // Специфичные методы для лазерных принтеров HP
    private void convertToPCL(String content) {
        System.out.println("Конвертируем в PCL...");
    }
    
    private void heatFuserUnit() {
        System.out.println("Нагрев термоэлемента до 180°C...");
    }
    
    // ... реализация остальных методов
}
			```
			```php
public class CanonMFUDriver implements PrinterDriver {
    private int cyanInk = 60;
    private int magentaInk = 55;
    private int yellowInk = 70;
    private int blackInk = 40;
    
    @Override
    public void print(String documentContent, int copies) {
        // Специфичная для струйных принтеров Canon логика
        prepareInkHeads(); // Подготовка печатающих головок
        mixColors(); // Смешивание цветов
        sprayInk(); // Распыление чернил
        dryPaper(); // Сушка бумаги
        
        System.out.println("Печатаем " + copies + " цветных копий на Canon Pixma");
        System.out.println("Используем фотокачество печати");
    }
    
    @Override
    public void scan(String source, String format) {
        // Реализация сканирования для Canon
        calibrateScanner(); // Калибровка сканера
        adjustBrightness(); // Настройка яркости
        captureImage(); // Захват изображения
        saveAsFormat(format); // Сохранение в нужном формате
        
        System.out.println("Сканируем с " + source + " в формате " + format);
    }
    
    @Override
    public void copy(int copies, boolean isDuplex) {
        // Реализация копирования для МФУ
        scan("планшет", "JPEG");
        print("скан документа", copies);
        System.out.println("Копируем " + copies + " копий" + 
                          (isDuplex ? " с двухсторонней печатью" : ""));
    }
    
    @Override
    public int getInkLevel() {
        // Для струйного принтера возвращаем уровень черного
        return blackInk;
    }
    
    @Override
    public void cleanHeads() {
        // Важная процедура для струйных принтеров
        runCleaningCycle(); // Запуск цикла очистки
        wasteInk(); // Сброс чернил в помпу
        checkNozzles(); // Проверка дюз
        
        System.out.println("Очистка печатающих головок Canon...");
        cyanInk -= 2; // Чернила тратятся на очистку
        magentaInk -= 2;
        yellowInk -= 2;
        blackInk -= 3;
    }
    
    // Специфичные методы для струйных принтеров Canon
    public int[] getAllInkLevels() {
        return new int[]{cyanInk, magentaInk, yellowInk, blackInk};
    }
    
    private void prepareInkHeads() {
        System.out.println("Подготовка печатающих головок...");
    }
    
    // ... реализация остальных методов
}
			```
			```php
// БАЗОВАЯ АБСТРАКЦИЯ - знает КАК управлять печатью через драйвер
public abstract class PrintService {
    // МОСТ: ссылка на реализацию (драйвер)
    protected PrinterDriver printerDriver;

    public PrintService(PrinterDriver driver) {
        this.printerDriver = driver;
    }

    // Общие для всех абстракций методы
    public void performPrint(String document) {
        printerDriver.print(document, 1);
    }
    
    public void checkStatus() {
        System.out.println("Статус: " + printerDriver.getStatus());
    }
}
			```
			```php
// 1. Абстракция для фоновой печати документов
public class DocumentPrintService extends PrintService {
    public DocumentPrintService(PrinterDriver driver) {
        super(driver);
    }
    
    // Специфичная для документов логика
    public void printDocument(Document doc, boolean isDuplex) {
        System.out.println("Добавляю документ в очередь печати: " + doc.getName());
        printerDriver.setPrintQuality(Quality.NORMAL);
        printerDriver.print(doc.getContent(), doc.getCopies());
    }
}

// 2. Абстракция для печати фотографий
public class PhotoPrintService extends PrintService {
    public PhotoPrintService(PrinterDriver driver) {
        super(driver);
    }
    
    // Специфичная для фото логика
    public void printPhoto(Image image, PaperSize size) {
        System.out.println("Подготовка фото к печати...");
        printerDriver.setPrintQuality(Quality.PHOTO);
        printerDriver.setPaperSize(size);
        printerDriver.print(image.getRasterData(), 1);
    }
}

// 3. Абстракция для службы сканирования
public class ScanService extends PrintService {
    public ScanService(PrinterDriver driver) {
        super(driver);
    }
    
    public void scanToEmail(String source, String email) {
        System.out.println("Сканирую для отправки на " + email);
        String scannedContent = printerDriver.scan(source, "PDF");
        // ... логика отправки по email
    }
}
			```
			```php
public class Office {
    public static void main(String[] args) {
        // ИЕРАРХИЯ РЕАЛИЗАЦИЙ (драйверы)
        PrinterDriver hpDriver = new HPLaserJetDriver();
        PrinterDriver canonDriver = new CanonMFUDriver();
        
        // ИЕРАРХИЯ АБСТРАКЦИЙ (сервисы) строят МОСТ к драйверам
        
        // 1. Документный сервис работает с HP
        DocumentPrintService docService = new DocumentPrintService(hpDriver);
        docService.printDocument(new Document("Отчет.pdf"), true);
        
        // 2. Фотосервис работает с Canon
        PhotoPrintService photoService = new PhotoPrintService(canonDriver);
        photoService.printPhoto(new Image("отпуск.jpg"), PaperSize.A4);
        
        // 3. Тот же драйвер Canon, но для сканирования
        ScanService scanService = new ScanService(canonDriver);
        scanService.scanToEmail("планшет", "boss@company.com");
        
        // 4. Можем легко переподключить сервис к другому драйверу!
        photoService = new PhotoPrintService(hpDriver); // Теперь печатаем фото на HP
        photoService.printPhoto(new Image("портрет.jpg"), PaperSize.LETTER);
    }
}
			```
		</details>
	- Composite - Когда нужно представить древовидную структуру объектов, а затем работать с ней так, как будто это единый объект.
		- <span color="red">Реальный пример</span>: 
	- Flyweight (Легковес) -  
		- <span color="red">Реальный пример</span>: наверно не было, но это кеширование обьектов по ключам, которые ва
- **Behaviorial**
	- **Chain of Responsibility** - позволяет передавать запросы последовательно по цепочке обработчиков. Каждый последующий обработчик решает, может ли он обработать запрос сам и стоит ли передавать запрос дальше по цепи.
		- <span color="red">Реальный пример:</span> росло количество ифов в проверке возможности доступа апределённых пользвателей при определённых условиях к функционалу и это было повторено во многих метсах. Добавили Chain of responsibility.<br>Где передавался обьект юзера в цепочку валидаторв, и каждый хендлер проверял своё. А для отдельного метода строилась своя цепочка валидаций.   
		<details>
			```php

namespace RefactoringGuru\ChainOfResponsibility\Conceptual;

/**
 * Интерфейс Обработчика объявляет метод построения цепочки обработчиков. Он
 * также объявляет метод для выполнения запроса.
 */
interface Handler
{
    public function setNext(Handler $handler): Handler;

    public function handle(string $request): ?string;
}

/**
 * Поведение цепочки по умолчанию может быть реализовано внутри базового класса
 * обработчика.
 */
abstract class AbstractHandler implements Handler
{
    /**
     * @var Handler
     */
    private $nextHandler;

    public function setNext(Handler $handler): Handler
    {
        $this->nextHandler = $handler;
        // Возврат обработчика отсюда позволит связать обработчики простым
        // способом, вот так:
        // $monkey->setNext($squirrel)->setNext($dog);
        return $handler;
    }

    public function handle(string $request): ?string
    {
        if ($this->nextHandler) {
            return $this->nextHandler->handle($request);
        }

        return null;
    }
}

/**
 * Все Конкретные Обработчики либо обрабатывают запрос, либо передают его
 * следующему обработчику в цепочке.
 */
class MonkeyHandler extends AbstractHandler
{
    public function handle(string $request): ?string
    {
        if ($request === "Banana") {
            return "Monkey: I'll eat the " . $request . ".\n";
        } else {
            return parent::handle($request);
        }
    }
}

class SquirrelHandler extends AbstractHandler
{
    public function handle(string $request): ?string
    {
        if ($request === "Nut") {
            return "Squirrel: I'll eat the " . $request . ".\n";
        } else {
            return parent::handle($request);
        }
    }
}

class DogHandler extends AbstractHandler
{
    public function handle(string $request): ?string
    {
        if ($request === "MeatBall") {
            return "Dog: I'll eat the " . $request . ".\n";
        } else {
            return parent::handle($request);
        }
    }
}

/**
 * Обычно клиентский код приспособлен для работы с единственным обработчиком. В
 * большинстве случаев клиенту даже неизвестно, что этот обработчик является
 * частью цепочки.
 */
function clientCode(Handler $handler)
{
    foreach (["Nut", "Banana", "Cup of coffee"] as $food) {
        echo "Client: Who wants a " . $food . "?\n";
        $result = $handler->handle($food);
        if ($result) {
            echo "  " . $result;
        } else {
            echo "  " . $food . " was left untouched.\n";
        }
    }
}

/**
 * Другая часть клиентского кода создает саму цепочку.
 */
$monkey = new MonkeyHandler();
$squirrel = new SquirrelHandler();
$dog = new DogHandler();

$monkey->setNext($squirrel)->setNext($dog);

/**
 * Клиент должен иметь возможность отправлять запрос любому обработчику, а не
 * только первому в цепочке.
 */
echo "Chain: Monkey > Squirrel > Dog\n\n";
clientCode($monkey);
echo "\n";

echo "Subchain: Squirrel > Dog\n\n";
clientCode($squirrel);
			```
		</details>
	- **Command** - *превращает запросы в объекты, позволяя передавать их как аргументы при вызове методов, ставить запросы в очередь, логировать их, а также поддерживать отмену операций.*
		- <span color="red">Реальный пример: </span>когда в очередь сообжений отправляем комманду отправить рассылку имейла на группу пользователей - знаем получаетеля.  
	- **Observer** (Event\\Listener) - это поведенческий паттерн проектирования, который создаёт механизм подписки, позволяющий одним объектам следить и реагировать на события, происходящие в других объектах.
	- <span color="red">**Strategy**</span>
	- Interpreter
	- Iterator
	- Mediator
	- Memento
	- State
	- Template Method
	- Visitor
## SOA
-  SOA можно рассматривать как *архитектурное масштабирование* и *формализацию* идеи, стоящей за Pure Fabrication.
Группа 1: Принципы Интерфейса и Взаимодействия
1. Стандарtized Contract (Стандартизированный контракт) - Сервисы взаимодействуют по строго определенным, стандартным контрактам (интерфейсам), часто с использованием WSDL, XSD в мире WS-\* или OpenAPI в современном мире.	Снижение связанности (Low Coupling). Клиенту не важно, на чем реализован сервис (Java, .NET), ему важен только его публичный контракт.
2. Loose Coupling (Слабая связанность) - Сервисы minimally зависят друг от друга. Они знают только о публичных контрактах друг друга, а не о внутренней реализации.	Гибкость и устойчивость к изменениям. Можно изменять или полностью переписывать сервис, не ломая его потребителей, пока контракт сохраняется.
3. Abstraction (Абстракция) - Сервис скрывает свою внутреннюю логику, предоставляя вовне только контракт и необходимые политики.	Упрощение использования и безопасность. Клиенты работают с "черным ящиком", что снижает complexity и скрывает детали реализации.
Группа 2: Принципы Дизайна Сервиса
1.  Autonomy (Автономность) - Сервис обладает высоким уровнем контроля над своей собственной средой и логикой. Он максимально независим от других сервисов и shared state.	Надежность, предсказуемость и управляемость. Сервис можно развертывать, тестировать и обслуживать независимо.
2. Statelessness (Отсутствие состояния) - Сервисы по возможности не хранят состояние (state) между вызовами. Каждый вызов содержит всю необходимую информацию.	Масштабируемость и надежность. Легко добавить еще один инстанс сервиса для обработки нагрузки, так как нет привязки к состоянию сессии на конкретном сервере.
Группа 3: Принципы Управления и Бизнес-Ценности
1. Reusability (Повторное использование) - Сервисы проектируются как компоненты, пригодные для многократного использования в разных бизнес-процессах и приложениях.	Снижение издержек и ускорение разработки. Не нужно писать одну и ту же функциональность заново для каждого проекта.
2. Discoverability (Обнаружаемость) -	Сервисы описаны метаданными так, чтобы их можно было обнаружить и понять через реестр сервисов (например, UDDI).	Управляемость и предотвращение дублирования. Разработчики могут найти и использовать существующие сервисы,而不是 создавать новые с той же функциональностью.
3. Composability (Композируемость) - Сервисы могут выступать в качестве строительных блоков, которые можно композировать (объединять) для создания сложных составных сервисов и бизнес-процессов (например, через BPEL).
## DDD {toggle="true"}
	- It's an **approach to software development** for complex domains, first formally introduced by **Eric Evans** in his book. It's primarily a set of principles and patterns that **focus on creating a software model** **that reflects the real-world business domain** it's intended to serve.
	<details>
	<summary>Problems that DDD solves.</summary>
		- **Communication gap:** This is the biggest problem DDD solves. Developers and business people often speak different languages
		- **Poorly organized and inefficient code**  Without clear guidance, business logic gets scattered everywhere—in controllers, service classes, and even the database.  
		- **Lack of business focus **It's easy for developers to get lost in technical details and lose what the business actually needs. DDD forces the entire team to constantly focus on the core business problem and its intricacies.
		- **Onboarding new team members** When the codebase is a direct reflection of the business domain, a new developer can look at the code and quickly understand what the system does.
	</details>
	## **Principles**
	- **Ubiquitous Language** - This is the cornerstone of DDD. It's a common, rigorous language shared by the development team and the business experts. This language is used not just in conversation, but is embedded directly into the code—in class names, method names, and module names.
	- **Bounded Contexts **- A large business domain is too complex to model as a single, unified model. A Bounded Context defines the boundaries within which a particular model and its ubiquitous language apply.
		<details>
		<summary>Example</summary>
			In the Shipping context, a Product has attributes like weight, dimensions, and is_hazardous.
			In the Marketing context, a Product has attributes like description, keywords, and promotional_tagline.
			DDD says it's okay, and even preferable, to have a ShippingProduct class and a MarketingProduct class, each with their own logic, rather than one giant, confusing Product class that tries to do everything.
		</details>
		Within a Bounded Context, we build a **rich**, object-oriented model. DDD provides several **tactical patterns** to build this model:
		- **Entities:** Objects that have a distinct identity that runs through time and different states. For example, an `Order` with a unique order ID. Even if the order's shipping address changes, it's still the same order.
		- **Value Objects:** An object that describes a characteristic (solely by their attributes) but has no conceptual identity. They are *immutable*. Examples include `Money` (with an amount and currency) or `Address`. Two addresses with the same street, city, and zip code are considered the same address.
		- **Aggregates:** A cluster of associated objects (Entities and Value Objects) that are treated as a single unit for data changes. One entity is the **Aggregate Root**, which is the only entry point for modifying the entire aggregate. This is crucial for ensuring data consistency and integrity.
			- Example**:** An `Order` (Aggregate Root) and its `OrderLineItems`. You don't change a `LineItem` directly; you ask the `Order` to do it, so the `Order` can enforce business rules (e.g., "you can't change an order after it's shipped").
		- **Domain Services:** When a significant business process or transformation doesn't naturally fit within a single Entity or Value Object, we model it as a Domain Service. For example, a `FundsTransferService` that handles the logic of moving money between two bank accounts.
		<details>
		<summary>**Repositories:** These handle the persistence and retrieval of Aggregates from the underlying database. They provide a collection-like interface for accessing domain objects, abstracting away the data storage details.</summary>
			A **DDD Repository** is a mechanism that provides a illusion of an in-memory collection for all objects of a specific type, but it's specifically designed for **Aggregate Roots only**. Its primary purpose is to encapsulate all the logic needed to obtain object references and persist changes.
			**Key Characteristics:**
			- It only deals with **Aggregate Roots**, not every single entity.
			- It has a **collection-oriented interface** with methods like `add()`, `remove()`, `find()`, and `nextIdentity()`.
			- It hides the complexities of data persistence and infrastructure.
			- It works hand-in-hand with the Domain Model, returning full Aggregates that are ready for business operations.
			**Example in PHP:**
			php
			```plain text
interface OrderRepository
{
    public function find(OrderId $orderId): ?Order;
    public function save(Order $order): void;
    public function nextIdentity(): OrderId;

// Collection-oriented queriespublic function findPendingOrders(): array;
    public function findOrdersByCustomer(CustomerId $customerId): array;
}
			```
		</details>
		<details>
		<summary>**Domain Events:** Used to communicate significant occurrences within the domain that other parts of the system might be interested in. For example, after an `Order` is confirmed, it might publish an `OrderConfirmed` event, which a separate service could listen for to initiate shipping.</summary>
			- **Domain Events**: These are events that represent something that happened in the domain.
			- **Integration Events**: These are events that are used to communicate between different bounded contexts or microservices.
		</details>
	<details>
	<summary>**Context mapping **"map" of your software landscape, showing the different "countries" (Bounded Contexts) and the "relationships and treaties" (the mappings) between them.</summary>
		![](https://prod-files-secure.s3.us-west-2.amazonaws.com/8a3cc761-c117-4f8e-9775-0208e44a3977/7881e417-24dc-46b2-a295-149fade32c9e/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB46664SI2WYZ%2F20260910%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260910T110301Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjELn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIAjqgNaQzJ%2FyyM%2BB5tW%2FvKO7sYA1n6IzhhTjuLOnrNReAiEA37TbBTshCfMKT%2Fk5gfwgqOJdE9r6vKAxQPtCu2S7k4QqiAQIgv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDFMLfMXScSwh94NlpircAyOJ6q%2BoYUgyc%2BlK2MWl9QhwEo3MzdRqtKCR8Zmd9av8Y8S48cM6fwR%2F%2B9eiheZCYcOpQMnlsnAE62iJfUGADZCPf8Z8QYvZhtoywtWaMbo8SJDysaz%2F5tTXEx%2FWHFqFWyLolEdE6984Hr4y6d2PdA07ZD2QB3Q2VzAosYUukkEZOiRznk5mG8eB4tzzBrhmDm1ZSE3NokEo5a2vEBwrwdo2akKynU45hJkXscp%2FpIiTpU1WKek0nvryD1zZ7o545Zzvk9Yl%2FmeQiPKuuh1Ho2xdQRHTwEE%2BHOIqekCOgts8AYQ5XjKGb0l95Zs0vfDkZpbbcUYevLaqC99KgKnp%2FiXLhfnqYds40z%2BrpjziLV3HruO5HesWrOR3cM6lsUAwOhVbKXQqxVb7HA9pzZ%2BWIN0fqcAICD9kxgWMvIiWO6bwU02gt5%2FGDSBLFIVhu7wSTU3N6qaoGu6qR2e0m6%2FRq%2FIp6EUiH2oVw6nfPY9HbwzygYedke6aYwNCYZT8Ut8Yky9pWmWzCS3RQ2iyETFTpQhXkn6IT1mKfE%2FbIG6REzfuTadbPx2F565BXMrqyRCh16aGuwDvlDYst3tSdQgestT7TWvaPDYDe99ntPvI4rgPnrtsS%2FP%2BW9nN%2BVKwMNvjidUGOqUBh3Feb%2F15C37T0UAcxOpe8TWYlK8dUAnmoqVQa5vPCydV1RzXamWAZVXyFJMxk6hrEoRYbfm46HvDopXyx6yvbb5XzsGHspUTrfsFDxJWhxhekfVJHR4cUMEg2yke5Twe2fEBVGrKOhE71HoSO1EHpdlSuF5sCPHf9IeTDEpGv8yPABS5tWNWhaLp8juS4xS9Jm2MfUGqg5Emmjj1OYujOPP%2FQoLs&X-Amz-Signature=14841db819fb1650113998706198960132bb479a735cc2e5681f032cb9f6f478&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
	</details>
	- **Strategic vs. Tactical Design**
		- **Strategic DDD**: Focuses on high-level structure—bounded contexts, context mapping, and team organization.
		- **Tactical DDD**: Involves concrete building blocks like entities, aggregates, and repositories.
## **DDD Layers** {toggle="true"}
	<columns>
		<column>
			### **Domain** {toggle="true"}
				- Entities & Aggregates
				- Value Objects
				- Domain Services
				- Domain Events
				- Repositories (interfaces, not implementations)
				**Domain Layer Responsibilities:**
				- Business rules and logic
				- Domain model integrity
				- Domain events
				- Business invariants
		</column>
		<column>
			### **Application** {toggle="true"}
				Application services
				Commands & Queries
				Command/Query Handlers
				DTOs 
				**Typical Flow: **HTTP Request → Controller → Command/Query → Application Service → Domain Layer → Respons
				**Application Layer Responsibilities:**
				- Input validation (syntactic, not business rules)
				- Transaction management
				- Security checks (authentication, authorization)
				- Orchestrating domain objects
				- Handling cross-cutting concerns
				- Returning DTOs, not domain entities
		</column>
		<column>
			### **Infrastructure** {toggle="true"}
				- Persistence Implementations
				- External Service Integrations
				- Framework-Specific Code
				- Message Queue & Event System Implementations
				- Caching Implementations
				- File System & Storage
				- Authentication & Security
				- Configuration & Environment
				- Migrations & Database Schema
				- Logging & Monitoring
				**Infrastructure Layer DOES:**
				- ✅ Database operations and ORM mappings
				- ✅ External API calls
				- ✅ File system operations
				- ✅ Email sending
				- ✅ Message queue handling
				- ✅ Caching implementations
				- ✅ Framework configuration
				- ✅ Authentication mechanisms
				- ✅ Logging and monitoring
				**Infrastructure Layer DOES NOT:**
				- ❌ Contain business rules
				- ❌ Make decisions about business logic
				- ❌ Define interfaces (those are in domain/application layers)
				- ❌ Coordinate use cases
		</column>
	</columns>
### Interview questions {toggle="true"}
	<details>
	<summary>Explain the difference between Entities and Value Objects. Provide examples in PHP.</summary>
		An Entity is defined by a unique identity that persists through change, while a Value Object is defined entirely by its attributes and has no conceptual identity.
		<table header-row="true">
<tr>
<td>**Feature**</td>
<td>**Entity**</td>
<td>**Value Object**</td>
</tr>
<tr>
<td>**Identity**</td>
<td>Defined by a unique ID. Attributes can change, but the ID remains.</td>
<td>**No conceptual identity.** Defined solely by the values of its attributes.</td>
</tr>
<tr>
<td>**Mutability**</td>
<td>Mutable. Its state can change over time.</td>
<td>**Immutable.** Once created, it cannot be altered. You create a new one instead.</td>
</tr>
<tr>
<td>**Equality**</td>
<td>Equal if their unique IDs are the same.</td>
<td>Equal if the values of **all** their attributes are the same.</td>
</tr>
<tr>
<td>**Lifecycle**</td>
<td>Has a lifecycle that can be long and complex. It must be tracked.</td>
<td>Can be created and destroyed freely. No need for tracking.</td>
</tr>
		</table>
		---
	</details>
	<details>
	<summary>Can Value Object contain domain logic? </summary>
		Yes, Value Objects absolutely should contain domain logic - but only the logic that naturally belongs to the concept they represent, does not implement complex business workflow and doesn't cross aggregate boundaries.
		**✅ Value Objects SHOULD Contain:**
		1. **Self-contained calculations**
			```plain text
$total = $price->multiply($quantity);
$newDate = $startDate->addDays(7);
			```
		2. **Validation of their own state**
			```plain text
private function validateEmail(string $email): void {
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        throw new InvalidEmailException();
    }
}
			```
		3. **Derived data from their attributes**
			```plain text
public function isBusinessHours(): bool {
    return $this->hour >= 9 && $this->hour <= 17;
}
			```
		4. **Comparison and equality logic**
			```plain text
public function isGreaterThan(Money $other): bool {
    return $this->amount > $other->amount;
}
			```
		**❌ Value Objects SHOULD NOT Contain:**
		1. **Logic that changes other objects**
			```plain text
// ❌ This modifies an Entitypublic function applyDiscount(Order $order): void {
    $order->applyDiscount($this);
}
			```
		2. **Logic that requires external dependencies**
			```plain text
// ❌ This depends on external servicepublic function convertCurrency(CurrencyConverter $converter): Money {
    return $converter->convert($this, $targetCurrency);
}
			```
		3. **Business rules spanning multiple aggregates**
			```plain text
// ❌ This coordinates multiple domain objectspublic function processPayment(Order $order, PaymentGateway $gateway): void {
    $gateway->charge($this);
    $order->markAsPaid();
}
			```
		4. **Logic with side effects**
			```plain text
// ❌ This has side effects (sending email)public function notifyCustomer(Customer $customer): void {
    $this->emailService->send($customer, $this);
}
			```
		<empty-block/>
	</details>
	<details>
	<summary>What are Aggregates and why are they needed? How to determine aggregate boundaries?</summary>
		Aggregates are clusters of objects treated as a single unit to enforce business rules and maintain consistency.
		Aggregate boundaries - the clear line separating what's inside the aggregate (and therefore controlled by the aggregate root) from what's outside (and therefore accessed through references or services).<br>How to determine aggregate buindaties:
		1. **Group by transactional needs** - Objects that must change together in one transaction belong together
		2. **Protect invariants** - Include only what's needed to enforce immediate business rules
		3. **Single entry point** - Identify the root entity that controls all access
		4. **Small is better** - Favor many small aggregates over few large ones
		5. **Reference externally** - Link to other aggregates by ID only, not object references
		6. **Challenge consistency** - Use eventual consistency between aggregates when possible
		7. **Listen to the domain** - Boundaries emerge from business operations, not data relationships
		**Key question**: "What objects must be 100% consistent with each other at all times?"
	</details>
	<details>
	<summary>Explain the concept of Ubiquitous Language. How do you apply it in code?</summary>
		Applying it in code is about making the domain model explicit and reflective of the business reality. Here are the key techniques with examples:
		<details>
		<summary>**1. Class, Method, and Variable Names**</summary>
			The most direct application. The names in your code should be terms from the domain.
			**Before (Technical Names):**
			```php
class OrderManager {
    public function process(Order $order) {
// ... vague "process" ...}
}
			```
			**After (Ubiquitous Language):**
			```php
class Order {
    public function confirmPayment() { ... }
    public function markAsFulfilled() { ... }
    public function cancel(CancellationReason $reason) { ... }
}
			```
			- `confirmPayment`, `markAsFulfilled`, and `cancel` are specific actions the business understands.
		</details>
		### **2. Modules and Bounded Contexts**
		<details>
		<summary>The high-level structure of your application should reflect the domain.</summary>
			```plain text
// Directory/Namespace structure
src/
├── Shipping/                           // Bounded Context: Shipping
│   ├── Domain/
│   │   ├── Model/
│   │   │   ├── Entity/
│   │   │   │   ├── Shipment.php
│   │   │   │   └── DeliveryRoute.php
│   │   │   ├── ValueObject/
│   │   │   │   ├── TrackingNumber.php
│   │   │   │   ├── Address.php
│   │   │   │   └── Weight.php
│   │   │   ├── Aggregate/
│   │   │   │   └── ShippingManifest.php
│   │   │   └── Event/
│   │   │       ├── ShipmentDispatched.php
│   │   │       └── DeliveryAttemptFailed.php
│   │   ├── Service/
│   │   │   ├── ShippingCostCalculator.php
│   │   │   └── RouteOptimizationService.php
│   │   └── Repository/
│   │       ├── ShipmentRepositoryInterface.php
│   │       └── CarrierRepositoryInterface.php
│   ├── Application/
│   │   ├── Command/
│   │   │   ├── CreateShipmentCommand.php
│   │   │   └── UpdateTrackingCommand.php
│   │   ├── Query/
│   │   │   └── GetShipmentStatusQuery.php
│   │   └── Service/
│   │       ├── ShippingApplicationService.php
│   │       └── TrackingApplicationService.php
│   └── Infrastructure/
│       ├── Persistence/
│       │   └── Doctrine/
│       │       ├── ShipmentRepository.php
│       │       └── Mapping/Shipment.orm.xml
│       ├── External/
│       │   ├── FedExApiClient.php
│       │   └── UPSShippingGateway.php
│       └── Event/
│           └── RabbitMQEventDispatcher.php
│
└── Invoicing/                          // Bounded Context: Invoicing
    ├── Domain/
    │   ├── Model/
    │   │   ├── Entity/
    │   │   │   ├── Invoice.php
    │   │   │   ├── InvoiceLine.php
    │   │   │   └── Customer.php         // Local entity - different from Shipping's Customer
    │   │   ├── ValueObject/
    │   │   │   ├── InvoiceNumber.php
    │   │   │   ├── TaxId.php
    │   │   │   └── Money.php
    │   │   ├── Aggregate/
    │   │   │   └── Invoice.php          // Aggregate Root
    │   │   └── Event/
    │   │       ├── InvoiceIssued.php
    │   │       ├── PaymentReceived.php
    │   │       └── InvoiceOverdue.php
    │   ├── Service/
    │   │   ├── InvoiceCalculator.php
    │   │   ├── TaxCalculationService.php
    │   │   └── LateFeeApplicator.php
    │   └── Repository/
    │       ├── InvoiceRepositoryInterface.php
    │       └── CustomerRepositoryInterface.php
    ├── Application/
    │   ├── Command/
    │   │   ├── CreateInvoiceCommand.php
    │   │   ├── ApplyPaymentCommand.php
    │   │   └── SendReminderCommand.php
    │   ├── Query/
    │   │   ├── GetOutstandingInvoicesQuery.php
    │   │   └── CalculateTaxQuery.php
    │   └── Service/
    │       ├── InvoiceApplicationService.php
    │       └── BillingApplicationService.php
    └── Infrastructure/
        ├── Persistence/
        │   └── Doctrine/
        │       ├── InvoiceRepository.php
        │       ├── CustomerRepository.php
        │       └── Mapping/Invoice.orm.xml
        ├── External/
        │   ├── TaxApiClient.php
        │   └── PaymentGateway.php
        └── Notification/
            └── EmailInvoiceSender.php
			```
		</details>
		This structure immediately communicates the core subdomains.
		### **3. Domain Events**
		Events are things that happened in the domain. Their names should be in the past tense, using the ubiquitous language.
		```php
class PaymentWasConfirmed { ... }
class ShipmentWasDelivered { ... }
class OrderWasCancelled {
    public function __construct(
        private OrderId $orderId,
        private CancellationReason $reason// Uses a domain term) {}
}
		```
		### **4. Value Objects for Primitive Obsession**
		Avoid using primitive types (strings, integers) for domain concepts. Create Value Objects that embody the domain term and its rules.
		**Before (Primitive Obsession):**
		```php
class Product {
    private string $sku;// Just a stringprivate float $price;// Just a floatprivate string $currency;// Just a string}
		```
		**After (Ubiquitous Language in VOs):**
		```php
class Product {
    private ProductSKU $sku;// A Value Object with validationprivate Money $price;// A Value Object with amount & currency}

class ProductSKU {
    private string $value;
// Constructor enforces SKU format rules (e.g., "ABC-12345")}

class Money {
    private float $amount;
    private Currency $currency;// Another Value Object}
		```
		Now, the code explicitly uses the terms `ProductSKU`, `Money`, and `Currency`.
		### **5. Domain Services for Processes**
		When an operation doesn't fit naturally on a single Entity, create a Domain Service named after the domain process.
		```php
// The business has a "Risk Assessment" process for new customersclass CustomerRiskAssessmentService {
    public function isAcceptableRisk(Customer $customer, Order $order): RiskAssessmentResult {
// ... complex logic using domain terms ...}
}
// The result is also a domain conceptclass RiskAssessmentResult {
    private bool $isApproved;
    private RiskLevel $riskLevel;// e.g., Low, Medium, High (an Enum)}
		```
	</details>
	<details>
	<summary>What is a DDD Repository and how does it differ from a regular DAO and GoF Repository pattern?</summary>
		A **DDD Repository** is a mechanism that provides a illusion of an in-memory collection for all objects of a specific type, but it's specifically designed for **Aggregate Roots only**. Its primary purpose is to encapsulate all the logic needed to obtain object references and persist changes.
		<empty-block/>
		<table header-row="true">
<tr>
<td>**Aspect**</td>
<td>**DDD Repository**</td>
<td>**GoF Repository Pattern**</td>
<td>**DAO (Data Access Object)**</td>
</tr>
<tr>
<td>**Purpose**</td>
<td>Manage Aggregate Root lifecycles as domain collections</td>
<td>Generic mediator between domain and data source</td>
<td>Data access abstraction for persistence operations</td>
</tr>
<tr>
<td>**Abstraction Layer**</td>
<td>**Domain layer**</td>
<td>Data access layer</td>
<td>Data access layer</td>
</tr>
<tr>
<td>**Scope and Specificity**</td>
<td>**Aggregate Root specific** only</td>
<td>Generic - works with any entity</td>
<td>Table/record specific</td>
</tr>
<tr>
<td>**What It Returns**</td>
<td>**Aggregate Roots only** with full domain behavior</td>
<td>Any domain objects or data structures</td>
<td>Data structures (arrays, DTOs, anemic entities)</td>
</tr>
<tr>
<td>**Typical Interface Methods**</td>
<td>collection-oriented interface<br>`save()`, `remove()`, `find()`, `nextIdentity()`, domain-specific queries</td>
<td>`persist()`, `remove()`, `find()`, `getAll()`</td>
<td>`insert()`, `update()`, `delete()`, `select()`</td>
</tr>
<tr>
<td>**Query Semantics**</td>
<td>**Domain-oriented**: <br>findPendingShipments()<br>findOverdueInvoices()<br>findAvailableHotels(CheckInDate, CheckOutDate)<br>findOrdersReadyForFulfillment()<br>findHighValueCustomers()<br>findProductsOutOfStock()</td>
<td>Generic object queries:<br>findByCriteria(criteria)<br>findWithStatus(status)<br>searchByName(name)</td>
<td>Database-oriented:<br>findByStatus('active')<br>findByCustomerId(123)<br>findCreatedAfter('2024-01-01')</td>
</tr>
<tr>
<td>**DDD Layer**</td>
<td>**Interface in Domain**, Implementation in Infrastructure</td>
<td>Infrastructure layer</td>
<td>Infrastructure layer</td>
</tr>
<tr>
<td>**Architectural Role**</td>
<td>Domain collection that abstracts persistence</td>
<td>Generic object persistence mediator</td>
<td>Data mapper - moves data to/from storage</td>
</tr>
<tr>
<td>**Design Focus**</td>
<td>**Domain integrity** and Ubiquitous Language</td>
<td>Object persistence abstraction</td>
<td>Data persistence and mapping</td>
</tr>
<tr>
<td>**Persistence Control**</td>
<td>**Primarily Implicit with UoW** (recommended)</td>
<td>**Explicit per-operation** OR **Implicit with UoW**</td>
<td>**Explicit per-operation**</td>
</tr>
		</table>
		<table header-row="true">
<tr>
<td>**Aspect**</td>
<td>**DDD Repository**</td>
<td>**DAO**</td>
</tr>
<tr>
<td>**Purpose**</td>
<td>Domain pattern for managing Aggregate lifecycles</td>
<td>Data access pattern for database operations</td>
</tr>
<tr>
<td>**Abstraction Level**</td>
<td>Higher-level domain concept</td>
<td>Lower-level data access</td>
</tr>
<tr>
<td>**What It Returns**</td>
<td>Full **Aggregate Roots** with enforced invariants</td>
<td>**Data structures** (arrays, rows, entities without behavior)</td>
</tr>
<tr>
<td>**Interface**</td>
<td>Collection-oriented (`add`, `remove`, `find`)</td>
<td>CRUD-oriented (`insert`, `update`, `delete`, `select`)</td>
</tr>
<tr>
<td>**Relationship with Domain**</td>
<td>Part of the **domain** model, understands Aggregate boundaries</td>
<td>Part of **infrastructure**, understands database schema</td>
</tr>
		</table>
		### **Key Insights:**
		- **DAO** is purely about **data access** with a technical, CRUD-focused mindset
		- **GoF Repository** is a **generic pattern** for object persistence that can work with any entities
		- **DDD Repository** is a **domain pattern** specifically designed for DDD, working only with Aggregate Roots and using domain language
		**Summary**
		- DDD Repository is a domain pattern specifically for Aggregate Roots, with a collection-oriented interface that preserves the domain model's integrity and uses the Ubiquitous Language.
		- DAO is about data access and typically returns anemic data structures.
		- GoF Repository is a generic pattern for object persistence.
		The DDD Repository makes your persistence mechanism "speak the language of the domain" while maintaining the important constraint that only Aggregate Roots are accessible through it.
	</details>
	<details>
	<summary>What are layers in DDD?</summary>
		**1. Domain Layer **The heart of the business containing entities, value objects, domain services, and business rules. Pure business concepts without technical concerns.
		**2. Application Layer **Coordinates tasks and orchestrates business objects. Defines application use cases and workflows without containing business logic.
		**3. Infrastructure Layer **Provides technical capabilities: persistence, messaging, external APIs. Implements interfaces defined by higher layers.
		**Dependency Flow**
			**Application → Domain ← Infrastructure**
			The Domain Layer remains independent, ensuring business logic is isolated from technical concerns.
	</details>
	<details>
	<summary>When Domain Services should be used?</summary>
		**Domain Services** in DDD are stateless services that implement domain logic that doesn't naturally fit within Entities or Value Objects. 
		**✅ USE Domain Services When:**
		1. Logic Spanning Multiple Aggregates
		```php
class OrderProcessingService
{
    public function __construct(
        private OrderRepository $orderRepository,
        private InventoryRepository $inventoryRepository
    ) {}

// Business logic that coordinates multiple aggregatespublic function fulfillOrder(OrderId $orderId): void
    {
        $order = $this->orderRepository->find($orderId);
        $inventory = $this->inventoryRepository->findByProduct($order->productId());

        if (!$inventory->hasSufficientStock($order->quantity())) {
            throw new InsufficientStockException();
        }

        $order->markAsFulfilled();
        $inventory->reserveStock($order->quantity());

        $this->orderRepository->save($order);
        $this->inventoryRepository->save($inventory);
    }
}
		```
		2. Complex Calculations Requiring Multiple Domain Objects
		```php
class ShippingCostCalculator
{
    public function calculate(
        Shipment $shipment,
        Route $route,
        Carrier $carrier
    ): Money {
        $baseCost = $carrier->baseRate();
        $weightCost = $shipment->weight()->kilograms() * $carrier->ratePerKg();
        $distanceCost = $route->distance()->kilometers() * $carrier->ratePerKm();

        return $baseCost->add($weightCost)->add($distanceCost);
    }
}
		```
		3. External System Interactions That Are Part of Domain
		```php
class TaxCalculationService
{
    public function __construct(
        private TaxRateProvider $taxRateProvider
    ) {}

// Domain logic that requires external datapublic function calculateTax(Order $order, Address $shippingAddress): Money
    {
        $taxRate = $this->taxRateProvider->getRateForAddress($shippingAddress);
        $taxableAmount = $order->calculateTaxableAmount();

        return $taxableAmount->multiply($taxRate);
    }
}
		```
		4. Domain Concepts That Are Actions, Not Things
		```php
class AccountTransferService
{
    public function transfer(
        Account $fromAccount,
        Account $toAccount,
        Money $amount
    ): void {
        if (!$fromAccount->canWithdraw($amount)) {
            throw new InsufficientFundsException();
        }

        $fromAccount->withdraw($amount);
        $toAccount->deposit($amount);

// Domain event could be recorded hereDomainEventPublisher::publish(
            new FundsTransferred($fromAccount->id(), $toAccount->id(), $amount)
        );
    }
}
		```
		**❌ DO NOT Use Domain Services When:**
		**1. Logic Naturally Belongs to an Entity**
		```plain text
// ❌ WRONG - This should be in Order entityclass OrderCalculator {
    public function calculateTotal(Order $order): Money {
// This logic belongs in Order entityreturn $order->calculateTotal();
    }
}

// ✅ CORRECT - Logic in the Entityclass Order {
    public function calculateTotal(): Money {
        $total = Money::zero();
        foreach ($this->lines as $line) {
            $total = $total->add($line->subtotal());
        }
        return $total->subtract($this->discount);
    }
}
		```
		2. Simple Value Object Operations
		```php
// ❌ WRONG - This should be in Money value objectclass MoneyCalculator {
    public function add(Money $a, Money $b): Money {
        return $a->add($b);
    }
}

// ✅ CORRECT - Logic in Value Objectclass Money {
    public function add(Money $other): Money {
        return new Money($this->amount + $other->amount, $this->currency);
    }
}
		```
		3. Application Coordination Logic
		```php
// ❌ WRONG - This is Application Service responsibilityclass OrderCreationService {
    public function createOrder(array $data): void {
// This coordinates too many concerns - belongs in Application Service
        $order = new Order($data);
        $this->orderRepository->save($order);
        $this->emailService->sendConfirmation($order);
        $this->inventoryService->reserveItems($order);
    }
}
		```
	</details>
	<details>
	<summary>What are Domain Events  and how to implement them in PHP?</summary>
		**Core Characteristics**<br>✅ Immutable - once created, cannot be changed
		✅ Past tense - something that already happened
		✅ Meaningful - business significance, not technical details
		✅ Self-describing - contain all relevant data
		✅ Lightweight - focused on what happened, not how to handle it
		## **Basic Implementation**
		### **1. Base Domain Event Interface**
		php
		```plain text
<?php

declare(strict_types=1);

interface DomainEvent
{
    public function occurredOn(): \DateTimeImmutable;
    public function eventId(): string;
    public function eventType(): string;
}
		```
		### **2. Abstract Base Domain Event**
		php
		```plain text
<?php

declare(strict_types=1);

abstract class AbstractDomainEvent implements DomainEvent
{
    private \DateTimeImmutable $occurredOn;
    private string $eventId;

    public function __construct()
    {
        $this->eventId = uniqid('', true);
        $this->occurredOn = new \DateTimeImmutable();
    }

    public function occurredOn(): \DateTimeImmutable
    {
        return $this->occurredOn;
    }

    public function eventId(): string
    {
        return $this->eventId;
    }

    public function eventType(): string
    {
        return static::class;
    }
}
		```
		## **Complete Implementation Example**
		### **Project Structure**
		text
		```plain text
src/
├── Shared/
│   ├── Domain/
│   │   └── Event/
│   │       ├── DomainEvent.php
│   │       ├── AbstractDomainEvent.php
│   │       ├── DomainEventSubscriber.php
│   │       └── DomainEventPublisher.php
│   └── Infrastructure/
│       └── Event/
│           └── SimpleEventDispatcher.php
├── Order/
│   ├── Domain/
│   │   ├── Event/
│   │   │   ├── OrderWasPlaced.php
│   │   │   ├── OrderWasPaid.php
│   │   │   ├── OrderWasShipped.php
│   │   │   └── OrderWasCancelled.php
│   │   └── Model/
│   │       └── Order.php
└── Notification/
    └── Application/
        └── Event/
            └── OrderEventsHandler.php
		```
		### **1. Concrete Domain Events**
		php
		```plain text
<?php
// src/Order/Domain/Event/OrderWasPlaced.phpdeclare(strict_types=1);

namespace Order\Domain\Event;

use Order\Domain\Model\OrderId;
use Order\Domain\Model\CustomerId;
use Order\Domain\Model\Money;
use Shared\Domain\Event\AbstractDomainEvent;

final class OrderWasPlaced extends AbstractDomainEvent
{
    public function __construct(
        private OrderId $orderId,
        private CustomerId $customerId,
        private Money $totalAmount,
        private \DateTimeImmutable $orderDate,
        private array $lineItems
    ) {
        parent::__construct();
    }

    public function orderId(): OrderId
    {
        return $this->orderId;
    }

    public function customerId(): CustomerId
    {
        return $this->customerId;
    }

    public function totalAmount(): Money
    {
        return $this->totalAmount;
    }

    public function orderDate(): \DateTimeImmutable
    {
        return $this->orderDate;
    }

    public function lineItems(): array
    {
        return $this->lineItems;
    }

// Optional: Serialization for event storagepublic function toArray(): array
    {
        return [
            'event_id' => $this->eventId(),
            'event_type' => $this->eventType(),
            'occurred_on' => $this->occurredOn()->format('Y-m-d H:i:s'),
            'order_id' => $this->orderId->toString(),
            'customer_id' => $this->customerId->toString(),
            'total_amount' => $this->totalAmount->toArray(),
            'order_date' => $this->orderDate->format('Y-m-d H:i:s'),
            'line_items' => array_map(fn($item) => $item->toArray(), $this->lineItems),
        ];
    }

// Optional: Factory method from array (for deserialization)public static function fromArray(array $data): self
    {
        return new self(
            OrderId::fromString($data['order_id']),
            CustomerId::fromString($data['customer_id']),
            Money::fromArray($data['total_amount']),
            \DateTimeImmutable::createFromFormat('Y-m-d H:i:s', $data['order_date']),
            array_map(fn($item) => OrderLineItem::fromArray($item), $data['line_items'])
        );
    }
}
		```
		php
		```plain text
<?php
// src/Order/Domain/Event/OrderWasPaid.phpdeclare(strict_types=1);

namespace Order\Domain\Event;

use Order\Domain\Model\OrderId;
use Order\Domain\Model\Money;
use Shared\Domain\Event\AbstractDomainEvent;

final class OrderWasPaid extends AbstractDomainEvent
{
    public function __construct(
        private OrderId $orderId,
        private Money $amountPaid,
        private string $paymentMethod,
        private string $transactionId,
        private \DateTimeImmutable $paidAt
    ) {
        parent::__construct();
    }

    public function orderId(): OrderId
    {
        return $this->orderId;
    }

    public function amountPaid(): Money
    {
        return $this->amountPaid;
    }

    public function paymentMethod(): string
    {
        return $this->paymentMethod;
    }

    public function transactionId(): string
    {
        return $this->transactionId;
    }

    public function paidAt(): \DateTimeImmutable
    {
        return $this->paidAt;
    }
}
		```
		### **2. Aggregate Root Recording Events**
		php
		```plain text
<?php
// src/Order/Domain/Model/Order.phpdeclare(strict_types=1);

namespace Order\Domain\Model;

use Order\Domain\Event\OrderWasPlaced;
use Order\Domain\Event\OrderWasPaid;
use Order\Domain\Event\OrderWasShipped;
use Order\Domain\Event\OrderWasCancelled;

class Order
{
    private OrderId $id;
    private CustomerId $customerId;
    private OrderStatus $status;
    private Money $totalAmount;
    private ?\DateTimeImmutable $paidAt = null;
    private ?\DateTimeImmutable $shippedAt = null;

/** @var DomainEvent[] */private array $recordedEvents = [];

    private function __construct() {}

    public static function place(
        OrderId $orderId,
        CustomerId $customerId,
        array $lineItems,
        Money $totalAmount
    ): self {
        $order = new self();
        $order->id = $orderId;
        $order->customerId = $customerId;
        $order->status = OrderStatus::PLACED;
        $order->totalAmount = $totalAmount;

// Record the domain event$order->recordEvent(new OrderWasPlaced(
            $orderId,
            $customerId,
            $totalAmount,
            new \DateTimeImmutable(),
            $lineItems
        ));

        return $order;
    }

    public function pay(
        Money $amountPaid,
        string $paymentMethod,
        string $transactionId
    ): void {
        if (!$this->status->canTransitionTo(OrderStatus::PAID)) {
            throw new \DomainException('Order cannot be paid in current state');
        }

        if (!$amountPaid->equals($this->totalAmount)) {
            throw new \DomainException('Payment amount must match order total');
        }

        $this->status = OrderStatus::PAID;
        $this->paidAt = new \DateTimeImmutable();

        $this->recordEvent(new OrderWasPaid(
            $this->id,
            $amountPaid,
            $paymentMethod,
            $transactionId,
            $this->paidAt
        ));
    }

    public function ship(string $trackingNumber): void
    {
        if (!$this->status->isPaid()) {
            throw new \DomainException('Only paid orders can be shipped');
        }

        $this->status = OrderStatus::SHIPPED;
        $this->shippedAt = new \DateTimeImmutable();

        $this->recordEvent(new OrderWasShipped(
            $this->id,
            $trackingNumber,
            $this->shippedAt
        ));
    }

    public function cancel(string $reason): void
    {
        if ($this->status->isShipped() || $this->status->isDelivered()) {
            throw new \DomainException('Cannot cancel shipped or delivered order');
        }

        $this->status = OrderStatus::CANCELLED;

        $this->recordEvent(new OrderWasCancelled(
            $this->id,
            $reason,
            new \DateTimeImmutable()
        ));
    }

    private function recordEvent(DomainEvent $event): void
    {
        $this->recordedEvents[] = $event;
    }

/**
     * @return DomainEvent[]
     */public function releaseEvents(): array
    {
        $events = $this->recordedEvents;
        $this->recordedEvents = [];

        return $events;
    }

    public function clearEvents(): void
    {
        $this->recordedEvents = [];
    }
}
		```
		### **3. Event Subscriber Interface**
		php
		```plain text
<?php
// src/Shared/Domain/Event/DomainEventSubscriber.phpdeclare(strict_types=1);

namespace Shared\Domain\Event;

interface DomainEventSubscriber
{
/**
     * @return string[] The event types this subscriber handles
     */public function subscribedTo(): array;

    public function handle(DomainEvent $event): void;

    public function handleBatch(array $events): void;
}
		```
		### **4. Event Dispatcher Implementation**
		php
		```plain text
<?php
// src/Shared/Infrastructure/Event/SimpleEventDispatcher.phpdeclare(strict_types=1);

namespace Shared\Infrastructure\Event;

use Shared\Domain\Event\DomainEvent;
use Shared\Domain\Event\DomainEventSubscriber;

class SimpleEventDispatcher
{
/** @var DomainEventSubscriber[][] */private array $subscribers = [];

    public function __construct(iterable $subscribers = [])
    {
        foreach ($subscribers as $subscriber) {
            $this->subscribe($subscriber);
        }
    }

    public function subscribe(DomainEventSubscriber $subscriber): void
    {
        foreach ($subscriber->subscribedTo() as $eventType) {
            $this->subscribers[$eventType][] = $subscriber;
        }
    }

    public function dispatch(DomainEvent $event): void
    {
        $eventType = get_class($event);

        if (!isset($this->subscribers[$eventType])) {
            return;
        }

        foreach ($this->subscribers[$eventType] as $subscriber) {
            $subscriber->handle($event);
        }
    }

    public function dispatchAll(array $events): void
    {
        foreach ($events as $event) {
            $this->dispatch($event);
        }
    }
}
		```
		### **5. Concrete Event Subscribers**
		php
		```plain text
<?php
// src/Notification/Application/Event/OrderEventsHandler.phpdeclare(strict_types=1);

namespace Notification\Application\Event;

use Order\Domain\Event\OrderWasPlaced;
use Order\Domain\Event\OrderWasPaid;
use Order\Domain\Event\OrderWasShipped;
use Shared\Domain\Event\DomainEvent;
use Shared\Domain\Event\DomainEventSubscriber;

class OrderEventsHandler implements DomainEventSubscriber
{
    public function __construct(
        private EmailService $emailService,
        private SmsService $smsService
    ) {}

    public function subscribedTo(): array
    {
        return [
            OrderWasPlaced::class,
            OrderWasPaid::class,
            OrderWasShipped::class,
        ];
    }

    public function handle(DomainEvent $event): void
    {
        match (get_class($event)) {
            OrderWasPlaced::class => $this->onOrderWasPlaced($event),
            OrderWasPaid::class => $this->onOrderWasPaid($event),
            OrderWasShipped::class => $this->onOrderWasShipped($event),
        };
    }

    public function handleBatch(array $events): void
    {
        foreach ($events as $event) {
            $this->handle($event);
        }
    }

    private function onOrderWasPlaced(OrderWasPlaced $event): void
    {
        $this->emailService->sendOrderConfirmation(
            $event->customerId(),
            $event->orderId(),
            $event->totalAmount()
        );
    }

    private function onOrderWasPaid(OrderWasPaid $event): void
    {
        $this->emailService->sendPaymentConfirmation(
            $event->orderId(),
            $event->amountPaid(),
            $event->paymentMethod()
        );
    }

    private function onOrderWasShipped(OrderWasShipped $event): void
    {
        $this->smsService->sendShippingNotification(
            $event->orderId(),
            $event->trackingNumber()
        );
    }
}
		```
		php
		```plain text
<?php
// src/Inventory/Application/Event/OrderPlacedHandler.phpdeclare(strict_types=1);

namespace Inventory\Application\Event;

use Order\Domain\Event\OrderWasPlaced;
use Shared\Domain\Event\DomainEvent;
use Shared\Domain\Event\DomainEventSubscriber;

class OrderPlacedHandler implements DomainEventSubscriber
{
    public function __construct(
        private InventoryRepository $inventoryRepository
    ) {}

    public function subscribedTo(): array
    {
        return [OrderWasPlaced::class];
    }

    public function handle(DomainEvent $event): void
    {
        $this->onOrderWasPlaced($event);
    }

    public function handleBatch(array $events): void
    {
        foreach ($events as $event) {
            $this->handle($event);
        }
    }

    private function onOrderWasPlaced(OrderWasPlaced $event): void
    {
        foreach ($event->lineItems() as $lineItem) {
            $this->inventoryRepository->reserveItem(
                $lineItem->productId(),
                $lineItem->quantity(),
                $event->orderId()
            );
        }
    }
}
		```
		### **6. Integration in Application Service**
		php
		```plain text
<?php
// src/Order/Application/Service/OrderApplicationService.phpdeclare(strict_types=1);

namespace Order\Application\Service;

use Order\Domain\Model\Order;
use Order\Domain\Model\OrderId;
use Order\Domain\Model\CustomerId;
use Order\Domain\Model\Money;
use Order\Domain\Repository\OrderRepository;
use Shared\Infrastructure\Event\SimpleEventDispatcher;

class OrderApplicationService
{
    public function __construct(
        private OrderRepository $orderRepository,
        private SimpleEventDispatcher $eventDispatcher
    ) {}

    public function placeOrder(array $orderData): void
    {
// Begin transaction if needed$order = Order::place(
            OrderId::generate(),
            CustomerId::fromString($orderData['customer_id']),
            $this->buildLineItems($orderData['items']),
            Money::fromFloat($orderData['total_amount'], 'USD')
        );

        $this->orderRepository->save($order);

// Dispatch events after successful persistence$events = $order->releaseEvents();
        $this->eventDispatcher->dispatchAll($events);

// Commit transaction if needed}

    public function payOrder(string $orderId, array $paymentData): void
    {
        $order = $this->orderRepository->find(OrderId::fromString($orderId));

        $order->pay(
            Money::fromFloat($paymentData['amount'], 'USD'),
            $paymentData['payment_method'],
            $paymentData['transaction_id']
        );

        $this->orderRepository->save($order);

        $events = $order->releaseEvents();
        $this->eventDispatcher->dispatchAll($events);
    }

    private function buildLineItems(array $items): array
    {
// Build order line items from datareturn array_map(fn($item) => OrderLineItem::fromArray($item), $items);
    }
}
		```
		### **7. Configuration (Dependency Injection)**
		php
		```plain text
<?php
// config/events.phpdeclare(strict_types=1);

use Notification\Application\Event\OrderEventsHandler;
use Inventory\Application\Event\OrderPlacedHandler;
use Shared\Infrastructure\Event\SimpleEventDispatcher;

$emailService = new EmailService();
$smsService = new SmsService();
$inventoryRepository = new InventoryRepository();

$subscribers = [
    new OrderEventsHandler($emailService, $smsService),
    new OrderPlacedHandler($inventoryRepository),
];

$eventDispatcher = new SimpleEventDispatcher($subscribers);

// Register in your DI container$container->set(SimpleEventDispatcher::class, $eventDispatcher);
		```
	</details>
	<details>
	<summary>How to organize folder structure in a PHP project with DDD?</summary>
		```php
src/
├── Shared/                          # Shared Kernel
│   ├── Domain/
│   │   ├── ValueObject/
│   │   │   ├── Uuid.php
│   │   │   ├── DateTimeRange.php
│   │   │   ├── Money.php
│   │   │   ├── Email.php
│   │   │   └── AggregateRoot.php
│   │   ├── Event/
│   │   │   ├── DomainEvent.php
│   │   │   ├── DomainEventSubscriber.php
│   │   │   └── EventDispatcher.php
│   │   └── Exception/
│   │       ├── DomainException.php
│   │       ├── InvalidArgumentException.php
│   │       └── EntityNotFoundException.php
│   ├── Application/
│   │   ├── Command/
│   │   │   └── CommandInterface.php
│   │   ├── Query/
│   │   │   └── QueryInterface.php
│   │   └── Service/
│   │       └── ApplicationService.php
│   └── Infrastructure/
│       ├── Bus/
│       │   ├── CommandBus.php
│       │   ├── QueryBus.php
│       │   └── EventBus.php
│       ├── Persistence/
│       │   └── Doctrine/
│       │       ├── EntityRepository.php
│       │       └── Types/
│       │           ├── UuidType.php
│       │           └── MoneyType.php
│       └── Serializer/
│           └── JsonSerializer.php
│
├── IdentityAccess/                  # Bounded Context: Identity & Access Management
│   ├── Domain/
│   │   ├── Model/
│   │   │   ├── Entity/
│   │   │   │   ├── User.php
│   │   │   │   ├── Role.php
│   │   │   │   └── Permission.php
│   │   │   ├── ValueObject/
│   │   │   │   ├── UserId.php
│   │   │   │   ├── HashedPassword.php
│   │   │   │   ├── Email.php
│   │   │   │   └── AuthToken.php
│   │   │   ├── Aggregate/
│   │   │   │   └── UserSession.php
│   │   │   ├── Event/
│   │   │   │   ├── UserRegistered.php
│   │   │   │   ├── UserLoggedIn.php
│   │   │   │   └── PasswordChanged.php
│   │   │   └── Exception/
│   │   │       ├── InvalidCredentialsException.php
│   │   │       └── UserAlreadyExistsException.php
│   │   ├── Service/
│   │   │   ├── PasswordHasher.php
│   │   │   ├── TokenGenerator.php
│   │   │   └── AuthenticationService.php
│   │   └── Repository/
│   │       ├── UserRepositoryInterface.php
│   │       └── RoleRepositoryInterface.php
│   ├── Application/
│   │   ├── Command/
│   │   │   ├── RegisterUserCommand.php
│   │   │   ├── LoginUserCommand.php
│   │   │   ├── ChangePasswordCommand.php
│   │   │   └── Handler/
│   │   │       ├── RegisterUserHandler.php
│   │   │       ├── LoginUserHandler.php
│   │   │       └── ChangePasswordHandler.php
│   │   ├── Query/
│   │   │   ├── GetUserQuery.php
│   │   │   ├── ValidateTokenQuery.php
│   │   │   └── Handler/
│   │   │       ├── GetUserHandler.php
│   │   │       └── ValidateTokenHandler.php
│   │   └── Service/
│   │       ├── IdentityApplicationService.php
│   │       └── AccessApplicationService.php
│   └── Infrastructure/
│       ├── Persistence/
│       │   └── Doctrine/
│       │       ├── Repository/
│       │       │   ├── UserRepository.php
│       │       │   └── RoleRepository.php
│       │       └── Mapping/
│       │           ├── User.orm.xml
│       │           └── Role.orm.xml
│       ├── Security/
│       │   ├── BcryptPasswordHasher.php
│       │   └── JwtTokenGenerator.php
│       └── Presentation/
│           ├── Controller/
│           │   ├── AuthController.php
│           │   └── UserController.php
│           ├── Request/
│           │   ├── RegisterRequest.php
│           │   └── LoginRequest.php
│           └── Response/
│               ├── UserResponse.php
│               └── AuthResponse.php
│
├── ProductCatalog/                  # Bounded Context: Product Management
│   ├── Domain/
│   │   ├── Model/
│   │   │   ├── Entity/
│   │   │   │   ├── Product.php
│   │   │   │   ├── Category.php
│   │   │   │   └── Brand.php
│   │   │   ├── ValueObject/
│   │   │   │   ├── ProductId.php
│   │   │   │   ├── SKU.php
│   │   │   │   ├── ProductStatus.php
│   │   │   │   └── ProductAttribute.php
│   │   │   ├── Aggregate/
│   │   │   │   └── Catalog.php
│   │   │   ├── Event/
│   │   │   │   ├── ProductCreated.php
│   │   │   │   ├── ProductUpdated.php
│   │   │   │   └── ProductDiscontinued.php
│   │   │   └── Exception/
│   │   │       ├── ProductNotFoundException.php
│   │   │       └── DuplicateSkuException.php
│   │   ├── Service/
│   │   │   ├── ProductSearchService.php
│   │   │   └── CategoryTreeService.php
│   │   └── Repository/
│   │       ├── ProductRepositoryInterface.php
│   │       ├── CategoryRepositoryInterface.php
│   │       └── CatalogRepositoryInterface.php
│   ├── Application/
│   │   ├── Command/
│   │   │   ├── CreateProductCommand.php
│   │   │   ├── UpdateProductCommand.php
│   │   │   ├── CategorizeProductCommand.php
│   │   │   └── Handler/
│   │   │       ├── CreateProductHandler.php
│   │   │       ├── UpdateProductHandler.php
│   │   │       └── CategorizeProductHandler.php
│   │   ├── Query/
│   │   │   ├── SearchProductsQuery.php
│   │   │   ├── GetProductQuery.php
│   │   │   ├── GetCategoryTreeQuery.php
│   │   │   └── Handler/
│   │   │       ├── SearchProductsHandler.php
│   │   │       ├── GetProductHandler.php
│   │   │       └── GetCategoryTreeHandler.php
│   │   └── Service/
│   │       ├── ProductApplicationService.php
│   │       └── CatalogApplicationService.php
│   └── Infrastructure/
│       ├── Persistence/
│       │   └── Doctrine/
│       │       ├── Repository/
│       │       │   ├── ProductRepository.php
│       │       │   ├── CategoryRepository.php
│       │       │   └── CatalogRepository.php
│       │       └── Mapping/
│       │           ├── Product.orm.xml
│       │           ├── Category.orm.xml
│       │           └── Brand.orm.xml
│       ├── Search/
│       │   └── ElasticsearchProductIndexer.php
│       └── Presentation/
│           ├── Controller/
│           │   ├── ProductController.php
│           │   └── CategoryController.php
│           ├── Request/
│           │   ├── CreateProductRequest.php
│           │   └── SearchProductsRequest.php
│           └── Response/
│               ├── ProductResponse.php
│               ├── CategoryResponse.php
│               └── ProductListResponse.php
│
├── OrderManagement/                 # Bounded Context: Order Processing
│   ├── Domain/
│   │   ├── Model/
│   │   │   ├── Entity/
│   │   │   │   ├── Order.php
│   │   │   │   ├── OrderLine.php
│   │   │   │   └── Customer.php
│   │   │   ├── ValueObject/
│   │   │   │   ├── OrderId.php
│   │   │   │   ├── OrderNumber.php
│   │   │   │   ├── OrderStatus.php
│   │   │   │   └── OrderTotal.php
│   │   │   ├── Aggregate/
│   │   │   │   └── Order.php
│   │   │   ├── Event/
│   │   │   │   ├── OrderPlaced.php
│   │   │   │   ├── OrderCancelled.php
│   │   │   │   ├── OrderPaid.php
│   │   │   │   └── OrderShipped.php
│   │   │   └── Exception/
│   │   │       ├── OrderNotFoundException.php
│   │   │       ├── InvalidOrderStateException.php
│   │   │       └── OrderAlreadyCancelledException.php
│   │   ├── Service/
│   │   │   ├── OrderCalculator.php
│   │   │   └── OrderValidator.php
│   │   └── Repository/
│   │       ├── OrderRepositoryInterface.php
│   │       └── CustomerRepositoryInterface.php
│   ├── Application/
│   │   ├── Command/
│   │   │   ├── PlaceOrderCommand.php
│   │   │   ├── CancelOrderCommand.php
│   │   │   ├── UpdateOrderStatusCommand.php
│   │   │   └── Handler/
│   │   │       ├── PlaceOrderHandler.php
│   │   │       ├── CancelOrderHandler.php
│   │   │       └── UpdateOrderStatusHandler.php
│   │   ├── Query/
│   │   │   ├── GetOrderQuery.php
│   │   │   ├── GetCustomerOrdersQuery.php
│   │   │   └── Handler/
│   │   │       ├── GetOrderHandler.php
│   │   │       └── GetCustomerOrdersHandler.php
│   │   └── Service/
│   │       ├── OrderApplicationService.php
│   │       └── CustomerApplicationService.php
│   └── Infrastructure/
│       ├── Persistence/
│       │   └── Doctrine/
│       │       ├── Repository/
│       │       │   ├── OrderRepository.php
│       │       │   └── CustomerRepository.php
│       │       └── Mapping/
│       │           ├── Order.orm.xml
│       │           ├── OrderLine.orm.xml
│       │           └── Customer.orm.xml
│       ├── External/
│       │   └── InventoryApiClient.php
│       └── Presentation/
│           ├── Controller/
│           │   ├── OrderController.php
│           │   └── CustomerController.php
│           ├── Request/
│           │   ├── PlaceOrderRequest.php
│           │   └── CancelOrderRequest.php
│           └── Response/
│               ├── OrderResponse.php
│               ├── OrderListResponse.php
│               └── CustomerOrderHistoryResponse.php
│
├── Shipping/                        # Bounded Context: Shipping & Logistics
│   ├── Domain/
│   │   ├── Model/
│   │   │   ├── Entity/
│   │   │   │   ├── Shipment.php
│   │   │   │   ├── DeliveryRoute.php
│   │   │   │   └── Carrier.php
│   │   │   ├── ValueObject/
│   │   │   │   ├── TrackingNumber.php
│   │   │   │   ├── Address.php
│   │   │   │   ├── Weight.php
│   │   │   │   ├── Dimensions.php
│   │   │   │   └── RouteOptimization.php
│   │   │   ├── Aggregate/
│   │   │   │   └── ShippingManifest.php
│   │   │   ├── Event/
│   │   │   │   ├── ShipmentCreated.php
│   │   │   │   ├── ShipmentDispatched.php
│   │   │   │   └── PackageDelivered.php
│   │   │   └── Exception/
│   │   │       ├── InvalidShippingAddressException.php
│   │   │       └── CarrierUnavailableException.php
│   │   ├── Service/
│   │   │   ├── ShippingCostCalculator.php
│   │   │   ├── RouteOptimizationService.php
│   │   │   └── CarrierSelectionService.php
│   │   └── Repository/
│   │       ├── ShipmentRepositoryInterface.php
│   │       ├── CarrierRepositoryInterface.php
│   │       └── DeliveryRouteRepositoryInterface.php
│   ├── Application/
│   │   ├── Command/
│   │   │   ├── CreateShipmentCommand.php
│   │   │   ├── DispatchShipmentCommand.php
│   │   │   ├── UpdateTrackingCommand.php
│   │   │   └── Handler/
│   │   │       ├── CreateShipmentHandler.php
│   │   │       ├── DispatchShipmentHandler.php
│   │   │       └── UpdateTrackingHandler.php
│   │   ├── Query/
│   │   │   ├── GetShippingRatesQuery.php
│   │   │   ├── TrackShipmentQuery.php
│   │   │   └── Handler/
│   │   │       ├── GetShippingRatesHandler.php
│   │   │       └── TrackShipmentHandler.php
│   │   └── Service/
│   │       ├── ShippingApplicationService.php
│   │       └── TrackingApplicationService.php
│   └── Infrastructure/
│       ├── Persistence/
│       │   └── Doctrine/
│       │       ├── Repository/
│       │       │   ├── ShipmentRepository.php
│       │       │   ├── CarrierRepository.php
│       │       │   └── DeliveryRouteRepository.php
│       │       └── Mapping/
│       │           ├── Shipment.orm.xml
│       │           ├── DeliveryRoute.orm.xml
│       │           └── Carrier.orm.xml
│       ├── External/
│       │   ├── FedExApiClient.php
│       │   ├── UPSShippingGateway.php
│       │   └── DHLShippingAdapter.php
│       └── Presentation/
│           ├── Controller/
│           │   ├── ShipmentController.php
│           │   └── TrackingController.php
│           ├── Request/
│           │   ├── CreateShipmentRequest.php
│           │   └── GetShippingRatesRequest.php
│           └── Response/
│               ├── ShipmentResponse.php
│               ├── ShippingRateResponse.php
│               └── TrackingResponse.php
│
└── Billing/                         # Bounded Context: Invoicing & Payments
    ├── Domain/
    │   ├── Model/
    │   │   ├── Entity/
    │   │   │   ├── Invoice.php
    │   │   │   ├── InvoiceLine.php
    │   │   │   └── Payer.php
    │   │   ├── ValueObject/
    │   │   │   ├── InvoiceNumber.php
    │   │   │   ├── TaxId.php
    │   │   │   ├── Money.php
    │   │   │   ├── PaymentStatus.php
    │   │   │   └── TaxRate.php
    │   │   ├── Aggregate/
    │   │   │   └── InvoiceAggregate.php
    │   │   ├── Event/
    │   │   │   ├── InvoiceIssued.php
    │   │   │   ├── PaymentReceived.php
    │   │   │   ├── InvoiceOverdue.php
    │   │   │   └── LateFeeApplied.php
    │   │   └── Exception/
    │   │       ├── InvoiceAlreadyPaidException.php
    │   │       ├── InvalidPaymentAmountException.php
    │   │       └── TaxCalculationException.php
    │   ├── Service/
    │   │   ├── InvoiceCalculator.php
    │   │   ├── TaxCalculationService.php
    │   │   └── LateFeeApplicator.php
    │   └── Repository/
    │       ├── InvoiceRepositoryInterface.php
    │       └── PayerRepositoryInterface.php
    ├── Application/
    │   ├── Command/
    │   │   ├── CreateInvoiceCommand.php
    │   │   ├── ApplyPaymentCommand.php
    │   │   ├── SendReminderCommand.php
    │   │   └── Handler/
    │   │       ├── CreateInvoiceHandler.php
    │   │       ├── ApplyPaymentHandler.php
    │   │       └── SendReminderHandler.php
    │   ├── Query/
    │   │   ├── GetOutstandingInvoicesQuery.php
    │   │   ├── CalculateTaxQuery.php
    │   │   └── Handler/
    │   │       ├── GetOutstandingInvoicesHandler.php
    │   │       └── CalculateTaxHandler.php
    │   └── Service/
    │       ├── InvoiceApplicationService.php
    │       └── BillingApplicationService.php
    └── Infrastructure/
        ├── Persistence/
        │   └── Doctrine/
        │       ├── Repository/
        │       │   ├── InvoiceRepository.php
        │       │   └── PayerRepository.php
        │       └── Mapping/
        │           ├── Invoice.orm.xml
        │           └── InvoiceLine.orm.xml
        ├── External/
        │   ├── TaxApiClient.php
        │   ├── PaymentGateway.php
        │   ├── StripePaymentAdapter.php
        │   └── PayPalPaymentGateway.php
        └── Presentation/
            ├── Controller/
            │   ├── InvoiceController.php
            │   └── PaymentController.php
            ├── Request/
            │   ├── CreateInvoiceRequest.php
            │   └── ProcessPaymentRequest.php
            └── Response/
                ├── InvoiceResponse.php
                ├── PaymentResponse.php
                └── BillingReportResponse.php

config/
├── packages/
│   ├── doctrine.yaml
│   ├── services.yaml
│   └── event_bus.yaml
├── routes/
│   ├── identity_access.yaml
│   ├── product_catalog.yaml
│   ├── order_management.yaml
│   ├── shipping.yaml
│   └── billing.yaml
└── parameters.yaml

tests/
├── Shared/
├── IdentityAccess/
│   ├── Domain/
│   ├── Application/
│   └── Infrastructure/
├── ProductCatalog/
│   ├── Domain/
│   ├── Application/
│   └── Infrastructure/
├── OrderManagement/
│   ├── Domain/
│   ├── Application/
│   └── Infrastructure/
├── Shipping/
│   ├── Domain/
│   ├── Application/
│   └── Infrastructure/
└── Billing/
    ├── Domain/
    ├── Application/
    └── Infrastructure/

public/
├── index.php
└── .htaccess

var/
├── cache/
├── log/
└── data/

docs/
├── context-maps/
├── domain-models/
└── api-documentation/
		```
	</details>
	<details>
	<summary>Where should business logic be located: in entities, services, or somewhere else?</summary>
		in Entities, Services and Value Objects, not in Infrastructure and not In Application layer
	</details>
	<details>
	</details>
	<details>
	<summary>_</summary>
	</details>
	<details>
	<summary><span color="red">How these layers fit into Hexagonal Architecture?</span></summary>
	</details>
	<details>
	<summary>How DDD fits CQRS approach?</summary>
	</details>
	<empty-block/>
## AOP (Aspect Oriented Programming)
Programming paradigm that aims to increase modularity by allowing the separation of **cross-cutting concerns**. It complements Object-Oriented Programming (OOP) by providing another way to think about program structure.
<details>
<summary>**Cross-cutting concerns** are functionalities that affect multiple parts of a system and don't fit neatly into a single module. Common examples include:</summary>
	- **Logging**
	- **Security/Authentication**
	- **Transaction management**
	- **Caching**
	- **Performance monitoring**
	- **Error handling**
	- **Audit trails**
	In traditional OOP, these concerns often end up scattered throughout your codebase, creating what's called **"code tangling"** and **"code scattering"**.
</details>
<details>
<summary>**AOP Patterns**</summary>
	[https://chat.deepseek.com/share/58f5c6xbf8x9oh5dvt](https://chat.deepseek.com/share/58f5c6xbf8x9oh5dvt)
</details>
## MVC/MVVM
- MVC
- MVVM
## Other Popular Patterns
- ORM
- DataMapper vs ActiveRecord
- EntityManager
-
## Code Smells & Anti-patterns
## Clean Architecture
## Hexagonal Architecture {toggle="true"}
	**Hexagonal Architecture** (also known as **Ports and Adapters**) is a software design pattern introduced by Alistair Cockburn in 2005. Its primary goal is to **decouple the core business logic of an application from external concerns**—such as databases, user interfaces, web frameworks, or third-party APIs—so the system becomes more - **testable, - maintainable, and - flexible**.
	**Core Idea**
	> The application core should not depend on external systems. Instead, external systems should plug into the core through well-defined interfaces.
	The core philosophy is that the application's business logic should be the **heart of the system**, and it shouldn't depend on or even be aware of *how* it is accessed (HTTP, CLI) or *where* its data is stored (MySQL, Redis, an API).
	<columns>
		<column ratio="50">
			**Key Concepts**
			1. **Application Core (Domain + Application Services)**
				- Contains **business rules**, use cases, and domain models
				- Has **no direct dependencies** on frameworks, databases, or external services
				- Communicates with the outside world **only through interfaces (ports)**
			2. **Ports**
				- **Interfaces** defined *inside* the core that declare what the system needs (e.g., `UserRepository`, `EmailService`)
				- Two types:
					- **Primary (Driving) Ports**: How the outside world *interacts with* the core (e.g., REST API, CLI commands)
					- **Secondary (Driven) Ports**: How the core *interacts with* external systems (e.g., database, SMTP server)
			3. **Adapters**
				- Concrete implementations of ports that **translate** between the core and external tech
				- Examples:
					- A **REST controller** (primary adapter) that calls a use case
					- A **Doctrine repository** (secondary adapter) that implements `UserRepository`
					- An **SMTP email adapter** that implements `EmailService`
					<empty-block/>
		</column>
		<column ratio="50">
			**Key Components: Ports and Adapters**
			The magic lies in how the inside communicates with the outside, which is defined by two concepts:
			1. **Ports (The Interfaces):**
				- A **Port** is an abstract interface that defines *how* the application wants to interact with the outside world. It represents a contract.
				- There are two types of ports:
					- **Driving Ports (Primary/Input):** These are how the outside world *drives* the application. They are use cases that the application exposes. Think of a `UserRegistrationService` interface or a `CreateOrderCommandHandler` interface.
					- **Driven Ports (Secondary/Output):** These are how the application *drives* the outside world to get things it needs. Think of a `UserRepository` interface (to save a user) or a `PaymentGateway` interface (to charge a credit card).
			2. **Adapters (The Implementations):**
				- An **Adapter** is a concrete implementation of a port. It's the "glue code" that translates between the application's core and a specific external technology.
				- Similarly, there are two types of adapters:
					- **Driving Adapters (Primary/Input):** These adapters call the driving ports. They are the entry points *into* the hexagon.
						- **Examples:**
							- A **REST Controller** (using Spring MVC or Laravel) that takes an HTTP request, translates it into a `CreateOrderCommand`, and calls the `CreateOrderCommandHandler` port.
							- A **CLI Command** that parses arguments and calls the same `CreateOrderCommandHandler` port.
					- **Driven Adapters (Secondary/Output):** These adapters implement the driven ports. They are called *by* the hexagon to interact with external resources.
						- **Examples:**
							- A **MySQLUserRepository** that implements the `UserRepository` interface. It knows how to map a `User` entity to SQL tables.
							- A **StripePaymentGateway** that implements the `PaymentGateway` interface. It knows how to make HTTP calls to the Stripe API.
		</column>
	</columns>
	<empty-block/>
## CQRS {toggle="true"}
	Command Query Responsibility Segregation - is an *architectural pattern* that separates the *operations* that read data (queries) from those that write or modify data (commands). The core idea is:
	*"Commands change state. Queries return data. Never the two shall mix."*
	It's based on the older **Command Query Separation (CQS)** principle, which states that an object's methods should be either:
	- **Commands:** That perform an action (a mutation) and return no data (`void`).
	- **Queries:** That return data and cause no side effects (they are idempotent).
	CQRS takes this concept and applies it at the <span underline="true">architectural level</span>, not just the object level. Instead of having a single, unified data model for both reading and writing, you split them into two separate models.
	<empty-block/>
	- The Command side is responsible for business logic and updating the state.
	- The Query side is responsible for providing denormalized, read-optimized views of the data.
	<details>
	<summary>Example</summary>
		**Without CQRS**
		```php
// Traditional CRUD service
class OrderService {
    public function placeOrder(OrderRequest $request): Order { /* ... */ }
    public function getOrder(int $id): Order { /* ... */ }
}
		```
		**With CQRS**
		```php
// Command
class PlaceOrderCommand {
    public string $customerId;
    public array $items;
}

// Command Handler
class PlaceOrderHandler {
    public function __invoke(PlaceOrderCommand $command): void {
        // Apply business logic, persist to write model
    }
}

// Query
class GetOrderQuery {
    public int $orderId;
}

// Query Handler
class GetOrderHandler {
    public function __invoke(GetOrderQuery $query): OrderDto {
        // Fetch from optimized read model (e.g., denormalized table or cache)
    }
}
		```
	</details>
	- **CQRS Architecture:** This separation creates a clear distinction:
		<table header-row="true">
		<colgroup>
		<col>
		<col width="499">
		<col width="470">
		</colgroup>
<tr>
<td></td>
<td>**Command Side (Write)**</td>
<td>**Query Side (Read)**</td>
</tr>
<tr>
<td>**Purpose**</td>
<td>Change the state of the system.</td>
<td>Get data from the system.</td>
</tr>
<tr>
<td>**Method Signature**</td>
<td>Returns `void` (or an ID/status).</td>
<td>Returns a Data Transfer Object (DTO).</td>
</tr>
<tr>
<td>**Model**</td>
<td>A rich domain model, full of business logic, invariants, and validation (often using DDD patterns like Aggregates).</td>
<td>A simple, flat, denormalized model optimized for specific views.</td>
</tr>
<tr>
<td>**Data Store**</td>
<td>Often the "source of truth," a normalized relational database.</td>
<td>Can be a completely different store—a read-optimized cache, a NoSQL database, an Elasticsearch index, or a materialized view.**H**</td>
</tr>
		</table>
		Class naming: Command, Query, Handler.
		**Benefits:**
		1. **Scalability:** You can scale the read and write sides independently. Reads are often 10x more frequent than writes.
		2. **Performance:** Read models can be highly denormalized, avoiding complex joins, leading to lightning-fast queries.
		3. **Flexibility:** The query side is completely decoupled. You can create multiple, different read models for different UIs (web, mobile, admin panel) without touching the core business logic.
		4. **Clarity & Simplicity:** The separation of concerns is absolute. Command handlers are focused on business rules, and query handlers are focused on data retrieval. This makes the code easier to understand and maintain.
		**Caveats (It's Not a Silver Bullet):**
		- **Complexity:** This is the biggest cost. You are introducing a more complex architecture. You now have two models, event handling, and eventual consistency to manage.
		- **Eventual Consistency:** The read model is updated *after* the write model. There is a tiny delay. A user might not see their change immediately. Your application must be designed to handle this.
	<columns>
		<column ratio="50">
			<details>
			<summary>**Query Flow**</summary>
				1. **The Query Request:**
					- It all starts when a client (like a web browser or a mobile app) needs data. Instead of a general-purpose `getData()` call, a specific **Query Object** is created and dispatched. This object is a simple Data Transfer Object (DTO) that contains all the parameters needed for the read.
					- **Example:** A `GetDashboardStatsQuery` containing a `userId` and a `dateRange`. Or a `FindProductsByCategoryQuery` with a `categoryId` and `sortOrder`.
				2. **The Query Handler:**
					- This query object is received by a dedicated **Query Handler**. This handler is a simple, single-purpose class. Its only job is to satisfy that specific query.
					- Unlike a Command Handler, a Query Handler contains **no business logic**. It doesn't make decisions or change state. It's a pure data retrieval mechanism.
				3. **Accessing the Read Model:**
					- The Query Handler then fetches the data from the **Read Model** (or Query Model). This is the critical part of the flow.
					- The Read Model is a highly denormalized, flat, and read-optimized data schema. It's often structured exactly as the UI needs it, pre-joining and pre-calculating data to avoid complex on-the-fly processing.
					- **Example:** Instead of joining `Users`, `Orders`, and `OrderItems` tables for a dashboard, the Read Model might be a single `user_order_summaries` table with columns like `user_id`, `user_name`, `total_orders`, and `total_revenue`.
				4. **Returning the Result:**
					- The Query Handler packages the data from the Read Model into a **Query Response DTO** and returns it. This DTO is also tailored to the specific view, containing no more and no less than what the client needs.
				### Interview Questions   {toggle="true"}
					<details>
					<summary>What classes participate in CQRS flow?</summary>
						**Command Side:**
						- Command Handlers
						- Domain Model (Entities, Aggregates)
						- Repositories (for writes)
						**Query Side:**
						- Query Handlers
						- Read Models / Projections
						- (Often) a separate Database
					</details>
					<details>
					<summary>How does Event Sourcing combine with CQRS?</summary>
					</details>
				### **Key Characteristics of the Queries Flow**
				To summarize, the Queries Flow is defined by:
				- **Simplicity and Speed:** The path from request to response is as direct as possible. There are no complex domain objects to hydrate, no business rules to execute.
				- **Intention-Revealing:** The names of the Query and its Handler are very specific (e.g., `GetCustomerOrderHistoryQuery`), which makes the code self-documenting and easy to understand.
				- **Scalability:** Because it's separate, the read side can be scaled independently. You can add read replicas of the database, use fast caching layers (like Redis), or even use a completely different type of database (like Elasticsearch for search queries) without affecting the core write-side business logic.
				- **Materialized Views:** In many systems, the Read Model is essentially a set of **materialized views** that are kept updated by the Command side (via Domain Events).
				### **A Concrete Example**
				Let's imagine a "Product Catalog" page in an e-commerce app.
				- **Command Flow (Write):** Would handle `CreateProductCommand`, involving a rich `Product` Aggregate with validation, pricing rules, etc., and persisting it to the normalized "products" table.
				- **Queries Flow (Read):**
					1. **Query:** `GetPaginatedProductCatalogQuery(page=1, pageSize=20, filters={...})`
					2. **Handler:** The `GetPaginatedProductCatalogHandler` receives this query.
					3. **Read Model:** It executes a simple `SELECT` statement against a `product_catalog_view`. This view might already have the product name, image URL, price, average rating, and category name pre-joined and ready to go.
					4. **Response:** It returns a `PaginatedProductListDto` containing exactly the 20 product previews needed for the first page of the UI.
				- \*In essence, the Queries Flow is the 'fast lane' for data retrieval in a CQRS system, deliberately designed to bypass the complexity of the domain model to deliver data as efficiently as possible."
			</details>
			<empty-block/>
		</column>
		<column ratio="50">
			<details>
			<summary>**Command Flow**</summary>
				1. **The Command Request:**
					- It begins when a client intends to *change something*. A **Command Object** is created. This command is an imperative; it's an instruction to perform a specific action.
					- **Key Characteristic:** A command is **named in the past tense**, as it represents an intention that will become a fact (e.g., `PlaceOrderCommand`, `UpdateCustomerAddressCommand`, `CancelShipmentCommand`).
					- The command object contains all the data required to execute the action.
				2. **The Command Handler:**
					- This command is dispatched to a dedicated **Command Handler**. Unlike a Query Handler, the Command Handler is the home for complex business logic.
					- Its job is to orchestrate the entire operation to fulfill the command, ensuring all business rules are followed.
				3. **Loading the Domain Model:**
					- The handler starts by loading the relevant **Aggregate Root** from the database. The aggregate is a cluster of related objects (Entities and Value Objects) that are treated as a single unit for data changes.
					- **Example:** For a `CancelOrderCommand`, the handler would load the `Order` aggregate, which includes the `Order` itself and its `OrderLineItems`.
				4. **Executing Business Logic:**
					- This is the core of the Commands Flow. The handler calls a method on the Aggregate Root, passing the data from the command.
					- The Aggregate then executes the business logic. It checks **invariants** (rules that must always be true).
					- **Example:** The `Order.cancel()` method would check invariants like:
						- "Is the order already shipped?" (If yes, throw a `CannotCancelShippedOrderException`).
						- "Is the current user authorized to cancel this order?"
						- "If canceled, should we restock the inventory?"
				5. **Persistence and Publishing Events:**
					- If all business rules are satisfied, the state of the Aggregate is persisted to the **Write Database** (the "source of truth"). This is often a normalized relational database.
					- Crucially, as a result of the state change, the Aggregate often generates one or more **Domain Events** (e.g., `OrderCancelledEvent`). These events are published to notify the rest of the system about what *has already happened*.
				6. **Side Effects (Updating the Read Model):**
					- This is the critical link between the Command and Query sides. The published Domain Event (like `OrderCancelledEvent`) is picked up by **Event Handlers** (or Projectors).
					- These handlers are responsible for updating the **Read Model**. For instance, an event handler would update the `order_summaries` read table, setting the `status` to 'cancelled'.
					- **This is why the read side is eventually consistent.** There is a slight delay between the command completing and the read model being updated.
				### **Key Characteristics of the Commands Flow**
				To summarize, the Commands Flow is defined by:
				- **Business Logic Centralization:** This is where all the critical rules and decisions of your domain live.
				- **Transaction Boundary:** The Aggregate acts as a consistency boundary. Everything within a single Aggregate is updated transactionally.
				- **Validation and Invariants:** It's focused on ensuring the system moves from one valid state to another.
				- **Imperative Nature:** It tells the system to "do something."
				- **Returns Minimal Data:** A command handler typically returns nothing (`void`), or at most a simple success status or the ID of the created entity. It does *not* return complex data; that's the job of a subsequent query.
				### **A Concrete Example: Placing an Order**
				Let's contrast it with the previous query example:
				- **Command: ****`PlaceOrderCommand({ userId: 123, items: [...] })`**
					1. **Handler:** `PlaceOrderHandler` receives the command.
					2. **Load:** It loads the `User` aggregate and the `Product` aggregates for each item (to check price and availability).
					3. **Logic:** It creates a new `Order` aggregate. The `Order` constructor and methods enforce rules: "Are all items in stock?", "Does the total meet the minimum order value?", "Is the user's payment method valid?"
					4. **Persistence & Event:** The new `Order` is saved to the "orders" table. An `OrderPlacedEvent` is published.
					5. **Side Effect:** An event handler listens for `OrderPlacedEvent` and updates the `user_order_summaries` read model. Another handler might trigger a payment process.
				**In essence, the Commands Flow is the protective, logic-heavy process that guards your system's state, while the Queries Flow is the optimized, simple process for presenting that state.** Understanding the distinct responsibilities of each flow is key to implementing CQRS effectively."
			</details>
			<empty-block/>
		</column>
	</columns>
	### Interview questions {toggle="true"}
		<details>
		<summary>What’s the difference between saynchroneous\\asyncroneous, event\\listener architecture, and immediate\\enventually consistent? And tell me what is related to Commands and what is related to Queries? </summary>
			## **The Three Independent Parameters**
			<table header-row="true">
<tr>
<td>**Parameter**</td>
<td>**Options**</td>
<td>**What it actually means**</td>
</tr>
<tr>
<td>**1. Execution model**</td>
<td>Synchronous / Asynchronous</td>
<td>Does the caller wait for completion?</td>
</tr>
<tr>
<td>**2. Architecture**</td>
<td>Direct call / Event-driven (listeners)</td>
<td>How components communicate</td>
</tr>
<tr>
<td>**3. Consistency model**</td>
<td>Immediate / Eventual</td>
<td>When do readers see the change?</td>
</tr>
			</table>
			---
			## **They're independent - here's proof**
			### **Example A: Command with synchronous execution + events + eventual consistency**
			csharp
			```plain text
// Caller waits, but framework still raises events
var result = await commandBus.SendAsync(new UpdateProfileCommand());

// Internally:
// 1. Update primary database (synchronous)
// 2. Raise ProfileUpdatedEvent (synchronous dispatch to handlers)
// 3. Event handler updates read model... eventually (async background)
// 4. Caller gets response immediately after step 1
			```
			### **Example B: Command with asynchronous execution + no events + immediate consistency**
			csharp
			```plain text
// Fire and forget, but still strongly consistent
commandBus.Send(new UpdateInventoryCommand()); // no await

// Internally (background thread):
// - Update database with locks/transactions
// - Any subsequent query immediately sees changes
// - No event system involved
			```
			---
			## **The common patterns (not rules)**
			<table header-row="true">
<tr>
<td>**Pattern**</td>
<td>**Execution**</td>
<td>**Events**</td>
<td>**Consistency**</td>
<td>**Typical use case**</td>
</tr>
<tr>
<td>**Classic CQRS**</td>
<td>Async command</td>
<td>Yes</td>
<td>Eventual</td>
<td>High-scale distributed system</td>
</tr>
<tr>
<td>**Simple CQRS**</td>
<td>Sync command</td>
<td>No</td>
<td>Immediate</td>
<td>Single service, separate read/write models</td>
</tr>
<tr>
<td>**Event Sourcing CQRS**</td>
<td>Async command</td>
<td>Yes (always)</td>
<td>Eventual</td>
<td>Audit trail, complex business logic</td>
</tr>
<tr>
<td>**Query side only**</td>
<td>Sync query</td>
<td>No</td>
<td>Immediate</td>
<td>Reporting, simple reads</td>
</tr>
			</table>
			---
			## **The critical insight**
			> **CQRS only mandates separate models for reads and writes.**
				The other three parameters are *architectural choices*, not requirements.
			You can mix them freely:
			csharp
			```plain text
// Valid combinations:
✅ Async command + events + eventual
✅ Sync command + events + eventual  // (less common but valid)
✅ Async command + no events + immediate
✅ Sync command + no events + immediate  // (just simple CQRS)
			```
			---
			## **Real-world guidance**
			- **Start simple**: Sync commands, no events, immediate consistency
			- **Add async only when** you need non-blocking I/O or background processing
			- **Add events only when** multiple components need to react
			- **Accept eventual consistency only when** you truly need the scaling/availability benefits
			The confusion arises because *event sourcing* + *messaging* + *eventual consistency* is the most hyped CQRS variant, not CQRS itself.
		</details>
## Event Sourcing {toggle="true"}
	Event Sourcing is a software ***architecture pattern*** where the state of an application is determined by a *sequence of events*, which are stored as the single source of truth. <br>Instead of storing just the *current state* (e.g., "User's balance is \$100"), you store the entire *history of actions* that led to that state (e.g., "Account Created", "Deposited \$50", "Deposited \$50", "Withdrew \$10").
	### **Key Components**
	- **Event:** An <span underline="true">immutable</span> record of a fact that occurred in the system. They are named in the past tense (e.g., `UserRegistered`, `OrderShipped`, `PaymentFailed`). They contain the data relevant to that fact.
		-
	- **Event Store:** Append-only database where events are persisted. It's an append-only log, meaning events can only be added, never modified or deleted.
	<details>
	<summary>**Aggregate / Entities:** The logical units of data (e.g., a `BankAccount`, an `Order`). </summary>
		**Aggregate** is responsible for:
		- **Command Handling:** It receives commands (e.g., "Deposit \$50") and decides if they are valid.
		- **Event Production:** If the command is valid, it produces one or more events (e.g., `DepositCompleted`).
		- **State Rehydration:** It can rebuild its current internal state by sequentially applying all the past events related to itself.
	</details>
	<details>
	<summary>**State Reconstruction:**  To retrieve the current state of an Aggregate, the application **replays** all the events related to that Aggregate in the order they occurred. This process rebuilds the state from its entire history.</summary>
		Since the event log is not optimized for querying (e.g., "show me all users in California"), you create "projections." These are read-optimized views of the data that are built by processing the event stream. This is the core of the **CQRS (Command Query Responsibility Segregation)** pattern, which often accompanies Event Sourcing.
	</details>
	### Characteristics {toggle="true"}
		- **Append-Only:** The event store is written to only by appending new events.
		- **Immutable History:** The complete history of changes is permanently preserved.
		- **Audit Trail:** The event log inherently provides a full audit trail, as every state change is recorded as a fact.
		- **Temporal Querying:** You can reconstruct the state of the system at any point in the past by replaying events up to that point.
		- **Separation of Write and Read Models (CQRS):** Event Sourcing is often paired with CQRS, where the event stream serves as the write model, and optimized, denormalized **read models** (projections) are built from the events to support efficient querying.
	### ** Other Components**
	- **Rehydration** is the process of reconstructing the current state of an Aggregate by sequentially applying all of its historical events from the event store.
	- **Snapshot** or **Aggregate Snapshot**
	-
	### **Databases To Store Events** {toggle="true"}
		- **Specialized Event Store Databases: **These are built specifically for Event Sourcing.
			- **EventStoreDB(KurrentDB):** The most prominent example. It is a database designed with the Event Sourcing pattern at its core, featuring streams per aggregate, persistent subscriptions, and a native projection engine.
		- **General-Purpose Databases (used as Event Stores): **Many systems successfully use conventional databases, often with specific schemas to model the event stream.
			- **Relational Databases (PostgreSQL, SQL Server, MySQL):** A table with columns for `AggregateId`, `Version`, `EventType`, and `EventData` (often JSON) is a very common and robust approach. PostgreSQL, with its excellent JSON support, is a particularly popular choice.
			- **NoSQL Databases:**
				- **Document Stores (MongoDB, CouchDB):** Can store an entire event stream (the sequence of events for one aggregate) as a single document. This is efficient for reading but can have document size limits.
				- **Column Stores (Apache Cassandra, ScyllaDB):** Excellent for write scalability and can efficiently read events by Aggregate ID.
		<empty-block/>
	### Interview questions {toggle="true"}
		What is Event Sourcing and how does it differ from the traditional approach with state storage?
		<details>
		<summary>What are the advantages and disadvantages of Event Sourcing?</summary>
			**Advantages:**
			- **Full history:** Every state change is stored, providing a full history.
			- **Temporal Queries:** Can query the state of the system at any point in time.
			- **Flexibility:** Easily create new read models (projections) for different query needs.
			- **Event-Driven Architecture:** Naturally fits with and enables event-driven systems.
			**Disadvantages:**
			- **Complexity:** Significant learning curve and architectural complexity.
			- **Event Schema Evolution:** Changing event structures over time can be challenging.
			- **Performance Overhead:** Rebuilding state by replaying events can be slow for large streams.
			- **Eventual Consistency:** The system is often eventually consistent, which can be hard to manage.
		</details>
		<details>
		<summary>Explain the difference between Domain Events and Integration Events.</summary>
			**Domain Events:**
			- Occur within a single **bounded context**
			- Represent something that happened in the **domain**
			- Internal implementation detail
			- Typically in-memory, synchronous
			**Integration Events:**
			- Communicate between **different bounded contexts/microservices**
			- Represent something that happened in the **system**
			- Public contract between services
			- Typically asynchronous, via message bus
		</details>
		<details>
		<summary>What is an Event Store and what requirements are placed on it?</summary>
			**Event Store**: A database optimized for storing events as an immutable, append-only log.
			**Key Requirements**:
			1. **Immutable & Append-Only** - Events cannot be modified or deleted once stored
			2. **Strong Ordering** - Maintains global sequence of events
			3. **Event Sourcing Support** - Stores complete state change history
			4. **Fast Reads** - Efficiently retrieve events by stream
			5. **Optimistic Concurrency** - Prevent conflicts with version checks
			6. **Subscription Model** - Real-time notifications for new events
			**Examples**: EventStoreDB, Axon Server, specialized databases rather than traditional RDBMS.
		</details>
		<details>
		<summary>How to properly structure a domain event in PHP? What data should it contain?</summary>
			A Domain Event should be a simple, immutable Data Transfer Object (DTO) that represents a fact about something that just happened in the domain.
			**Essential Components:**
			1. **Event ID:** A unique identifier for this specific event occurrence.
			2. **Aggregate ID:** The identifier of the aggregate root that raised the event.
			3. **Event Type:** A name that describes what happened.
			4. **Timestamp:** When the event occurred.
			5. **Event Data (Payload):** The relevant state of the aggregate at the time of the event.
			6. **Metadata (Optional but recommended):** Contextual information like user ID, correlation ID, etc.
		</details>
		<details>
		<summary>How to design a database schema for an Event Store?</summary>
			### **Core Tables**
			### **1. The ****`events`**** Table (The Main Ledger)**
			This is the most important table. It stores the immutable events themselves.
			sql
			```plain text
CREATE TABLE events (
-- Unique identifier for this specific event instance
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

-- The stream this event belongs to (e.g., "Order-1234")
    stream_id VARCHAR(255) NOT NULL,

-- The version of the stream AFTER this event is applied-- This must be unique within a stream for optimistic concurrency.
    stream_version INTEGER NOT NULL,

-- The type of the event (e.g., "OrderCreated", "ItemAdded")
    event_type VARCHAR(255) NOT NULL,

-- The event data, typically stored as JSON/JSONB
    event_data JSONB NOT NULL,

-- When this event was committed to the store
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

-- Optional metadata (correlationId, causationId, user info)
    metadata JSONB,

-- Ensures event order and uniqueness within a streamUNIQUE (stream_id, stream_version)
);

-- Index for efficiently reading a stream in orderCREATE INDEX idx_events_stream_id_version ON events (stream_id, stream_version);
-- Index for global subscriptions and projectionsCREATE INDEX idx_events_occurred_at ON events (occurred_at);
-- Index for querying by event type (if needed)CREATE INDEX idx_events_event_type ON events (event_type);
			```
			**Column Explanations:**
			- `event_id`: A global unique identifier for the event. Useful for idempotency and logging.
			- `stream_id`: Identifies the aggregate instance the event belongs to.
			- `stream_version`: The crucial field for **optimistic concurrency control**. It must be incremented sequentially for each event in a stream. The unique constraint `(stream_id, stream_version)` is what prevents concurrent writers from inserting events at the same version.
			- `event_type`: Used by the application to determine which class to deserialize the `event_data` into.
			- `event_data`: The serialized payload of the event. Using `JSONB` (in PostgreSQL) is common as it's flexible and queryable. Alternatives are pure JSON or BLOB.
			- `occurred_at`: The timestamp when the event was stored. This provides the definitive order for global event sequence.
			- `metadata`: A separate JSON field for non-domain data crucial for auditing and diagnostics (e.g., `correlation_id`, `causation_id`, `user_id`).
			---
			### **2. The ****`streams`**** Table (Optional, for Metadata)**
			This table is optional but highly recommended. It caches metadata about each stream (aggregate).
			sql
			```plain text
CREATE TABLE streams (
    stream_id VARCHAR(255) PRIMARY KEY,
-- The current version of the stream. This is a cache of the highest version in the `events` table.
    stream_version INTEGER NOT NULL DEFAULT 0,
-- The type of the aggregate (e.g., "Order", "Customer")
    stream_type VARCHAR(255) NOT NULL,
-- Timestamp of when the stream was created
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()

-- Other aggregate-specific cache can go here, but keep it minimal.);
			```
			**Purpose:**
			- **Performance:** Quickly check the current version of a stream without running a `MAX(stream_version)` query on the potentially large `events` table. This is critical for the concurrency check during an append operation.
			- **Consistency:** Provides a logical lock or a single place to update when appending new events in a transaction.
			- **Discovery:** Allows you to list all existing streams.
			---
			### **How the Append Operation Works**
			Appending a new event to a stream `Order-1234` is done within a transaction:
			1. **Start a transaction.**
			2. **Check Concurrency:**
				- `SELECT stream_version FROM streams WHERE stream_id = 'Order-1234' FOR UPDATE;`
				- The `FOR UPDATE` clause locks the row, preventing other concurrent writes to the same stream.
			3. **Validate:** Ensure the current `stream_version` from the `streams` table matches the expected version your application logic computed. If not, abort the transaction (optimistic concurrency failure).
			4. **Insert the Event:**
				- `INSERT INTO events (stream_id, stream_version, event_type, event_data, ...) VALUES ('Order-1234', 5, 'OrderShipped', '{"shippingId": "fedex-999"}', ...);`
				- The `UNIQUE (stream_id, stream_version)` constraint is the final safeguard against duplicates.
			5. **Update the Stream:**
				- `UPDATE streams SET stream_version = 5 WHERE stream_id = 'Order-1234';`
			6. **Commit the transaction.**
			This two-table design, linked by `stream_id` and protected by a transaction, ensures data consistency and enforces the core rules of Event Sourcing.
			---
			### **Advanced Considerations & Enhancements**
			1. **Snapshots Table:** For aggregates with long event streams, rebuilding state from hundreds of events is slow. You can periodically store a snapshot of the aggregate's state at a specific version.
				sql
				```plain text
CREATE TABLE snapshots (
    stream_id VARCHAR(255) PRIMARY KEY,
-- The version of the stream this snapshot represents
    stream_version INTEGER NOT NULL,
-- The serialized state of the aggregate at this version
    snapshot_data JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
				```
				To rebuild state, you load the latest snapshot and then only replay events that occurred after its version.
			2. **Global Sequence (****`global_version`****):** Add a `BIGSERIAL` or auto-incrementing `global_version` column to the `events` table. This provides a strict, database-generated global order for all events, which is invaluable for **subscriptions and projections** that need to process events across all streams in the exact order they were committed.
			3. **Idempotency & Deduplication:** The `event_id` can be used with a unique constraint to reject duplicate event inserts, ensuring idempotent operations if a client retries a command.
			4. **Archiving/Purging:** While events are immutable, there may be legal requirements to archive or delete data. The schema can be extended with an `is_archived` flag or designed to support partitioning by date for easier data lifecycle management.
		</details>
		<details>
		<summary>What data needs to be stored together with an event (metadata)?</summary>
			### **1. Identity & Core Metadata**
			This data is essential for storing and retrieving the event.
			- **Event ID:** A globally unique identifier for this specific event instance (e.g., a UUID). Critical for idempotency (ensuring the same event isn't processed twice).
			- **Event Type:** The name of the event (e.g., `OrderConfirmed`, `PaymentFailed`). This tells the system how to deserialize the `event_data`.
			- **Stream ID:** The unique identifier of the stream (aggregate) this event belongs to (e.g., `Order-1234`).
			- **Stream Version:** The version of the stream *after* this event is applied. This is the key to optimistic concurrency control.
			### **2. Causation & Correlation Metadata**
			This data is vital for debugging, tracing, and understanding the flow of commands and events through a distributed system.
			- **Correlation ID:** A unique identifier that is passed along through every command and event that is part of the same business operation or user request. It allows you to group all events related to a single initial action.
			- **Causation ID:** The ID of the command or event that *directly caused* this event to be generated. This allows you to trace the cause-and-effect chain. (e.g., A `PaymentReceived` event was caused by a `ProcessPayment` command).
			### **3. Temporal Metadata**
			Information about when things happened.
			- **Recorded At / Logged At:** The timestamp when the event was *persisted to the event store*. This is the definitive, system-generated order of events.
			- **Occurred At:** The timestamp when the event *actually happened in the business domain*. This may be slightly earlier than the `recorded_at` time and is provided by the application.
			### **4. Source & Actor Metadata**
			Information about who or what was responsible for the event.
			- **User ID:** The identifier of the user who initiated the action that led to this event.
			- **Service/Application ID:** The name or identifier of the service that produced the event (e.g., `BillingService-v1.2`).
			- **Machine/IP Address:** The source of the event (useful for low-level debugging).
			### **5. Schema & Structural Metadata**
			Information needed to correctly interpret the event data.
			- **Schema Version:** The version of the event's schema (e.g., `v2`). This is crucial for managing event schema evolution over time, allowing the system to upcast old events to new versions.
			---
			### **Example in a Database Schema**
			Putting it all together, an `events` table might look like this:
			sql
			```plain text
CREATE TABLE events (
-- Core Event Data
    event_id UUID PRIMARY KEY,
    event_type VARCHAR(255) NOT NULL,
    event_data JSONB NOT NULL,-- The core business facts-- Stream Information
    stream_id VARCHAR(255) NOT NULL,
    stream_version INTEGER NOT NULL,

-- Temporal Metadata
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    occurred_at TIMESTAMPTZ NOT NULL,

-- Causation & Correlation Metadata
    correlation_id UUID NOT NULL,
    causation_id UUID NOT NULL,

-- Source & Actor Metadata
    user_id VARCHAR(100),
    service_id VARCHAR(100),

-- Schema Metadata
    schema_version VARCHAR(10) NOT NULL DEFAULT 'v1',

-- Constraint for concurrencyUNIQUE (stream_id, stream_version)
);
			```
			### **Summary: Why is this Metadata So Important?**
			- **Debugging & Tracing:** With `correlation_id` and `causation_id`, you can reconstruct the entire story of a user request across services.
			- **Audit & Compliance:** You have a complete, immutable record of who did what, when, and why (`user_id`, `occurred_at`, causal chain).
			- **Operational Robustness:** `event_id` enables idempotent processing, and `schema_version` allows for safe evolution of your system.
			- **Performance & Analysis:** Metadata allows for efficient indexing and querying (e.g., finding all events for a user, or all events related to a specific business process).
		</details>
		<details>
		<summary>What are projections and what are they needed for?</summary>
			Think of them as **materialized views** of your event stream. They:
			- **Listen** to events from the event store
			- **Transform** and **aggregate** those events
			- **Build** specialized read models for different use cases
		</details>
		<details>
		<summary>How to implement an Event Bus for publishing events?</summary>
			**In-Memory Event Bus**
			**Simple implementation:**
			- Observer pattern with subscriber registry
			- Events published to interested subscribers
			- Synchronous processing within same process
			**Other Event Bus Options:**
			### **Message Brokers**
			- **RabbitMQ** - Advanced routing, queues, persistence
			- **Apache Kafka** - High throughput, event streaming, replay
			- **AWS SNS/SQS** - Cloud pub/sub with queuing
			- **Azure Service Bus** - Enterprise messaging
			- **Google Pub/Sub** - Cloud-native scaling
			### **Database-Based**
			- **Outbox Pattern** - Events stored in DB table, polled by subscribers
			- **Change Data Capture** - Database logs as event source
			- **Transactional outbox** - Events written atomically with business data
			### **Specialized Event Stores**
			- **EventStoreDB** - Built-in subscriptions and projections
			- **Axon Server** - Event bus + store combined
			### **Service Mesh**
			- **Istio** - Service-to-service event routing
			- **Linkerd** - Transparent service communication
			## **Key Considerations:**
			- **Delivery guarantees** (at-least-once, at-most-once, exactly-once)
			- **Ordering** (per aggregate vs global)
			- **Persistence** (in-memory vs durable)
			- **Scalability** (single node vs distributed)
			- **Error handling** (retries, dead letter queues)
			**Choose based on:** scale requirements, delivery guarantees, infrastructure constraints, and operational complexity.
		</details>
		<details>
		<summary>Explain the difference between Domain Events and Integration Events.</summary>
			A **Domain Event** is a notification of something that happened *within a single business domain or bounded context*. It represents a past-tense fact that is significant to domain experts.
			An **Integration Event** is a notification of a fact that is relevant *to other external systems, services, or bounded contexts*. It is used to propagate state changes and achieve eventual consistency across the system.
		</details>
## <span color="red">Distributed System Patterns</span>
<details>
<summary>distributed system patterns <br>[https://martinfowler.com/articles/patterns-of-distributed-systems/](https://martinfowler.com/articles/patterns-of-distributed-systems/)</summary>
	## **1. Communication Patterns**
	Patterns that define how services discover each other and exchange data.
	- **Client-Server**
		A foundational model where a client sends a request to a server, which processes it and returns a response. It separates the roles of requester and provider.
	- **Publish-Subscribe**
		Publishers send messages to topics without knowing subscribers; subscribers express interest in topics and receive relevant messages. This decouples event producers from consumers.
	- **Message Channel**
		A logical pipe that connects applications for message passing. It provides a reliable pathway for data transfer between components.
	- **Message Router**
		Consumes a message from one channel and republishes it to another based on conditions, decoupling message sources from destinations.
	- **Message Translator**
		Converts data formats between systems to resolve incompatibilities, enabling heterogeneous applications to communicate.
	- **Service Discovery**
		Dynamically finds the network location of a service without hard‑coded addresses, essential in dynamic cloud environments.
	- **API Gateway**
		A single entry point for external clients that routes requests to appropriate internal services, handles authentication, and may perform protocol translation.
	- **Request-Reply**
		A synchronous communication pattern where a requester sends a message and expects a response from the receiver, often used in REST or RPC.
	---
	## **2. Resilience Patterns**
	Patterns that ensure a system can withstand and recover from failures.
	- **Circuit Breaker**
		Monitors for failures when calling a remote service; after a threshold, it trips and subsequent calls fail fast or use a fallback, preventing cascading failures.
	- **Bulkhead**
		Isolates system components into separate pools (like ship compartments) so failure in one does not bring down the whole system.
	- **Transaction Log Tailing**
		Reads changes from a database’s commit log to publish messages reliably; a core implementation technique for the Transactional Outbox pattern.
	- **Leader Election**
		Ensures that among a group of nodes, one is chosen as leader to coordinate tasks; if the leader fails, another is elected.
	- **Heartbeat / Failure Detector**
		Nodes send periodic signals (heartbeats) to indicate they are alive; missing heartbeats trigger failure detection and recovery actions.
	- **Generation Clock**
		A monotonic number used to distinguish current leadership from stale leadership, preventing split‑brain scenarios.
	- **Retry with Exponential Backoff**
		Automatically retries a failed operation with increasing delays between attempts, reducing load on recovering services.
	- **Dead Letter Queue**
		A holding area for messages that cannot be processed successfully, allowing later inspection and reprocessing without losing data.
	---
	## **3. Data Management Patterns**
	Patterns that address storing, accessing, and maintaining consistency across distributed data.
	- **Saga**
		Manages a distributed transaction as a sequence of local transactions, each with a compensating action to undo changes if a step fails.
	- **Command Query Responsibility Segregation (CQRS)**
		Separates write (command) and read (query) models, allowing each to be optimized and scaled independently.
	- **Event Sourcing**
		Stores all changes to an application state as a sequence of immutable events; the current state can be rebuilt by replaying events.
	- **Sharding / Partitioning**
		Distributes data across multiple databases (shards) based on a shard key to achieve horizontal scaling.
	- **Completeness Guarantee**
		Ensures that a consumer receives a defined set of events from a producer, sufficient to rebuild the producer’s state correctly.
	- **Decision Tracking**
		Records business decisions (e.g., “Order Approved”) as events along with the data that influenced them, enabling auditability and replay.
	- **Two-Phase Commit (2PC)**
		A protocol to achieve atomic commitment across multiple nodes: a coordinator asks all participants to prepare, then commits if all agree.
	- **Consensus Algorithm (e.g., Paxos, Raft)**
		Enables a set of nodes to agree on a single value despite failures, forming the basis for replicated state machines.
	- **Versioned Value**
		Stores data with an explicit version number; updates are allowed only if the version matches, enabling optimistic concurrency control.
	- **Write-Ahead Log**
		Records every change to a log before applying it to storage, ensuring durability and enabling recovery after crashes.
	---
	## **4. Deployment Patterns**
	Patterns for packaging, deploying, and managing applications in containerized environments.
	- **Sidecar**
		Deploys a helper container alongside the main application container, sharing its lifecycle and providing supporting features (logging, monitoring) without modifying the main code.
	- **Ambassador**
		A specialized sidecar that proxies network connections to/from the main container, handling concerns like service discovery, retries, and circuit breaking.
	- **Adapter**
		A sidecar that presents a standardized interface to the outside world, normalizing outputs (e.g., logs, metrics) from the main container into a format expected by external systems.
	- **Replicated Service**
		Runs multiple identical instances of a stateless service behind a load balancer to achieve scalability and high availability.
	- **Init Container**
		Runs a separate container to perform setup tasks (e.g., database migrations, permission changes) before the main application container starts.
	- **Operator**
		A custom Kubernetes controller that encodes human operational knowledge into software to automate management of complex applications.
	---
	## **5. Processing Patterns**
	Patterns for handling large-scale, parallel, or time-based computational tasks.
	- **Scatter/Gather**
		A root node fans out a request to many leaf nodes, each processes its subset of data, and the root gathers and aggregates the results.
	- **Work Queue**
		Distributes tasks among multiple worker processes; tasks are placed in a queue, and workers pull tasks when ready, enabling parallel processing.
	- **Event-Driven Batch Processing**
		Triggers batch jobs in response to events rather than fixed schedules, allowing near‑real‑time reaction to data changes.
	- **Passage of Time Event**
		A central scheduler emits generic time‑based events (e.g., `DayPassed`) that interested services listen to, decoupling them from scheduling logic.
	- **MapReduce**
		A programming model for processing large datasets: a *map* step processes key‑value pairs to generate intermediate results, and a *reduce* step aggregates those results.
	- **Stream Processing**
		Processes unbounded data streams in real time, often using operators like windowing, filtering, and aggregation.
	- **Batch Aggregation**
		Periodically collects and processes data in bulk, commonly used for reporting or analytics where latency is less critical.
</details>
<details>
<summary>Here is an exhaustive list of distributed systems patterns, reorganized with clear, single-concept categories. Each pattern includes a concise description for easy understanding.</summary>
	## **1. Communication Patterns**
	Patterns that define how services discover each other and exchange data.
	- **Client-Server**
		A foundational model where a client sends a request to a server, which processes it and returns a response. It separates the roles of requester and provider.
	- **Publish-Subscribe**
		Publishers send messages to topics without knowing subscribers; subscribers express interest in topics and receive relevant messages. This decouples event producers from consumers.
	- **Message Channel**
		A logical pipe that connects applications for message passing. It provides a reliable pathway for data transfer between components.
	- **Message Router**
		Consumes a message from one channel and republishes it to another based on conditions, decoupling message sources from destinations.
	- **Message Translator**
		Converts data formats between systems to resolve incompatibilities, enabling heterogeneous applications to communicate.
	- **Service Discovery**
		Dynamically finds the network location of a service without hard‑coded addresses, essential in dynamic cloud environments.
	- **API Gateway**
		A single entry point for external clients that routes requests to appropriate internal services, handles authentication, and may perform protocol translation.
	- **Request-Reply**
		A synchronous communication pattern where a requester sends a message and expects a response from the receiver, often used in REST or RPC.
	---
	## **2. Resilience Patterns**
	Patterns that ensure a system can withstand and recover from failures.
	- **Circuit Breaker**
		Monitors for failures when calling a remote service; after a threshold, it trips and subsequent calls fail fast or use a fallback, preventing cascading failures.
	- **Bulkhead**
		Isolates system components into separate pools (like ship compartments) so failure in one does not bring down the whole system.
	- **Transaction Log Tailing**
		Reads changes from a database’s commit log to publish messages reliably; a core implementation technique for the Transactional Outbox pattern.
	- **Leader Election**
		Ensures that among a group of nodes, one is chosen as leader to coordinate tasks; if the leader fails, another is elected.
	- **Heartbeat / Failure Detector**
		Nodes send periodic signals (heartbeats) to indicate they are alive; missing heartbeats trigger failure detection and recovery actions.
	- **Generation Clock**
		A monotonic number used to distinguish current leadership from stale leadership, preventing split‑brain scenarios.
	- **Retry with Exponential Backoff**
		Automatically retries a failed operation with increasing delays between attempts, reducing load on recovering services.
	- **Dead Letter Queue**
		A holding area for messages that cannot be processed successfully, allowing later inspection and reprocessing without losing data.
	---
	## **3. Data Management Patterns**
	Patterns that address storing, accessing, and maintaining consistency across distributed data.
	- **Saga**
		Manages a distributed transaction as a sequence of local transactions, each with a compensating action to undo changes if a step fails.
	- **Command Query Responsibility Segregation (CQRS)**
		Separates write (command) and read (query) models, allowing each to be optimized and scaled independently.
	- **Event Sourcing**
		Stores all changes to an application state as a sequence of immutable events; the current state can be rebuilt by replaying events.
	- **Sharding / Partitioning**
		Distributes data across multiple databases (shards) based on a shard key to achieve horizontal scaling.
	- **Completeness Guarantee**
		Ensures that a consumer receives a defined set of events from a producer, sufficient to rebuild the producer’s state correctly.
	- **Decision Tracking**
		Records business decisions (e.g., “Order Approved”) as events along with the data that influenced them, enabling auditability and replay.
	- **Two-Phase Commit (2PC)**
		A protocol to achieve atomic commitment across multiple nodes: a coordinator asks all participants to prepare, then commits if all agree.
	- **Consensus Algorithm (e.g., Paxos, Raft)**
		Enables a set of nodes to agree on a single value despite failures, forming the basis for replicated state machines.
	- **Versioned Value**
		Stores data with an explicit version number; updates are allowed only if the version matches, enabling optimistic concurrency control.
	- **Write-Ahead Log**
		Records every change to a log before applying it to storage, ensuring durability and enabling recovery after crashes.
	---
	## **4. Deployment Patterns**
	Patterns for packaging, deploying, and managing applications in containerized environments.
	- **Sidecar**
		Deploys a helper container alongside the main application container, sharing its lifecycle and providing supporting features (logging, monitoring) without modifying the main code.
	- **Ambassador**
		A specialized sidecar that proxies network connections to/from the main container, handling concerns like service discovery, retries, and circuit breaking.
	- **Adapter**
		A sidecar that presents a standardized interface to the outside world, normalizing outputs (e.g., logs, metrics) from the main container into a format expected by external systems.
	- **Replicated Service**
		Runs multiple identical instances of a stateless service behind a load balancer to achieve scalability and high availability.
	- **Init Container**
		Runs a separate container to perform setup tasks (e.g., database migrations, permission changes) before the main application container starts.
	- **Operator**
		A custom Kubernetes controller that encodes human operational knowledge into software to automate management of complex applications.
	---
	## **5. Processing Patterns**
	Patterns for handling large-scale, parallel, or time-based computational tasks.
	- **Scatter/Gather**
		A root node fans out a request to many leaf nodes, each processes its subset of data, and the root gathers and aggregates the results.
	- **Work Queue**
		Distributes tasks among multiple worker processes; tasks are placed in a queue, and workers pull tasks when ready, enabling parallel processing.
	- **Event-Driven Batch Processing**
		Triggers batch jobs in response to events rather than fixed schedules, allowing near‑real‑time reaction to data changes.
	- **Passage of Time Event**
		A central scheduler emits generic time‑based events (e.g., `DayPassed`) that interested services listen to, decoupling them from scheduling logic.
	- **MapReduce**
		A programming model for processing large datasets: a *map* step processes key‑value pairs to generate intermediate results, and a *reduce* step aggregates those results.
	- **Stream Processing**
		Processes unbounded data streams in real time, often using operators like windowing, filtering, and aggregation.
	- **Batch Aggregation**
		Periodically collects and processes data in bulk, commonly used for reporting or analytics where latency is less critical.
</details>
#### **Dual Write Problem** 
<details>
<summary>occurs whenever an application performs write operations on **two different systems** (e.g., a database and a message queue, or a database and a cache) as part of a single transaction, and one of those writes fails.</summary>
	### **1. The Classic Anatomy of the Problem**
	Imagine an e-commerce application. When an order is placed, you must:
	1. Write the `Order` record to the **PostgreSQL database**.
	2. Publish an `OrderCreated` event to **Kafka** so that the shipping and billing services can react.
	In your code, this looks like:
	python
	```plain text
db.save(order)           # Write 1
kafka.publish(event)     # Write 2
	```
	**The failure scenarios:**
	- **Scenario A:** The database save succeeds, but Kafka is down. The publish fails. The order exists in the DB, but shipping never gets notified. The customer waits forever for a shipment.
	- **Scenario B:** The database save takes too long and times out, so your code rolls back the DB write. But unbeknownst to you, the DB *actually committed* before the timeout, and your code goes on to publish the Kafka event. Now shipping starts, but the order isn't in the DB, leading to a catastrophic orphaned workflow.
	---
	### **2. Where the Dual Write Problem Manifests**
	While the DB + Queue is the textbook example, this issue appears in several modern architectural patterns:
	- **Database + Cache (Write-Aside):** Updating the DB and invalidating/updating Redis.
	- **Database + Search Index:** Writing to PostgreSQL and syncing to Elasticsearch.
	- **Microservices (Synchronous REST):** Service A updates its DB, then calls Service B via HTTP to update its DB.
	- **File Storage + Metadata DB:** Uploading a file to S3 and saving the file metadata in a relational DB.
	### **3. The Illusion of "Try-Catch" (Why it fails)**
	The naive solution is to use a try-catch block:
	```python
try:
    db.save(order)
    kafka.publish(event)
except Exception:
    db.rollback()
    kafka.rollback() # Doesn't exist!
	```
	**Why this fails:** Most message queues and caches do **not** support distributed transactions (XA transactions) because they are not ACID-compliant databases. Even if they did, coordinating a 2-Phase-Commit (2PC) across a database and a queue introduces massive latency, complexity, and blocking issues, which is why modern systems reject this approach.
	<empty-block/>
	<empty-block/>
</details>
<details>
<summary>Solutions:</summary>
	### **The Standard Solutions**
	Since atomicity across heterogenous systems is impossible, we must achieve **eventual consistency** through architectural patterns. Here are the 4 canonical solutions, ranked from simplest to most robust.
	#### **Solution A: The Transactional Outbox Pattern (The Gold Standard)**
	This is the most widely accepted solution in microservices. Instead of writing to the external system directly, you write the event to an **Outbox table** within your primary ACID database, as part of the same local transaction.
	python
	```plain text
db.begin_transaction()
db.save(order)                # 1. Save the business data
db.save(outbox_event)         # 2. Save the event in the same DB
db.commit_transaction()       # 3. Atomic commit!
	```
	Now, a separate asynchronous **Message Relay** (e.g., Debezium CDC, or a scheduled poller) reads from the Outbox table and publishes the event to Kafka.
	- **If the relay fails**, it just retries.
	- **If Kafka is down**, the relay retries indefinitely.
	- Because the outbox is part of the DB, you only have one write to manage.
	#### **Solution B: The Two-Phase Commit (2PC) / XA Transactions**
	This uses a distributed transaction coordinator to synchronize the DB and the message broker.
	**Pros:** Strong atomicity (all-or-nothing).
	**Cons:** Blocks resources, severely impacts performance, reduces availability (if the coordinator dies, the system locks up), and is famously difficult to debug. Most modern engineers actively avoid this.
	#### **Solution C: The "First Write Wins" / Idempotent Consumer (The "Best Effort" approach)**
	You accept that the external write might fail. You always write to your primary database first. If the second write (to Kafka/Redis) fails, you log the error and implement a **Retry with Exponential Backoff**.
	**Crucial requirement:** The downstream consumer must be **idempotent**. If you retry the Kafka message 3 times, the shipping service must process it exactly once (using a unique `orderId` to deduplicate). This guarantees that even if the second write fails and retries, no duplicate harm is done.
	#### **Solution D: The Saga Pattern (For Microservices)**
	If the "external system" is another microservice's database (via REST/gRPC), you use a **Choreographed Saga**.
	- Service A updates its DB and emits an event.
	- Service B listens, updates its DB, and emits a completion/failure event.
	- If Service B fails, Service A listens to the failure event and executes a **compensating transaction** (e.g., cancels the order).
		This completely avoids a single point of coordination, pushing the dual-write problem into asynchronous event streams.
	---
	### **5. The "Read-Your-Writes" Twist (Cache Invalidation)**
	The Dual Write Problem becomes particularly nasty when dealing with a **Database + Cache**, because of the "Read-Your-Writes" consistency requirement.
	If you write to the DB and then update the cache, and the cache update fails, a subsequent read (within the same user session) might read stale data from the cache.
	**The fix here is the "Cache-Aside with Delete":** Instead of *updating* the cache on a write, you *delete* the cache entry. Then, the next read triggers a cache miss and reloads the fresh data from the DB. If the cache deletion fails, you retry it. You have not corrupted the cache; you've just left a slightly stale entry that will expire naturally via TTL.
	---
	### **6. The Hidden Pitfalls (What most blogs don't tell you)**
	- **Ordering issues:** If you use the Outbox pattern and your relay publishes messages asynchronously, messages might arrive out of order. You must encode the event version or timestamp in the payload and use **idempotency keys** on the consumer side to handle late-arriving older events.
	- **The "Outbox Relay" single point of failure:** If your CDC (Change Data Capture) pipeline goes down, your downstream systems fall behind. You must monitor the Outbox table's size aggressively.
	- **Cross-rollback complexity:** If you successfully write to System A, successfully write to System B, but your business logic *after* these writes throws an exception, you cannot roll back System B. You must design your system so that downstream writes are fire-and-forget, or wrap the entire process in a Saga with compensating actions.
	---
	### **Summary: Which solution should you choose?**
	<table header-row="true">
<tr>
<td>**Scenario**</td>
<td>**Recommended Solution**</td>
</tr>
<tr>
<td>**DB + Kafka/RabbitMQ**</td>
<td>**Transactional Outbox** (with Debezium). Do not write to the queue in the request thread.</td>
</tr>
<tr>
<td>**DB + Redis Cache**</td>
<td>**Cache-Aside with Delete**. Update DB first, then delete the cache (retry on failure).</td>
</tr>
<tr>
<td>**Microservice A + Microservice B**</td>
<td>**Choreographed Saga**. Use events to trigger B, and implement compensating transactions.</td>
</tr>
<tr>
<td>**Strict ACID is non-negotiable**</td>
<td>Use **XA/2PC**, but be prepared to sacrifice performance, and keep the transaction scope *extremely* short.</td>
</tr>
	</table>
	Ultimately, solving the Dual Write Problem forces you to accept **eventual consistency**. The goal is not to prevent the dual write from happening, but to architect the system so that if the second write fails, the system automatically reconciles itself without manual intervention.
</details>
## <span color="red">Microservices\\Distributed Architecture</span>
### **Microservices communication**
**Synchronous Communication **(Direct, Request-Response)
<details>
<summary>**HTTP/REST APIs**</summary>
	Use cases: User-facing requests, immediate data needs
	Pros: Simple, well-understood, HTTP status codes
	Cons: Tight coupling, single point of failure
</details>
<details>
<summary>**gRPC (High Performance)**</summary>
	Use cases: Internal service communication, streaming
	Pros: Fast binary protocol, bidirectional streaming, strong typing
	Cons: More complex, requires HTTP/2
</details>
<details>
<summary>**GraphQL (Flexible Queries)**</summary>
	Use cases: Complex data requirements, mobile clients
	Pros: No over-fetching, single endpoint, self-documenting
	Cons: Complex caching, potential performance issues
</details>
**Asynchronous Communication **(Event-Driven)
<details>
<summary>**Message Brokers**</summary>
	**Popular Brokers**:
	- **RabbitMQ**: Feature-rich, good for complex routing
	- **Apache Kafka**: High throughput, event sourcing
	- **AWS SQS/SNS**: Managed, cloud-native
	- **Redis Pub/Sub**: Simple, fast for basic needs
	**Use cases**: Notifications, background processing, data replication
	**Pros**: Loose coupling, better fault tolerance, scalability
	**Cons**: Complexity, eventual consistency, debugging challenges
</details>
<details>
<summary>**Event Sourcing**</summary>
	**Use cases**: Financial systems, audit requirements, complex business logic
	**Pros**: Complete audit trail, temporal queries
	**Cons**: Complex, different programming model
</details>
### 2PC
**Phase 1: Voting Phase**
**Phase 2: Commit/Abort Phase**
### SAGA
<details>
<summary>**SAGA** - is a **failure management pattern** that coordinates a series of local transactions across multiple microservices.</summary>
	- Instead of a single *ACID* transaction, it *breaks the operation into a sequence of local transactions*, each updating its own service's database and publishing an event or message to trigger the next step.<br>If any step in the sequence fails, the SAGA executes a series of ***compensating transactions*** to undo the changes made by the preceding steps.<br>**Key Idea:** It provides *eventual consistency *(BASE consistency model) rather than strong, immediate consistency.
	- There are two primary ways to implement a SAGA: **Choreography** and **Orchestration**<span color="red">.</span>
	<details>
	<summary>**SAGA Choreography (Event-Driven)<br>**In this style, there is no central coordinator. Each service produces and listens for **events** (or messages) to decide what to do next. It's a **decentralized** approach.</summary>
		**How it works for our "Place an Order" example:**
		1. **Order Service:** Creates a `PENDING` order and publishes an `OrderCreated` event.
		2. **Payment Service:** Listens for `OrderCreated`, charges the customer, and publishes a `PaymentProcessed` event.
		3. **Inventory Service:** Listens for `PaymentProcessed`, reserves the items, and publishes an `InventoryReserved` event.
		4. **Order Service:** Listens for `InventoryReserved` and changes the order status to `CONFIRMED`.
		**What happens on failure?**
		Let's say the payment fails.
		1. **Payment Service:** Fails to charge the customer and publishes a `PaymentFailed` event.
		2. **Order Service:** Listens for `PaymentFailed` and updates the order status to `CANCELLED`.
		3. **(Optional) Inventory Service:** If it had already reserved items on a previous successful payment that later failed in shipping, it would listen for `OrderCancelled` and release the reservation.
		**Pros:**
		- Simple, no single point of failure.
		- Loosely coupled; services don't need to know about each other, only the events.
		**Cons:**
		- Can become complex and hard to debug as the workflow grows.
		- Risk of cyclic dependencies between events.
		- It's difficult to understand the overall business workflow by looking at the code.
	</details>
	<details>
	<summary>**SAGA Orchestration (Command-Driven)<br>**A central **orchestrator** (a separate service) takes responsibility for telling the participants what to do and when. The orchestrator manages the entire workflow.</summary>
		**How it works for our "Place an Order" example:**
		1. **Order Service** asks the **SAGA Orchestrator** to start the "Create Order" SAGA.
		2. The **Orchestrator** sends a `ExecutePayment` command to the **Payment Service**.
		3. The **Payment Service** replies with `PaymentSucceeded`.
		4. The **Orchestrator** then sends a `ReserveInventory` command to the **Inventory Service**.
		5. The **Inventory Service** replies with `InventoryReserved`.
		6. The **Orchestrator** finally sends an `ApproveOrder` command to the **Order Service**.
		**What happens on failure?**
		Let's say the inventory is out of stock.
		1. The **Inventory Service** replies with `InventoryReservationFailed`.
		2. The **Orchestrator**, knowing the sequence has failed, starts the compensation flow.
		3. It sends a `RefundPayment` command to the **Payment Service**.
		4. It then sends a `RejectOrder` command to the **Order Service**.
		**Pros:**
		- Centralized control over the workflow. Easier to understand and reason about.
		- Easier to implement complex flows involving conditional logic, parallel steps, or timeouts.
		- Reduced coupling between participating services; they only need to understand the orchestrator's commands.
		**Cons:**
		- Additional complexity of managing the orchestrator service.
		- A potential single point of failure (though this can be mitigated).
	</details>
	<table header-row="true">
<tr>
<td>**Feature**</td>
<td>**Choreography**</td>
<td>**Orchestration**</td>
</tr>
<tr>
<td>**Control**</td>
<td>Distributed</td>
<td>Centralized</td>
</tr>
<tr>
<td>**Complexity**</td>
<td>Low for simple flows, high for complex ones</td>
<td>Medium to High</td>
</tr>
<tr>
<td>**Coupling**</td>
<td>Loosely coupled (via events)</td>
<td>Coupled to the orchestrator</td>
</tr>
<tr>
<td>**Ease of Understanding**</td>
<td>Difficult</td>
<td>Easier</td>
</tr>
	</table>
	In practice, **SAGA Orchestration is generally preferred for complex, long-running business processes** because it provides better control, visibility, and separation of concerns.
	<details>
	<summary>**Compensating Transactions**</summary>
		This is the most critical concept in a SAGA. For every action, you must define a compensating transaction that logically undoes it.
		- `Create Order` -\> `Cancel Order` (change status to cancelled)
		- `Process Payment` -\> `Refund Payment`
		- `Reserve Inventory` -\> `Release Inventory`
		**Important:** Compensating transactions are *not* always the exact inverse. For example, "Refund Payment" might involve a different API call and business logic than "Process Payment." They must be **idempotent** (safe to retry multiple times without unintended side effects).
		<empty-block/>
	</details>
</details>
### Strangler Fig Pattern
Pattern for incrementally migrating legacy systems by gradually replacing specific pieces of functionality with new applications and services.
<empty-block/>
<page url="https://app.notion.com/p/3c89c92c96f5801088dbd05d56315ec8">DDD</page>