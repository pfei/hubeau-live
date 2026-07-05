import { useEffect, useState } from "react";
import ObservationChart from "./ObservationChart";
import { useObservations, useStations } from "./useHubeau";

export default function App() {
  const [department, setDepartment] = useState("");
  const [stationCode, setStationCode] = useState("");
  const [dark, setDark] = useState(true); // dark by default

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
  }, [dark]);

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
    <main style={{ padding: "0 0 48px" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "flex-end",
          padding: "12px 0",
        }}
      >
        <button
          onClick={() => setDark((d) => !d)}
          aria-label="Toggle light/dark mode"
          style={{
            background: "none",
            border: "1px solid var(--border)",
            borderRadius: "6px",
            padding: "6px 12px",
            cursor: "pointer",
            color: "var(--text)",
            fontSize: "16px",
          }}
        >
          {dark ? "☀️" : "🌙"}
        </button>
      </div>

      <h1>hubeau-live</h1>
      <p>Real-time French hydrometric data</p>

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "12px",
          margin: "24px auto",
          maxWidth: "600px",
        }}
      >
        <input
          type="text"
          inputMode="numeric"
          pattern="[0-9]*"
          placeholder="Department code (e.g. 33)"
          value={department}
          onChange={(e) => {
            setDepartment(e.target.value);
            setStationCode("");
          }}
          maxLength={3}
          style={{
            width: "100%",
            boxSizing: "border-box",
            padding: "10px 14px",
            fontSize: "16px",
          }}
        />

        {stationsLoading && <p>Loading stations...</p>}
        {stationsError && <p>Error: {stationsError}</p>}
        {stations.length > 0 && (
          <select
            value={stationCode}
            onChange={(e) => setStationCode(e.target.value)}
            style={{
              width: "100%",
              boxSizing: "border-box",
              padding: "10px 14px",
              fontSize: "16px",
            }}
          >
            <option value="">Select a station</option>
            {stations.map((s) => (
              <option key={s.code} value={s.code}>
                {s.name} — {s.river}
              </option>
            ))}
          </select>
        )}
      </div>

      {obsLoading && <p>Loading observations...</p>}
      {obsError && <p>Error: {obsError}</p>}
      {series && <ObservationChart series={series} />}
    </main>
  );
}
