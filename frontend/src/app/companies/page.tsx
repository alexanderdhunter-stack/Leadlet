"use client";

import { useEffect, useState } from "react";
import { Building2, Search, ChevronRight, Loader2 } from "lucide-react";

interface Company {
  id: string;
  name_printed: string;
  name_english?: string;
  business_type?: string;
  description?: string;
  certifications?: string[];
  industries_served?: string[];
  created_at: string;
}

export default function CompaniesPage() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetchCompanies();
  }, []);

  const fetchCompanies = async (searchTerm?: string) => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (searchTerm) params.set("search", searchTerm);

      const response = await fetch(`/api/v1/companies?${params}`);
      if (response.ok) {
        const data = await response.json();
        setCompanies(data);
      }
    } catch (err) {
      console.error("Failed to fetch companies:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchCompanies(search);
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Companies</h1>
          <p className="text-gray-600 mt-1">
            Browse all extracted company profiles
          </p>
        </div>
        <a href="/" className="btn-primary">
          + Add New
        </a>
      </div>

      {/* Search */}
      <form onSubmit={handleSearch} className="mb-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search companies..."
            className="w-full pl-10 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>
      </form>

      {/* Company List */}
      {loading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
        </div>
      ) : companies.length === 0 ? (
        <div className="card text-center py-12">
          <Building2 className="w-12 h-12 mx-auto text-gray-300 mb-4" />
          <h3 className="text-lg font-medium text-gray-900">No companies yet</h3>
          <p className="text-gray-600 mt-1 mb-4">
            Upload leaflet images to extract company data
          </p>
          <a href="/" className="btn-primary inline-block">
            Upload Images
          </a>
        </div>
      ) : (
        <div className="space-y-4">
          {companies.map((company) => (
            <a
              key={company.id}
              href={`/companies/${company.id}`}
              className="card block hover:shadow-md transition-shadow group"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3">
                    <Building2 className="w-5 h-5 text-primary-600 flex-shrink-0" />
                    <h3 className="text-lg font-medium text-gray-900 group-hover:text-primary-600">
                      {company.name_printed}
                    </h3>
                  </div>
                  {company.name_english && company.name_english !== company.name_printed && (
                    <p className="text-gray-500 text-sm mt-1 ml-8">
                      {company.name_english}
                    </p>
                  )}
                  {company.description && (
                    <p className="text-gray-600 mt-2 ml-8 line-clamp-2">
                      {company.description}
                    </p>
                  )}
                  <div className="flex flex-wrap gap-2 mt-3 ml-8">
                    {company.business_type && (
                      <span className="badge badge-gray">{company.business_type}</span>
                    )}
                    {company.industries_served?.slice(0, 3).map((industry, i) => (
                      <span key={i} className="badge badge-blue">
                        {industry}
                      </span>
                    ))}
                    {company.certifications?.slice(0, 2).map((cert, i) => (
                      <span key={i} className="badge badge-green">
                        {cert}
                      </span>
                    ))}
                  </div>
                </div>
                <ChevronRight className="w-5 h-5 text-gray-400 group-hover:text-primary-600 flex-shrink-0" />
              </div>
            </a>
          ))}
        </div>
      )}
    </div>
  );
}
