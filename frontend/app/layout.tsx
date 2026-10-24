import "./globals.css";
import React from "react";

export const metadata = {
  title: "OpenKuta - Deterministic CAS Assessment & Vision Grader",
  description: "Procedural math worksheet generator, Typst layout engine, and CV line-by-line step grader",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css"
          crossOrigin="anonymous"
        />
      </head>
      <body className="antialiased font-sans">{children}</body>
    </html>
  );
}

