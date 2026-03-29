import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export const Input = React.forwardRef(({ className, label, error, ...props }, ref) => {
  return (
    <div className="flex flex-col gap-1 w-full">
      {label && <label className="text-sm font-medium text-text-main">{label}</label>}
      <input
        ref={ref}
        className={twMerge(clsx(
          "w-full rounded-2xl border border-border-color bg-white px-4 py-3 text-text-main transition-all focus:border-city-blue focus:outline-none focus:ring-4 focus:ring-[#ff870024] disabled:bg-[#f5efe6] disabled:opacity-50",
          error && "border-danger-red focus:ring-danger-red",
          className
        ))}
        {...props}
      />
      {error && <span className="text-xs text-danger-red mt-1">{error}</span>}
    </div>
  );
});

Input.displayName = 'Input';
