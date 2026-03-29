import React from 'react';
import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  Title,
  Tooltip,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

import { Card } from '../shared/Card';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export function MonthlyFlow({ flow }) {
  if (!flow || flow.length === 0) {
    return null;
  }

  const labels = flow.map((entry) => entry.month.slice(0, 7));

  const data = {
    labels,
    datasets: [
      {
        label: 'Fluxo Reajustável',
        data: flow.map((entry) => entry.gross_adjustable || 0),
        backgroundColor: '#0056b3',
      },
      {
        label: 'Fluxo Irreajustável',
        data: flow.map((entry) => entry.gross_fixed || 0),
        backgroundColor: '#10b981',
      },
      {
        label: 'Comissão Direta',
        data: flow.map((entry) => entry.direct_commission || 0),
        backgroundColor: '#ef4444',
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: { stacked: true },
      y: { stacked: true },
    },
    plugins: {
      legend: { position: 'bottom' },
      title: { display: false },
    },
  };

  return (
    <Card className="mt-6 flex h-[400px] flex-col">
      <h2 className="mb-4 text-lg font-semibold text-city-blue-dark">
        Fluxo Mensal Projetado
      </h2>
      <div className="min-h-0 flex-1">
        <Bar options={options} data={data} />
      </div>
    </Card>
  );
}
