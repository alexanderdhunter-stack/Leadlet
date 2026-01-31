"use client";

import { useState, useEffect } from "react";
import { Download, FileSpreadsheet, Building2, Package, Award, Users } from "lucide-react";

interface Company {
  id: string;
  name_printed: string;
}

export default function ExportPage() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [selectedCompany, setSelectedCompany] = useState<string>("");

  useEffect(() => {
    fetchCompanies();
  }, []);

  const fetchCompanies = async () => {
    try {
      const response = await fetch("/api/v1/companies");
      if (response.ok) {
        const data = await response.json();
        setCompanies(data);
      }
    } catch (err) {
      console.error("Failed to fetch companies:", err);
    }
  };

  const handleDownload = (type: string) => {
    const params = selectedCompany ? `?company_id=${selectedCompany}` : "";
    window.open(`/api/v1/export/${type}/download${params}`, "_blank");
  };

  const exportTypes = [
    {
      id: "company-profile",
      name: "Company Profile",
      description: "Company overview, capabilities, certifications, and contact information",
      icon: Building2,
      color: "text-blue-600 bg-blue-100",
    },
    {
      id: "products",
      name: "Products",
      description: "Complete product catalogue with specs, claims, and categorization",
      icon: Package,
      color: "text-green-600 bg-green-100",
    },
    {
      id: "claims",
      name: "Claims & Certifications",
      description: "All claims and certifications at company and product level",
      icon: Award,
      color: "text-yellow-600 bg-yellow-100",
    },
    {
      id: "contacts",
      name: "Contacts",
      description: "Contact information including emails, phones, and addresses",
      icon: Users,
      color: "text-purple-600 bg-purple-100",
    },
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Export Data</h1>
        <p className="text-gray-600">
          Download extracted data as Excel-ready CSV files
        </p>
      </div>

      {/* Company Filter */}
      <div className="card mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Filter by Company (optional)
        </label>
        <select
          value={selectedCompany}
          onChange={(e) => setSelectedCompany(e.target.value)}
          className="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
        >
          <option value="">All Companies</option>
          {companies.map((company) => (
            <option key={company.id} value={company.id}>
              {company.name_printed}
            </option>
          ))}
        </select>
      </div>

      {/* Export Options */}
      <div className="grid md:grid-cols-2 gap-4">
        {exportTypes.map((type) => (
          <div key={type.id} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start gap-4">
              <div className={`p-3 rounded-lg ${type.color}`}>
                <type.icon className="w-6 h-6" />
              </div>
              <div className="flex-1">
                <h3 className="font-medium text-gray-900">{type.name}</h3>
                <p className="text-sm text-gray-600 mt-1">{type.description}</p>
                <button
                  onClick={() => handleDownload(type.id)}
                  className="mt-4 inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 font-medium text-sm"
                >
                  <Download className="w-4 h-4" />
                  Download CSV
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* CSV Format Info */}
      <div className="card mt-8 bg-gray-50">
        <div className="flex items-start gap-3">
          <FileSpreadsheet className="w-5 h-5 text-gray-400 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-medium text-gray-900">CSV Format</h3>
            <p className="text-sm text-gray-600 mt-1">
              All exports are in CSV format compatible with Microsoft Excel, Google Sheets,
              and other spreadsheet applications. Multi-value fields are separated by pipes (|)
              for easy parsing.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
