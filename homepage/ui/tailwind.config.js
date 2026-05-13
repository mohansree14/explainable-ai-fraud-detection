/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                background: "#FFFFFF",
                bgSection: "#F8FAFC",
                card: "#EEF2F7",
                border: "#CBD5E1",
                navy: "#0B1F3A",
                navyHover: "#0F2A4D",
                primary: "#2563EB",
                heading: "#0F172A",
                body: "#334155",
                muted: "#64748B",
                accent: "#4ABAFF",
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
                serif: ['Georgia', 'serif'],
            }
        },
    },
    plugins: [],
}
