import React, { useState } from 'react';
import { ThemeProvider } from './context/ThemeContext';
import Header from './components/Header';
import Navigation from './components/Navigation';
import OverviewDashboard from './pages/OverviewDashboard';
import DiseaseDiagnosis from './pages/DiseaseDiagnosis';
import CropRecommendation from './pages/CropRecommendation';
import YieldPrediction from './pages/YieldPrediction';

export function AppContent() {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <div className="min-h-screen bg-[var(--bg-main)] text-[var(--text-primary)] flex flex-col font-sans selection:bg-white selection:text-black transition-colors duration-300 overflow-y-auto">
      {/* Top Header */}
      <Header />

      {/* Navigation Tabs */}
      <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Page Content Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6">
        {activeTab === 'overview' && <OverviewDashboard setActiveTab={setActiveTab} />}
        {activeTab === 'disease' && <DiseaseDiagnosis />}
        {activeTab === 'crop' && <CropRecommendation />}
        {activeTab === 'yield' && <YieldPrediction />}
      </main>

      {/* Footer - Centered Text */}
      <footer className="border-t border-[var(--border-card)] bg-[var(--bg-card)] py-4 text-center text-xs font-mono-tech text-[var(--text-muted)] transition-colors duration-300 mt-auto">
        <div className="max-w-7xl mx-auto px-4 flex justify-center items-center text-center">
          <span>CROP.AI — EXPLAINABLE & UNCERTAINTY-AWARE DECISION SUPPORT</span>
        </div>
      </footer>
    </div>
  );
}

export function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
}

export default App;
