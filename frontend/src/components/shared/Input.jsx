import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export const Input = React.forwardRef(({ className, inputClassName, label, error, prefix, suffix, ...props }, ref) => {
  return (
    <div className={clsx("flex flex-col gap-1 w-full", className)}>
      {label && <label className="text-sm font-medium text-text-main">{label}</label>}
      
      <div className={clsx(
        "relative flex w-full items-center overflow-hidden rounded-2xl border border-border-color bg-white transition-all focus-within:border-city-blue focus-within:ring-4 focus-within:ring-[#ff870024]",
        error && "border-danger-red focus-within:ring-danger-red",
        props.disabled && "bg-[#f5efe6] opacity-50"
      )}>
        {prefix && (
          <span className="flex h-full items-center bg-slate-50 px-3 text-xs font-bold text-slate-400 border-r border-border-color/40 select-none">
            {prefix}
          </span>
        )}
        
        <input
          ref={ref}
          className={twMerge(clsx(
            "w-full bg-transparent px-4 py-3 text-sm text-text-main outline-none placeholder:text-text-muted disabled:cursor-not-allowed",
            inputClassName
          ))}
          {...props}
        />

        {suffix && (
          <span className="flex h-full items-center bg-slate-50 px-3 text-xs font-bold text-slate-400 border-l border-border-color/40 select-none">
            {suffix}
          </span>
        )}
      </div>
      
      {error && <span className="text-xs text-danger-red mt-1">{error}</span>}
    </div>
  );
});

Input.displayName = 'Input';
