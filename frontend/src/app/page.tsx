"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, FileImage, Loader2, CheckCircle, XCircle, Building2 } from "lucide-react";

interface ExtractionResult {
  identity_resolution: {
    primary_company_name: string;
    english_name?: string;
    is_ambiguous: boolean;
    evidence_images: string[];
  };
  company: {
    name_printed: string;
    description?: string;
    business_type?: string;
    certifications?: string[];
  };
  products: Array<{
    name: string;
    category?: string;
    description?: string;
  }>;
  retrieval_brief: string;
}

interface IngestionResponse {
  session_id: string;
  status: string;
  company_id?: string;
  extraction_result?: ExtractionResult;
  error_message?: string;
}

export default function Home() {
  const [files, setFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<IngestionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles((prev) => [...prev, ...acceptedFiles]);
    setResult(null);
    setError(null);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/jpeg": [".jpg", ".jpeg"],
      "image/png": [".png"],
      "image/webp": [".webp"],
      "image/gif": [".gif"],
    },
    maxSize: 50 * 1024 * 1024, // 50MB
  });

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleUpload = async () => {
    if (files.length === 0) return;

    setUploading(true);
    setError(null);

    const formData = new FormData();
    files.forEach((file) => {
      formData.append("files", file);
    });
    formData.append("treat_as_single_bundle", "true");

    try {
      const response = await fetch("/api/v1/ingestion/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      const data: IngestionResponse = await response.json();
      setResult(data);

      if (data.status === "failed") {
        setError(data.error_message || "Processing failed");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  const clearAll = () => {
    setFiles([]);
    setResult(null);
    setError(null);
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Multi-Image Leaflet Ingestion
        </h1>
        <p className="text-gray-600">
          Upload multiple pages of company brochures to extract structured data
        </p>
      </div>

      {/* Upload Zone */}
      <div className="card mb-6">
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
            isDragActive
              ? "border-primary-500 bg-primary-50"
              : "border-gray-300 hover:border-gray-400"
          }`}
        >
          <input {...getInputProps()} />
          <Upload className="w-12 h-12 mx-auto text-gray-400 mb-4" />
          {isDragActive ? (
            <p className="text-primary-600 font-medium">Drop the images here...</p>
          ) : (
            <>
              <p className="text-gray-600 mb-2">
                Drag & drop leaflet images here, or click to select
              </p>
              <p className="text-sm text-gray-400">
                Supports JPG, PNG, WebP, GIF (max 50MB each)
              </p>
            </>
          )}
        </div>

        {/* File List */}
        {files.length > 0 && (
          <div className="mt-6">
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-medium text-gray-900">
                Selected Images ({files.length})
              </h3>
              <button onClick={clearAll} className="text-sm text-red-600 hover:text-red-700">
                Clear all
              </button>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {files.map((file, index) => (
                <div
                  key={index}
                  className="relative group bg-gray-100 rounded-lg overflow-hidden"
                >
                  <div className="aspect-square flex items-center justify-center">
                    <FileImage className="w-8 h-8 text-gray-400" />
                  </div>
                  <div className="absolute inset-x-0 bottom-0 bg-black/60 p-2">
                    <p className="text-white text-xs truncate">{file.name}</p>
                  </div>
                  <button
                    onClick={() => removeFile(index)}
                    className="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    <XCircle className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Upload Button */}
        {files.length > 0 && !result && (
          <div className="mt-6 flex justify-center">
            <button
              onClick={handleUpload}
              disabled={uploading}
              className="btn-primary flex items-center gap-2"
            >
              {uploading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Processing {files.length} images...
                </>
              ) : (
                <>
                  <Upload className="w-5 h-5" />
                  Process {files.length} Images
                </>
              )}
            </button>
          </div>
        )}
      </div>

      {/* Error Display */}
      {error && (
        <div className="card bg-red-50 border-red-200 mb-6">
          <div className="flex items-start gap-3">
            <XCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-medium text-red-800">Processing Error</h3>
              <p className="text-red-600 text-sm mt-1">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Results Display */}
      {result && result.status === "completed" && result.extraction_result && (
        <div className="space-y-6">
          {/* Success Header */}
          <div className="card bg-green-50 border-green-200">
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-medium text-green-800">
                  Successfully Extracted Data
                </h3>
                <p className="text-green-600 text-sm mt-1">
                  Found {result.extraction_result.products?.length || 0} products from{" "}
                  {result.extraction_result.identity_resolution?.primary_company_name}
                </p>
              </div>
            </div>
          </div>

          {/* Company Overview */}
          <div className="card">
            <div className="flex items-center gap-3 mb-4">
              <Building2 className="w-6 h-6 text-primary-600" />
              <h2 className="text-xl font-semibold">Company Overview</h2>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  {result.extraction_result.company.name_printed}
                </h3>
                {result.extraction_result.company.business_type && (
                  <p className="text-gray-500 text-sm mb-3">
                    {result.extraction_result.company.business_type}
                  </p>
                )}
                <p className="text-gray-600">
                  {result.extraction_result.company.description}
                </p>
              </div>

              {result.extraction_result.company.certifications &&
                result.extraction_result.company.certifications.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-500 mb-2">
                      Certifications
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {result.extraction_result.company.certifications.map(
                        (cert, i) => (
                          <span key={i} className="badge badge-green">
                            {cert}
                          </span>
                        )
                      )}
                    </div>
                  </div>
                )}
            </div>
          </div>

          {/* Products */}
          {result.extraction_result.products &&
            result.extraction_result.products.length > 0 && (
              <div className="card">
                <h2 className="text-xl font-semibold mb-4">
                  Products ({result.extraction_result.products.length})
                </h2>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {result.extraction_result.products.map((product, i) => (
                    <div
                      key={i}
                      className="bg-gray-50 rounded-lg p-4 border hover:border-primary-300 transition-colors"
                    >
                      <h3 className="font-medium text-gray-900">{product.name}</h3>
                      {product.category && (
                        <span className="badge badge-blue mt-1">
                          {product.category}
                        </span>
                      )}
                      {product.description && (
                        <p className="text-sm text-gray-600 mt-2 line-clamp-2">
                          {product.description}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

          {/* Retrieval Brief */}
          {result.extraction_result.retrieval_brief && (
            <div className="card bg-blue-50 border-blue-200">
              <h3 className="font-medium text-blue-800 mb-2">Retrieval Brief</h3>
              <p className="text-blue-700 text-sm">
                {result.extraction_result.retrieval_brief}
              </p>
            </div>
          )}

          {/* Actions */}
          <div className="flex gap-4 justify-center">
            {result.company_id && (
              <a
                href={`/companies/${result.company_id}`}
                className="btn-primary"
              >
                View Full Details
              </a>
            )}
            <button onClick={clearAll} className="btn-secondary">
              Process More Images
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
