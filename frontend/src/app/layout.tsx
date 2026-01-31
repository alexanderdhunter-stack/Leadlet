import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Leadlet - Multi-Image Leaflet Ingestion",
  description: "Extract and structure company information from brochures and leaflets",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gray-50">
          <nav className="bg-white shadow-sm border-b">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between h-16">
                <div className="flex items-center">
                  <a href="/" className="text-xl font-bold text-primary-600">
                    Leadlet
                  </a>
                </div>
                <div className="flex items-center space-x-4">
                  <a
                    href="/"
                    className="text-gray-600 hover:text-gray-900 px-3 py-2"
                  >
                    Upload
                  </a>
                  <a
                    href="/companies"
                    className="text-gray-600 hover:text-gray-900 px-3 py-2"
                  >
                    Companies
                  </a>
                  <a
                    href="/export"
                    className="text-gray-600 hover:text-gray-900 px-3 py-2"
                  >
                    Export
                  </a>
                </div>
              </div>
            </div>
          </nav>
          <main>{children}</main>
        </div>
      </body>
    </html>
  );
}
