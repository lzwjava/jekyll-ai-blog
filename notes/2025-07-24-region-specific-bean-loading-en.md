---
audio: false
generated: true
lang: en
layout: post
title: Dynamic Region-Specific Beans
translated: false
type: note
---

### Understanding the Requirement

It sounds like you're building a Spring Boot/Java Spring application that needs to support multiple regions (or "nationalities") such as Singapore (SG), Hong Kong (HK), and Taiwan (TW). You want to load or inject different beans dynamically, particularly for a `CoreController` class, using features like `@Autowired` and bean management.

This is a common scenario for **multi-tenancy** or **region-specific configurations**, where behavior (e.g., services, configurations, or controllers) varies by region. In Spring, you can't easily switch entire controller classes at runtime, but you can:

1. Use **Spring Profiles** for environment-specific bean loading (e.g., separate deployments or activations for each region). This is compile-time or startup-time.
2. Use **runtime selection** with the Strategy Pattern, where you inject multiple beans (e.g., via a Map) and select the right one based on a request parameter, header, or context (e.g., user's region).

Since you mentioned "multiple nationality development" and examples like SG/HK/TW, I'll assume this needs to handle multiple regions in a single application instance (runtime switching). If it's separate deployments per region, profiles are simpler.

I'll explain both approaches with code examples. We'll assume `CoreController` depends on a region-specific service (e.g., `CoreService` interface with implementations for each region). This way, the controller stays the same, but its behavior changes via injected beans.

### Approach 1: Using Spring Profiles for Region-Specific Bean Loading (Startup-Time)

This is ideal if you deploy separate instances per region (e.g., via environment variables or application properties). Beans are loaded conditionally based on the active profile.

#### Step 1: Define the Interface and Implementations

Create an interface for the region-specific logic:

```java
public interface CoreService {
    String getRegionMessage();
}
```

Implementations for each region:

```java
// SgCoreService.java
@Service
@Profile("sg")  // Only load this bean if 'sg' profile is active
public class SgCoreService implements CoreService {
    @Override
    public String getRegionMessage() {
        return "Welcome from Singapore!";
    }
}

// HkCoreService.java
@Service
@Profile("hk")
public class HkCoreService implements CoreService {
    @Override
    public String getRegionMessage() {
        return "Welcome from Hong Kong!";
    }
}

// TwCoreService.java
@Service
@Profile("tw")
public class TwCoreService implements CoreService {
    @Override
    public String getRegionMessage() {
        return "Welcome from Taiwan!";
    }
}
```

#### Step 2: Autowire in CoreController

```java
@RestController
public class CoreController {
    private final CoreService coreService;

    @Autowired
    public CoreController(CoreService coreService) {
        this.coreService = coreService;
    }

    @GetMapping("/message")
    public String getMessage() {
        return coreService.getRegionMessage();
    }
}
```

#### Step 3: Activate Profiles

- In `application.properties` or via command line:
  - Run with `--spring.profiles.active=sg` for Singapore beans.
  - This ensures only the `SgCoreService` bean is created and autowired.
- For custom conditions beyond profiles, use `@ConditionalOnProperty` (e.g., `@ConditionalOnProperty(name = "app.region", havingValue = "sg")`).

This approach is simple but requires restarting or separate apps per region. Not suitable for handling all regions in one runtime instance.

### Approach 2: Runtime Bean Selection with @Autowired Map (Strategy Pattern)

For a single application handling multiple regions dynamically (e.g., based on HTTP request headers like `X-Region: sg`), use a Map of beans. Spring can autowire all implementations into a Map<String, CoreService>, where the key is the bean name.

#### Step 1: Define the Interface and Implementations

Same as above, but without `@Profile`:

```java
public interface CoreService {
    String getRegionMessage();
}

// SgCoreService.java
@Service("sgCoreService")  // Explicit bean name for Map key
public class SgCoreService implements CoreService {
    @Override
    public String getRegionMessage() {
        return "Welcome from Singapore!";
    }
}

// HkCoreService.java
@Service("hkCoreService")
public class HkCoreService implements CoreService {
    @Override
    public String getRegionMessage() {
        return "Welcome from Hong Kong!";
    }
}

// TwCoreService.java
@Service("twCoreService")
public class TwCoreService implements CoreService {
    @Override
    public String getRegionMessage() {
        return "Welcome from Taiwan!";
    }
}
```

#### Step 2: Autowire a Map in CoreController

```java
@RestController
public class CoreController {
    private final Map<String, CoreService> coreServices;

    @Autowired  // Spring auto-populates the map with all CoreService beans, keyed by bean name
    public CoreController(Map<String, CoreService> coreServices) {
        this.coreServices = coreServices;
    }

    @GetMapping("/message")
    public String getMessage(@RequestHeader("X-Region") String region) {  // Or use @RequestParam if it's a query param
        CoreService service = coreServices.get(region.toLowerCase() + "CoreService");
        if (service == null) {
            throw new IllegalArgumentException("Unsupported region: " + region);
        }
        return service.getRegionMessage();
    }
}
```

- Here, `@Autowired` on the Map injects all `CoreService` implementations automatically.
- Bean names must match your key logic (e.g., "sgCoreService").
- For selection: Use a request header/param to determine the region. This makes it dynamic per request.

#### Optional: Using @Qualifier for Specific Injection

If you want to inject a specific bean manually:

```java
@RestController
public class CoreController {
    @Autowired
    @Qualifier("sgCoreService")  // Injects only the SG bean
    private CoreService sgCoreService;

    // ... similarly for others
}
```

But this isn't dynamic; use the Map for runtime switching.

#### Step 3: Configuration and Best Practices

- In your Spring Boot main class: `@SpringBootApplication` is sufficient; Spring scans for `@Service` beans.
- Handle defaults: Add a fallback service if no region matches.
- For more complex conditions, use `@ConditionalOnExpression` or custom `@Conditional` annotations on beans.
- Thread safety: Since controllers are singleton by default, the Map is safe as long as services are stateless.
- Testing: Use `@SpringBootTest` with mock requests to test different regions.

### Which Approach to Choose?

- Use **Profiles** if regions are separated by deployment/environment (e.g., different servers for SG/HK/TW).
- Use **Map/Strategy** for a unified app handling all regions at runtime (more flexible for microservices).

If this doesn't match your exact setup (e.g., if `CoreController` itself needs to be different per region), you could use multiple controllers with `@RequestMapping` conditions or a factory to create controllers dynamically—but that's rarer and more complex.

If you provide more details (e.g., how the region is determined), I can refine this!
