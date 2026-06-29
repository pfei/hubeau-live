import { useEffect, useState } from "react";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export interface Station {
  code: string;
  name: string;
  river: string;
  department: string;
  latitude: number | null;
  longitude: number | null;
}

export interface Observation {
  timestamp: string;
  flow_m3s: number | null;
  height_m: number | null;
}

export interface ObservationSeries {
  station: Station;
  observations: Observation[];
  period_hours: number;
}

export function useStations(department: string) {
  const [stations, setStations] = useState<Station[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (department.length < 2) {
      setStations([]);
      return;
    }

    setLoading(true);
    setError(null);

    fetch(`${API_BASE}/api/v1/stations/?department=${department}`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json() as Promise<Station[]>;
      })
      .then(setStations)
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [department]);

  return { stations, loading, error };
}

export function useObservations(stationCode: string, periodHours: number = 24) {
  const [series, setSeries] = useState<ObservationSeries | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!stationCode) {
      setSeries(null);
      return;
    }

    setLoading(true);
    setError(null);

    fetch(
      `${API_BASE}/api/v1/observations/${stationCode}?period_hours=${periodHours}`,
    )
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json() as Promise<ObservationSeries>;
      })
      .then(setSeries)
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [stationCode, periodHours]);

  return { series, loading, error };
}
