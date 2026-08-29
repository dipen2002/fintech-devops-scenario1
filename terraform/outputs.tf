# ==============================================================================
# FinTechFlow - Terraform Infrastructure Outputs
# ==============================================================================

output "environment" {
  description = "Target deployment environment"
  value       = var.environment
}

output "application_name" {
  description = "Application service name"
  value       = var.app_name
}

output "application_version" {
  description = "Current deployed application version"
  value       = var.app_version
}

output "active_traffic_slot" {
  description = "Slot currently serving live user requests"
  value       = var.active_traffic_slot
}

output "active_service_url" {
  description = "Simulated primary load balancer endpoint"
  value       = "http://localhost:${var.active_traffic_slot == "blue" ? var.blue_slot_port : var.green_slot_port}"
}

output "blue_slot_url" {
  description = "Blue slot endpoint (Production Baseline)"
  value       = "http://localhost:${var.blue_slot_port}"
}

output "green_slot_url" {
  description = "Green slot endpoint (Release Candidate)"
  value       = "http://localhost:${var.green_slot_port}"
}

output "health_check_endpoint" {
  description = "Automated health check probe URL"
  value       = "http://localhost:${var.active_traffic_slot == "blue" ? var.blue_slot_port : var.green_slot_port}/health"
}

output "metrics_endpoint" {
  description = "Application metrics URL"
  value       = "http://localhost:${var.active_traffic_slot == "blue" ? var.blue_slot_port : var.green_slot_port}/metrics"
}

output "manifest_path" {
  description = "Path to the generated infrastructure deployment manifest"
  value       = local_file.environment_manifest.filename
}
