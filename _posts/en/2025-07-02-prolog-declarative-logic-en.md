---
audio: false
generated: true
lang: en
layout: post
title: 'Prolog: Logic-Based Declarative Programming'
translated: false
type: note
---

Prolog, short for "Programming in Logic," is a **declarative programming language** that stands in stark contrast to imperative languages like Python, Java, or C++. Instead of telling the computer *how* to solve a problem step-by-step, you describe *what* the problem is, and Prolog uses its built-in inference engine to find solutions.

It's particularly well-suited for problems involving **logic, symbolic reasoning, and knowledge representation**, making it a cornerstone in the field of Artificial Intelligence (AI), natural language processing, and expert systems.

### Key Concepts of Prolog:

1.  **Facts:**
    Facts are fundamental truths about the world that you provide to Prolog. They represent unconditional assertions.

      * **Syntax:** `predicate(argument1, argument2, ...).`
      * **Examples:**
          * `man(john).` (John is a man)
          * `woman(mary).` (Mary is a woman)
          * `parent(john, mary).` (John is a parent of Mary)
          * `capital_of(france, paris).` (Paris is the capital of France)

2.  **Rules:**
    Rules define relationships between facts. They state that a certain fact is true if one or more other facts (or conditions) are true.

      * **Syntax:** `head :- body.` (Read as "head is true if body is true")
          * The `head` is a single predicate.
          * The `body` is a conjunction of one or more predicates, separated by commas (`,`), which means "AND".
      * **Examples:**
          * `happy(X) :- likes(X, pizza).` (X is happy if X likes pizza)
          * `father(X, Y) :- parent(X, Y), male(X).` (X is the father of Y if X is a parent of Y AND X is male)
          * `grandparent(G, C) :- parent(G, P), parent(P, C).` (G is a grandparent of C if G is a parent of P AND P is a parent of C)

3.  **Queries:**
    Once you've defined your facts and rules (your "knowledge base"), you can ask Prolog questions, called queries, to retrieve information or verify relationships.

      * **Syntax:** `?- query.`
      * Prolog attempts to satisfy the query by finding variables that make the query true, based on the established facts and rules. If multiple solutions exist, you can often prompt Prolog for more by typing a semicolon (`;`).
      * **Examples:**
          * `?- man(john).` (Is John a man?)
          * `?- parent(john, X).` (Who is John a parent of? - `X` is a variable)
          * `?- grandparent(elizabeth, william).` (Is Elizabeth a grandparent of William?)

4.  **Variables:**
    Variables in Prolog are used to represent unknown values. They always start with an uppercase letter or an underscore (`_`). Unlike variables in imperative languages, they are not memory locations that can be reassigned; rather, they are placeholders that Prolog tries to unify with values to satisfy a query.

5.  **Unification:**
    This is the core mechanism of Prolog. Unification is a pattern-matching process that attempts to make two terms identical by assigning values to variables. If a match is found, the variables are "bound" to those values. If no match is possible, the unification fails.

6.  **Backtracking:**
    When Prolog tries to satisfy a query, it works through the facts and rules in a depth-first manner. If a path leads to a dead end (a goal cannot be satisfied), Prolog "backtracks" to a previous choice point and tries an alternative path. This systematic search allows it to find all possible solutions to a query.

### How Prolog Works (Simplified):

1.  You load a Prolog program (a collection of facts and rules) into the interpreter.
2.  You pose a query.
3.  Prolog tries to prove the query by matching it against its facts and the heads of its rules.
4.  If a rule's head matches, Prolog then tries to prove the conditions in the rule's body (these become sub-goals).
5.  This process continues recursively until all sub-goals are satisfied by facts or by successfully proven rules.
6.  If a solution is found, Prolog presents the variable bindings. If multiple solutions exist, it can backtrack to find them.

### Advantages of Prolog:

  * **Declarative Nature:** Focus on *what* to solve, not *how*. This can lead to more concise and readable code for certain problems.
  * **Built-in Logic and Inference:** Powerful mechanisms for logical reasoning and searching.
  * **Excellent for Symbolic AI:** Ideal for expert systems, natural language processing, knowledge representation, and theorem proving.
  * **Pattern Matching and Unification:** Simplifies complex data manipulation.
  * **Backtracking:** Automates the search for solutions, which would be manually programmed in other languages.

### Disadvantages of Prolog:

  * **Learning Curve:** The declarative paradigm can be challenging for those used to imperative programming.
  * **Performance:** Can be less efficient for numerical computations or I/O-intensive tasks compared to imperative languages.
  * **Limited I/O and Graphics:** Not designed for complex user interfaces or graphical applications.
  * **Debugging:** Tracing the execution flow in Prolog can sometimes be tricky due to backtracking.

-----

### Prolog Code Examples:

To run these examples, you'll need a Prolog interpreter (like SWI-Prolog, which is free and widely used). You typically save your code in a file with a `.pl` extension (e.g., `family.pl`) and then load it into the interpreter.

**Example 1: Family Relationships**

Let's define some basic family relationships.

**`family.pl`:**

```prolog
% Facts: Define basic relationships
male(john).
male(jim).
male(george).
female(mary).
female(lisa).
female(susan).

parent(john, lisa).   % John is a parent of Lisa
parent(john, jim).    % John is a parent of Jim
parent(mary, lisa).   % Mary is a parent of Lisa
parent(mary, jim).    % Mary is a parent of Jim
parent(lisa, george). % Lisa is a parent of George
parent(jim, susan).   % Jim is a parent of Susan

% Rules: Define derived relationships
father(X, Y) :- parent(X, Y), male(X).         % X is the father of Y if X is a parent of Y AND X is male.
mother(X, Y) :- parent(X, Y), female(X).        % X is the mother of Y if X is a parent of Y AND X is female.
child(X, Y) :- parent(Y, X).                    % X is a child of Y if Y is a parent of X.
grandparent(G, C) :- parent(G, P), parent(P, C). % G is a grandparent of C if G is a parent of P AND P is a parent of C.
sibling(X, Y) :- parent(P, X), parent(P, Y), X \= Y. % X and Y are siblings if they share a parent P, and X is not the same as Y.
```

**Running in a Prolog Interpreter (e.g., SWI-Prolog):**

```prolog
?- consult('family.pl').
% family.pl compiled 0.00 sec, 7 clauses
true.

% Queries:

?- male(john).
true.

?- female(jim).
false.

?- parent(john, lisa).
true.

?- parent(X, jim). % Who is a parent of Jim?
X = john ;           % Type ';' for more solutions
X = mary.
false.

?- father(john, lisa).
true.

?- mother(mary, jim).
true.

?- grandparent(john, george).
true.

?- grandparent(X, susan). % Who is a grandparent of Susan?
X = john ;
X = mary.
false.

?- sibling(lisa, jim).
true.

?- sibling(lisa, george).
false. % Because they don't share *all* parents
```

**Example 2: Simple Knowledge Base (Animals)**

**`animals.pl`:**

```prolog
% Facts about animals and their properties
animal(dog).
animal(cat).
animal(bird).
animal(fish).

has_fur(dog).
has_fur(cat).
flies(bird).
swims(fish).

eats(dog, bones).
eats(cat, fish).
eats(bird, seeds).
eats(fish, plankton).

% Rules
is_mammal(X) :- animal(X), has_fur(X). % A mammal is an animal that has fur.
can_fly(X) :- animal(X), flies(X).     % Something can fly if it's an animal and flies.
```

**Running in a Prolog Interpreter:**

```prolog
?- consult('animals.pl').
% animals.pl compiled 0.00 sec, 10 clauses
true.

% Queries:

?- animal(cat).
true.

?- has_fur(dog).
true.

?- eats(cat, X). % What does a cat eat?
X = fish.

?- is_mammal(dog).
true.

?- is_mammal(bird).
false.

?- can_fly(X). % What animals can fly?
X = bird.
false.
```

These examples illustrate the declarative nature of Prolog, where you define the relationships and properties, and the system infers answers to your queries.
