import { useState } from "react";
import ObservationChart from "./ObservationChart";
import { useObservations, useStations } from "./useHubeau";

export default function App() {
  const [department, setDepartment] = useState("");
  const [stationCode, setStationCode] = useState("");

  const {
    stations,
    loading: stationsLoading,
    error: stationsError,
  } = useStations(department);
  const {
    series,
    loading: obsLoading,
    error: obsError,
  } = useObservations(stationCode);

  return (
    <main>
      <h1>hubeau-live</h1>
      <p>Real-time French hydrometric data</p>

      {/* Step 1: department */}
      <input
        type="text"
        placeholder="Department (e.g. 33)"
        value={department}
        onChange={(e) => {
          setDepartment(e.target.value);
          setStationCode("");
        }}
        maxLength={3}
      />

      {/* Step 2: stations */}
      {stationsLoading && <p>Loading stations...</p>}
      {stationsError && <p>Error: {stationsError}</p>}
      {stations.length > 0 && (
        <select
          value={stationCode}
          onChange={(e) => setStationCode(e.target.value)}
        >
          <option value="">Select a station</option>
          {stations.map((s) => (
            <option key={s.code} value={s.code}>
              {s.name} — {s.river}
            </option>
          ))}
        </select>
      )}

      {/* Step 3: chart */}
      {obsLoading && <p>Loading observations...</p>}
      {obsError && <p>Error: {obsError}</p>}
      {series && <ObservationChart series={series} />}
    </main>
  );
}
