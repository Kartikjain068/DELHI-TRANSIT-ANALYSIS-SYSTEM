import { useEffect, useState } from "react";
import "../App.css";

export default function StationSelector() {
  const [mode, setMode] = useState("metro");
  const [stations, setStations] = useState([]);
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [routeInfo, setRouteInfo] = useState(null);
  const [loadingStations, setLoadingStations] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  // Fetch stations whenever mode changes
  useEffect(() => {
    setLoadingStations(true);
    setStart("");
    setEnd("");
    setRouteInfo(null);

    fetch(`http://localhost:5000/stations?mode=${mode}`)
      .then(res => res.json())
      .then(data => {
        setStations(data.stations || []);
        setLoadingStations(false);
      })
      .catch(err => {
        console.error("Error fetching stations:", err);
        setLoadingStations(false);
      });
  }, [mode]);

  // Calculate route
  const handleCalculate = () => {
    if (!start || !end) {
      setErrorMessage("Please select both start and end stations.");
      return;
    }

    setErrorMessage("");

    fetch(`http://localhost:5000/route?mode=${mode}&start=${start}&end=${end}`)
      .then(res => res.json())
      .then(data => setRouteInfo(data))
      .catch(err => console.error("Route error:", err));
  };

  return (
    <div className="selector-container">
      <h1>Delhi Transit Route Finder</h1>

      {/* Mode Dropdown */}
      <div className="mode-dropdown">
        <select value={mode} onChange={(e) => setMode(e.target.value)}>
          <option value="metro">Metro</option>
          <option value="bus">Bus</option>
        </select>
      </div>

      {/* Station Dropdowns */}
      <div className="dropdowns">
        <select value={start} onChange={(e) => setStart(e.target.value)}>
          <option value="">Select Start</option>
          {loadingStations ? (
            <option>Loading...</option>
          ) : (
            stations.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))
          )}
        </select>

        <select value={end} onChange={(e) => setEnd(e.target.value)}>
          <option value="">Select End</option>
          {loadingStations ? (
            <option>Loading...</option>
          ) : (
            stations.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))
          )}
        </select>
      </div>

      {errorMessage && (
        <p className="error-text">{errorMessage}</p>
      )}

      <button className="calculate-btn" onClick={handleCalculate}>
        Calculate Route
      </button>

      {routeInfo && (
        <div className="result-box">
          <p><strong>Mode:</strong> {routeInfo.mode.toUpperCase()}</p>
          <p><strong>Stops:</strong> {routeInfo.stops}</p>
          <p><strong>Estimated Time:</strong> {routeInfo.approx_time_minutes} mins</p>
        </div>
      )}
    </div>
  );
}
