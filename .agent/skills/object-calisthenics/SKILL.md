---
name: object-calisthenics
description: Enforces Object Calisthenics rules for better object-oriented design and code quality.
allowed-tools: Read, Write, Edit
version: 1.0
priority: HIGH
---

# Object Calisthenics - Object-Oriented Design Standards

> **CORE SKILL** - Apply the 9 rules of Object Calisthenics to ensure high-quality, maintainable, and readable object-oriented code.

---

## 9 Rules of Object Calisthenics

### 1. Only One Level Of Indentation Per Method
Never nest control structures (if, for, while) inside each other. Use Extract Method to keep functions flat.

**Bad Approach:**
```typescript
function processUsers(users: User[]) {
  for (const user of users) {
    if (user.isActive()) {
      user.sendEmail();
    }
  }
}
```

**Good Approach:**
```typescript
function processUsers(users: User[]) {
  for (const user of users) {
    processSingleUser(user);
  }
}

function processSingleUser(user: User) {
  if (user.isActive()) {
    user.sendEmail();
  }
}
```

### 2. Don't Use The ELSE Keyword
Use guard clauses or early returns instead of `else` to reduce cognitive load and nested logic.

**Bad Approach:**
```typescript
function login(user: User) {
  if (user.isValid()) {
    authenticate(user);
  } else {
    throw new Error("Invalid");
  }
}
```

**Good Approach:**
```typescript
function login(user: User) {
  if (!user.isValid()) {
    throw new Error("Invalid");
  }
  authenticate(user);
}
```

### 3. Wrap All Primitives And Strings
Encapsulate all primitives within objects to give them clear boundaries and domain meaning.

**Bad Approach:**
```typescript
function processPayment(amount: number, currency: string) {
  process(amount, currency);
}
```

**Good Approach:**
```typescript
class Money {
  constructor(private readonly amount: number, private readonly currency: string) {}
}

function processPayment(money: Money) {
  process(money);
}
```

### 4. First Class Collections
Any class that contains a collection should contain no other member variables. Wrap the collection to provide domain-specific behaviors.

**Bad Approach:**
```typescript
class Team {
  public members: User[];
  public name: string;
}
```

**Good Approach:**
```typescript
class Team {
  public name: string;
}

class Members {
  constructor(private readonly users: User[]) {}
  
  public filterActive(): Members {
    return new Members(this.users.filter(u => u.isActive()));
  }
}
```

### 5. One Dot Per Line
Avoid chaining method calls across multiple objects to respect the Law of Demeter.

**Bad Approach:**
```typescript
const city = user.getAddress().getCity();
```

**Good Approach:**
```typescript
const city = user.getCity();
```

### 6. Don't Abbreviate
Always use full, explicit names for variables, methods, and classes to reveal intent clearly.

**Bad Approach:**
```typescript
function calcAvg(arr: number[]) {
  return calculate(arr);
}
```

**Good Approach:**
```typescript
function calculateAverage(numbers: number[]) {
  return calculate(numbers);
}
```

### 7. Keep All Entities Small
Classes should be no longer than 50 lines. Packages/Namespaces should have no more than 10 files. 

### 8. No Classes With More Than Two Instance Variables
High cohesion requires small classes with few responsibilities. Strive to decompose classes into smaller entities.

**Bad Approach:**
```typescript
class User {
  private id: string;
  private firstName: string;
  private lastName: string;
  private emailAddress: string;
}
```

**Good Approach:**
```typescript
class Name {
  constructor(private readonly first: string, private readonly last: string) {}
}

class Email {
  constructor(private readonly address: string) {}
}

class User {
  constructor(private readonly name: Name, private readonly email: Email) {}
}
```

### 9. No Getters/Setters/Properties
Tell, Don't Ask. Objects should hide their internal state and expose operations instead of just returning values.

**Bad Approach:**
```typescript
const balance = account.getBalance();
account.setBalance(balance + 100);
```

**Good Approach:**
```typescript
account.deposit(100);
```

---

## Specific Constraints
- **NO COMMENTS IN CODE:** Never write comments inside the codebase or examples.
- **ENGLISH ONLY:** All code logic, including variable names and text strings, must execute exclusively in English.
