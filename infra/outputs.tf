output "api_invoke_url" {
  value       = aws_apigatewayv2_stage.default.invoke_url
  description = "API Gateway invoke URL"
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.url_shortener.name
}
