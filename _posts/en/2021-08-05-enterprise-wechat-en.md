---
audio: false
generated: false
image: false
lang: en
layout: post
title: Integrating With Enterprise WeChat
translated: false
type: post
---

During my time at ShowMeBug, I contributed to the Enterprise WeChat Integration project. This involved integrating ShowMeBug with Enterprise WeChat, providing seamless access to technical interview tools within the Enterprise WeChat ecosystem. I utilized technologies such as Ruby, Ruby on Rails, PostgreSQL, and the WeChat SDK to create a smooth user experience for both interviewers and candidates.

This blog post was composed with the assistance of AI around February 2025.

---

### Key Points
- It seems likely that integrating ShowMeBug with Enterprise WeChat involves setting up an account, obtaining API credentials, and using Ruby on Rails to make API calls, given the technologies mentioned.
- Research suggests using the Enterprise WeChat API for tasks like sending messages, with authentication handled via access tokens.
- The evidence leans toward using HTTParty in Ruby for API requests, with potential use of gems like "wechat" by Eric-Guo for easier integration.

### What is Enterprise WeChat and ShowMeBug Integration?
Enterprise WeChat, also known as WeChat Work, is a communication and collaboration platform for businesses, offering APIs for integration with applications. ShowMeBug, based on the context, appears to be a web application built with Ruby on Rails, likely for technical interviews, and the integration aims to provide seamless access within the Enterprise WeChat ecosystem.

### Setting Up and Using the API
To integrate, you'll need to:
- Register for an Enterprise WeChat account and verify your organization, then create an application to get an app ID and app secret.
- Use these credentials to obtain an access token, essential for API calls, by requesting from [this endpoint](https://qyapi.weixin.qq.com/cgi-bin/gettoken).
- Make API calls, such as sending messages, using the access token, with endpoints like [message.send](https://qyapi.weixin.qq.com/cgi-bin/message.send).

### Example in Ruby on Rails
Here's how you might implement it:
- Install the HTTParty gem for HTTP requests.
- Create a class to manage access tokens, caching them to avoid frequent requests.
- Use a method to send messages, ensuring to replace placeholders like "YOUR_AGENT_ID" with actual values from your Enterprise WeChat console.

This approach ensures a smooth integration, enhancing communication within your organization.

---

### Survey Note: Detailed Integration of ShowMeBug with Enterprise WeChat Using APIs

#### Introduction
This note explores the integration of ShowMeBug, a hypothetical Ruby on Rails web application for technical interviews, with Enterprise WeChat (WeChat Work), a communication and collaboration platform designed for businesses. The integration, as indicated, involves using Ruby, Ruby on Rails, PostgreSQL, and the WeChat SDK, aiming to provide seamless access to ShowMeBug's tools within the Enterprise WeChat ecosystem. This survey provides a comprehensive guide, covering setup, API usage, and best practices, based on available documentation and resources.

#### Background on Enterprise WeChat
Enterprise WeChat, launched by Tencent, is tailored for internal business communication, offering features like messaging, file sharing, and task management. It provides APIs for developers to integrate external applications, enabling functionalities such as custom bots and notifications. The platform is particularly useful for enhancing organizational workflows, with over 1 billion monthly active users, making it a significant tool for business integration.

#### Understanding ShowMeBug and Integration Needs
ShowMeBug, based on the context, is likely a platform for conducting technical interviews, and the integration with Enterprise WeChat aims to embed its tools within the platform for seamless access by interviewers and candidates. The use of Ruby on Rails suggests a web-based application, with PostgreSQL for data storage, possibly for user information, interview logs, or message history. The mention of the WeChat SDK indicates leveraging existing libraries for API interactions, which we'll explore further.

#### Setting Up an Enterprise WeChat Account
To begin integration, you must set up an Enterprise WeChat account:
- **Registration and Verification:** Visit the official website, register, and verify your organization's identity, a process that may involve submitting business documents.
- **Application Creation:** Within the account, create an application to obtain an app ID and app secret, crucial for API authentication. These credentials are found in the developer portal of Enterprise WeChat.

This setup ensures you have the necessary permissions and credentials to interact with the API, a foundational step for integration.

#### Obtaining API Credentials
After setting up, obtain the app ID and app secret from the Enterprise WeChat developer console. These are used to authenticate API requests, particularly for obtaining an access token, which is required for most API operations. The credentials should be stored securely, using environment variables in your Ruby on Rails application to avoid hardcoding, enhancing security.

#### Using the API in Ruby on Rails
To interact with the Enterprise WeChat API in a Ruby on Rails application, you'll make HTTP requests to the API endpoints. The HTTParty gem is recommended for simplicity in handling HTTP requests. The integration involves several key steps:

##### Step 1: Getting an Access Token
The access token is essential for API calls and is obtained by making a GET request to the token endpoint:
- **Endpoint:** `https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=APPID&corpsecret=APPSECRET`
- **Response:** Contains the access token and its expiration time (typically 2 hours), which needs periodic refreshing.

To manage this in Ruby, you can create a class to handle token fetching and caching:

```ruby
class WeChatAPI
  def initialize(app_id, app_secret)
    @app_id = app_id
    @app_secret = app_secret
    @access_token = nil
    @token_expiry = nil
  end

  def access_token
    if @access_token && Time.current < @token_expiry
      @access_token
    else
      response = HTTParty.get("https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=#{@app_id}&corpsecret=#{@app_secret}")
      if response['errcode'] == 0
        @access_token = response['access_token']
        @token_expiry = Time.current + response['expires_in'].seconds
        @access_token
      else
        raise "Failed to get access token: #{response['errmsg']}"
      end
    end
  end
end
```

This implementation caches the token to avoid frequent requests, improving performance.

##### Step 2: Making API Calls
With the access token, you can make API calls, such as sending a text message. The endpoint for sending messages is:
- **Endpoint:** `https://qyapi.weixin.qq.com/cgi-bin/message.send?access_token=ACCESSTOKEN`
- **Payload Example:**
  ```json
  {
      "touser": "USERID",
      "msgtype": "text",
      "agentid": "AGENTID",
      "text": {
          "content": "Hello, world!"
      }
  }
  ```

In Ruby, you can implement a method to send messages:

```ruby
def send_message(to_user, message_content)
  url = "https://qyapi.weixin.qq.com/cgi-bin/message.send?access_token=#{access_token}"
  payload = {
    "touser" => to_user,
    "msgtype" => "text",
    "agentid" => "YOUR_AGENT_ID",  # Replace with your agent ID
    "text" => {
      "content" => message_content
    }
  }
  response = HTTParty.post(url, body: payload.to_json)
  if response['errcode'] == 0
    true
  else
    false
  end
end
```

Here, "YOUR_AGENT_ID" should be replaced with the actual agent ID from your Enterprise WeChat console, which identifies the application making the request.

#### Handling Authentication and Token Management
The access token's validity (typically 2 hours) requires management to ensure continuous API access. Implement a scheduler or background job, such as using Sidekiq or Delayed Job in Rails, to refresh the token before expiration. This ensures your application remains functional without interruptions, a critical aspect for production environments.

#### Best Practices for Integration
To ensure a robust integration, consider the following:
- **Error Handling:** Always check API response error codes (e.g., `errcode` in the response) and handle them appropriately, logging errors for debugging.
- **Security:** Store app ID and app secret in environment variables, not in source code, to prevent exposure. Use Rails' `dotenv` gem for this purpose.
- **Performance:** Cache access tokens to reduce API calls to the token endpoint, as frequent requests can lead to rate limiting.
- **Documentation:** Refer to the official Enterprise WeChat API documentation for updates, though note it may primarily be in Chinese, requiring translation for English users.

#### Role of PostgreSQL and WeChat SDK
The mention of PostgreSQL suggests it's used for storing data related to the integration, such as user mappings between ShowMeBug and Enterprise WeChat, message logs, or interview data. This database integration ensures persistence and scalability, crucial for handling large volumes of data.

The WeChat SDK likely refers to third-party libraries, such as the "wechat" gem by Eric-Guo, which simplifies API interactions. This gem, available on GitHub ([API, command and message handling for WeChat in Rails](https://github.com/Eric-Guo/wechat)), supports both public and enterprise accounts, offering features like message handling and OAuth. Using such a gem can reduce development time, though understanding the API directly, as shown, provides deeper control.

#### Alternative Approach: Using Ruby Gems
For developers seeking easier integration, consider using Ruby gems like "wechat" by Eric-Guo. Install it via:
```bash
gem install wechat
```
Then, follow the gem's documentation for setup, which handles much of the API complexity, including token management and message sending. This approach is particularly useful for rapid development but may limit customization compared to direct API usage.

#### Conclusion
Integrating ShowMeBug with Enterprise WeChat involves setting up an account, obtaining credentials, and using Ruby on Rails to interact with the API, leveraging HTTParty for requests and managing access tokens for authentication. Best practices ensure security, performance, and reliability, with PostgreSQL supporting data storage and potential use of gems like "wechat" simplifying the process. This integration enhances communication and collaboration, providing a seamless experience for ShowMeBug users within the Enterprise WeChat ecosystem.

#### Table: Summary of Integration Steps

| Step                  | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| Set Up Account        | Register, verify, and create an application for app ID and secret.          |
| Obtain Credentials    | Get app ID and app secret from the developer console.                      |
| Get Access Token      | Request token using `https://qyapi.weixin.qq.com/cgi-bin/gettoken`.         |
| Make API Calls        | Use token for operations like sending messages via `https://qyapi.weixin.qq.com/cgi-bin/message.send`. |
| Manage Tokens         | Cache and refresh tokens to ensure continuous access.                      |
| Best Practices        | Handle errors, secure credentials, optimize performance, and refer to docs. |

This table summarizes the key actions, ensuring a structured approach to integration.

#### Key Citations
- [API, command and message handling for WeChat in Rails](https://github.com/Eric-Guo/wechat)
