"use client";

import Image from "next/image";

interface Props {
  sources: string[];
}

function getDomain(url: string) {
  try {
    return new URL(url).hostname.replace("www.", "");
  } catch {
    return url;
  }
}

export function SourcesList({ sources }: Props) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="rounded-xl border border-zinc-200 dark:border-zinc-800 overflow-hidden">
      <div
        className="px-5 py-4 border-b border-zinc-200 dark:border-zinc-800
                      bg-white dark:bg-zinc-900"
      >
        <h2 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
          Sources
          <span className="ml-2 text-xs font-normal text-zinc-400 dark:text-zinc-500">
            {sources.length} references
          </span>
        </h2>
      </div>
      <div className="p-4 bg-white dark:bg-zinc-900">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {sources.map((url, i) => (
            <a
              key={i}
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-3 p-3 rounded-lg border border-zinc-100 dark:border-zinc-800
                         hover:border-zinc-300 dark:hover:border-zinc-600 
                         hover:bg-zinc-50 dark:hover:bg-zinc-800/50
                         transition-all duration-150 group"
            >
              <div className="w-7 h-7 rounded-md bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center shrink-0">
                <Image
                  src={`https://www.google.com/s2/favicons?domain=${getDomain(url)}&sz=32`}
                  alt=""
                  className="w-4 h-4"
                  onError={(e) => {
                    (e.target as HTMLImageElement).style.display = "none";
                  }}
                  width="50"
                  height="50"
                />
              </div>
              <div className="min-w-0">
                <p
                  className="text-xs font-medium text-zinc-700 dark:text-zinc-300 truncate
                               group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors"
                >
                  {getDomain(url)}
                </p>
                <p className="text-xs text-zinc-400 dark:text-zinc-500 truncate">
                  {url}
                </p>
              </div>
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}
