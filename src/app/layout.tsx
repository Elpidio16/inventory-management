import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Inventory Management System",
  description: "Manage your inventory with entries and exits tracking",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-100">
        <nav className="bg-gray-900 text-white shadow-lg">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <h1 className="text-2xl font-bold">📦 Inventory Management</h1>
          </div>
        </nav>
        {children}
      </body>
    </html>
  );
}
