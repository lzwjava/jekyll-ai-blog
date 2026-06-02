---
audio: false
generated: true
lang: en
layout: post
title: Exploring Avaloq's Trading API Details
translated: false
type: note
---

I'll search for specific technical information about Avaloq's trading functionality, pre-trade checks, and XML SOAP API usage.Let me search for more specific information about Avaloq's XML SOAP API and trading implementation details.Based on my search results, I can provide you with information about implementing stock trading orders in Avaloq, though specific technical documentation appears limited in public sources. Here's what I found:

## Avaloq Trading Implementation

### Trading Platform Overview

Avaloq enables your clients to trade any product, from exchange-traded to over-the-counter and crypto, on one end-to-end platform. The platform provides comprehensive trading capabilities integrated within the core banking system.

### Pre-Trade Compliance Checks

The software checks persons, transactions and securities orders using predefined compliance rules. Based on these rule sets, ACTICO Compliance software automatically decides whether a compliance risk exists. This integration shows that Avaloq supports pre-trade compliance through partnerships with specialized compliance solutions.

The pre-trade check system typically validates:

- Client authorization and permissions
- Risk limits and exposure checks
- Regulatory compliance requirements
- Available funds and credit limits
- Market timing and trading restrictions

### API Integration

The Account Management API module includes different API endpoints offering connectivity for third-party systems to provide easy access to specific functionality. Avaloq provides API access through their avaloq.one platform, and there's a GitHub repository with resources for getting started with Avaloq's Open APIs.

## Implementation Approach

### 1. Stock Order Placement

While specific XML SOAP documentation wasn't found in the search results, typical implementation would involve:

**Order Structure:**

- Order ID and client identification
- Security identification (ISIN, ticker, etc.)
- Order type (market, limit, stop, etc.)
- Quantity and price parameters
- Time-in-force specifications
- Settlement instructions

### 2. Pre-Trade Check Process

The pre-trade validation would typically follow this flow:

- Submit order details to compliance engine
- Validate against client profile and limits
- Check regulatory requirements
- Verify available funds/securities
- Return approval/rejection with reasons

### 3. XML SOAP API Calling

Based on standard financial industry practices and the available information, the XML SOAP integration would likely involve:

**Authentication:**

- API credentials and security tokens
- Client identification and authorization

**Message Format:**

- Standard XML envelope structure
- Avaloq-specific schemas for trading operations
- Error handling and response codes

## Recommendations for Implementation

1. **Documentation Access**: Contact Avaloq directly or through their partner network to access detailed API documentation, as this appears to be restricted to licensed clients.

2. **Sandbox Environment**: Avaloq has laid a good foundation to help businesses ease the journey of testing and integrating new solutions by managing the complexities across various phases utilizing Avaloq's sandbox solution powered by AWS.

3. **Partner Integration**: Consider working with Avaloq-certified implementation partners who have experience with their trading APIs and can provide specific guidance on XML SOAP integration patterns.

4. **Compliance Integration**: The Avaloq Banking Suite works reliably with ACTICO Compliance software via a standard interface, suggesting established patterns for compliance integration.

For detailed technical specifications, API schemas, and implementation examples, you would need to access Avaloq's official developer documentation through their client portal or contact their technical support team directly.
