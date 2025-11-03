import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Videogames Chatbot - AI Gaming Assistant",
  description: "AI-powered chatbot for Steam games with advanced search and analysis",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
