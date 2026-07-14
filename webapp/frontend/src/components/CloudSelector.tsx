/**
 * CloudSelector — pill/tab buttons for choosing the active cloud provider.
 *
 * Active:   filled background (brand colour) + white text
 * Inactive: transparent background + coloured border + coloured text
 */

import React from "react";
import { CLOUD_PROVIDERS } from "../types";
import type { CloudProvider } from "../types";

interface Props {
  selected: CloudProvider;
  onChange: (provider: CloudProvider) => void;
  disabled?: boolean;
}

const CloudSelector: React.FC<Props> = ({ selected, onChange, disabled = false }) => {
  return (
    <div className="cloud-selector" role="group" aria-label="Select cloud provider">
      {CLOUD_PROVIDERS.map((option) => {
        const isActive = selected === option.value;
        return (
          <button
            key={option.value}
            type="button"
            className="cloud-pill"
            aria-pressed={isActive}
            disabled={disabled}
            onClick={() => onChange(option.value)}
            style={
              isActive
                ? {
                    backgroundColor: option.color,
                    borderColor: option.color,
                    color: "#ffffff",
                  }
                : {
                    backgroundColor: "transparent",
                    borderColor: option.color,
                    color: option.color,
                  }
            }
          >
            {option.label}
          </button>
        );
      })}
    </div>
  );
};

export default CloudSelector;
