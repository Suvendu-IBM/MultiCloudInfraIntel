/**
 * ChatWindow — scrollable list of chat messages.
 *
 * - User messages: right-aligned, brand-coloured background
 * - Assistant messages: left-aligned, surface background, Markdown rendered
 * - Error messages: left-aligned, red-tinted background
 *
 * Auto-scrolls to the latest message whenever the messages array changes.
 */

import React, { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import { CLOUD_PROVIDERS } from "../types";
import type { Message } from "../types";

interface Props {
  messages: Message[];
  loading: boolean;
}

/** Map cloud provider value → brand colour for the user bubble header */
const providerColor = (cp: string): string =>
  CLOUD_PROVIDERS.find((p) => p.value === cp)?.color ?? "#6366f1";

const ChatWindow: React.FC<Props> = ({ messages, loading }) => {
  const bottomRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom whenever messages change or loading state toggles
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <div className="chat-window" role="log" aria-live="polite" aria-label="Chat messages">
      {messages.length === 0 && !loading && (
        <div className="chat-empty">
          <p>Select a cloud provider above, then ask a question.</p>
          <p className="chat-empty-hint">
            Try: &ldquo;Which EC2 instances have been idle for the past 2 weeks?&rdquo;
          </p>
        </div>
      )}

      {messages.map((msg) => {
        if (msg.role === "user") {
          return (
            <div key={msg.id} className="message-row message-row--user">
              <div
                className="message-bubble message-bubble--user"
                style={{ borderColor: providerColor(msg.cloudProvider) }}
              >
                <div
                  className="message-meta"
                  style={{ color: providerColor(msg.cloudProvider) }}
                >
                  {CLOUD_PROVIDERS.find((p) => p.value === msg.cloudProvider)?.label ?? "All Clouds"}
                </div>
                <p className="message-text">{msg.text}</p>
              </div>
            </div>
          );
        }

        if (msg.role === "error") {
          return (
            <div key={msg.id} className="message-row message-row--assistant">
              <div className="message-bubble message-bubble--error">
                <div className="message-meta message-meta--error">Error</div>
                <p className="message-text">{msg.text}</p>
              </div>
            </div>
          );
        }

        // assistant
        return (
          <div key={msg.id} className="message-row message-row--assistant">
            <div className="message-bubble message-bubble--assistant">
              <div className="message-meta">AI Agent</div>
              <div className="message-markdown">
                <ReactMarkdown>{msg.text}</ReactMarkdown>
              </div>
            </div>
          </div>
        );
      })}

      {loading && (
        <div className="message-row message-row--assistant">
          <div className="message-bubble message-bubble--assistant">
            <div className="message-meta">AI Agent</div>
            <div className="loading-dots" aria-label="Loading response">
              <span />
              <span />
              <span />
            </div>
          </div>
        </div>
      )}

      {/* Scroll anchor */}
      <div ref={bottomRef} />
    </div>
  );
};

export default ChatWindow;
