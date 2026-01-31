"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import {
  Building2,
  Package,
  Award,
  Globe,
  Mail,
  Phone,
  MapPin,
  ChevronLeft,
  Loader2,
  Download,
} from "lucide-react";

interface CompanyOverview {
  company_name: string;
  tagline?: string;
  short_description: string;
  business_type?: string;
  core_capabilities: string[];
  industries_served: string[];
  markets_regions: string[];
  certifications: string[];
  key_differentiators: string[];
  contact_summary: Record<string, string>;
}

interface ProductCard {
  id: string;
  name: string;
  category?: string;
  subcategory?: string;
  short_description: string;
  key_specs: Record<string, string>;
  formats: string[];
  claims: string[];
  certifications: string[];
  confidence: string;
}

interface ProductCatalogue {
  company_id: string;
  company_name: string;
  categories: Record<string, ProductCard[]>;
  total_products: number;
}

export default function CompanyDetailPage() {
  const params = useParams();
  const companyId = params.id as string;

  const [overview, setOverview] = useState<CompanyOverview | null>(null);
  const [catalogue, setCatalogue] = useState<ProductCatalogue | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeCategory, setActiveCategory] = useState<string | null>(null);

  useEffect(() => {
    if (companyId) {
      fetchData();
    }
  }, [companyId]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [overviewRes, catalogueRes] = await Promise.all([
        fetch(`/api/v1/companies/${companyId}/overview`),
        fetch(`/api/v1/companies/${companyId}/catalogue`),
      ]);

      if (overviewRes.ok) {
        const overviewData = await overviewRes.json();
        setOverview(overviewData);
      }

      if (catalogueRes.ok) {
        const catalogueData = await catalogueRes.json();
        setCatalogue(catalogueData);
        // Set first category as active
        const categories = Object.keys(catalogueData.categories || {});
        if (categories.length > 0) {
          setActiveCategory(categories[0]);
        }
      }
    } catch (err) {
      console.error("Failed to fetch company data:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async (type: string) => {
    window.open(`/api/v1/export/${type}/download?company_id=${companyId}`, "_blank");
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
      </div>
    );
  }

  if (!overview) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-8">
        <div className="card text-center py-12">
          <h3 className="text-lg font-medium text-gray-900">Company not found</h3>
          <a href="/companies" className="btn-primary inline-block mt-4">
            Back to Companies
          </a>
        </div>
      </div>
    );
  }

  const categories = Object.keys(catalogue?.categories || {});

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Back Link */}
      <a
        href="/companies"
        className="inline-flex items-center text-gray-600 hover:text-gray-900 mb-6"
      >
        <ChevronLeft className="w-4 h-4 mr-1" />
        Back to Companies
      </a>

      {/* Company Header */}
      <div className="card mb-6">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-3">
              <Building2 className="w-8 h-8 text-primary-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  {overview.company_name}
                </h1>
                {overview.tagline && (
                  <p className="text-gray-500 italic">{overview.tagline}</p>
                )}
              </div>
            </div>
          </div>

          {/* Export Menu */}
          <div className="relative group">
            <button className="btn-secondary flex items-center gap-2">
              <Download className="w-4 h-4" />
              Export
            </button>
            <div className="absolute right-0 top-full mt-2 bg-white rounded-lg shadow-lg border py-2 min-w-[160px] hidden group-hover:block z-10">
              <button
                onClick={() => handleExport("company-profile")}
                className="w-full text-left px-4 py-2 hover:bg-gray-100"
              >
                Company Profile
              </button>
              <button
                onClick={() => handleExport("products")}
                className="w-full text-left px-4 py-2 hover:bg-gray-100"
              >
                Products
              </button>
              <button
                onClick={() => handleExport("claims")}
                className="w-full text-left px-4 py-2 hover:bg-gray-100"
              >
                Claims
              </button>
              <button
                onClick={() => handleExport("contacts")}
                className="w-full text-left px-4 py-2 hover:bg-gray-100"
              >
                Contacts
              </button>
            </div>
          </div>
        </div>

        {/* Description */}
        <p className="text-gray-600 mt-4">{overview.short_description}</p>

        {/* Info Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
          {overview.business_type && (
            <div>
              <h4 className="text-sm font-medium text-gray-500 mb-1">
                Business Type
              </h4>
              <p className="text-gray-900">{overview.business_type}</p>
            </div>
          )}

          {overview.industries_served.length > 0 && (
            <div>
              <h4 className="text-sm font-medium text-gray-500 mb-2">
                Industries
              </h4>
              <div className="flex flex-wrap gap-1">
                {overview.industries_served.map((ind, i) => (
                  <span key={i} className="badge badge-blue">
                    {ind}
                  </span>
                ))}
              </div>
            </div>
          )}

          {overview.markets_regions.length > 0 && (
            <div>
              <h4 className="text-sm font-medium text-gray-500 mb-2">Markets</h4>
              <div className="flex flex-wrap gap-1">
                {overview.markets_regions.map((market, i) => (
                  <span key={i} className="badge badge-gray">
                    {market}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Certifications */}
        {overview.certifications.length > 0 && (
          <div className="mt-6 pt-6 border-t">
            <div className="flex items-center gap-2 mb-3">
              <Award className="w-5 h-5 text-green-600" />
              <h4 className="font-medium text-gray-900">Certifications</h4>
            </div>
            <div className="flex flex-wrap gap-2">
              {overview.certifications.map((cert, i) => (
                <span key={i} className="badge badge-green">
                  {cert}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Contact Summary */}
        {Object.keys(overview.contact_summary).length > 0 && (
          <div className="mt-6 pt-6 border-t">
            <h4 className="font-medium text-gray-900 mb-3">Contact</h4>
            <div className="flex flex-wrap gap-4">
              {overview.contact_summary.website && (
                <a
                  href={overview.contact_summary.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700"
                >
                  <Globe className="w-4 h-4" />
                  Website
                </a>
              )}
              {overview.contact_summary.email && (
                <a
                  href={`mailto:${overview.contact_summary.email}`}
                  className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-900"
                >
                  <Mail className="w-4 h-4" />
                  {overview.contact_summary.email}
                </a>
              )}
              {overview.contact_summary.phone && (
                <span className="inline-flex items-center gap-2 text-gray-600">
                  <Phone className="w-4 h-4" />
                  {overview.contact_summary.phone}
                </span>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Product Catalogue */}
      {catalogue && catalogue.total_products > 0 && (
        <div className="card">
          <div className="flex items-center gap-2 mb-6">
            <Package className="w-6 h-6 text-primary-600" />
            <h2 className="text-xl font-semibold">
              Product Catalogue ({catalogue.total_products})
            </h2>
          </div>

          {/* Category Tabs */}
          {categories.length > 1 && (
            <div className="flex flex-wrap gap-2 mb-6 pb-4 border-b">
              {categories.map((cat) => (
                <button
                  key={cat}
                  onClick={() => setActiveCategory(cat)}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                    activeCategory === cat
                      ? "bg-primary-600 text-white"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}
                >
                  {cat} ({catalogue.categories[cat].length})
                </button>
              ))}
            </div>
          )}

          {/* Products Grid */}
          {activeCategory && catalogue.categories[activeCategory] && (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {catalogue.categories[activeCategory].map((product) => (
                <div
                  key={product.id}
                  className="bg-gray-50 rounded-lg p-4 border hover:border-primary-300 transition-colors"
                >
                  <h3 className="font-medium text-gray-900">{product.name}</h3>
                  {product.subcategory && (
                    <span className="badge badge-gray text-xs mt-1">
                      {product.subcategory}
                    </span>
                  )}
                  {product.short_description && (
                    <p className="text-sm text-gray-600 mt-2 line-clamp-2">
                      {product.short_description}
                    </p>
                  )}

                  {/* Specs */}
                  {Object.keys(product.key_specs).length > 0 && (
                    <div className="mt-3 pt-3 border-t border-gray-200">
                      <div className="text-xs text-gray-500 space-y-1">
                        {Object.entries(product.key_specs)
                          .slice(0, 3)
                          .map(([key, val]) => (
                            <div key={key}>
                              <span className="font-medium">{key}:</span> {val}
                            </div>
                          ))}
                      </div>
                    </div>
                  )}

                  {/* Claims/Certs */}
                  {(product.claims.length > 0 || product.certifications.length > 0) && (
                    <div className="flex flex-wrap gap-1 mt-3">
                      {product.certifications.slice(0, 2).map((cert, i) => (
                        <span key={i} className="badge badge-green text-xs">
                          {cert}
                        </span>
                      ))}
                      {product.claims.slice(0, 2).map((claim, i) => (
                        <span key={i} className="badge badge-blue text-xs">
                          {claim}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
