import React, { useState } from 'react';
import axios from 'axios';
import ForecastChart from './components/ForecastChart';

function App() {
  const [forecastData, setForecastData] = useState(null);
  const [error, setError] = useState('');

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(
        'http://localhost:8000/api/upload-csv',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          timeout: 30000  // Увеличьте таймаут до 30 секунд
        }
      );

      if (!response.data.forecast) {
        throw new Error('Invalid response format');
      }

      setForecastData(response.data);
    } catch (err) {
      console.error('Error details:', err);
      setError(err.message);
    }

  };

  return (
    <div className="App">
      <h1>Simple Analysis and Forecasting Time Series</h1>
      <input type="file" accept=".csv" onChange={handleFileUpload} />
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {forecastData && forecastData.forecast && (
        <ForecastChart data={forecastData.forecast} />
      )}
    </div>
  );
}

export default App;
