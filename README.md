# Serverless URL Shortener with Full Observability on AWS

A production-style serverless URL shortener built to demonstrate DevOps and Platform Engineering skills — IaC, least-privilege IAM, and a full observability stack.

## Architecture

![Architecture Diagram](flowchartURL.png)

**YACE port changed in newer versions**  
The official documentation and most tutorials reference port `5608` as YACE's metrics 
port. In v0.65.0+, YACE listens internally on port `5000`. So in Docker Compose one
 has to map `5608:5000` instead of `5608:5608`.
