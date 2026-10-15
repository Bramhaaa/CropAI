import React, { useEffect, useState } from 'react';
import { Sprout, AlertCircle, MapPin } from 'lucide-react';
import { api } from '../api/client';
import MetricCard from '../components/MetricCard';
import SliderInput from '../components/SliderInput';

export function CropRecommendation() {
  const [params, setParams] = useState({
    state: 'Karnataka',
    district: 'Bangalore',
    year: 2017,
    top_k: 5,
    nitrogen: 50,
    phosphorus: 50,
    potassium: 50,
    temperature: 25,
    humidity: 75,
    ph: 6.5,
    rainfall: 120,
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [locations, setLocations] = useState({});
  const [locationsLoading, setLocationsLoading] = useState(true);

  useEffect(() => {
    api.getIndianCropLocations()
      .then((availableLocations) => {
        setLocations(availableLocations);
        const states = Object.keys(availableLocations);
        const initialState = states.includes(params.state) ? params.state : states[0];
        const districts = availableLocations[initialState] || [];
        updateParam('state', initialState);
        updateParam('district', districts[0] || '');
      })
      .catch(() => setError('INDIAN LOCATION DATA UNAVAILABLE.'))
      .finally(() => setLocationsLoading(false));
  }, []);

  const states = Object.keys(locations);
  const districts = locations[params.state] || [];

  const handleStateChange = (state) => {
    updateParam('state', state);
    updateParam('district', (locations[state] || [])[0] || '');
    setResult(null);
  };

  const updateParam = (key, value) => {
    setParams((previous) => ({ ...previous, [key]: value }));
  };

  const handleRecommend = async () => {
    setLoading(true);
    setError(null);
    try {
      setResult(await api.recommendIndianCrop(params));
    } catch (err) {
      setError(err.response?.data?.detail || 'INDIAN RECOMMENDATION ENGINE FAILURE.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-5">
      <div>
        <div className="flex items-center space-x-2 text-xs font-mono-tech text-[var(--text-muted)] mb-1">
          <MapPin className="w-3.5 h-3.5" />
          <span>MODULE 02 / INDIAN CROP SUITABILITY RANKER</span>
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-[var(--text-primary)] font-mono-tech">
          INDIAN CROP RECOMMENDATION ENGINE
        </h1>
        <p className="text-xs text-[var(--text-muted)] font-mono-tech mt-2 max-w-3xl">
          Historical crop suitability recommendations based on Indian district, state, and national crop occurrence data.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        <div className="lg:col-span-5 space-y-3">
          <div className="bg-[var(--bg-card)] border border-[var(--border-card)] rounded-xl p-4 sm:p-5 space-y-3 font-mono-tech transition-colors duration-300">
            <span className="text-xs text-[var(--text-primary)] font-medium block border-b border-[var(--border-card)] pb-2">
              INDIAN LOCATION & SOIL/WEATHER
            </span>
            <div className="space-y-3">
              <label className="block text-xs text-[var(--text-muted)]">
                <span className="block mb-1">STATE</span>
                <select
                  value={params.state}
                  onChange={(event) => handleStateChange(event.target.value)}
                  disabled={locationsLoading || states.length === 0}
                  className="w-full rounded border border-[var(--border-card)] bg-[var(--bg-inner)] px-3 py-2 text-[var(--text-primary)] outline-none focus:border-[var(--border-hover)]"
                >
                  {locationsLoading && <option>Loading states...</option>}
                  {states.map((state) => <option key={state} value={state}>{state}</option>)}
                </select>
              </label>
              <label className="block text-xs text-[var(--text-muted)]">
                <span className="block mb-1">DISTRICT</span>
                <select
                  value={params.district}
                  onChange={(event) => updateParam('district', event.target.value)}
                  disabled={locationsLoading || districts.length === 0}
                  className="w-full rounded border border-[var(--border-card)] bg-[var(--bg-inner)] px-3 py-2 text-[var(--text-primary)] outline-none focus:border-[var(--border-hover)]"
                >
                  {locationsLoading && <option>Loading districts...</option>}
                  {districts.map((district) => <option key={district} value={district}>{district}</option>)}
                </select>
              </label>
              <label className="block text-xs text-[var(--text-muted)]">
                <span className="block mb-1">REFERENCE YEAR</span>
                <input
                  type="number"
                  min="2010"
                  max="2035"
                  value={params.year}
                  onChange={(event) => updateParam('year', Number(event.target.value))}
                  className="w-full rounded border border-[var(--border-card)] bg-[var(--bg-inner)] px-3 py-2 text-[var(--text-primary)] outline-none focus:border-[var(--border-hover)]"
                />
              </label>
              <div className="border-t border-[var(--border-card)] pt-3 space-y-2">
                <span className="block text-xs text-[var(--text-primary)]">SOIL & CLIMATIC SIGNALS</span>
                <SliderInput
                  label="NITROGEN (N)"
                  min={0}
                  max={140}
                  value={params.nitrogen}
                  onChange={(value) => updateParam('nitrogen', value)}
                  unit="mg/kg"
                />
                <SliderInput
                  label="PHOSPHORUS (P)"
                  min={5}
                  max={145}
                  value={params.phosphorus}
                  onChange={(value) => updateParam('phosphorus', value)}
                  unit="mg/kg"
                />
                <SliderInput
                  label="POTASSIUM (K)"
                  min={5}
                  max={205}
                  value={params.potassium}
                  onChange={(value) => updateParam('potassium', value)}
                  unit="mg/kg"
                />
                <SliderInput
                  label="TEMPERATURE"
                  min={10}
                  max={50}
                  step={0.5}
                  value={params.temperature}
                  onChange={(value) => updateParam('temperature', value)}
                  unit="°C"
                />
                <SliderInput
                  label="HUMIDITY"
                  min={10}
                  max={100}
                  value={params.humidity}
                  onChange={(value) => updateParam('humidity', value)}
                  unit="%"
                />
                <SliderInput
                  label="SOIL PH"
                  min={3.5}
                  max={10}
                  step={0.1}
                  value={params.ph}
                  onChange={(value) => updateParam('ph', value)}
                />
                <SliderInput
                  label="RAINFALL"
                  min={20}
                  max={300}
                  value={params.rainfall}
                  onChange={(value) => updateParam('rainfall', value)}
                  unit="mm"
                />
              </div>
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
              {loading ? 'RANKING INDIAN CROPS...' : 'RECOMMEND INDIAN CROPS'}
            </button>
          </div>

          <div className="bg-[var(--bg-card)] border border-[var(--border-card)] rounded-xl p-4 text-xs font-mono-tech text-[var(--text-muted)] space-y-1">
            <div className="text-[var(--text-primary)]">MODEL EVALUATION</div>
            <div>Test accuracy: 100.0%</div>
            <div>Indian crop-history records: 27,676</div>
          </div>
        </div>

        <div className="lg:col-span-7 space-y-6">
          {result ? (
            <div className="space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <MetricCard
                  label="RECOMMENDED CROP"
                  value={result.recommended_crop.toUpperCase()}
                  badge="TOP CHOICE"
                />
                <MetricCard
                  label="LOCATION"
                  value={result.district.toUpperCase()}
                  badge={result.state.toUpperCase()}
                />
              </div>

              <div className="bg-[var(--bg-card)] border border-[var(--border-card)] rounded-xl p-5 space-y-3 font-mono-tech transition-colors duration-300">
                <span className="text-xs text-[var(--text-primary)] font-medium block uppercase tracking-wider">
                  TOP INDIAN CROP ALTERNATIVES
                </span>
                <div className="space-y-2 pt-1">
                  {result.top_recommendations.map((item, index) => (
                    <div key={item.crop} className="flex items-center justify-between p-2.5 bg-[var(--bg-inner)] rounded border border-[var(--border-card)] text-xs">
                      <div className="flex items-center space-x-2">
                        <span className="w-5 h-5 rounded bg-[var(--bg-card)] border border-[var(--border-card)] flex items-center justify-center text-[10px] text-[var(--text-primary)] font-bold">
                          {String(index + 1).padStart(2, '0')}
                        </span>
                        <span className="text-[var(--text-primary)] font-medium capitalize">{item.crop}</span>
                      </div>
                      <span className="text-[var(--text-muted)] font-mono">{(item.probability * 100).toFixed(1)}%</span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="text-xs text-[var(--text-muted)] font-mono-tech">
                SOURCE: {result.data_source} · MODEL: {result.model_version}
              </div>
            </div>
          ) : (
            <div className="bg-[var(--bg-card)] border border-[var(--border-card)] rounded-xl p-12 text-center font-mono-tech space-y-3 transition-colors duration-300">
              <Sprout className="w-8 h-8 text-[var(--text-dim)] mx-auto" />
              <p className="text-xs text-[var(--text-muted)]">ENTER AN INDIAN STATE AND DISTRICT TO BEGIN</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default CropRecommendation;
