import React, { useState } from 'react';
import { Sprout, AlertCircle } from 'lucide-react';
import { api } from '../api/client';
import MetricCard from '../components/MetricCard';
import SliderInput from '../components/SliderInput';
import MonochromeShapChart from '../components/MonochromeShapChart';

export function CropRecommendation() {
  const [params, setParams] = useState({
    nitrogen: 50,
    phosphorus: 50,
    potassium: 50,
    temperature: 25.0,
    humidity: 75.0,
    ph: 6.5,
    rainfall: 120.0,
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const updateParam = (key, val) => {
    setParams((prev) => ({ ...prev, [key]: val }));
  };

  const handleRecommend = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.recommendCrop(params);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'RECOMMENDATION ENGINE FAILURE.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-5">
      {/* Header */}
      <div>
        <div className="flex items-center space-x-2 text-xs font-mono-tech text-[var(--text-muted)] mb-1">
          <Sprout className="w-3.5 h-3.5" />
          <span>MODULE 02 / TABULAR CLASSIFIER</span>
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-[var(--text-primary)] font-mono-tech">
          CROP RECOMMENDATION ENGINE
        </h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column: Inputs */}
        <div className="lg:col-span-5 space-y-3">
          <div className="bg-[var(--bg-card)] border border-[var(--border-card)] rounded-xl p-4 sm:p-5 space-y-3 font-mono-tech transition-colors duration-300">
            <span className="text-xs text-[var(--text-primary)] font-medium block border-b border-[var(--border-card)] pb-2">
              SOIL & CLIMATIC METRICS
            </span>

            <div className="space-y-2">
              <SliderInput
                label="NITROGEN (N)"
                min={0}
                max={140}
                value={params.nitrogen}
                onChange={(v) => updateParam('nitrogen', v)}
                unit="mg/kg"
              />
              <SliderInput
                label="PHOSPHORUS (P)"
                min={5}
                max={145}
                value={params.phosphorus}
                onChange={(v) => updateParam('phosphorus', v)}
                unit="mg/kg"
              />
              <SliderInput
                label="POTASSIUM (K)"
                min={5}
                max={205}
                value={params.potassium}
                onChange={(v) => updateParam('potassium', v)}
                unit="mg/kg"
              />
              <SliderInput
                label="TEMPERATURE"
                min={10}
                max={50}
                step={0.5}
                value={params.temperature}
                onChange={(v) => updateParam('temperature', v)}
                unit="°C"
              />
              <SliderInput
                label="HUMIDITY"
                min={10}
                max={100}
                value={params.humidity}
                onChange={(v) => updateParam('humidity', v)}
                unit="%"
              />
              <SliderInput
                label="SOIL PH"
                min={3.5}
                max={10.0}
                step={0.1}
                value={params.ph}
                onChange={(v) => updateParam('ph', v)}
              />
              <SliderInput
                label="RAINFALL"
                min={20}
                max={300}
                value={params.rainfall}
                onChange={(v) => updateParam('rainfall', v)}
                unit="mm"
              />
            </div>

            {error && (
              <div className="bg-[var(--bg-inner)] border border-[var(--border-card)] text-[var(--text-primary)] text-xs font-mono-tech p-3 rounded flex items-center space-x-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <button
              onClick={handleRecommend}
              disabled={loading}
              className={`w-full py-2.5 rounded font-mono-tech text-xs font-semibold tracking-wider cursor-pointer ${
                loading
                  ? 'bg-[var(--bg-inner)] text-[var(--text-dim)] border border-[var(--border-card)] cursor-not-allowed'
                  : 'btn-invert'
              }`}
            >
              {loading ? 'COMPUTING RECOMMENDATION...' : 'COMPUTE CROP RECOMMENDATION'}
            </button>
          </div>
        </div>

        {/* Right Column: Results & SHAP */}
        <div className="lg:col-span-7 space-y-6">
          {result ? (
            <div className="space-y-6">
              {/* Primary Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <MetricCard
                  label="RECOMMENDED CROP"
                  value={result.recommended_crop.toUpperCase()}
                  badge="TOP CHOICE"
                />
                <MetricCard
                  label="CALIBRATED PROBABILITY"
                  value={`${(result.confidence * 100).toFixed(1)}%`}
                  badge="SIGMOID"
                />
              </div>

              {/* Top Alternatives List */}
              <div className="bg-[var(--bg-card)] border border-[var(--border-card)] rounded-xl p-5 space-y-3 font-mono-tech transition-colors duration-300">
                <span className="text-xs text-[var(--text-primary)] font-medium block uppercase tracking-wider">
                  TOP CROP ALTERNATIVES
                </span>
                <div className="space-y-2 pt-1">
                  {result.top_recommendations.slice(0, 3).map((item, idx) => (
                    <div key={idx} className="flex items-center justify-between p-2.5 bg-[var(--bg-inner)] rounded border border-[var(--border-card)] text-xs">
                      <div className="flex items-center space-x-2">
                        <span className="w-5 h-5 rounded bg-[var(--bg-card)] border border-[var(--border-card)] flex items-center justify-center text-[10px] text-[var(--text-primary)] font-bold">
                          0{idx + 1}
                        </span>
                        <span className="text-[var(--text-primary)] font-medium capitalize">{item.crop}</span>
                      </div>
                      <span className="text-[var(--text-muted)] font-mono">{(item.probability * 100).toFixed(1)}%</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* SHAP Explanation Chart */}
              <MonochromeShapChart
                contributions={result.explanation?.top_features}
                title={`SHAP FEATURE ATTRIBUTION: ${result.recommended_crop.toUpperCase()}`}
              />
            </div>
          ) : (
            <div className="bg-[var(--bg-card)] border border-[var(--border-card)] rounded-xl p-12 text-center font-mono-tech space-y-3 transition-colors duration-300">
              <Sprout className="w-8 h-8 text-[var(--text-dim)] mx-auto" />
              <p className="text-xs text-[var(--text-muted)]">AWAITING PARAMETER INPUT</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default CropRecommendation;
