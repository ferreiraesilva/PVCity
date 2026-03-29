import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export const Select = React.forwardRef(({ 
  className, 
  label, 
  options = [], 
  error, 
  variant = 'default',
  size = 'md',
  ...props 
}, ref) => {
  const isMinimal = variant === 'minimal';
  const isSmall = size === 'sm';

  return (
    <div className={clsx("flex flex-col gap-1 w-full", className)}>
      {label && <label className="text-sm font-medium text-text-main">{label}</label>}
      <select
        ref={ref}
        className={twMerge(clsx(
          "w-full appearance-none transition-all focus:outline-none focus:ring-4 focus:ring-[#ff870024] disabled:cursor-not-allowed",
          isMinimal 
            ? "border-b border-transparent bg-transparent focus:border-city-blue focus:bg-white" 
            : "rounded-2xl border border-border-color bg-white focus:border-city-blue",
          isSmall ? "px-2 py-2 text-xs" : "px-4 py-3 text-sm",
          isMinimal && "px-1 py-1.5",
          error && "border-danger-red focus:ring-danger-red",
          props.disabled && !isMinimal && "bg-[#f5efe6] opacity-50",
          props.disabled && isMinimal && "opacity-75"
        ))}
        {...props}
      >
        <option value="" disabled hidden>Selecione...</option>
        {options.map((opt, i) => (
          <option key={i} value={opt.value !== undefined ? opt.value : opt}>
            {opt.label || opt}
          </option>
        ))}
      </select>
      {error && <span className="text-xs text-danger-red mt-1">{error}</span>}
    </div>
  );
});

Select.displayName = 'Select';
