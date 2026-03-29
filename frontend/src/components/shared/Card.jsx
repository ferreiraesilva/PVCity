import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function Card({ className, children, ...props }) {
  return (
    <div className={twMerge(clsx("card-panel rounded-[28px] p-6", className))} {...props}>
      {children}
    </div>
  );
}
