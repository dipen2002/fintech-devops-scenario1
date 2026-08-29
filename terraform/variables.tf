# ==============================================================================
# FinTechFlow - Terraform Variables Definition
# ==============================================================================

variable "environment" {
  description = "Target deployment environment (development, staging, production)"
  type        = string
  default     = "staging"

  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be one of: development, staging, production."
  }
}

variable "app_name" {
  description = "Name of the application service"
  type        = string
  default     = "FinTechFlow"
}

variable "app_version" {
  description = "Semantic version of the container image release"
  type        = string
  default     = "1.0.0"
}

variable "container_port" {
  description = "Container internal listening port"
  type        = number
  default     = 5000
}

variable "blue_slot_port" {
  description = "Host routing port for Blue production slot"
  type        = number
  default     = 5001
}

variable "green_slot_port" {
  description = "Host routing port for Green staging/candidate slot"
  type        = number
  default     = 5002
}

variable "active_traffic_slot" {
  description = "Active target group receiving live user traffic (blue or green)"
  type        = string
  default     = "blue"

  validation {
    condition     = contains(["blue", "green"], var.active_traffic_slot)
    error_message = "Active traffic slot must be either 'blue' or 'green'."
  }
}

variable "enable_observability" {
  description = "Flag to enable metrics collection and health check polling"
  type        = bool
  default     = true
}
