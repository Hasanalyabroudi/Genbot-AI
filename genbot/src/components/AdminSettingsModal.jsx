import React, { useState, useEffect } from 'react';

const AdminSettingsModal = ({
  isOpen,
  onClose,
  onSave,
  initialModel,
  initialTemperature,
  selectedCompany
}) => {
  const [hoverSave, setHoverSave] = useState(false);
  const [hoverCancel, setHoverCancel] = useState(false);
  const [modelValue, setModelValue] = useState(initialModel);
  const [temperatureValue, setTemperatureValue] = useState(initialTemperature);

  // When the modal opens or the selected company changes, initialize the local state.
  useEffect(() => {
    if (selectedCompany) {
      setModelValue(initialModel);
      setTemperatureValue(initialTemperature);
    }
  }, [selectedCompany, initialModel, initialTemperature]);

  if (!isOpen) return null;

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        right: 0,
        bottom: 0,
        left: 0,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'rgba(26, 32, 44, 0.5)',
        zIndex: 50,
      }}
    >
      <div
        style={{
          backgroundColor: 'white',
          padding: '24px',
          borderRadius: '8px',
          boxShadow:
            '0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05)',
          width: '384px',
        }}
      >
        <h2
          style={{
            fontSize: '20px',
            fontWeight: 600,
            color: '#2d3748',
            marginBottom: '16px',
          }}
        >
          Settings for {selectedCompany}
        </h2>
        <div>
          <div style={{ marginBottom: '8px' }}>
            <strong>Name:</strong> {selectedCompany}
          </div>
          <div style={{ marginBottom: '8px' }}>
            <strong>Pages Scraped:</strong> 342
          </div>
          <div style={{ marginBottom: '8px' }}>
            <label style={{ marginRight: '8px' }}><strong>Model:</strong></label>
            <select
              value={modelValue}
              onChange={(e) => setModelValue(e.target.value)}
              style={{
                padding: '4px',
                border: '1px solid #e2e8f0',
                borderRadius: '4px',
              }}
            >
              <option value="GPT-4o">GPT-4o</option>
              <option value="GPT-4">GPT-4</option>
              <option value="GPT-3.5">GPT-3.5</option>
            </select>
          </div>
          <div style={{ marginBottom: '8px' }}>
            <label style={{ marginRight: '8px' }}><strong>Temperature:</strong></label>
            <input
              type="range"
              min="0"
              max="2"
              step="0.1"
              value={temperatureValue}
              onChange={(e) => setTemperatureValue(e.target.value)}
              style={{ verticalAlign: 'middle' }}
            />
            <span style={{ marginLeft: '8px' }}>{temperatureValue}</span>
          </div>
          <div style={{ marginBottom: '8px' }}>
            <strong>Status: </strong>
            <span style={{ color: 'green' }}>
              active
            </span>
          </div>
        </div>
        <div
          style={{
            marginTop: '16px',
            display: 'flex',
            justifyContent: 'flex-end',
            gap: '8px',
          }}
        >
          <button
            onClick={() => {
              // Discard changes.
              onClose();
            }}
            onMouseEnter={() => setHoverCancel(true)}
            onMouseLeave={() => setHoverCancel(false)}
            style={{
              padding: '8px 16px',
              backgroundColor: hoverCancel ? '#cbd5e0' : '#e2e8f0',
              borderRadius: '6px',
              border: 'none',
              cursor: 'pointer',
            }}
          >
            Cancel
          </button>
          <button
            className="bg-[rgb(67,56,202)] hover:bg-[rgb(57,46,192)] text-white"
            onClick={() => {
              // Save new settings.
              if (onSave) {
                onSave({ model: modelValue, temperature: temperatureValue });
              }
              onClose();
            }}
            onMouseEnter={() => setHoverSave(true)}
            onMouseLeave={() => setHoverSave(false)}
            style={{
              padding: '8px 16px',
              backgroundColor: hoverSave ? 'rgb(57,46,192)' : 'rgb(67,56,202)',
              borderRadius: '6px',
              border: 'none',
              cursor: 'pointer',
              color: 'white',
            }}
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
};

export default AdminSettingsModal;
