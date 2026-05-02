/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'gray': {
          '50': '#f9fafb',
          '100': '#f3f4f6',
          '200': '#e5e7eb',
          '300': '#d1d5db',
          '400': '#9ca3af',
          '500': '#6b7280',
          '600': '#4b5563',
          '700': '#374151',
          '800': '#1f2937',
          '900': '#111827',
        },
        'blue': {
          '500': '#3b82f6',
          '600': '#2563eb',
        },
        'yellow': {
          '400': '#facc15',
          '500': '#eab308',
        },
        'red': {
          '500': '#ef4444',
          '600': '#dc2626',
        },
      }
    },
  },
  plugins: [],
  safelist: [
    'bg-white', 'bg-gray-50', 'bg-gray-100', 'bg-gray-700', 'bg-gray-800', 'bg-gray-900',
    'text-white', 'text-black', 'text-gray-300', 'text-gray-400', 'text-gray-600', 'text-blue-600', 'text-red-600', 'text-yellow-500',
    'border', 'border-gray-200', 'border-gray-600', 'border-t', 'border-b',
    'shadow', 'shadow-lg', 'hover:shadow-lg',
    'rounded-lg', 'rounded-md',
    'p-4', 'p-6', 'px-4', 'py-2', 'py-3', 'px-6',
    'mb-2', 'mb-3', 'mb-4', 'mb-6', 'gap-1', 'gap-2', 'gap-3', 'gap-4', 'gap-6', 'gap-8',
    'grid', 'grid-cols-2', 'grid-cols-4', 'grid-cols-6',
    'flex', 'flex-col', 'items-center', 'justify-between',
    'font-bold', 'font-semibold', 'text-xs', 'text-sm', 'text-xl',
    'max-w-7xl', 'w-full', 'h-40', 'h-full', 'min-h-screen',
    'hover:opacity-80', 'hover:shadow-lg', 'transition',
    'line-clamp-2', 'truncate',
  ]
}
