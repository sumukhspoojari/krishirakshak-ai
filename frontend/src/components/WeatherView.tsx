import React, { useEffect, useState } from 'react';
import type { WeatherInfo, Language } from '../types';
import { apiClient } from '../services/api';
import { CloudRain, Wind, Droplets, AlertCircle, CheckCircle2, ShieldAlert } from 'lucide-react';

interface WeatherViewProps {
  currentLanguage: Language;
}

export const WeatherView: React.FC<WeatherViewProps> = ({ currentLanguage }) => {
  const [weather, setWeather] = useState<WeatherInfo | null>(null);
  const [location, setLocation] = useState('Mandya, Karnataka');
  const [loading, setLoading] = useState(true);

  const fetchWeather = async (loc: string) => {
    setLoading(true);
    try {
      const data = await apiClient.getWeather(loc);
      setWeather(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWeather(location);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div className="section-header">
        <h3 className="section-title">
          <CloudRain size={24} color="#047857" />
          {currentLanguage === 'kn' && 'ಕೃಷಿ ಹವಾಮಾನ ಮತ್ತು ರೋಗ ಅಪಾಯ ಸೂಚ್ಯಂಕ'}
          {currentLanguage === 'hi' && 'कृषि मौसम और रोग जोखिम सूचकांक'}
          {currentLanguage === 'te' && 'వ్యవసాయ వాతావరణం & వ్యాధి ప్రమాద సూచిక'}
          {currentLanguage === 'en' && 'Agro-Meteorological Disease Risk Advisory'}
        </h3>

        <div style={{ display: 'flex', gap: '8px' }}>
          {['Mandya, Karnataka', 'Raichur, Karnataka', 'Guntur, AP'].map((loc) => (
            <button
              key={loc}
              className={`sample-image-pill ${location === loc ? 'active' : ''}`}
              onClick={() => {
                setLocation(loc);
                fetchWeather(loc);
              }}
              style={location === loc ? { background: '#d1fae5', borderColor: '#10b981', fontWeight: 700 } : {}}
            >
              📍 {loc}
            </button>
          ))}
        </div>
      </div>

      {loading || !weather ? (
        <div style={{ textAlign: 'center', padding: '40px' }}>Loading weather parameters...</div>
      ) : (
        <>
          {/* Main Weather Metric Cards */}
          <div className="weather-card-grid">
            <div className="weather-box">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>📍 {weather.location}</span>
                <span className="crop-badge">{weather.condition}</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px' }}>
                <span className="temp-huge">{weather.temperature}°C</span>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Air Temperature</span>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '8px', marginTop: '16px' }}>
                <div style={{ textAlign: 'center', background: '#f8fafc', padding: '8px', borderRadius: '8px' }}>
                  <Droplets size={18} color="#2563eb" style={{ margin: '0 auto 2px' }} />
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Humidity</div>
                  <strong style={{ fontSize: '0.88rem' }}>{weather.humidity}%</strong>
                </div>
                <div style={{ textAlign: 'center', background: '#f8fafc', padding: '8px', borderRadius: '8px' }}>
                  <CloudRain size={18} color="#059669" style={{ margin: '0 auto 2px' }} />
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Rainfall</div>
                  <strong style={{ fontSize: '0.88rem' }}>{weather.rainfall_mm} mm</strong>
                </div>
                <div style={{ textAlign: 'center', background: '#f8fafc', padding: '8px', borderRadius: '8px' }}>
                  <Wind size={18} color="#d97706" style={{ margin: '0 auto 2px' }} />
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Wind</div>
                  <strong style={{ fontSize: '0.88rem' }}>{weather.wind_kmh} km/h</strong>
                </div>
              </div>
            </div>

            {/* Disease & Spraying Risk Evaluation */}
            <div className="weather-box">
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <ShieldAlert size={18} color="#dc2626" /> Agro-Meteorological Risk Index:
              </h4>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '0.85rem' }}>🍄 Fungal Disease Window:</span>
                  <span className={`risk-tag ${weather.fungal_disease_risk}`}>
                    {weather.fungal_disease_risk} Risk
                  </span>
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '0.85rem' }}>🐛 Pest Activity Window (Thrips/Mites):</span>
                  <span className={`risk-tag ${weather.pest_activity_risk}`}>
                    {weather.pest_activity_risk} Risk
                  </span>
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '0.85rem' }}>🚜 Foliar Spraying Condition:</span>
                  <span style={{
                    fontSize: '0.75rem',
                    fontWeight: 700,
                    color: weather.can_spray ? '#059669' : '#dc2626',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}>
                    {weather.can_spray ? <CheckCircle2 size={14} /> : <AlertCircle size={14} />}
                    {weather.can_spray ? 'Favorable Today' : 'Avoid Spraying'}
                  </span>
                </div>
              </div>

              <div style={{
                background: '#ecfdf5',
                border: '1px solid #10b981',
                borderRadius: '8px',
                padding: '10px 12px',
                marginTop: '12px',
                fontSize: '0.82rem',
                color: '#065f46'
              }}>
                <strong>🌾 KrishiRakshak Advisory:</strong> {weather.advisory}
              </div>
            </div>
          </div>

          {/* 3-Day Agro Forecast */}
          <div className="weather-box">
            <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginBottom: '12px' }}>
              🗓 3-Day Agro-Weather Forecast
            </h4>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '12px' }}>
              {weather.forecast_3days.map((f, i) => (
                <div key={i} style={{ background: '#f8fafc', border: '1px solid var(--border-light)', borderRadius: '8px', padding: '12px', textAlign: 'center' }}>
                  <strong style={{ fontSize: '0.88rem', display: 'block', marginBottom: '4px' }}>{f.day}</strong>
                  <div style={{ fontSize: '1.2rem', fontWeight: 800, color: 'var(--primary-800)' }}>{f.temp}</div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Humidity: {f.humidity}</div>
                  <div style={{ fontSize: '0.78rem', color: '#2563eb' }}>Rain Probability: {f.rain_chance}</div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
};
