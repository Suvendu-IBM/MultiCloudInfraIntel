/**
 * Shared TypeScript types for the PESAMultiCloudIntel chat application.
 */

// ---------------------------------------------------------------------------
// Cloud provider
// ---------------------------------------------------------------------------

export type CloudProvider = "all" | "aws" | "azure" | "gcp";

export interface CloudProviderOption {
  value: CloudProvider;
  label: string;
  /** Brand colour used for the pill button */
  color: string;
}

export const CLOUD_PROVIDERS: CloudProviderOption[] = [
  { value: "all",   label: "All Clouds", color: "#6366f1" },
  { value: "aws",   label: "AWS",        color: "#f97316" },
  { value: "azure", label: "Azure",      color: "#3b82f6" },
  { value: "gcp",   label: "GCP",        color: "#ef4444" },
];

// ---------------------------------------------------------------------------
// Chat messages
// ---------------------------------------------------------------------------

export type MessageRole = "user" | "assistant" | "error";

export interface Message {
  id: string;
  role: MessageRole;
  text: string;
  cloudProvider: CloudProvider;
  timestamp: Date;
}

// ---------------------------------------------------------------------------
// API shapes
// ---------------------------------------------------------------------------

export interface ChatRequest {
  question: string;
  cloud_provider: CloudProvider;
}

export interface ChatResponse {
  answer: string;
  cloud_provider: string;
}
