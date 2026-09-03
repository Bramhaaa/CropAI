import React, { useState } from 'react';
import { Upload, Scan, AlertCircle, Shield, Eye } from 'lucide-react';
import { api } from '../api/client';
import MetricCard from '../components/MetricCard';

export function DiseaseDiagnosis() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (file) => {
    if (!file) return;
    if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) {
      setError('UNSUPPORTED FORMAT. PLEASE UPLOAD JPG, PNG, OR WEBP.');
      return;
    }
    setError(null);
    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setResult(null);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;
    setLoading(true);
    setError(null);

    try {
      const data = await api.predictDisease(selectedFile);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'INFERENCE ENGINE FAILURE. PLEASE TRY AGAIN.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <div className="flex items-center space-x-2 text-xs font-mono-tech text-[var(--text-muted)] mb-1">
          <Scan className="w-3.5 h-3.5" />
          <span>MODULE 01 / VISION MODEL</span>
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-[var(--text-primary)] font-mono-tech">
          PLANT PATHOLOGY DIAGNOSIS
        </h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Image Upload */}
        <div className="lg:col-span-5 space-y-4">
          <div className="bg-[var(--bg-card)] border border-[var(--border-card)] rounded-xl p-5 space-y-4 transition-colors duration-300">
            <span className="text-xs font-mono-tech text-[var(--text-primary)] font-medium block">
              INPUT LEAF IMAGE
            </span>

            <div
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleDrop}
              className="border-2 border-dashed border-[var(--border-card)] rounded-lg p-6 text-center hover:border-[var(--border-hover)] transition-colors cursor-pointer bg-[var(--bg-inner)] relative"
            >
              <input
                type="file"
                accept="image/jpeg,image/png,image/webp"
                onChange={(e) => e.target.files && handleFileChange(e.target.files[0])}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />

              {previewUrl ? (
                <div className="space-y-3">
                  <img
                    src={previewUrl}
                    alt="Selected leaf"
                    className="max-h-56 mx-auto rounded border border-[var(--border-card)] object-contain"
                  />
                  <p className="text-[11px] font-mono-tech text-[var(--text-muted)] truncate">
                    {selectedFile?.name}
                  </p>
                </div>
              ) : (
                <div className="space-y-3 py-4">
                  <div className="w-10 h-10 mx-auto rounded-full bg-[var(--bg-card)] border border-[var(--border-card)] flex items-center justify-center text-[var(--text-muted)]">
                    <Upload className="w-5 h-5" />
                  </div>
                  <div className="space-y-1">
                    <p className="text-xs font-mono-tech text-[var(--text-primary)]">DROP LEAF IMAGE HERE OR CLICK TO BROWSE</p>
                    <p className="text-[10px] font-mono-tech text-[var(--text-muted)]">FORMATS: JPG, PNG, WEBP (MAX 5MB)</p>
                  </div>
                </div>
              )}
            </div>

            {error && (
              <div className="bg-[var(--bg-inner)] border border-[var(--border-card)] text-[var(--text-primary)] text-xs font-mono-tech p-3 rounded flex items-center space-x-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <button
              onClick={handleAnalyze}
              disabled={!selectedFile || loading}
              className={`w-full py-3 rounded font-mono-tech text-xs font-semibold tracking-wider cursor-pointer ${
                !selectedFile || loading
                  ? 'bg-[var(--bg-inner)] text-[var(--text-dim)] border border-[var(--border-card)] cursor-not-allowed'
                  : 'btn-invert'
              }`}
            >
              {loading ? 'RUNNING DIAGNOSIS...' : 'EXECUTE DIAGNOSIS'}
            </button>
          </div>
        </div>

        {/* Right Column: Results */}
        <div className="lg:col-span-7 space-y-6">
          {result ? (
            <div className="space-y-6">
              {/* Primary Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <MetricCard
                  label="PREDICTED DIAGNOSIS"
                  value={result.prediction.replace(/___/g, ' - ')}
                  badge="PATHOGEN"
                />
                <MetricCard
                  label="CONFIDENCE SCORE"
                  value={`${(result.confidence * 100).toFixed(1)}%`}
                  badge="CALIBRATED"
                />
              </div>

              {/* Uncertainty Metric Panel */}
              <div className="bg-[var(--bg-card)] border border-[var(--border-card)] rounded-xl p-5 space-y-3 font-mono-tech transition-colors duration-300">
                <div className="flex items-center justify-between text-xs text-[var(--text-primary)] font-medium">
                  <span className="flex items-center space-x-2">
                    <Shield className="w-3.5 h-3.5" />
                    <span>PREDICTIVE UNCERTAINTY (MC DROPOUT 10-PASS)</span>
                  </span>
                  <span className="text-[var(--text-muted)]">{result.uncertainty.reliability.toUpperCase()} RELIABILITY</span>
                </div>
                <div className="grid grid-cols-2 gap-4 pt-1 text-xs">
                  <div className="bg-[var(--bg-inner)] border border-[var(--border-card)] p-3 rounded">
                    <span className="text-[var(--text-muted)] text-[10px] block">PREDICTIVE ENTROPY</span>
                    <span className="text-[var(--text-primary)] font-bold text-sm">{result.uncertainty.entropy.toFixed(4)}</span>
                  </div>
                  <div className="bg-[var(--bg-inner)] border border-[var(--border-card)] p-3 rounded">
                    <span className="text-[var(--text-muted)] text-[10px] block">NORMALIZED ENTROPY</span>
                    <span className="text-[var(--text-primary)] font-bold text-sm">{result.uncertainty.normalized_entropy.toFixed(4)}</span>
                  </div>
                </div>
              </div>

              {/* Top Probabilities Table */}
              <div className="bg-[var(--bg-card)] border border-[var(--border-card)] rounded-xl p-5 space-y-3 font-mono-tech transition-colors duration-300">
                <span className="text-xs text-[var(--text-primary)] font-medium block uppercase tracking-wider">
                  TOP PROBABILITY DISTRIBUTION
                </span>
                <div className="space-y-2 pt-1">
                  {result.top_predictions.slice(0, 4).map((item, idx) => (
                    <div key={idx} className="space-y-1">
                      <div className="flex justify-between text-xs text-[var(--text-primary)]">
                        <span>{item.class.replace(/___/g, ' - ')}</span>
                        <span>{(item.probability * 100).toFixed(1)}%</span>
                      </div>
                      <div className="h-1.5 bg-[var(--bar-track)] rounded-full overflow-hidden">
                        <div
                          style={{ width: `${item.probability * 100}%` }}
                          className="h-full bg-[var(--bar-bg)] rounded-full"
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Grad-CAM Overlay */}
              {result.explanation?.overlay_base64 && (
                <div className="bg-[var(--bg-card)] border border-[var(--border-card)] rounded-xl p-5 space-y-3 font-mono-tech transition-colors duration-300">
                  <div className="flex items-center space-x-2 text-xs text-[var(--text-primary)] font-medium">
                    <Eye className="w-3.5 h-3.5" />
                    <span>GRAD-CAM VISUAL EXPLANATION MAP</span>
                  </div>
                  <div className="pt-2">
                    <img
                      src={`data:image/png;base64,${result.explanation.overlay_base64}`}
                      alt="Grad-CAM Overlay"
                      className="max-h-72 mx-auto rounded border border-[var(--border-card)] object-contain"
                    />
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="bg-[var(--bg-card)] border border-[var(--border-card)] rounded-xl p-12 text-center font-mono-tech space-y-3 transition-colors duration-300">
              <Scan className="w-8 h-8 text-[var(--text-dim)] mx-auto" />
              <p className="text-xs text-[var(--text-muted)]">AWAITING IMAGE INPUT FOR DIAGNOSIS</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default DiseaseDiagnosis;
