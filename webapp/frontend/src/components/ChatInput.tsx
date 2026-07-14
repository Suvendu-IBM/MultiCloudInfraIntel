/**
 * ChatInput — textarea + Send button.
 *
 * - Enter submits the form
 * - Shift+Enter inserts a newline
 * - Disabled while a request is in flight (loading=true)
 * - Auto-focuses on mount
 */

import React, { useEffect, useRef } from "react";

interface Props {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  loading: boolean;
  placeholder?: string;
}

const ChatInput: React.FC<Props> = ({
  value,
  onChange,
  onSubmit,
  loading,
  placeholder = "Ask a question about your cloud infrastructure…",
}) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-focus on mount
  useEffect(() => {
    textareaRef.current?.focus();
  }, []);

  // Auto-resize textarea height to fit content (max 6 lines)
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 144)}px`; // 144px ≈ 6 lines
  }, [value]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!loading && value.trim()) {
        onSubmit();
      }
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!loading && value.trim()) {
      onSubmit();
    }
  };

  return (
    <form className="chat-input-form" onSubmit={handleSubmit} aria-label="Ask a question">
      <textarea
        ref={textareaRef}
        className="chat-input-textarea"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        disabled={loading}
        rows={1}
        aria-label="Question input"
        aria-describedby="send-hint"
      />
      <button
        type="submit"
        className="chat-input-send"
        disabled={loading || !value.trim()}
        aria-label="Send question"
      >
        {loading ? (
          <span className="send-spinner" aria-hidden="true" />
        ) : (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="currentColor"
            aria-hidden="true"
          >
            <path d="M2.01 21 23 12 2.01 3 2 10l15 2-15 2z" />
          </svg>
        )}
      </button>
      <span id="send-hint" className="sr-only">
        Press Enter to send, Shift+Enter for a new line.
      </span>
    </form>
  );
};

export default ChatInput;
