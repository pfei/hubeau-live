import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import type { ObservationSeries } from "./useHubeau";

interface Props {
  series: ObservationSeries;
}

function formatTime(timestamp: string): string {
  return new Date(timestamp).toLocaleTimeString("fr-FR", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

const API_BASE = import.meta.env.VITE_API_URL ?? "";

export default function ObservationChart({ series }: Props) {
  const data = series.observations.map((o) => ({
    time: formatTime(o.timestamp),
    flow: o.flow_m3s,
    height: o.height_m,
  }));

  const apiUrl = `${API_BASE}/api/v1/observations/${series.station.code}?period_hours=${series.period_hours}`;

  return (
    <div>
      <h2>
        {series.station.name} — last {series.period_hours}h
      </h2>
      <p>
        <a href={apiUrl} target="_blank" rel="noopener noreferrer">
          ↗ API
        </a>
      </p>

      <h3>Discharge (m³/s)</h3>
      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={data}>
          <XAxis dataKey="time" minTickGap={40} />
          <YAxis />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="flow"
            dot={false}
            strokeWidth={2}
            stroke="#2563eb"
          />
        </LineChart>
      </ResponsiveContainer>

      <h3>Height (m)</h3>
      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={data}>
          <XAxis dataKey="time" minTickGap={40} />
          <YAxis />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="height"
            dot={false}
            strokeWidth={2}
            stroke="#16a34a"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
