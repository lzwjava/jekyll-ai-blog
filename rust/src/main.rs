use reqwest::Client;
use serde::{Deserialize, Serialize};
use std::env;

#[derive(Debug, Serialize)]
struct ChatRequest {
    model: String,
    messages: Vec<Message>,
}

#[derive(Debug, Serialize, Deserialize)]
struct Message {
    role: String,
    content: String,
}

#[derive(Debug, Deserialize)]
struct ChatResponse {
    choices: Vec<Choice>,
}

#[derive(Debug, Deserialize)]
struct Choice {
    message: Message,
}

async fn call_mistral_api(prompt: &str, model: &str) -> Result<String, reqwest::Error> {
    let api_key = env::var("MISTRAL_API_KEY").expect("MISTRAL_API_KEY must be set");
    let client = Client::new();
    let url = "https://api.mistral.ai/v1/chat/completions";

    let messages = vec![Message {
        role: "user".to_string(),
        content: prompt.to_string(),
    }];

    let request_body = ChatRequest {
        model: model.to_string(),
        messages,
    };

    let response = client
        .post(url)
        .header("Authorization", format!("Bearer {}", api_key))
        .header("Content-Type", "application/json")
        .json(&request_body)
        .send()
        .await?;

    let response_body: ChatResponse = response.json().await?;
    let content = response_body.choices[0].message.content.clone();

    Ok(content)
}

#[tokio::main]
async fn main() -> Result<(), reqwest::Error> {
    let response = call_mistral_api("Hello", "mistral-tiny").await?;
    println!("Response: {}", response);
    Ok(())
}
