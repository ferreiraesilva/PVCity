import React, { useState, useEffect, useCallback, useRef } from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * CurrencyInput - A specialized input for BRL currency and percentages.
 * - Handles pt-BR formatting (1.200,50) internally.
 * - Prevents cursor jumping.
 * - Accepts millions and precise decimal values.
 * - Exposes a raw numeric value to the parent.
 */
export const CurrencyInput = React.forwardRef(({ 
  value, 
  onValueChange, 
  prefix, 
  suffix, 
  variant = 'minimal',
  size = 'sm',
  precision = 2,
  isPercent = false,
  className,
  inputClassName,
  ...props 
}, ref) => {
  // Local string state to handle the raw user input without re-renders jumping the cursor
  const [displayValue, setDisplayValue] = useState('');
  const isEditing = useRef(false);

  // Formatter for pt-BR
  const format = useCallback((num) => {
    if (num === null || num === undefined || num === '') return '';
    return Number(num).toLocaleString('pt-BR', {
      minimumFractionDigits: precision,
      maximumFractionDigits: precision,
    });
  }, [precision]);

  // Sync external value to internal display value only when not editing
  useEffect(() => {
    if (!isEditing.current) {
      setDisplayValue(format(value));
    }
  }, [value, format]);

  const handleChange = (e) => {
    const rawValue = e.target.value;
    
    // Allow digits, one comma, and one hyphen for typing
    // Clean anything that isn't a digit or the decimal separator
    const cleaned = rawValue.replace(/[^\d,-]/g, '').replace(',', '.');
    const numericValue = parseFloat(cleaned);
    
    setDisplayValue(rawValue); // Keep what the user is typing exactly
    
    if (!isNaN(numericValue)) {
      onValueChange(numericValue);
    } else if (cleaned === '') {
      onValueChange('');
    }
  };

  const handleBlur = (e) => {
    isEditing.current = false;
    // Format strictly on blur to the canonical state
    setDisplayValue(format(value));
    if (props.onBlur) props.onBlur(e);
  };

  const handleFocus = (e) => {
    isEditing.current = true;
    if (props.onFocus) props.onFocus(e);
  };

  const isMinimal = variant === 'minimal';
  const isSmall = size === 'sm';

  return (
    <div className={clsx("relative flex w-full items-center overflow-hidden transition-all focus-within:ring-4 focus-within:ring-[#ff870024]", 
      isMinimal 
        ? "border-b border-transparent focus-within:border-city-blue focus-within:bg-white" 
        : "rounded-2xl border border-border-color bg-white focus-within:border-city-blue",
      props.disabled && "opacity-75"
    )}>
      {prefix && (
        <span className={clsx("flex h-full items-center text-[10px] font-black text-slate-400 select-none", isMinimal ? "pl-2 pr-1" : "bg-slate-50 px-3 border-r")}>
          {prefix}
        </span>
      )}
      
      <input
        ref={ref}
        type="text"
        className={twMerge(clsx(
          "w-full bg-transparent text-text-main outline-none placeholder:text-text-muted",
          isSmall ? "px-2 py-2 text-xs" : "px-4 py-3 text-sm",
          isMinimal && "px-1 py-1.5",
          inputClassName
        ))}
        value={displayValue}
        onChange={handleChange}
        onFocus={handleFocus}
        onBlur={handleBlur}
        {...props}
      />

      {suffix && (
        <span className={clsx("flex h-full items-center text-[10px] font-black text-slate-400 select-none", isMinimal ? "pr-2 pl-1" : "bg-slate-50 px-3 border-l")}>
          {suffix}
        </span>
      )}
    </div>
  );
});

CurrencyInput.displayName = 'CurrencyInput';
