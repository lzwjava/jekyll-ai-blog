---
audio: false
generated: true
image: false
lang: en
layout: post
model: deepseek/deepseek-v3.2-exp
title: Boosting JaCoCo Coverage in Java Spring
translated: false
type: note
---

Here's a comprehensive strategy to increase JaCoCo coverage in your large Java Spring project with 30+ APIs:

## 1. **Configuration Optimization**

### Maven Configuration

```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.11</version>
    <executions>
        <execution>
            <id>prepare-agent</id>
            <goals>
                <goal>prepare-agent</goal>
            </goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>verify</phase>
            <goals>
                <goal>report</goal>
            </goals>
        </execution>
        <execution>
            <id>check</id>
            <goals>
                <goal>check</goal>
            </goals>
            <configuration>
                <rules>
                    <rule>
                        <element>BUNDLE</element>
                        <limits>
                            <limit>
                                <counter>LINE</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.80</minimum>
                            </limit>
                        </limits>
                    </rule>
                </rules>
            </configuration>
        </execution>
    </executions>
</plugin>
```

### Multi-module Setup (if applicable)

```xml
<!-- In parent pom -->
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.11</version>
</plugin>

<!-- In aggregation module -->
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <executions>
        <execution>
            <id>report-aggregate</id>
            <phase>verify</phase>
            <goals>
                <goal>report-aggregate</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

## 2. **Test Strategy by Layer**

### Unit Tests (Highest Priority)

```java
// Service Layer Tests
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @Test
    void shouldCreateUserSuccessfully() {
        // Given
        UserRequest request = new UserRequest("john", "john@email.com");
        User user = User.builder().name("john").email("john@email.com").build();
        when(userRepository.save(any(User.class))).thenReturn(user);

        // When
        UserResponse response = userService.createUser(request);

        // Then
        assertThat(response.getName()).isEqualTo("john");
        verify(userRepository).save(any(User.class));
    }
}

// Repository Layer Tests
@DataJpaTest
class UserRepositoryTest {

    @Autowired
    private TestEntityManager entityManager;

    @Autowired
    private UserRepository userRepository;

    @Test
    void shouldFindByEmail() {
        // Given
        User user = User.builder().name("john").email("john@email.com").build();
        entityManager.persist(user);

        // When
        Optional<User> found = userRepository.findByEmail("john@email.com");

        // Then
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("john");
    }
}
```

### Integration Tests

```java
@SpringBootTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@TestPropertySource(locations = "classpath:application-test.properties")
class UserIntegrationTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void shouldCreateUserViaApi() {
        // Given
        UserRequest request = new UserRequest("john", "john@email.com");

        // When
        ResponseEntity<UserResponse> response = restTemplate.postForEntity(
            "/api/users",
            request,
            UserResponse.class
        );

        // Then
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(response.getBody().getName()).isEqualTo("john");
    }
}
```

### Controller Tests

```java
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Test
    void shouldReturnUserById() throws Exception {
        // Given
        UserResponse userResponse = new UserResponse(1L, "john", "john@email.com");
        when(userService.getUserById(1L)).thenReturn(userResponse);

        // When & Then
        mockMvc.perform(get("/api/users/1"))
               .andExpect(status().isOk())
               .andExpect(jsonPath("$.name").value("john"));
    }
}
```

## 3. **Coverage Improvement Techniques**

### Test Data Builders

```java
public class UserTestBuilder {

    public static User.UserBuilder defaultUser() {
        return User.builder()
                  .id(1L)
                  .name("john")
                  .email("john@email.com")
                  .createdAt(LocalDateTime.now());
    }
}

// Usage in tests
User user = UserTestBuilder.defaultUser().build();
```

### Parameterized Tests

```java
@ParameterizedTest
@ValueSource(strings = {"valid@email.com", "test@domain.com", "user@example.org"})
void shouldValidateEmailFormat(String email) {
    UserRequest request = new UserRequest("test", email);
    assertThat(validator.isValid(request)).isTrue();
}
```

### Exception Testing

```java
@Test
void shouldThrowUserNotFoundException() {
    // Given
    when(userRepository.findById(999L)).thenReturn(Optional.empty());

    // When & Then
    assertThatThrownBy(() -> userService.getUserById(999L))
        .isInstanceOf(UserNotFoundException.class)
        .hasMessage("User not found with id: 999");
}
```

## 4. **Common Low-Coverage Areas to Target**

### Configuration Classes

```java
@Test
void shouldLoadConfigurationProperties() {
    // Given
    EnvironmentTestUtils.addEnvironment(
        context,
        "app.security.jwt.secret=secret",
        "app.security.jwt.expiration=3600"
    );

    // When
    context.refresh();
    JwtProperties props = context.getBean(JwtProperties.class);

    // Then
    assertThat(props.getSecret()).isEqualTo("secret");
}
```

### Exception Handlers

```java
@Test
void shouldHandleValidationException() throws Exception {
    // Given
    MethodArgumentNotValidException exception = mock(MethodArgumentNotValidException.class);

    // When
    ResponseEntity<ErrorResponse> response =
        exceptionHandler.handleValidationException(exception);

    // Then
    assertThat(response.getStatusCode()).isEqualTo(HttpStatus.BAD_REQUEST);
}
```

### Mappers and Converters

```java
@Test
void shouldMapUserToUserResponse() {
    // Given
    User user = UserTestBuilder.defaultUser().build();

    // When
    UserResponse response = userMapper.toResponse(user);

    // Then
    assertThat(response.getId()).isEqualTo(1L);
    assertThat(response.getName()).isEqualTo("john");
}
```

## 5. **Advanced Techniques**

### Test Coverage for Conditional Logic

```java
@Test
void shouldCoverAllUserStatusScenarios() {
    // Test ACTIVE status
    User activeUser = UserTestBuilder.defaultUser().status(UserStatus.ACTIVE).build();
    assertThat(activeUser.canLogin()).isTrue();

    // Test INACTIVE status
    User inactiveUser = UserTestBuilder.defaultUser().status(UserStatus.INACTIVE).build();
    assertThat(inactiveUser.canLogin()).isFalse();

    // Test SUSPENDED status
    User suspendedUser = UserTestBuilder.defaultUser().status(UserStatus.SUSPENDED).build();
    assertThat(suspendedUser.canLogin()).isFalse();
}
```

### Integration Test with Testcontainers

```java
@Testcontainers
@SpringBootTest
class UserRepositoryIT {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:13");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Test
    void shouldPersistUserWithDatabase() {
        // Real database integration test
    }
}
```

## 6. **CI/CD Integration**

### Maven Command for Coverage

```bash
mvn clean verify jacoco:report
```

### Coverage Check in Pipeline

```yaml
# GitHub Actions example
- name: Test and Coverage
  run: mvn clean verify jacoco:check
```

## 7. **Quick Wins for Immediate Improvement**

1. **Add missing unit tests for simple getters/setters**
2. **Test all exception scenarios**
3. **Cover all controller endpoints**
4. **Test validation logic**
5. **Add tests for utility classes**

## 8. **Monitoring and Reporting**

### Generate Reports

```bash
# Generate HTML reports
mvn jacoco:report

# Generate aggregated report for multi-module
mvn jacoco:report-aggregate
```

Start by focusing on the critical business logic and APIs with the lowest coverage. Use the JaCoCo HTML reports to identify exactly which lines and branches are not covered, then write targeted tests for those specific areas.
