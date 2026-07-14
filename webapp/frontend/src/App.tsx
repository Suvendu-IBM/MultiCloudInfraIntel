/**
 * App — root component for the PESAMultiCloudIntel chat UI.
 *
 * State managed here:
 *   messages      — full conversation history
 *   input         — current textarea value
 *   cloudProvider — selected provider pill (all | aws | azure | gcp)
 *   loading       — true while awaiting ICA API response
 */

import React, { useState, useCallback } from "react";
import "./App.css";

import CloudSelector from "./components/CloudSelector";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";
import { sendChat } from "./api/chat";
import type { CloudProvider, Message } from "./types";

/** Generate a simple unique id for each message */
const uid = (): string =>
  `${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;

const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");
  const [cloudProvider, setCloudProvider] = useState<CloudProvider>("all");
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = useCallback(async () => {
    const question = input.trim();
    if (!question || loading) return;

    // Append the user message immediately
    const userMsg: Message = {
      id: uid(),
      role: "user",
      text: question,
      cloudProvider,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const data = await sendChat(question, cloudProvider);

      const assistantMsg: Message = {
        id: uid(),
        role: "assistant",
        text: data.answer,
        cloudProvider,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      const errorMsg: Message = {
        id: uid(),
        role: "error",
        text: err instanceof Error ? err.message : "An unexpected error occurred.",
        cloudProvider,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  }, [input, cloudProvider, loading]);

  return (
    <div className="app">
      <header className="app-header">
        <h1 className="app-title">
          <span>PESA</span>MultiCloudIntel
        </h1>
        <CloudSelector
          selected={cloudProvider}
          onChange={setCloudProvider}
          disabled={loading}
        />
      </header>

      <main style={{ flex: 1, display: "flex", flexDirection: "column" as const, overflow: "hidden" }}>
        <ChatWindow messages={messages} loading={loading} />
        <ChatInput
          value={input}
          onChange={setInput}
          onSubmit={handleSubmit}
          loading={loading}
        />
      </main>
    </div>
  );
};

export default App;
