import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export const Input = React.forwardRef(({ 
  className, 
  inputClassName, 
  label, 
  error, 
  prefix, 
  suffix, 
  variant = 'default', // 'default' or 'minimal'
  size = 'md', // 'md' or 'sm'
  ...props 
}, ref) => {
  const isMinimal = variant === 'minimal';
  const isSmall = size === 'sm';

  return (
    <div className={clsx("flex flex-col gap-1 w-full", className)}>
      {label && <label className="text-sm font-medium text-text-main">{label}</label>}
      
      <div className={clsx(
        "relative flex w-full items-center overflow-hidden transition-all focus-within:ring-4 focus-within:ring-[#ff870024]",
        isMinimal 
          ? "border-b border-transparent focus-within:border-city-blue focus-within:bg-white" 
          : "rounded-2xl border border-border-color bg-white focus-within:border-city-blue",
        error && "border-danger-red focus-within:ring-danger-red",
        props.disabled && !isMinimal && "bg-[#f5efe6] opacity-50",
        props.disabled && isMinimal && "opacity-75"
      )}>
        {prefix && (
          <span className={clsx(
            "flex h-full items-center text-[10px] font-black text-slate-400 select-none",
            isMinimal ? "pl-2 pr-1" : "bg-slate-50 px-3 border-r border-border-color/40"
          )}>
            {prefix}
          </span>
        )}
        
        <input
          ref={ref}
          className={twMerge(clsx(
            "w-full bg-transparent text-text-main outline-none placeholder:text-text-muted disabled:cursor-not-allowed",
            isSmall ? "px-2 py-2 text-xs" : "px-4 py-3 text-sm",
            isMinimal && "px-1 py-1.5",
            inputClassName
          ))}
          {...props}
        />

        {suffix && (
          <span className={clsx(
            "flex h-full items-center text-[10px] font-black text-slate-400 select-none",
            isMinimal ? "pr-2 pl-1" : "bg-slate-50 px-3 border-l border-border-color/40"
          )}>
            {suffix}
          </span>
        )}
      </div>
      
      {error && <span className="text-xs text-danger-red mt-1">{error}</span>}
    </div>
  );
});

Input.displayName = 'Input';
