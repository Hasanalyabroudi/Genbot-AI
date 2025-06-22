import React, { useState } from 'react';
import { FiSettings } from 'react-icons/fi';
import AdminSettingsModal from './AdminSettingsModal';

const CompanyCardItem = ({ name, onSelect, adminControls, onOpenModal }) => {
  const [hover, setHover] = useState(false);
  const [settingsHover, setSettingsHover] = useState(false);

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '12px',
        borderRadius: '6px',
        cursor: 'pointer',
        backgroundColor: hover ? '#f1f5f9' : 'transparent',
        transition: 'background-color 150ms ease',
      }}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      onClick={() => onSelect(name)}
    >
      <button
        style={{
          flexGrow: 1,
          textAlign: 'left',
          backgroundColor: 'transparent',
          border: 'none',
          padding: 0,
          margin: 0,
          cursor: 'pointer',
        }}
        onClick={(e) => {
          e.stopPropagation();
          onSelect(name);
        }}
      >
        {name}
      </button>
      {adminControls && (
        <div style={{ height: '100%', display: 'flex', alignItems: 'center' }}>
          <button
            style={{
              padding: '8px',
              borderRadius: '6px',
              height: '100%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              backgroundColor: settingsHover ? '#e2e8f0' : 'transparent',
              transition: 'background-color 150ms ease',
              border: 'none',
              cursor: 'pointer',
            }}
            onMouseEnter={() => setSettingsHover(true)}
            onMouseLeave={() => setSettingsHover(false)}
            onClick={(e) => {
              e.stopPropagation();
              onOpenModal(name);
            }}
          >
            <FiSettings style={{ color: '#4a5568' }} />
          </button>
        </div>
      )}
    </div>
  );
};

const CompanyCards = ({
  universities,
  selectedUniversity,
  onSelect,
  adminControls = false,
  initialSettings,
  onSaveSettings,
}) => {
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedCompany, setSelectedCompany] = useState(null);

  const handleOpenModal = (university) => {
    setSelectedCompany(university);
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
    setSelectedCompany(null);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
      {universities.map((university) => (
        <CompanyCardItem
          key={university}
          name={university}
          onSelect={onSelect}
          adminControls={adminControls}
          onOpenModal={handleOpenModal}
        />
      ))}
      <AdminSettingsModal
        isOpen={modalOpen}
        onClose={handleCloseModal}
        selectedCompany={selectedCompany}
        initialModel={
          selectedCompany && initialSettings && initialSettings[selectedCompany]
            ? initialSettings[selectedCompany].model
            : 'GPT-4o'
        }
        initialTemperature={
          selectedCompany && initialSettings && initialSettings[selectedCompany]
            ? initialSettings[selectedCompany].temperature
            : '1'
        }
        onSave={onSaveSettings}
      />
    </div>
  );
};

export default CompanyCards;
