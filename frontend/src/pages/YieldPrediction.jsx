import React, { useState } from 'react';
import { TrendingUp, AlertCircle, ShieldAlert } from 'lucide-react';
import { api } from '../api/client';
import MetricCard from '../components/MetricCard';
import SelectInput from '../components/SelectInput';
import MonochromeShapChart from '../components/MonochromeShapChart';

const STATES = [
  'Punjab', 'Maharashtra', 'Uttar Pradesh', 'Tamil Nadu', 'West Bengal',
  'Karnataka', 'Gujarat', 'Madhya Pradesh', 'Andhra Pradesh', 'Haryana',
  'Bihar', 'Odisha', 'Rajasthan', 'Kerala', 'Assam'
];

const CROPS = [
  'Rice', 'Maize', 'Chickpea', 'Cotton', 'Mango', 'Banana', 'Grapes', 'Wheat', 'Sugarcane', 'Arhar/Tur'
];

const SEASONS = [
  'Kharif     ', 'Rabi   ', 'Summer', 'Whole Year', 'Winter', 'Autumn'
];

export function YieldPrediction() {
  const [state, setState] = useState('Punjab');
  const [crop, setCrop] = useState('Rice');
  const [season, setSeason] = useState('Kharif     ');
  const [area, setArea] = useState(1000.0);
  const [confLevel, setConfLevel] = useState(0.90);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handlePredict = async () => {
    setLoading(true);
    setError(null);
    try {
      const payload = {
        state,
        crop,
        season,
        area_hectares: area,
        confidence_level: confLevel,
      };
      const data = await api.predictYield(payload);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'YIELD ENGINE PREDICTION FAILURE.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-5">
      {/* Header */}
      <div>
        <div className="flex items-center space-x-2 text-xs font-mono-tech text-[var(--text-muted)] mb-1">
          <TrendingUp className="w-3.5 h-3.5" />
          <span>MODULE 03 / CONFORMAL REGRESSOR</span>
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-[var(--text-primary)] font-mono-tech">
          AGRICULTURAL YIELD FORECASTING
        </h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column: Parameter Inputs */}
        <div className="lg:col-span-5 space-y-3">
          <div className="bg-[var(--bg-card)] border border-[var(--border-card)] rounded-xl p-4 sm:p-5 space-y-3 font-mono-tech transition-colors duration-300">
            <span className="text-xs text-[var(--text-primary)] font-medium block border-b border-[var(--border-card)] pb-2">
              AGRICULTURAL REGRESSION METRICS
            </span>

            <div className="space-y-2.5">
              <SelectInput
                label="STATE LOCATION"
                options={STATES}
                value={state}
                onChange={setState}
              />
              <SelectInput
                label="TARGET CROP"
                options={CROPS}
                value={crop}
                onChange={setCrop}
              />
              <SelectInput
                label="CULTIVATION SEASON"
                options={SEASONS}
                value={season}
                onChange={setSeason}
              />

              <div className="bg-[var(--bg-inner)] border border-[var(--border-card)] rounded-lg p-2.5 space-y-1.5 transition-colors duration-300">
                <label className="block text-xs text-[var(--text-primary)] font-medium">
                  CULTIVATED AREA (HECTARES)
                </label>
                <input
                  type="number"
                  min={0.1}
                  max={10000000}
                  value={area}
                  onChange={(e) => setArea(parseFloat(e.target.value) || 0)}
                  className="w-full bg-[var(--bg-card)] border border-[var(--border-card)] rounded px-3 py-1.5 text-xs font-mono-tech text-[var(--text-primary)] focus:outline-none focus:border-[var(--border-hover)] transition-colors duration-300"
                />
              </div>

              <SelectInput
                label="CONFORMAL CONFIDENCE LEVEL"
                options={[
                  { value: 0.90, label: '90% CONFIDENCE (RECOMMENDED)' },
                  { value: 0.95, label: '95% CONFIDENCE' },
                  { value: 0.80, label: '80% CONFIDENCE' },
                ]}
                value={confLevel}
                onChange={(v) => setConfLevel(parseFloat(v))}
              />
            </div>

            {error && (
              <div className="bg-[var(--bg-inner)] border border-[var(--border-card)] text-[var(--text-primary)] text-xs font-mono-tech p-3 rounded flex items-center space-x-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <button
              onClick={handlePredict}
              disabled={loading}
              className={`w-full py-2.5 rounded font-mono-tech text-xs font-semibold tracking-wider cursor-pointer ${
                loading
                  ? 'bg-[var(--bg-inner)] text-[var(--text-dim)] border border-[var(--border-card)] cursor-not-allowed'
                  : 'btn-invert'
              }`}
            >
              {loading ? 'CALCULATING CONFORMAL YIELD...' : 'PREDICT EXPECTED YIELD'}
            </button>
          </div>
        </div>

        {/* Right Column: Results & SHAP */}
        <div className="lg:col-span-7 space-y-6">
          {result ? (
            <div className="space-y-6">
              {/* Metric Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <MetricCard
                  label="PREDICTED YIELD"
                  value={`${result.predicted_yield.toFixed(2)}`}
                  badge="POINT ESTIMATE"
                />
                <MetricCard
                  label={`${(result.interval.confidence_level * 100).toFixed(0)}% CONFORMAL BOUNDS`}
                  value={`[${result.interval.lower.toFixed(2)}, ${result.interval.upper.toFixed(2)}]`}
                  badge="STATISTICAL"
                />
              </div>

              {/* Conformal Guarantee Note */}
              <div className="bg-[var(--bg-card)] border border-[var(--border-card)] rounded-xl p-5 space-y-2 font-mono-tech text-xs transition-colors duration-300">
                <div className="flex items-center space-x-2 text-[var(--text-primary)] font-medium">
                  <ShieldAlert className="w-3.5 h-3.5" />
                  <span>CONFORMAL PREDICTION GUARANTEE</span>
                </div>
                <p className="text-[var(--text-muted)] text-[11px] leading-relaxed">
                  Under the requested <span className="text-[var(--text-primary)] font-bold">{(result.interval.confidence_level * 100).toFixed(0)}%</span> statistical confidence level, true crop yield is mathematically guaranteed to fall between <span className="text-[var(--text-primary)] font-bold">{result.interval.lower.toFixed(2)}</span> and <span className="text-[var(--text-primary)] font-bold">{result.interval.upper.toFixed(2)}</span> {result.unit}.
                </p>
              </div>

              {/* SHAP Influence Breakdown */}
              <MonochromeShapChart
                contributions={result.explanation?.top_features}
                title={`FEATURE INFLUENCE ON YIELD (${result.predicted_yield.toFixed(2)} T/HA)`}
              />
            </div>
          ) : (
            <div className="bg-[var(--bg-card)] border border-[var(--border-card)] rounded-xl p-12 text-center font-mono-tech space-y-3 transition-colors duration-300">
              <TrendingUp className="w-8 h-8 text-[var(--text-dim)] mx-auto" />
              <p className="text-xs text-[var(--text-muted)]">AWAITING REGRESSION PARAMETERS</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default YieldPrediction;
