---
audio: false
generated: true
lang: en
layout: post
title: Implementing Multi-threaded Validation with CompletableFuture
translated: false
type: note
---

If we use `CompletableFuture` in a Spring Boot application for multi-threaded validation, it provides a modern, flexible way to handle asynchronous tasks. Below, I’ll explain how to implement it, highlight its advantages and challenges, and provide a complete solution tailored to validating multiple rules concurrently.

### Implementing Multi-threaded Validation with CompletableFuture

`CompletableFuture` is part of Java’s concurrency API and allows you to execute tasks asynchronously, chain operations, and handle results or exceptions elegantly. Here’s how we can use it to validate multiple rules in parallel, stopping as soon as one fails.

#### Step 1: Define the Validation Logic

First, let’s assume we have a service that defines individual validation rules. Each rule might involve database access or complex logic, so we’ll use Spring’s `@Transactional` annotation for proper transaction management.

```java
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class RuleValidator {

    @Transactional(readOnly = true)
    public boolean validateRule(int ruleId) {
        // Simulate validation logic (e.g., database query)
        return performValidation(ruleId);
    }

    private boolean performValidation(int ruleId) {
        // Example: even rule IDs pass, odd ones fail
        return ruleId % 2 == 0;
    }
}
```

#### Step 2: Implement Validation Service with CompletableFuture

Now, let’s create a service that runs multiple validation rules concurrently using `CompletableFuture`. We’ll use an `ExecutorService` to manage threads and ensure that if any rule fails, we can stop processing the others.

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;

@Service
public class ValidationService {
    private static final Logger log = LoggerFactory.getLogger(ValidationService.class);
    private final ExecutorService executorService;
    private final RuleValidator ruleValidator;

    @Autowired
    public ValidationService(ExecutorService executorService, RuleValidator ruleValidator) {
        this.executorService = executorService;
        this.ruleValidator = ruleValidator;
    }

    public boolean validateAllRules() {
        // Create a list to hold all futures
        List<CompletableFuture<Boolean>> futures = new ArrayList<>();

        // Submit 10 validation rules (for example)
        for (int i = 0; i < 10; i++) {
            final int ruleId = i;
            CompletableFuture<Boolean> future = CompletableFuture.supplyAsync(() -> {
                try {
                    return ruleValidator.validateRule(ruleId);
                } catch (Exception e) {
                    log.error("Validation failed for rule " + ruleId, e);
                    return false; // Treat exceptions as failures
                }
            }, executorService);
            futures.add(future);
        }

        // Create a future to track the overall result
        CompletableFuture<Boolean> resultFuture = new CompletableFuture<>();

        // Monitor each future for failure
        for (CompletableFuture<Boolean> future : futures) {
            future.thenAccept(result -> {
                if (!result && !resultFuture.isDone()) {
                    // First failure detected
                    resultFuture.complete(false);
                    // Cancel remaining tasks
                    futures.forEach(f -> {
                        if (!f.isDone()) {
                            f.cancel(true);
                        }
                    });
                }
            });
        }

        // If all futures complete successfully, mark as true
        CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]))
                .thenRun(() -> {
                    if (!resultFuture.isDone()) {
                        resultFuture.complete(true);
                    }
                });

        try {
            return resultFuture.get(); // Block until result is available
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error during validation", e);
            return false;
        }
    }
}
```

#### How It Works

1. **Task Submission**:
   - We create a `CompletableFuture` for each rule using `supplyAsync()`, which runs the validation logic asynchronously.
   - The `executorService` (injected via Spring) manages the thread pool.

2. **Failure Detection**:
   - Each future is monitored using `thenAccept()`. If any rule returns `false`, we complete the `resultFuture` with `false` and cancel the remaining futures.

3. **Success Case**:
   - `CompletableFuture.allOf()` waits for all futures to complete. If no failures occur, it completes `resultFuture` with `true`.

4. **Result Retrieval**:
   - We block on `resultFuture.get()` to obtain the final result, handling any exceptions that might occur.

### Advantages of Using CompletableFuture

- **Flexibility**: You can chain operations (e.g., `thenApply`, `thenCompose`) to process results further if needed.
- **Exception Handling**: Built-in methods like `exceptionally()` or `handle()` make it easy to manage errors.
- **Non-blocking Design**: It supports a reactive programming style, which can be extended for more complex workflows.

### Challenges

- **Cancellation**: Unlike `ExecutorService` with `CompletionService` (where you can easily poll for the first result and cancel others), `CompletableFuture` requires manual cancellation of other futures when one fails. This adds complexity.
- **Complexity**: The code can become harder to read and maintain compared to a simpler loop-based approach with `ExecutorService`.

### Example Usage

To use this in a Spring Boot application, you’d configure an `ExecutorService` bean:

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

@Configuration
public class AppConfig {
    @Bean
    public ExecutorService executorService() {
        return Executors.newFixedThreadPool(10); // Adjust size as needed
    }
}
```

Then, call the service from a controller or another component:

```java
@RestController
public class ValidationController {
    private final ValidationService validationService;

    @Autowired
    public ValidationController(ValidationService validationService) {
        this.validationService = validationService;
    }

    @GetMapping("/validate")
    public ResponseEntity<String> validate() {
        boolean result = validationService.validateAllRules();
        return ResponseEntity.ok(result ? "All rules passed" : "Validation failed");
    }
}
```

### Conclusion

Using `CompletableFuture` for multi-threaded validation in Spring Boot is a viable approach, especially if you value its asynchronous, chainable nature. It allows you to run validation rules concurrently and handle results flexibly. However, if your primary goal is simplicity—especially for detecting the first failure and canceling remaining tasks—the traditional `ExecutorService` with `CompletionService` might be easier to implement and maintain. With `CompletableFuture`, you gain power and flexibility at the cost of slightly more complex cancellation logic.
