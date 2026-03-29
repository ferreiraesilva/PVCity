import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function Button({ className, variant = 'primary', children, ...props }) {
  const baseStyle = "inline-flex cursor-pointer items-center justify-center rounded-full px-5 py-2.5 font-semibold transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50";
  
  const variants = {
    primary: "bg-city-blue text-city-blue-dark hover:-translate-y-0.5 hover:bg-[#ff961f] focus:ring-city-blue-light",
    secondary: "bg-[#fff1dc] text-city-blue-dark hover:bg-[#ffe7c0] focus:ring-city-blue-light",
    success: "bg-success-green text-white hover:-translate-y-0.5 hover:bg-[#27785a] focus:ring-success-green",
    outline: "border border-[#d7c4aa] bg-white text-city-blue-dark hover:bg-[#fff8ef] focus:ring-city-blue-light"
  };

  return (
    <button className={twMerge(clsx(baseStyle, variants[variant], className))} {...props}>
      {children}
    </button>
  );
}
