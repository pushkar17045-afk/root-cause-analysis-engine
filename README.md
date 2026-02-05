# Root Cause Analysis Engine

## Overview
The Root Cause Analysis Engine is a backend microservice designed to assist in diagnosing failures in distributed systems. It ingests logs and event data from multiple services, correlates them based on severity and occurrence patterns, and returns a ranked list of probable root causes.

The service is intentionally API-driven and backend-only, reflecting how real-world reliability and SRE tooling is typically built and consumed.

---

## Problem Statement
In distributed systems, failures rarely occur in isolation. A single fault often propagates across services, producing a large volume of logs and errors. Identifying the *actual root cause* from this noise is time-consuming and error-prone.

This project addresses that problem by providing a deterministic, explainable approach to root cause analysis using log correlation rather than guesswork.

---

## Key Features
- API-based log and event ingestion
- Deterministic correlation logic (no black-box ML)
- Ranking of probable root causes with confidence scores
- Health and self-documentation endpoints
- Publicly deployed backend service with automatic CI/CD

---

## Architecture
The service is designed as a standalone backend microservice:

- **API Layer**: Exposes endpoints for analysis, health checks, and documentation
- **Analysis Engine**: Correlates events using severity weighting and frequency
- **Deployment**: Cloud-hosted with automatic redeployments on each commit

No frontend is included by design; the service is intended to be consumed programmatically or integrated with other systems.

---

## API Endpoints

### `GET /`
Returns basic service metadata and available endpoints.

### `GET /health`
Health check endpoint to verify that the service is running.

### `GET /docs`
Returns a JSON description of supported endpoints and expected payload formats.

### `POST /analyze`
Analyzes submitted logs/events and returns probable root causes.

#### Request Payload
```json
{
  "events": [
    {
      "timestamp": 1710000123,
      "service": "service_c",
      "level": "ERROR",
      "message": "Database connection lost"
    },
    {
      "timestamp": 1710000135,
      "service": "service_b",
      "level": "ERROR",
      "message": "Timeout while calling service_c"
    }
  ]
}
