import React from 'react';
import CompanyCard from './CompanyCard';
import mcgillLogo from './pics/algonquin-logo.png';
import uottawaLogo from './pics/uottawa-logo.png';
import carletonLogo from './pics/carleton-logo.png';

const SupportedCompanies = () => {
  const companies = [
    { logo: mcgillLogo, name: 'McGill University', link: '/chat' },
    { logo: uottawaLogo, name: 'University of Ottawa', link: '/chat' },
    { logo: carletonLogo, name: 'Carleton University', link: '/chat' },
  ];

  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '24px', justifyContent: 'center', marginTop: '32px' }}>
      {companies.map((company, index) => (
        <CompanyCard key={index} logo={company.logo} name={company.name} link={company.link} />
      ))}
    </div>
  );
};

export default SupportedCompanies;
