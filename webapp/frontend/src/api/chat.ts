/**
 * API client for the PESAMultiCloudIntel backend.
 *
 * All requests go to /api/chat, which Vite proxies to http://localhost:8001
 * during development.  In production, a reverse proxy handles the routing.
 */

import axios, { AxiosError } from "axios";
import type { ChatRequest, ChatResponse } from "../types";

const api = axios.create({
  baseURL: "/",
  headers: { "Content-Type": "application/json" },
});

/**
 * Send a question to the ICA Workflow API via the backend adapter.
 *
 * @param question       Natural language question from the user.
 * @param cloudProvider  One of: all | aws | azure | gcp.
 * @returns              The AI-generated answer string.
 * @throws               Error with a user-readable message on failure.
 */
export async function sendChat(
  question: string,
  cloudProvider: string
): Promise<ChatResponse> {
  const payload: ChatRequest = {
    question,
    cloud_provider: cloudProvider as ChatRequest["cloud_provider"],
  };

  try {
    const response = await api.post<ChatResponse>("/api/chat", payload);
    return response.data;
  } catch (err) {
    const axiosErr = err as AxiosError<{ detail?: string }>;

    // Server returned an error response (4xx / 5xx)
    if (axiosErr.response) {
      const detail = axiosErr.response.data?.detail;
      const status = axiosErr.response.status;

      if (status === 422) {
        throw new Error(
          detail
            ? `Validation error: ${detail}`
            : "Invalid request — check the question and cloud provider."
        );
      }
      if (status === 502) {
        throw new Error(
          detail ?? "The ICA Workflow API is unavailable. Please try again."
        );
      }
      throw new Error(detail ?? `Server error (HTTP ${status}).`);
    }

    // Network error or request never left the browser
    if (axiosErr.request) {
      throw new Error(
        "Cannot reach the backend. Make sure the server is running on port 8001."
      );
    }

    // Unexpected error
    throw new Error("An unexpected error occurred. Please try again.");
  }
}
