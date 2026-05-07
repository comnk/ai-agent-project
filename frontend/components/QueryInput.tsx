"use client";

import { useState } from "react";
import { useTheme } from "./ThemeProvider";

interface Props {
  onSubmit: (query: string) => void;
  loading: boolean;
}

export function QueryInput({ onSubmit, loading }: Props) {
  const [value, setValue] = useState("");
  const { theme, toggle } = useTheme();

  const handleSubmit = () => {
    if (value.trim() && !loading) onSubmit(value.trim());
  };

  const suggestions = [
    "Will AI replace software engineers?",
    "Is remote work better than office work?",
    "What jobs will automation eliminate?",
  ];

  return (
    <div className="w-full">
      <div className="relative">
        <textarea
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSubmit();
            }
          }}
          placeholder="Enter a research question..."
          rows={3}
          className="w-full resize-none rounded-xl border border-zinc-200 dark:border-zinc-700 
                     bg-white dark:bg-zinc-900 text-zinc-900 dark:text-zinc-100 
                     placeholder-zinc-400 dark:placeholder-zinc-500
                     px-5 py-4 text-base focus:outline-none focus:ring-2 
                     focus:ring-indigo-500 dark:focus:ring-indigo-400
                     transition-all duration-200 shadow-sm"
        />
      </div>

      <div className="mt-3 flex items-center justify-between gap-3">
        <div className="flex flex-wrap gap-2">
          {suggestions.map((s) => (
            <button
              key={s}
              onClick={() => setValue(s)}
              className="text-xs px-3 py-1.5 rounded-full border border-zinc-200 dark:border-zinc-700
                         text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100
                         hover:border-zinc-400 dark:hover:border-zinc-500 transition-all duration-150"
            >
              {s}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <button
            onClick={toggle}
            className="p-2 rounded-lg border border-zinc-200 dark:border-zinc-700
                       text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100
                       transition-all duration-150"
            title="Toggle theme"
          >
            {theme === "dark" ? (
              <svg
                className="w-4 h-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707M17.657 17.657l-.707-.707M6.343 6.343l-.707-.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
                />
              </svg>
            ) : (
              <svg
                className="w-4 h-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
                />
              </svg>
            )}
          </button>

          <button
            onClick={handleSubmit}
            disabled={!value.trim() || loading}
            className="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 
                       disabled:opacity-40 disabled:cursor-not-allowed
                       text-white font-medium text-sm transition-all duration-150
                       shadow-sm hover:shadow-indigo-500/25 hover:shadow-md"
          >
            {loading ? "Analyzing..." : "Run Analysis"}
          </button>
        </div>
      </div>
    </div>
  );
}
