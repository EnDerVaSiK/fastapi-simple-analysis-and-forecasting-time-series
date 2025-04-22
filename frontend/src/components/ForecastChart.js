import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS } from 'chart.js/auto';

export default function ForecastChart({ data }) {
  // Проверка данных перед рендерингом
  if (!data || !data.ds || !data.yhat) {
    return <div>No forecast data available</div>;
  }

  // Преобразуем объекты в массивы
  const labels = Object.values(data.ds);
  const values = Object.values(data.yhat);

  const chartData = {
    labels: labels.map(d => new Date(d).toLocaleDateString()),
    datasets: [
      {
        label: 'Forecast',
        data: values,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }
    ]
  };

  return (
    <div style={{ width: '800px', margin: '20px auto' }}>
      <Line data={chartData} />
    </div>
  );
}