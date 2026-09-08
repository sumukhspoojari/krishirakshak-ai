import React, { useEffect, useState } from 'react';
import type { SchemeInfo, Language } from '../types';
import { apiClient } from '../services/api';
import { Building2, ExternalLink } from 'lucide-react';

interface SchemesViewProps {
  currentLanguage: Language;
}

export const SchemesView: React.FC<SchemesViewProps> = ({ currentLanguage }) => {
  const [schemes, setSchemes] = useState<SchemeInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('All');

  useEffect(() => {
    apiClient.getSchemes().then((data) => {
      setSchemes(data);
      setLoading(false);
    });
  }, []);

  const categories = ['All', 'Direct Income Support', 'Crop Insurance', 'Subsidized Credit', 'Soil Testing & Fertility', 'Mechanization & Subsidy'];

  const filteredSchemes = selectedCategory === 'All'
    ? schemes
    : schemes.filter((s) => s.category === selectedCategory);

  const getLocalizedName = (s: SchemeInfo) => {
    if (currentLanguage === 'kn') return s.name_kn;
    if (currentLanguage === 'hi') return s.name_hi;
    if (currentLanguage === 'te') return s.name_te;
    return s.name;
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div className="section-header">
        <div>
          <h3 className="section-title">
            <Building2 size={24} color="#047857" />
            {currentLanguage === 'kn' && 'ರೈತರಿಗಾಗಿ ಸರ್ಕಾರದ ಪ್ರಮುಖ ಯೋಜನೆಗಳು ಮತ್ತು ಬೆಳೆ ವಿಮೆ'}
            {currentLanguage === 'hi' && 'किसानों के लिए सरकारी योजनाएं और फसल बीमा'}
            {currentLanguage === 'te' && 'రైతుల కోసం ప్రభుత్వ పథకాలు & పంట బీమా'}
            {currentLanguage === 'en' && 'Government Agricultural Assistance & Schemes'}
          </h3>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
            Central and State Government initiatives to protect farmers from crop loss and reduce financial risks.
          </p>
        </div>
      </div>

      {/* Category Pills */}
      <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '4px' }}>
        {categories.map((cat) => (
          <button
            key={cat}
            className={`sample-image-pill ${selectedCategory === cat ? 'active' : ''}`}
            onClick={() => setSelectedCategory(cat)}
            style={selectedCategory === cat ? { background: '#d1fae5', borderColor: '#10b981', fontWeight: 700 } : {}}
          >
            {cat}
          </button>
        ))}
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px' }}>Loading schemes...</div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '16px' }}>
          {filteredSchemes.map((s) => (
            <div key={s.id} className="goal-card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '8px', marginBottom: '8px' }}>
                  <span className="crop-badge">{s.category}</span>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 600 }}>Govt Verified</span>
                </div>

                <h4 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--primary-900)', marginBottom: '6px' }}>
                  {getLocalizedName(s)}
                </h4>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '12px' }}>
                  ({s.name})
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '0.84rem' }}>
                  <div style={{ background: '#ecfdf5', padding: '8px 10px', borderRadius: '6px', color: '#065f46' }}>
                    <strong>🎁 ಸೌಲಭ್ಯ (Benefits): </strong> {s.benefits}
                  </div>
                  <div>
                    <strong>👥 ಅರ್ಹತೆ (Eligibility): </strong> {s.eligibility}
                  </div>
                  <div style={{ color: 'var(--text-medium)' }}>
                    <strong>📝 ಅರ್ಜಿ ಸಲ್ಲಿಸುವ ವಿಧಾನ: </strong> {s.how_to_apply}
                  </div>
                </div>
              </div>

              <div style={{ marginTop: '16px', paddingTop: '12px', borderTop: '1px solid var(--border-light)', display: 'flex', justifyContent: 'flex-end' }}>
                <a
                  href={s.official_link}
                  target="_blank"
                  rel="noreferrer"
                  className="btn-primary"
                  style={{ textDecoration: 'none', fontSize: '0.78rem', padding: '6px 12px' }}
                >
                  ಅಧಿಕೃತ ಪೋರ್ಟಲ್ (Official Portal) <ExternalLink size={13} />
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
